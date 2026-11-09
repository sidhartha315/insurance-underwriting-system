import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"

SEED = 20261022

SOURCE_FILES = [
    "src/generators/master_data.py",
    "src/generators/transaction_data.py",
    "src/services/premium.py",
    "src/services/underwriting.py",
    "src/anomaly/inject_anomalies.py",
    "src/anomaly/evaluate_anomalies.py",
    "src/validation/checks.py",
    "src/validation/anomaly_detector.py",
    "src/database/models.py",
]

def calculate_checksum(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def create_manifest():

    manifest = {
        "project": "Insurance Underwriting System",
        "version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "random_seed": SEED,
        "data_provenance": {
            "type": "synthetic",
            "external_datasets_used": False,
            "description": (
                "Data generated programmatically for an insurance "
                "underwriting workflow challenge."
            )
        },
        "source_files": [],
        "exports": []
    }

    for relative_path in SOURCE_FILES:
        file_path = BASE_DIR / relative_path

        if file_path.exists():
            manifest["source_files"].append({
                "path": relative_path,
                "sha256": calculate_checksum(file_path)
            })
        else:
            print(f"WARNING: Missing source file: {relative_path}")

    export_dir = OUTPUT_DIR / "datasets"

    if export_dir.exists():
        for file_path in sorted(export_dir.rglob("*")):
            if file_path.is_file():
                manifest["exports"].append({
                    "path": str(file_path.relative_to(BASE_DIR)),
                    "size_bytes": file_path.stat().st_size,
                    "sha256": calculate_checksum(file_path)
                })

    output_path = OUTPUT_DIR / "source_manifest.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=4)

    print("\nSOURCE MANIFEST CREATED")
    print("=" * 40)
    print("Seed:", SEED)
    print("Source files:", len(manifest["source_files"]))
    print("Export files:", len(manifest["exports"]))
    print("Saved:", output_path)


if __name__ == "__main__":
    create_manifest()