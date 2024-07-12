import logging
import os
from src.scraping.web_scraper_processor import WebScraperProcessor
from src.linkedin_user_processing import get_user_info
from src.utils import (
    LEAD_SUMMARY_AND_FACTS_FILENAME,
    save_lead_summary_and_facts,
    read_lead_summary_and_facts,
    setup_logging,
)
from src.generative_ai_utils import (
    get_personalized_message,
    get_lead_facts_and_summary,
)

LOG_FILE_PATH = "logs/get_links_to_scrape.log"


def get_lead_facts(datapath: str, text: str) -> str:
    """
    Retrieves or generates lead facts and summary.

    Args:
        datapath (str): Path to the data directory.
        text (str): Text to process if summary does not exist.

    Returns:
        str: Lead facts and summary.
    """
    if not os.path.exists(os.path.join(datapath, LEAD_SUMMARY_AND_FACTS_FILENAME)):
        # Generate lead facts and summary if not already saved
        lead_facts_and_summary = get_lead_facts_and_summary(text)
        save_lead_summary_and_facts(datapath, lead_facts_and_summary)
    else:
        # Read lead facts and summary from file
        lead_facts_and_summary = read_lead_summary_and_facts(datapath)

    return lead_facts_and_summary


def process(company_url: str, user_id: str, style: str, additional_notes: str) -> str:
    """
    Process company and user information to generate a personalized message.

    Args:
        company_url (str): URL of the company's website.
        user_id (str): ID of the user (e.g., LinkedIn ID).
        style (str): Style of the personalized message.
        additional_notes (str)

    Returns:
        str: Personalized message generated based on input parameters.
    """
    # Set up logging
    setup_logging(LOG_FILE_PATH)
    logging.info(f"Company URL: {company_url}, User ID: {user_id}")

    # Initialize web scraper processor with company URL
    web_scraper_processor = WebScraperProcessor(company_url)
    web_scraper_processor.run()

    # Get data path from web scraper processor
    datapath = web_scraper_processor.datapath

    # Get company facts and summary from web scraper processor
    company_facts_and_summary = web_scraper_processor.get_company_facts()

    # Get user information based on data path and user ID
    lead_info = get_user_info(datapath, user_id)

    # Get lead facts and summary based on data path, lead info, and user ID
    lead_facts_and_summary = get_lead_facts_and_summary(datapath, lead_info, user_id)

    # Generate personalized message using data path, user ID, company facts and summary,
    # lead facts and summary, style and additional_notes
    personalised_message = get_personalized_message(
        datapath,
        user_id,
        company_facts_and_summary,
        lead_facts_and_summary,
        style,
        additional_notes,
    )

    logging.info(f"Personalised message: {personalised_message}")

    return personalised_message
