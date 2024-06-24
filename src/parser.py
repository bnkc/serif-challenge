import logging
import re
import time
from urllib.parse import parse_qs, urlparse

from .config import OUTPUT_FILE_PATH
from .models import FileLocation, ReportingPlans, ReportingStructure
from .utils import read_json, write_json, log_time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL_PATTERN = re.compile(
    r"https://anthembcbsco\.mrf\.bcbs\.com/\d{4}-\d{2}_\d{3}_39\w+_in-network-rates_\d+_of_\d+\.json\.gz"
)


def _is_relevant_plan(plan: ReportingPlans) -> bool:
    """
    Check if the plan is relevant based on its name.
    In this case, we are looking for Anthem PPO plans.
    """
    return plan.plan_name and "ANTHEM" in plan.plan_name and "PPO" in plan.plan_name  # type: ignore


def _is_url_expired(url: str) -> bool:
    """
    Check if a URL has expired based on its query parameters.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    expiration_timestamp = int(query_params.get("Expires", [0])[0])
    current_timestamp = int(time.time())
    return current_timestamp > expiration_timestamp


def _is_relevant_file(file_info: FileLocation) -> bool:
    """
    Check if a file location is relevant based on its pattern and description.
    In this case, we are looking for "In-Network Negotiated Rates Files". We
    Also use regex to to find the digit after the date in the URL. 39... == NY

    """
    return (
        URL_PATTERN.match(file_info.location)  # type: ignore
        and "In-Network Negotiated Rates Files" == file_info.description
        and not _is_url_expired(file_info.location)
    )


def _extract_urls_from_record(record: ReportingStructure) -> set[str]:
    """
    Extract relevant URLs from a single reporting structure record.
    """
    urls = set()
    for plan in record.reporting_plans:
        if _is_relevant_plan(plan):
            if record.in_network_files:
                for file_info in record.in_network_files:
                    if _is_relevant_file(file_info):
                        urls.add(file_info.location)
    return urls


@log_time
def extract_urls(file_path: str) -> set[str]:
    """
    Extract relevant URLs for Anthem PPO plans from a JSON file and write them to a machine readable file.
    """
    unique_urls = set()
    try:
        for record in read_json(file_path):
            record = ReportingStructure(**record)
            urls = _extract_urls_from_record(record)
            unique_urls.update(urls)

        write_json(OUTPUT_FILE_PATH, list(unique_urls))
        logger.info(f"Extracted {len(unique_urls)} unique URLs.")
    except Exception as e:  # Should be more specific
        logger.error(f"Error processing file {file_path}: {e}")
    return unique_urls
