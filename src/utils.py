import logging
from urllib.parse import urlparse
import os
import json
from typing import List

ALL_LINKS_FILENAME = "all_links.json"
SUMMARY_LINKS_FILENAME = "summary_links.json"

ALL_LINKS_DICT_KEY = "all_links"
SUMMARY_DICT_KEY = "summary_links"

WEBSITE_INFO_FILENAME = "website_info.txt"
WEBSITE_SUMMARY_INFO_FILENAME = "website_summary_info.txt"

COMPANY_SUMMARY_AND_FACTS_FILENAME = "company_summary_and_facts.txt"
LEAD_SUMMARY_AND_FACTS_FILENAME = "lead_summary_and_facts.txt"

LEAD_SUMMARY_FILENAME = "_lead_summary.txt"


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


def get_url_datapath(url: str, create: bool = True) -> str:
    domain_folder_name = get_domain_data_folder(url)

    # Determine the output directory
    domain_folder_name_relative = os.path.join("../data", domain_folder_name)

    if create:
        os.makedirs(domain_folder_name_relative, exist_ok=True)

    logging.info(f"Directory created: {domain_folder_name}")

    return domain_folder_name_relative


def read_links(filename: str, path: str, dict_key: str) -> List[str]:
    file_path_to_read = os.path.join(path, filename)

    with open(file_path_to_read, "r") as json_file:
        links = json.load(json_file)

    links = links.get(dict_key)

    logging.info(f"Links are read from: {file_path_to_read}")

    return links


def read_all_links(path: str) -> List[str]:
    return read_links(ALL_LINKS_FILENAME, path, ALL_LINKS_DICT_KEY)


def read_summary_links(path: str) -> List[str]:
    return read_links(SUMMARY_LINKS_FILENAME, path, SUMMARY_DICT_KEY)


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
    filename: str = ALL_LINKS_FILENAME,
) -> None:
    save_links(filename, path, links, dict_key)


def save_summary_links(
    path: str,
    links: List[str],
    dict_key: str = "summary_links",
    filename: str = SUMMARY_LINKS_FILENAME,
) -> None:
    save_links(filename, path, links, dict_key)


def save_txt(path: str, filename: str, text: str):
    full_filepath = os.path.join(path, filename)
    with open(full_filepath, "w") as file:
        file.write(text)

    logging.info(f"Saved txt to: {full_filepath}, file lenght: {len(text)}")


def read_txt(path: str, filename: str) -> str:
    full_filepath = os.path.join(path, filename)
    with open(full_filepath, "r") as file:
        text = file.read()

    logging.info(f"Read txt from: {full_filepath}, file lenght: {len(text)}")

    return text


def save_website_info(path: str, website_info: str):
    save_txt(path, WEBSITE_INFO_FILENAME, website_info)
    logging.info("Saved website info")


def save_summary_info(path: str, summary_info: str):
    save_txt(path, WEBSITE_SUMMARY_INFO_FILENAME, summary_info)
    logging.info("Saved summary info")


def read_website_info(path: str) -> str:
    text = read_txt(path, WEBSITE_INFO_FILENAME)
    logging.info("Read website info")
    return text


def read_summary_info(path: str) -> str:
    text = read_txt(path, WEBSITE_SUMMARY_INFO_FILENAME)
    logging.info("Read website summary info")
    return text


def save_company_summary_and_facts(path: str, text: str):
    save_txt(path, COMPANY_SUMMARY_AND_FACTS_FILENAME, text)
    logging.info("Saved company summary and facts")


def read_company_summary_and_facts(path: str) -> str:
    text = read_txt(path, COMPANY_SUMMARY_AND_FACTS_FILENAME)
    logging.info("Read company summary and facts")
    return text


def save_lead_summary_and_facts(path: str, text: str):
    save_txt(path, LEAD_SUMMARY_AND_FACTS_FILENAME, text)
    logging.info("Saved lead summary and facts")


def read_lead_summary_and_facts(path: str) -> str:
    text = read_txt(path, LEAD_SUMMARY_AND_FACTS_FILENAME)
    logging.info("Read lead summary and facts")
    return text


def save_lead_summary(path, lead_facts_and_summary, user_id) -> None:
    lead_filename = user_id + LEAD_SUMMARY_FILENAME
    save_txt(path, lead_filename, lead_facts_and_summary)
    logging.info("Saved lead_facts_and_summary")


def read_lead_summary(path, user_id) -> str:
    lead_filename = user_id + LEAD_SUMMARY_FILENAME
    text = read_txt(path, lead_filename)
    logging.info("Read lead_facts_and_summary")
    return text
