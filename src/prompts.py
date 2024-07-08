PERSONALIZED_MESSAGE_PROMPT = """
I have provided the facts and summary about a user, as well as the facts and summary about my company. Additionally, there are chunks of information from my company that highlight mutual interests and potential benefits for the user. Please create a hyper-personalized sales message using this information. The style of the message should be [insert style, e.g., formal, friendly, persuasive, etc.]. Add something to praise the user and build connections with them. Say more about how my company can improve their life and business than about me.

User Facts and Summary:

Name: [User Name]
Company: [User's Company]
Role: [User's Role]
Interests: [User's Interests]
Pain Points: [User's Pain Points]
Goals: [User's Goals]
Summary: [Summary about the user]
My Company Facts and Summary:

Company Name: [My Company Name]
Industry: [Industry]
Key Products/Services: [Key Products/Services]
Unique Selling Points: [Unique Selling Points]
Company Values: [Company Values]
Success Stories: [Success Stories]
Summary: [Summary about my company]
Closest Chunks from RAG with Company Information:

[Chunk 1]
[Chunk 2]
[Chunk 3]
Style:
[Insert style, e.g., formal, friendly, persuasive, etc.]

Example of Output:

Hyper-Personalized Sales Message:

Dear [User Name],

I hope this message finds you well. I recently came across your impressive work at [User's Company], particularly your role as [User's Role]. Your leadership in [specific project or achievement] and your dedication to [User's Interests] are truly inspiring. It's clear that you are deeply committed to [User's Goals], and I admire how you have addressed [User's Pain Points] with such innovative approaches.

At [My Company Name], we share your passion for excellence and innovation. Our mission is to empower professionals like you with our [Key Products/Services], specifically designed to enhance your work and make your goals more achievable.

For instance, [Chunk 1] highlights how our solutions can directly address [User's Pain Points], providing you with tools to streamline your processes and achieve better results. Moreover, [Chunk 2] showcases how we align with your values of [specific value], ensuring that our partnership is not only beneficial but also harmonious with your vision.

Our [Unique Selling Points] have been instrumental in transforming the operations of many clients, much like [Success Story], where we helped [another client] achieve [specific outcome]. I believe that our expertise can similarly propel your initiatives forward, making your work easier, more efficient, and significantly more impactful.

I'd love to explore how we can tailor our services to support your outstanding efforts at [User's Company] and discuss the potential benefits that our collaboration could bring to your business.

Thank you for your time, and I look forward to the opportunity to connect.

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
