import logging
import os
import sys

from src.api import spl
from src.configuration.custom_formatter import CustomFormatter

USE_TEST_FILES = True

# config logger
root_logger = logging.getLogger()
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(CustomFormatter())
root_logger.addHandler(console_handler)

log_level = os.environ.get("LOG_LEVEL")
if not log_level:
    log_level = "INFO"

root_logger.setLevel(log_level)
logging.info("Set log level: " + log_level)

store_dir = os.path.join(os.getcwd(), 'store')
card_details_df = spl.get_card_details()
current_season = spl.get_current_season()
settings = spl.get_settings()
# season_end_dates_array = spl.get_season_end_times()
dark_theme = 'cyborg'
light_theme = 'minty'
current_theme = dark_theme

file_prefix = ""
if USE_TEST_FILES:
    file_prefix = "_test_file_"

file_extension = '.csv'
