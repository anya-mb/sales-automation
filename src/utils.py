import logging

# import re
from urllib.parse import urlparse
import os
import json
from typing import List


def setup_logging(logfile_path: str):
    """
    Setup logging configuration to log messages to both a file and the console.

    Args:
        logfile_path (str): Path to the log file where log messages will be saved.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(logfile_path), logging.StreamHandler()],
    )


def get_domain_data_folder(url: str) -> str:
    """
    Generate a directory name based on the domain of the URL.

    Args:
        url (str): The URL to derive the directory name from.

    Returns:
        str: The directory name.
    """
    # Replace dots with underscores for the folder name
    domain = urlparse(url).netloc
    folder_name = domain.replace(".", "_")

    # Create the folder if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)
    return folder_name


def read_links(filename: str, path: str, dict_key: str) -> List[str]:
    file_path_to_read = os.path.join(path, filename)

    with open(file_path_to_read, "r") as json_file:
        links = json.load(json_file)

    links = links.get(dict_key)

    logging.info(f"Links are read from: {file_path_to_read}")

    return links


def read_all_links(filename: str, path: str, dict_key: str = "all_links") -> dict:
    return read_links(filename, path, dict_key)


def read_summary_links(
    filename: str, path: str, dict_key: str = "summary_links"
) -> dict:
    return read_links(filename, path, dict_key)


def save_links(filename: str, path: str, links: List[str], dict_key: str) -> None:
    file_path_to_save = os.path.join(path, filename)

    links_dict = {dict_key: links}

    with open(file_path_to_save, "w") as json_file:
        json.dump(links_dict, json_file, indent=4)

    logging.info(f"Links are saved to: {file_path_to_save}, dict key: {dict_key}")


def save_all_links(
    path: str,
    links: List[str],
    dict_key: str = "all_links",
    filename: str = "all_links.json",
) -> None:
    save_links(filename, path, links, dict_key)


def save_summary_links(
    path: str,
    links: List[str],
    dict_key: str = "summary_links",
    filename: str = "summary_links.json",
) -> None:
    save_links(filename, path, links, dict_key)


def save_website_info(path: str, website_info: str):
    scraped_website_filepath = os.path.join(path, "website_info.txt")
    with open(scraped_website_filepath, "w") as file:
        file.write(website_info)

    logging.info(f"Scraped website saved to: {scraped_website_filepath}")


def save_summary_info(path: str, summary_info: str):
    scraped_summary_filepath = os.path.join(path, "website_summary_info.txt")
    with open(scraped_summary_filepath, "w") as file:
        file.write(summary_info)

    logging.info(f"Scraped website summary saved to: {scraped_summary_filepath}")


# def read_website_info(path: str) -> str:
#     scraped_website_filepath = os.path.join(path, 'website_info.txt')
#     try:
#         with open(scraped_website_filepath, 'r') as file:
#             website_info = file.read()
#         logging.info(f"Scraped website read from: {scraped_website_filepath}")
#         return website_info
#     except FileNotFoundError as fnf_error:
#         logging.error(f"File not found: {scraped_website_filepath}")
#         raise fnf_error
#     except Exception as e:
#         logging.error(f"An error occurred while reading the file: {e}")
#         raise e
