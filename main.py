from src.pipeline import run_pipeline


if __name__ == "__main__":
    summary = run_pipeline()
    print("Technical Request Document Assistant")
    print("----------------------------------")
    for key, value in summary.items():
        print(f"{key}: {value}")

