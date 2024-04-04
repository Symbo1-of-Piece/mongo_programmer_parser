import logging
import logging.handlers
from pathlib import Path


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime) - %(funcName) - %(levelname) - %(message)")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

log_file_name: Path = Path().home / "auto-programmer_exporter" / "logs" / "log.log"
if not log_file_name.parent.exists():
    log_file_name.parent.mkdir(parents=True, exist_ok=True)


file_handler = logging.handlers.RotatingFileHandler(log_file_name, maxBytes=10_000_000, backupCount=1)
file_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

