import subprocess
import sys


def run_step(module_name, description):
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
    print("INSURANCE UNDERWRITING SYSTEM - DATA GENERATION")

    run_step("src.generators.master_data", "Generating master data")

    run_step("src.generators.transaction_data", "Generating transactions")

    run_step("src.anomaly.inject_anomalies", "Injecting five deliberate anomalies")

    print("\nALL DATA GENERATION STEPS COMPLETED")