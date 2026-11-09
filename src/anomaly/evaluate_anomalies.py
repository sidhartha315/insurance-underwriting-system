import json
from pathlib import Path

import pandas as pd


GROUND_TRUTH_FILE = Path("outputs/ground_truth/ground_truth.csv")
DETECTED_FILE = Path("outputs/detected_anomalies.csv")

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def evaluate_anomalies():

    if not GROUND_TRUTH_FILE.exists():
        raise FileNotFoundError(GROUND_TRUTH_FILE)

    if not DETECTED_FILE.exists():
        raise FileNotFoundError(DETECTED_FILE)

    ground_truth = pd.read_csv(GROUND_TRUTH_FILE)
    detected = pd.read_csv(DETECTED_FILE)

    # Standardize column names
    if "record_id" in detected.columns:
        detected = detected.rename(
            columns={"record_id": "entity_id"}
        )

    required = {"entity_id", "issue_type"}

    for name, df in [
        ("Ground truth", ground_truth),
        ("Detected anomalies", detected)
    ]:
        missing = required - set(df.columns)

        if missing:
            raise ValueError(
                f"{name} missing columns: {missing}. "
                f"Available: {list(df.columns)}"
            )

    # Standardize values
    for df in [ground_truth, detected]:
        df["entity_id"] = df["entity_id"].astype(str).str.strip()
        df["issue_type"] = df["issue_type"].astype(str).str.strip()

    # Match the different premium labels
    detected["issue_type"] = detected["issue_type"].replace({
        "PREMIUM_MISMATCH": "PREMIUM_OUTSIDE_FORMULA"
    })

    truth_set = set(zip(
        ground_truth["entity_id"],
        ground_truth["issue_type"]
    ))

    detected_set = set(zip(
        detected["entity_id"],
        detected["issue_type"]
    ))

    tp_set = truth_set & detected_set
    fp_set = detected_set - truth_set
    fn_set = truth_set - detected_set

    tp = len(tp_set)
    fp = len(fp_set)
    fn = len(fn_set)

    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0
    )

    metrics = {
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "ground_truth_count": len(truth_set),
        "detected_count": len(detected_set)
    }

    # Save detailed comparison
    details = []

    for entity_id, issue_type in sorted(truth_set):
        details.append({
            "entity_id": entity_id,
            "issue_type": issue_type,
            "result": (
                "TRUE_POSITIVE"
                if (entity_id, issue_type) in tp_set
                else "FALSE_NEGATIVE"
            )
        })

    for entity_id, issue_type in sorted(fp_set):
        details.append({
            "entity_id": entity_id,
            "issue_type": issue_type,
            "result": "FALSE_POSITIVE"
        })

    pd.DataFrame(details).to_csv(
        OUTPUT_DIR / "anomaly_evaluation_details.csv",
        index=False
    )

    pd.DataFrame([metrics]).to_csv(
        OUTPUT_DIR / "anomaly_evaluation_metrics.csv",
        index=False
    )

    with open(
        OUTPUT_DIR / "anomaly_evaluation_metrics.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(metrics, file, indent=4)

    print("\nANOMALY MODEL EVALUATION")
    print("=" * 40)
    print(f"True Positives : {tp}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")
    print("-" * 40)
    print(f"Precision      : {precision:.4f}")
    print(f"Recall         : {recall:.4f}")
    print(f"F1 Score       : {f1:.4f}")
    print("=" * 40)
    print("\nEvaluation reports saved in outputs/")


if __name__ == "__main__":
    evaluate_anomalies()
