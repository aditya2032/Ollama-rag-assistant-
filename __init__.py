"""Central application settings."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "knowledge_base.txt"

# These Hugging Face GGUF names are pulled locally by Ollama on first use.
DEFAULT_EMBEDDING_MODEL = "hf.co/CompendiumLabs/bge-base-en-v1.5-gguf"
DEFAULT_CHAT_MODEL = "hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF"
