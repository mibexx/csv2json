import importlib.metadata
import logging
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent.parent
SERVICE_NAME = "CSV2JSON_"

def _get_version() -> str:
    """Get the package version."""
    try:
        return importlib.metadata.version("csv2json")
    except importlib.metadata.PackageNotFoundError:
        return "0.1.0"  # Default during development


class ApplicationConfig(BaseSettings):
    """Application configuration."""

    name: str = "CSV 2 JSON"
    version: str = Field(default_factory=_get_version)
    log_level: int = logging.INFO

    model_config = SettingsConfigDict(
        env_prefix=SERVICE_NAME,
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
class UiConfig(BaseSettings):
    
    APP_NAME: str = "MBX CSV 2 JSON Converter"
    DEBUG: bool = False
    TESTING: bool = False
    
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    
    # API Configuration for connecting to the CSV2JSON API
    API_URL: str = Field(default="http://localhost:5000")
    
    model_config = SettingsConfigDict(
        env_prefix="",
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_config() -> ApplicationConfig:
    """Get the application configuration singleton."""
    return ApplicationConfig()

@lru_cache
def get_ui_config() -> UiConfig:
    """Get the application configuration singleton."""
    return UiConfig()