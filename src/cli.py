import argparse

from sales_automation import process


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

    return parser.parse_args()


def run():
    args = parse_arguments()
    url = args.url
    process(url)


if __name__ == "__main__":
    run()
