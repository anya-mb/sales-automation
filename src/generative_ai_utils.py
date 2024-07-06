import re

SUMMARY_SYSTEM_PROMPT = """
I'm scraping website to learn more about the product it offers, what are the benefits of using it and what are the competitive advantages of this company or its products.

Help me decide what 10 links out of all links should I scrape, put the most useful links first, I'll send you links. Return the JSON with key "useful_links" and value is list of links.

My life depends on this. I will tip you generously if you follow the instructions and do a great job. Only return the JSON with key "useful_links" and value is list of links, no other text is needed.

"""


def clean_llm_output(llm_output: str) -> str:
    # Use regex to remove everything before the first { and after the last }
    cleaned_output = re.sub(
        r"^.*?({.*}).*$", r"\1", llm_output.lower(), flags=re.DOTALL
    )
    return cleaned_output


def build_rag(website_info: str, datapath: str) -> bool:
    # save to datapath and rag_directory
    return False


def get_facts_and_summary(summary_info: str) -> str:
    # generates company facts and summary with LLM
    return ""


def get_presonalised_message(
    company_facts_and_summary: str, lead_facts_and_summary: str, rag_datapath: str
) -> str:
    # prompt for LLM with company_facts_and_summary, lead_facts_and_summary and rag chuncks
    return "You're the best! Buy out product!"
