# """
# UT Dallas Parking Scraper (Direct from _code.php/_code.php/_code.php)
# ----------------------------------------------------------------------
# Scrapes garage data directly from the provided HTML endpoint.
# Logs progress, parses parking info, and stores results to CSV.
# """

# import csv
# import logging
# import time

# import requests
# import urllib3
# from bs4 import BeautifulSoup

# # Target URL — you said this one works, so let's go with it.
# URL = "https://services.utdallas.edu/transit/garages/_code.php/_code.php/_code.php/"
# CSV_FILENAME = "utd_parking_triple_code.csv"
# LOG_FILENAME = "utd_parking_triple_code.log"

# # Configure logging
# logging.basicConfig(
#     filename=LOG_FILENAME,
#     filemode="a",
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     level=logging.DEBUG,
# )


# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# def fetch_parking_html(url: str = URL) -> BeautifulSoup:
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#         "AppleWebKit/537.36 (KHTML, like Gecko) "
#         "Chrome/120.0 Safari/537.36"
#     }

#     logging.info(f"Requesting HTML data from {url}")
#     response = requests.get(url, headers=headers, timeout=15, verify=False)
#     response.raise_for_status()

#     logging.debug(f"Fetched {len(response.text)} characters from server.")
#     return BeautifulSoup(response.text, "html.parser")


# def parse_parking_data(soup: BeautifulSoup) -> list:
#     """
#     Parse the HTML and extract parking structure data.

#     Args:
#         soup (BeautifulSoup): Parsed HTML from fetch_parking_html().

#     Returns:
#         list[dict]: Extracted parking records.
#     """
#     data = []
#     tables = soup.find_all("table", class_="parking")
#     logging.info(f"Found {len(tables)} parking structures in the HTML.")

#     for t_index, table in enumerate(tables, start=1):
#         caption_tag = table.find("caption")
#         caption = (
#             caption_tag.get_text(strip=True) if caption_tag else f"Unknown_{t_index}"
#         )
#         logging.debug(f"Processing table: {caption}")

#         for row in table.select("tbody tr"):
#             cols = [c.get_text(strip=True) for c in row.find_all("td")]
#             if len(cols) == 3:
#                 record = {
#                     "garage": caption,
#                     "level": cols[0],
#                     "permit_type": cols[1],
#                     "available_spaces": cols[2],
#                 }
#                 data.append(record)
#                 logging.debug(f"  Parsed row: {record}")

#     return data


# def save_to_csv(data: list, filename: str = CSV_FILENAME) -> None:
#     """
#     Save the extracted data into a CSV file with timestamp.

#     Args:
#         data (list): Parsed parking data.
#         filename (str): Output CSV file path.
#     """
#     timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
#     with open(filename, "a", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         for row in data:
#             writer.writerow(
#                 [
#                     timestamp,
#                     row["garage"],
#                     row["level"],
#                     row["permit_type"],
#                     row["available_spaces"],
#                 ]
#             )
#     logging.info(f"Saved {len(data)} records to {filename}")


# if __name__ == "__main__":
#     logging.info("=== Starting UTD Parking Scraper (triple _code.php) ===")
#     try:
#         soup = fetch_parking_html()
#         records = parse_parking_data(soup)

#         for r in records:
#             print(r)

#         save_to_csv(records)
#         logging.info("Scraping completed successfully.")
#     except Exception as e:
#         logging.exception(f"Scraper failed with error: {e}")
#         print(f"[ERROR] {e}")


"""
UT Dallas Parking Scraper (JSON Output Version)
-----------------------------------------------
Scrapes parking garage data and stores it as structured JSON.
"""

import json
import logging
import time
import requests
import urllib3
from bs4 import BeautifulSoup

# Target URL — yes, the triple one that somehow works.
URL = "https://services.utdallas.edu/transit/garages/_code.php/_code.php/_code.php/"
# JSON_FILENAME = "utd_parking_triple_code.json"
JSON_FILENAME = "./Data/scraped_data/utd_parking_triple_code.json"
LOG_FILENAME = "utd_parking_triple_code.log"

# Configure logging
logging.basicConfig(
    filename=LOG_FILENAME,
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.DEBUG,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_parking_html(url: str = URL) -> BeautifulSoup:
    """Fetch raw HTML from the parking page."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    logging.info(f"Requesting HTML data from {url}")
    response = requests.get(url, headers=headers, timeout=15, verify=False)
    response.raise_for_status()

    logging.debug(f"Fetched {len(response.text)} characters of HTML.")
    return BeautifulSoup(response.text, "html.parser")


def parse_parking_data(soup: BeautifulSoup) -> list:
    """Extract parking data as a list of dictionaries."""
    data = []
    tables = soup.find_all("table", class_="parking")
    logging.info(f"Found {len(tables)} parking structures in the HTML.")

    for t_index, table in enumerate(tables, start=1):
        caption_tag = table.find("caption")
        caption = (
            caption_tag.get_text(strip=True) if caption_tag else f"Unknown_{t_index}"
        )
        logging.debug(f"Processing table: {caption}")

        for row in table.select("tbody tr"):
            cols = [c.get_text(strip=True) for c in row.find_all("td")]
            if len(cols) == 3:
                record = {
                    "garage": caption,
                    "level": cols[0],
                    "permit_type": cols[1],
                    "available_spaces": cols[2],
                }
                data.append(record)
                logging.debug(f"  Parsed row: {record}")

    return data


def save_to_json(data: list, filename: str = JSON_FILENAME) -> None:
    """Save parsed data into a JSON file with timestamp."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    wrapped_data = {"timestamp": timestamp, "record_count": len(data), "data": data}

    try:
        # Read old data if file exists
        try:
            with open(filename, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
            if isinstance(existing_data, list):
                # Convert to dict-style history if previous format was array
                existing_data = {"history": existing_data}
        except FileNotFoundError:
            existing_data = {"history": []}

        existing_data["history"].append(wrapped_data)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4)

        logging.info(f"Saved {len(data)} records to {filename}")

    except Exception as e:
        logging.exception(f"Failed to save JSON: {e}")
        raise


if __name__ == "__main__":
    logging.info("=== Starting UTD Parking Scraper (JSON Mode) ===")
    try:
        soup = fetch_parking_html()
        records = parse_parking_data(soup)

        for r in records:
            print(r)

        save_to_json(records)
        logging.info("Scraping completed successfully.")
    except Exception as e:
        logging.exception(f"Scraper failed with error: {e}")
        print(f"[ERROR] {e}")
