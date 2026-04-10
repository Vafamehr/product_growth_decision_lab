from pathlib import Path


# =========================
# ROOT DIRECTORY
# =========================
# Points to project root (product_growth_decision_lab/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# =========================
# CORE DIRECTORIES
# =========================
SRC_DIR = BASE_DIR / "src"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
DOCS_DIR = BASE_DIR / "docs"


# =========================
# ARTIFACT SUBDIRECTORIES
# =========================
DATA_DIR = ARTIFACTS_DIR / "data"
METRICS_DIR = ARTIFACTS_DIR / "metrics"
ANALYSIS_DIR = ARTIFACTS_DIR / "analysis"
EXPERIMENTS_DIR = ARTIFACTS_DIR / "experiments"
REPORTS_DIR = ARTIFACTS_DIR / "reports"


# =========================
# ENSURE DIRECTORIES EXIST
# =========================
def ensure_directories():
    directories = [
        DATA_DIR,
        METRICS_DIR,
        ANALYSIS_DIR,
        EXPERIMENTS_DIR,
        REPORTS_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


# =========================
# OPTIONAL: AUTO-CREATE
# =========================
if __name__ == "__main__":
    ensure_directories()
    print("All artifact directories are ready.")