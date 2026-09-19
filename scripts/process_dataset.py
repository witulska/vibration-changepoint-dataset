#!/usr/bin/env python3
"""Build the archived and processed vibration change-point dataset.

Reads Physics Toolbox exports from --source (CSV and XLSX), writes a
reproducible archive to data/raw/ and FAIR-style files to data/processed/,
and regenerates catalogs, checksums, and the processing log.

Example:
    python scripts/process_dataset.py --source /path/to/my_data
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
DOC_DIR = ROOT / "documentation"
METADATA_DIR = ROOT / "metadata"

COLUMN_MAP = {
    "time": "time_s",
    "gFx": "gforce_x",
    "gFy": "gforce_y",
    "gFz": "gforce_z",
    "wx": "ang_vel_x",
    "wy": "ang_vel_y",
    "wz": "ang_vel_z",
    "ax": "lin_acc_x",
    "ay": "lin_acc_y",
    "az": "lin_acc_z",
}

SENSOR_COLUMNS = {
    "gforce_x": "g_force_meter",
    "gforce_y": "g_force_meter",
    "gforce_z": "g_force_meter",
    "ang_vel_x": "gyroscope",
    "ang_vel_y": "gyroscope",
    "ang_vel_z": "gyroscope",
    "lin_acc_x": "linear_accelerometer",
    "lin_acc_y": "linear_accelerometer",
    "lin_acc_z": "linear_accelerometer",
}

UNITS = {
    "time_s": "s",
    "gforce_x": "g",
    "gforce_y": "g",
    "gforce_z": "g",
    "ang_vel_x": "rad/s",
    "ang_vel_y": "rad/s",
    "ang_vel_z": "rad/s",
    "lin_acc_x": "m/s^2",
    "lin_acc_y": "m/s^2",
    "lin_acc_z": "m/s^2",
}

DROPPED_COLUMNS = {"TgF", "tgf", "TGF"}

# Metadata from Witulska & Wyłomańska (2022), Table 2, plus collection dates
# recovered from original local folder names (not from the time column).
MEASUREMENTS = [
    {
        "measurement_id": 1,
        "source_name": "pomiar_nr1.csv",
        "subject": "person",
        "n_regimes_reported": 2,
        "variance_change_factor": "dynamic_of_motion_change",
        "sensors_reported": "g_force_meter",
        "collection_date": "2021-09-03",
        "experiment_note": (
            "Person changing gait. Observer-declared break associated with a "
            "change from walking to running."
        ),
        "breaks": [(66.0, 68.0)],
    },
    {
        "measurement_id": 2,
        "source_name": "pomiar_nr2.csv",
        "subject": "person",
        "n_regimes_reported": 2,
        "variance_change_factor": "dynamic_of_motion_change",
        "sensors_reported": "g_force_meter;gyroscope",
        "collection_date": "2021-09-03",
        "experiment_note": (
            "Person: rotation, then about 30 s walking, then about 30 s running. "
            "Header comment in the original export described this protocol."
        ),
        "breaks": [(43.0, 44.0)],
    },
    {
        "measurement_id": 3,
        "source_name": "pomiar_nr3.xlsx",
        "subject": "person",
        "n_regimes_reported": 3,
        "variance_change_factor": "dynamic_of_motion_change",
        "sensors_reported": "g_force_meter;gyroscope",
        "collection_date": "2021-09-03",
        "experiment_note": (
            "Person walking and running (original Excel sheet name: "
            "chodzenie-bieganie-chodzenie). Two observer-declared breaks."
        ),
        "breaks": [(72.0, 74.0), (132.0, 134.0)],
    },
    {
        "measurement_id": 4,
        "source_name": "pomiar_nr4.csv",
        "subject": "person",
        "n_regimes_reported": 5,
        "variance_change_factor": "dynamic_of_motion_change",
        "sensors_reported": "g_force_meter;linear_accelerometer",
        "collection_date": "2021-09-03",
        "experiment_note": (
            "Person: rotation, then about 30 s walking, 30 s running, 30 s walking, "
            "30 s jumping, 30 s walking. Header comment in the original export "
            "described this protocol."
        ),
        "breaks": [(48.0, 50.0), (79.0, 81.0), (109.0, 111.0), (139.0, 141.0)],
    },
    {
        "measurement_id": 5,
        "source_name": "pomiar_nr5.csv",
        "subject": "motorbike",
        "n_regimes_reported": 3,
        "variance_change_factor": "surface_change",
        "sensors_reported": "g_force_meter;gyroscope",
        "collection_date": "2021-09-04",
        "experiment_note": (
            "Motorbike on a route with cobblestone (sett) and asphalt segments. "
            "Observer notes (removed from files) indicated roughly 50 km/h on the "
            "first half of the route and 80 km/h on the second half."
        ),
        "breaks": [(85.0, 87.0), (214.0, 216.0)],
    },
    {
        "measurement_id": 6,
        "source_name": "pomiar_nr6.csv",
        "subject": "motorbike",
        "n_regimes_reported": 3,
        "variance_change_factor": "surface_change",
        "sensors_reported": "g_force_meter",
        "collection_date": "2021-09-04",
        "experiment_note": (
            "Motorbike on a route with cobblestone (sett) and asphalt segments. "
            "Observer notes (removed from files) indicated about 60 km/h on both halves."
        ),
        "breaks": [(49.0, 51.0), (179.0, 181.0)],
    },
    {
        "measurement_id": 7,
        "source_name": "pomiar_nr7.csv",
        "subject": "motorbike",
        "n_regimes_reported": 3,
        "variance_change_factor": "surface_change",
        "sensors_reported": "g_force_meter;gyroscope",
        "collection_date": "2021-09-04",
        "experiment_note": (
            "Motorbike on a route with cobblestone (sett) and asphalt segments. "
            "Observer notes (removed from files) indicated about 50 km/h on both halves."
        ),
        "breaks": [(56.0, 58.0), (211.0, 213.0)],
    },
    {
        "measurement_id": 8,
        "source_name": "pomiar_nr8.csv",
        "subject": "car",
        "n_regimes_reported": 3,
        "variance_change_factor": "surface_change",
        "sensors_reported": "g_force_meter",
        "collection_date": "2021-09-04",
        "experiment_note": (
            "Car on a route with cobblestone (sett) and asphalt segments. The source "
            "paper reports 3 regimes but lists three observer intervals (see methods)."
        ),
        "breaks": [(103.0, 104.0), (197.0, 199.0), (279.0, 281.0)],
    },
    {
        "measurement_id": 9,
        "source_name": "pomiar_nr9.csv",
        "subject": "car",
        "n_regimes_reported": 3,
        "variance_change_factor": "surface_change",
        "sensors_reported": "g_force_meter;gyroscope",
        "collection_date": "2021-09-07",
        "experiment_note": (
            "Car on a route with cobblestone (sett) and asphalt segments."
        ),
        "breaks": [(91.0, 93.0), (149.0, 151.0)],
    },
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def decode_csv_bytes(data: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-8", "cp1250"):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return data.decode("cp1250", errors="replace"), "cp1250-replace"


def is_comment_header(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith("#"):
        return True
    if stripped.startswith('"') and not re.match(r'^"?time[;,\t]', stripped, flags=re.I):
        return True
    return False


def parse_source_csv(path: Path) -> tuple[pd.DataFrame, dict]:
    raw_bytes = path.read_bytes()
    text, encoding = decode_csv_bytes(raw_bytes)
    lines = text.splitlines()
    comment_lines = []
    i = 0
    while i < len(lines) and is_comment_header(lines[i]) and "time;" not in lines[i].lower():
        comment_lines.append(lines[i])
        i += 1
    remaining = lines[i:]
    table = pd.read_csv(
        io.StringIO("\n".join(remaining)),
        sep=";",
        engine="python",
    )
    extra_notes = []
    keep_cols = []
    for col in table.columns:
        name = str(col).strip()
        if name.startswith("Unnamed") or name == "" or name.lower() == "nan":
            notes = (
                table[col]
                .dropna()
                .astype(str)
                .map(str.strip)
            )
            extra_notes.extend([n for n in notes.tolist() if n])
        else:
            keep_cols.append(col)
    table = table[keep_cols].copy()
    table.columns = [str(c).strip() for c in table.columns]
    info = {
        "encoding_detected": encoding,
        "comment_header_lines": comment_lines,
        "extra_notes_n": len(extra_notes),
        "extra_notes_redacted": True,
        "n_source_lines": len(lines),
    }
    return table, info


def parse_source_xlsx(path: Path) -> tuple[pd.DataFrame, dict]:
    workbook = load_workbook(path, read_only=True, data_only=True)
    sheet_names = workbook.sheetnames
    abs_path = None
    try:
        abs_path = workbook.path
    except Exception:
        abs_path = None
    workbook.close()
    table = pd.read_excel(path, sheet_name=0)
    table.columns = [str(c).strip() for c in table.columns]
    info = {
        "encoding_detected": "xlsx",
        "excel_sheet_names": sheet_names,
        "comment_header_lines": [],
        "extra_notes_n": 0,
        "extra_notes_redacted": True,
        "local_path_metadata_removed": True,
        "source_abs_path_present": bool(abs_path),
    }
    return table, info


def sanitize_numeric_table(table: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    dropped = []
    keep = []
    for col in table.columns:
        if str(col) in DROPPED_COLUMNS:
            dropped.append(str(col))
            continue
        keep.append(col)
    out = table[keep].copy()
    for col in out.columns:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    return out, dropped


def rename_columns(table: pd.DataFrame) -> pd.DataFrame:
    unknown = [c for c in table.columns if c not in COLUMN_MAP]
    if unknown:
        raise ValueError(f"Unexpected columns: {unknown}")
    renamed = table.rename(columns=COLUMN_MAP)
    ordered = [COLUMN_MAP[c] for c in table.columns]
    return renamed[ordered]


def sensors_from_columns(columns: list[str]) -> list[str]:
    found = []
    for col in columns:
        sensor = SENSOR_COLUMNS.get(col)
        if sensor and sensor not in found:
            found.append(sensor)
    return found


def write_raw_csv(path: Path, table: pd.DataFrame) -> None:
    """Archive numeric source columns, including TgF if present, UTF-8 CSV with ';'."""
    path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(path, sep=";", index=False, lineterminator="\n")


def write_raw_xlsx(path: Path, table: pd.DataFrame, sheet_name: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    safe_name = sheet_name[:31] if sheet_name else "measurement"
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        table.to_excel(writer, sheet_name=safe_name, index=False)


def summarize(table: pd.DataFrame) -> dict:
    time = table["time_s"]
    dt = time.diff().dropna()
    dt_pos = dt[dt > 0]
    median_dt = float(dt_pos.median()) if len(dt_pos) else None
    return {
        "n_rows": int(len(table)),
        "n_unique_times": int(time.nunique(dropna=True)),
        "n_duplicate_times": int(time.duplicated().sum()),
        "time_start_s": float(time.min()),
        "time_end_s": float(time.max()),
        "duration_s": float(time.max() - time.min()),
        "median_positive_dt_s": median_dt,
        "mean_positive_dt_s": float(dt_pos.mean()) if len(dt_pos) else None,
        "min_positive_dt_s": float(dt_pos.min()) if len(dt_pos) else None,
        "max_positive_dt_s": float(dt_pos.max()) if len(dt_pos) else None,
        "apparent_row_rate_hz": (None if not median_dt else 1.0 / median_dt),
        "n_missing_cells": int(table.isna().sum().sum()),
        "missing_by_column": {c: int(table[c].isna().sum()) for c in table.columns},
        "columns": list(table.columns),
        "sensors_present": sensors_from_columns(list(table.columns)),
    }


def json_ready(value):
    if isinstance(value, dict):
        return {k: json_ready(v) for k, v in value.items()}
    if isinstance(value, list):
        return [json_ready(v) for v in value]
    if isinstance(value, float):
        return value
    return value


def write_processed(measurement_id: int, table: pd.DataFrame, meta: dict) -> dict:
    stem = f"measurement_{measurement_id:02d}"
    csv_path = PROCESSED_DIR / f"{stem}.csv"
    tsv_path = PROCESSED_DIR / f"{stem}.tsv"
    json_path = PROCESSED_DIR / f"{stem}.json"
    table.to_csv(csv_path, index=False, lineterminator="\n")
    table.to_csv(tsv_path, sep="\t", index=False, lineterminator="\n")
    payload = {
        "measurement_id": measurement_id,
        "metadata": json_ready(meta),
        "column_units": {c: UNITS[c] for c in table.columns},
        "missing_value_code": "empty field; no missing numeric values in this file",
        "n_rows": int(len(table)),
        "records": json.loads(table.to_json(orient="records")),
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return {
        "csv": csv_path.name,
        "tsv": tsv_path.name,
        "json": json_path.name,
        "sha256_csv": sha256_file(csv_path),
        "sha256_tsv": sha256_file(tsv_path),
        "sha256_json": sha256_file(json_path),
    }


def write_combined_xlsx(frames: dict[int, pd.DataFrame]) -> Path:
    path = PROCESSED_DIR / "measurements.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        catalog_rows = []
        for measurement_id, table in frames.items():
            sheet = f"m{measurement_id:02d}"
            table.to_excel(writer, sheet_name=sheet, index=False)
            catalog_rows.append(
                {
                    "measurement_id": measurement_id,
                    "sheet": sheet,
                    "n_rows": len(table),
                    "columns": ",".join(table.columns),
                }
            )
        pd.DataFrame(catalog_rows).to_excel(writer, sheet_name="index", index=False)
    return path


def write_catalogs(rows: list[dict], change_points: list[dict]) -> None:
    catalog = pd.DataFrame(rows)
    catalog.to_csv(DOC_DIR / "measurements_catalog.csv", index=False, lineterminator="\n")
    pd.DataFrame(change_points).to_csv(
        DOC_DIR / "change_points.csv", index=False, lineterminator="\n"
    )
    mapping = pd.DataFrame(
        [
            {
                "source_column": src,
                "processed_column": dst,
                "unit": UNITS[dst],
                "sensor": SENSOR_COLUMNS.get(dst, ""),
                "description": {
                    "time_s": "Time from the start of the recording",
                    "gforce_x": "G-force, device X axis",
                    "gforce_y": "G-force, device Y axis",
                    "gforce_z": "G-force, device Z axis",
                    "ang_vel_x": "Angular velocity, device X axis",
                    "ang_vel_y": "Angular velocity, device Y axis",
                    "ang_vel_z": "Angular velocity, device Z axis",
                    "lin_acc_x": "Linear acceleration (gravity removed), device X axis",
                    "lin_acc_y": "Linear acceleration (gravity removed), device Y axis",
                    "lin_acc_z": "Linear acceleration (gravity removed), device Z axis",
                }[dst],
            }
            for src, dst in COLUMN_MAP.items()
        ]
    )
    mapping.to_csv(DOC_DIR / "column_mapping.csv", index=False, lineterminator="\n")


def write_processing_log(records: list[dict], generated_at: str) -> None:
    lines = [
        "# Processing log",
        "",
        f"Generated: {generated_at}",
        "Script: `scripts/process_dataset.py`",
        "",
        "This file is produced by the processing script. It lists every operation",
        "applied to each source file.",
        "",
        "## Operations applied to every file",
        "",
        "1. Detect encoding (UTF-8, UTF-8 BOM, or Windows-1250 / `cp1250`) or read Excel.",
        "2. Drop comment header rows (lines starting with `#` or a quoted protocol note).",
        "3. Drop extra unnamed columns that held free-text observer notes.",
        "4. Convert remaining columns to numeric values (`pandas.to_numeric`).",
        "5. Write an archived copy under `data/raw/` with original Physics Toolbox",
        "   column names, original semicolon delimiter (CSV) or a cleaned Excel sheet,",
        "   **including** `TgF` when it was present. Local filesystem paths from Excel",
        "   metadata are not copied.",
        "6. Drop column `TgF` if present (total g-force magnitude; not used in the paper table).",
        "7. Rename columns to stable names (`time` → `time_s`, `gFx` → `gforce_x`, …).",
        "8. Write processed CSV (comma-separated), TSV, and JSON under `data/processed/`.",
        "9. Do not interpolate, resample, detrend, or impute. Duplicate timestamps are kept.",
        "",
        "## Per-file notes",
        "",
    ]
    for rec in records:
        lines.append(f"### Measurement {rec['measurement_id']:02d} (`{rec['source_name']}`)")
        lines.append("")
        lines.append(f"- Source encoding / format: `{rec['encoding_detected']}`")
        if rec.get("excel_sheet_names"):
            lines.append(f"- Excel sheet names: {rec['excel_sheet_names']}")
        if rec.get("comment_header_lines"):
            lines.append("- Removed comment header (protocol text only; not stored).")
        if rec.get("extra_notes_n"):
            lines.append(
                f"- Removed {rec['extra_notes_n']} free-text observer note cell(s) "
                "from trailing columns (route/speed notes; incidental place names redacted)."
            )
        if rec.get("dropped_tgf"):
            lines.append("- Dropped column `TgF` in the processed files.")
        else:
            lines.append("- No `TgF` column in the source.")
        lines.append(
            f"- Rows: {rec['n_rows']}; unique timestamps: {rec['n_unique_times']}; "
            f"duplicate timestamps: {rec['n_duplicate_times']}."
        )
        lines.append(
            f"- Time range: {rec['time_start_s']:.6f} s to {rec['time_end_s']:.6f} s "
            f"(duration {rec['duration_s']:.6f} s)."
        )
        lines.append(
            f"- Missing numeric cells: {rec['n_missing_cells']} "
            f"(by column: {rec['missing_by_column']})."
        )
        lines.append(f"- Processed columns: {', '.join(rec['columns'])}.")
        lines.append(f"- SHA-256 (processed CSV): `{rec['sha256_csv']}`.")
        lines.append("")
    (DOC_DIR / "processing_log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_checksums(paths: list[Path]) -> None:
    lines = []
    for path in sorted(paths):
        rel = path.relative_to(ROOT).as_posix()
        lines.append(f"{sha256_file(path)}  {rel}")
    (PROCESSED_DIR / "checksums.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def copy_or_ingest(source_dir: Path) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    DOC_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("/workspaces/chasm_tests/my_data"),
        help="Directory with original pomiar_nr*.csv / pomiar_nr3.xlsx files",
    )
    args = parser.parse_args()
    source_dir = args.source.resolve()
    if not source_dir.is_dir():
        raise SystemExit(f"Source directory not found: {source_dir}")

    copy_or_ingest(source_dir)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    frames: dict[int, pd.DataFrame] = {}
    catalog_rows = []
    change_points = []
    log_records = []
    checksum_paths: list[Path] = []

    for spec in MEASUREMENTS:
        src = source_dir / spec["source_name"]
        if not src.exists():
            raise SystemExit(f"Missing source file: {src}")
        if src.suffix.lower() == ".xlsx":
            numeric_source, info = parse_source_xlsx(src)
        else:
            numeric_source, info = parse_source_csv(src)

        raw_path = RAW_DIR / spec["source_name"]
        if src.suffix.lower() == ".xlsx":
            sheet = info["excel_sheet_names"][0] if info.get("excel_sheet_names") else "data"
            write_raw_xlsx(raw_path, numeric_source, sheet)
        else:
            write_raw_csv(raw_path, numeric_source)
        checksum_paths.append(raw_path)

        processed, dropped = sanitize_numeric_table(numeric_source)
        renamed = rename_columns(processed)
        if renamed.isna().any().any():
            bad = renamed.isna().sum()
            raise SystemExit(f"Non-numeric or missing values in measurement {spec['measurement_id']}: {bad.to_dict()}")

        summary = summarize(renamed)
        meta = {
            "measurement_id": spec["measurement_id"],
            "source_file": spec["source_name"],
            "subject": spec["subject"],
            "collection_date": spec["collection_date"],
            "variance_change_factor": spec["variance_change_factor"],
            "n_regimes_reported": spec["n_regimes_reported"],
            "n_declared_breaks": len(spec["breaks"]),
            "sensors_reported_in_paper": spec["sensors_reported"].split(";"),
            "experiment_note": spec["experiment_note"],
            "related_article": (
                "Witulska, J., & Wyłomańska, A. (2022). Identification of the "
                "structure break point for data with changing variance. "
                "Mathematica Applicanda, 50(1), 65-106. "
                "https://doi.org/10.14708/ma.v50i1.7155"
            ),
        }
        paths = write_processed(spec["measurement_id"], renamed, {**meta, **summary})
        frames[spec["measurement_id"]] = renamed
        checksum_paths.extend(
            [
                PROCESSED_DIR / paths["csv"],
                PROCESSED_DIR / paths["tsv"],
                PROCESSED_DIR / paths["json"],
            ]
        )

        sensors_present = ";".join(summary["sensors_present"])
        catalog_rows.append(
            {
                "measurement_id": spec["measurement_id"],
                "source_file": spec["source_name"],
                "processed_csv": paths["csv"],
                "subject": spec["subject"],
                "collection_date": spec["collection_date"],
                "variance_change_factor": spec["variance_change_factor"],
                "n_regimes_reported": spec["n_regimes_reported"],
                "n_declared_breaks": len(spec["breaks"]),
                "declared_break_intervals_s": ";".join(
                    f"[{a:.0f},{b:.0f}]" if a.is_integer() and b.is_integer() else f"[{a},{b}]"
                    for a, b in spec["breaks"]
                ),
                "theoretical_change_points_s": ";".join(
                    f"{(a + b) / 2:.1f}" for a, b in spec["breaks"]
                ),
                "sensors_reported_in_paper": spec["sensors_reported"],
                "sensors_present": sensors_present,
                "n_rows": summary["n_rows"],
                "n_unique_times": summary["n_unique_times"],
                "n_duplicate_times": summary["n_duplicate_times"],
                "time_start_s": summary["time_start_s"],
                "time_end_s": round(summary["time_end_s"], 6),
                "duration_s": round(summary["duration_s"], 6),
                "paper_total_time_s": {
                    1: 83.74,
                    2: 77.72,
                    3: 201.53,
                    4: 181.88,
                    5: 265.49,
                    6: 233.66,
                    7: 274.62,
                    8: 344.88,
                    9: 176.55,
                }[spec["measurement_id"]],
                "n_missing_cells": summary["n_missing_cells"],
                "columns": ",".join(summary["columns"]),
                "sha256_csv": paths["sha256_csv"],
            }
        )
        for idx, (start, end) in enumerate(spec["breaks"], start=1):
            change_points.append(
                {
                    "measurement_id": spec["measurement_id"],
                    "break_index": idx,
                    "interval_start_s": start,
                    "interval_end_s": end,
                    "theoretical_change_point_s": (start + end) / 2.0,
                    "source": "observer_declared_interval_median_Witulska_Wylomanska_2022",
                }
            )
        log_records.append(
            {
                **spec,
                **info,
                **summary,
                **paths,
                "dropped_tgf": bool(dropped),
            }
        )

    xlsx_path = write_combined_xlsx(frames)
    checksum_paths.append(xlsx_path)
    write_catalogs(catalog_rows, change_points)
    write_processing_log(log_records, generated_at)
    write_checksums(checksum_paths)

    release_meta = {
        "title": "Smartphone vibration measurements with observer-declared variance change points",
        "version": "1.0.0",
        "date_published": date.today().isoformat(),
        "generated_at_utc": generated_at,
        "license": "CC-BY-4.0",
        "n_measurements": len(MEASUREMENTS),
        "n_processed_rows": int(sum(len(v) for v in frames.values())),
        "related_identifiers": [
            {
                "relation": "isSupplementTo",
                "identifier": "10.14708/ma.v50i1.7155",
                "scheme": "doi",
            }
        ],
    }
    (METADATA_DIR / "release.json").write_text(
        json.dumps(release_meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(release_meta, indent=2))
    print(f"Wrote raw files to {RAW_DIR}")
    print(f"Wrote processed files to {PROCESSED_DIR}")


if __name__ == "__main__":
    main()
