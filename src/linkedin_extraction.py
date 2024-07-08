from dotenv import load_dotenv, find_dotenv
import os
from linkedin_api import Linkedin

_ = load_dotenv(find_dotenv())  # read local .env file

# Authenticate using any Linkedin account credentials
api = Linkedin(os.environ["LINKEDIN_LOGIN"], os.environ["LINKEDIN_PASSWORD"])


def get_user_info(user_id: str) -> str:

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
    print(len(lead_information))

    profile_posts = api.get_profile_posts(user_id, post_count=10)
    posts = "Posts:\n" + "\n\n".join(
        [post.get("commentary").get("text").get("text") for post in profile_posts]
    )
    print(len(posts))
    return "user info"
