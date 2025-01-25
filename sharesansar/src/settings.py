import os
from datetime import date
from dotenv import load_dotenv
from typing import Tuple
from rich.console import Console

load_dotenv()
console = Console()

class ConfigError(Exception):
    pass

class Settings:
    @property
    def dates(self) -> Tuple[date, date]:
        try:
            start = date.fromisoformat(os.getenv("START_DATE"))
            end = date.fromisoformat(os.getenv("END_DATE"))
            if start > end:
                raise ConfigError("START_DATE must be before END_DATE")
            return start, end
        except (TypeError, ValueError) as e:
            raise ConfigError("Invalid date format in .env") from e

    @property
    def sector(self) -> str:
        sector = os.getenv("SECTOR")
        if not sector:
            raise ConfigError("SECTOR must be specified in .env")
        return sector

    @property
    def headless(self) -> bool:
        return os.getenv("HEADLESS", "true").lower() == "true"

    @property
    def max_workers(self) -> int:
        try:
            return int(os.getenv("MAX_WORKERS", "5"))
        except ValueError as e:
            raise ConfigError("Invalid MAX_WORKERS value") from e

    @property
    def retry_config(self) -> dict:
        return {
            'attempts': int(os.getenv("RETRY_ATTEMPTS", "5")),
            'initial_timeout': float(os.getenv("INITIAL_TIMEOUT", "10")),
            'backoff_factor': float(os.getenv("BACKOFF_FACTOR", "1.5")),
            'slow_threshold': float(os.getenv("SLOW_THRESHOLD", "25")),
            'average_window': int(os.getenv("AVERAGE_WINDOW", "5")),
        }

config = Settings()