from dotenv import load_dotenv, find_dotenv
import os
from linkedin_api import Linkedin
import logging
from src.utils import save_lead_summary, read_lead_summary, LEAD_SUMMARY_FILENAME

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Authenticate using LinkedIn account credentials
api = Linkedin(os.environ["LINKEDIN_LOGIN"], os.environ["LINKEDIN_PASSWORD"])


def extract_user_info(user_id: str) -> str:
    """
    Extract user information and recent posts from LinkedIn using the LinkedIn API.

    Args:
        user_id (str): LinkedIn user ID.

    Returns:
        str: Concatenated string of user information and posts.
    """
    # Retrieve basic profile information
    profile = api.get_profile(user_id)
    useful_keys = [
        "summary",
        "industryName",
        "firstName",
        "lastName",
        "headline",
        "geoLocationName",
        "experience",
        "honors",
        "volunteer",
        "certifications",
        "publications",
    ]
    lead_information = [f"{key}:\n{profile.get(key)}\n" for key in useful_keys]
    lead_information = "\n".join(lead_information)
    logging.info(
        f"Retrieved user information from LinkedIn, character length: {len(lead_information)}"
    )

    # Retrieve recent posts from user's profile
    profile_posts = api.get_profile_posts(user_id, post_count=10)
    posts = "Posts:\n" + "\n\n".join(
        [post.get("commentary").get("text").get("text") for post in profile_posts]
    )
    logging.info(f"Retrieved user posts from LinkedIn, character length: {len(posts)}")

    # Combine user information and posts into a single string
    user_info = lead_information + posts

    return user_info


def get_user_info(path: str, user_id: str) -> str:
    """
    Retrieve user information and save it to a local file if not already cached.

    Args:
        path (str): Path to the directory where user information will be stored.
        user_id (str): LinkedIn user ID.

    Returns:
        str: User information as a concatenated string.
    """
    user_folder = os.path.join(path, user_id)
    os.makedirs(user_folder, exist_ok=True)

    # Check if user information has been cached locally
    if not os.path.exists(os.path.join(user_folder, LEAD_SUMMARY_FILENAME)):
        user_info = extract_user_info(user_id)
        save_lead_summary(user_folder, user_info)
    else:
        user_info = read_lead_summary(user_folder)

    return user_info
