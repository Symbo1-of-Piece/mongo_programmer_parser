import logging
import logging.handlers
from pathlib import Path


logger = logging.getLogger("main")
logger.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime) - %(funcName) - %(levelname) - %(message)")

stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)

log_file_name: Path = Path().home() / "auto-programer-db" / "logs" / "log.log"
if not log_file_name.parent.exists():
    log_file_name.parent.mkdir(parents=True, exist_ok=True)


file_handler = logging.FileHandler(log_file_name)
# file_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

