import argparse

from src.sales_automation import process


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
        "--user_id",
        type=str,
        default="andrew-huberman",
        help="User ID to write personalized message to",
    )
    parser.add_argument(
        "--style",
        type=str,
        default="Professional",
        help="Style of a personalized message",
    )

    return parser.parse_args()


def run():
    args = parse_arguments()
    url = args.url
    user_id = args.user_id
    style = args.style
    process(url, user_id, style)


if __name__ == "__main__":
    run()
