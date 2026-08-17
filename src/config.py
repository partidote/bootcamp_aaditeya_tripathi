import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

def get_key(name: str, default: Optional[str] = None) -> Optional[str]:
    """Retrieve environment variable key value safely."""
    return os.getenv(name, default)
