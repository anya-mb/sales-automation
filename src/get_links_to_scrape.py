import requests

# import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Set
import os
import argparse
import logging
from utils import setup_logging, get_domain_data_folder, save_links

LOG_FILE_PATH = "../logs/get_links_to_scrape.log"


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Get links to scrape from the provided URL"
    )
    parser.add_argument(
        "--url",
        type=str,
        default="https://www.therocketbrew.com",
        help="URL to find links on and save them",
    )
    parser.add_argument(
        "--depth", type=int, default=2, help="The depth to go to find links to scrape"
    )
    parser.add_argument(
        "--path_to_save",
        type=str,
        default=None,
        help="Path to save JSON files for links",
    )

    return parser.parse_args()


def process_one_link(url: str) -> Set[str]:
    """
    Process a single URL to extract links from it.

    Args:
        url (str): The URL to process.

    Returns:
        Set[str]: A set of extracted links from the URL.
    """
    try:
        # Fetch the HTML content of the URL
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract and clean links
        links = {urljoin(url, a_tag["href"]) for a_tag in soup.find_all("a", href=True)}
        clean_links = get_clean_links(links)
        return filter_same_domain_links(clean_links, url)
    except requests.RequestException as e:
        logging.error(f"Error fetching the URL {url}: {e}")
        return set()


def get_all_links(url: str, depth: int = 1) -> List[str]:
    """
    Recursively get all links from the root URL up to a specified depth.

    Args:
        url (str): The root URL.
        depth (int): The depth to crawl.

    Returns:
        List[str]: A list of all links found.
    """
    visited_links = set()
    links_to_visit = {url}

    # Traverse the links up to the specified depth
    for _ in range(depth):
        new_links = set()
        for link in links_to_visit:
            new_links.update(process_one_link(link))
        visited_links.update(links_to_visit)
        links_to_visit = new_links - visited_links

    visited_links.update(links_to_visit)
    return list(visited_links)


def get_clean_links(links: Set[str]) -> Set[str]:
    """
    Clean and filter a set of links.

    Args:
        links (Set[str]): The set of links to clean.

    Returns:
        Set[str]: The cleaned set of links.
    """
    # Only keep links starting with http://www. or https://www. and remove trailing slashes
    return {
        link.rstrip("/")
        for link in links
        if link.startswith(("https://www.", "http://www."))
    }


def filter_same_domain_links(links: Set[str], url: str) -> Set[str]:
    """
    Filter links to keep only those within the same domain as the given URL.

    Args:
        links (Set[str]): The set of links to filter.
        url (str): The reference URL to determine the domain.

    Returns:
        Set[str]: The filtered set of links.
    """
    # Extract the domain from the URL
    domain = urlparse(url).netloc
    return {link for link in links if urlparse(link).netloc == domain}


def main():
    """
    Main function to orchestrate the link extraction and saving process.
    """
    # Parse command-line arguments
    args = parse_arguments()
    setup_logging(LOG_FILE_PATH)

    logging.info(f"Arguments: {args}")

    domain_folder_name = get_domain_data_folder(args.url)

    # Determine the output directory
    domain_folder_name_relative = args.path_to_save or os.path.join(
        "../data", domain_folder_name
    )
    os.makedirs(domain_folder_name_relative, exist_ok=True)

    # Extract links and save them to a JSON file
    links = get_all_links(args.url, args.depth)
    logging.info(
        f"Extracted {len(links)} links from URL: {args.url} with depth: {args.depth}"
    )

    links_data = {"all_links": links}
    file_path_to_save = os.path.join(
        domain_folder_name_relative, f"all_links_depth_{args.depth}.json"
    )

    # Save links to json file
    save_links(file_path_to_save, links_data)

    logging.info(f"Saved all links to {file_path_to_save}")


if __name__ == "__main__":
    main()
