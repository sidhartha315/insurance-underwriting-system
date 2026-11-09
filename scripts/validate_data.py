import subprocess
import sys

def run_validation(module_name, description):
    print("\n" + "=" * 55)
    print(description)
    print("=" * 55)

    result = subprocess.run(
        [sys.executable, "-m", module_name],
        check=False
    )

    if result.returncode != 0:
        raise SystemExit(f"FAILED: {description}")

    print(f"SUCCESS: {description}")


if __name__ == "__main__":
    print("INSURANCE DATA VALIDATION")

    run_validation(
        "src.validation.checks",
        "Running data validation"
    )

    run_validation(
        "src.validation.anomaly_detector",
        "Running anomaly detection"
    )

    print("\nVALIDATION COMPLETED")