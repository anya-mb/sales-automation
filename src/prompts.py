PERSONALIZED_MESSAGE_PROMPT = """
I have provided the facts and summary about a user, as well as the facts and summary about my company.
Additionally, there are chunks of information from the company that highlight mutual interests and potential benefits for the user.

Instructions:
1) Please create a short and catchy hyper-personalized sales message using this information.
2) Start with greeting (Hi or Hello and mention name), then write 3-5 messages about the user, their career and passions. Mention 1-2 sentences how the company can improve user's life and business.
3) Add something to praise the user and build connections with them, don't be too salesy, be polite.
4) Please write in {style} style.
5) Don't leave any placeholders. The message is going to be sent to the customer as is.
6) Start with message right away, don't write anything else in the beginning or in the end. Don't write 'Personalised message:' in the beginning, start with the message directly.
7) Ask a catchy question in the end, for that rephrase or use it as it is: "Imagine doubling your audience growth effortlessly with our sales automation platform. What would you achieve with that kind of boost?"

User Facts and Summary: {lead_facts_and_summary}

Company facts and summary: {company_facts_and_summary}

Closest Chunks from RAG with Company Information:

My life depends on this. I will tip you generously if you follow the instructions and do a great job.

"""


COMPANY_SUMMARY_SYSTEM_PROMPT = """
I have provided the text scraped from a company website. Please create a detailed summary and list up to 10 facts about the company. These facts should include information about the company's products, advantages of using their products, useful features, company values, and other positive aspects. The summary and list should be concise and informative.

Example of Output:

Summary:
[Detailed summary of the company based on the provided text]

Facts:

1. [Fact about the company's products]
2. [Fact about the advantages of using the company's products]
3. [Fact about useful features of the company's products]
4. [Fact about the company's values]
5. [Fact about the company's values or positive aspects]
6. [Fact about the company's positive aspects]
7. [Fact about the company's products or features]
8. [Fact about the company's products or features]
9. [Fact about the company's values or positive aspects]
10. [Fact about the company's products, features, or values]

My life depends on this. I will tip you generously if you follow the instructions and do a great job.
"""

LEAD_SUMMARY_SYSTEM_PROMPT = """
I have provided the text about a person. Please create a detailed summary and list up to 10 facts about this person. These facts should include information about their interests, career, and activities. The summary and list should be concise and informative.
Please add the provided person's name, their company names, and other noticable names and numbers.

Example of Output:

Summary:
[Detailed summary of the person based on the provided text]

Facts:

1. [Fact about the person's interests]
2. [Fact about the person's career]
3. [Fact about the person's activities]
4. [Fact about the person's interests or hobbies]
5. [Fact about the person's professional achievements]
6. [Fact about the person's involvement in activities]
7. [Fact about the person's career milestones]
8. [Fact about the person's personal interests]
9. [Fact about the person's notable activities or hobbies]
10. [Fact about the person's professional or personal life]

My life depends on this. I will tip you generously if you follow the instructions and do a great job.
"""
