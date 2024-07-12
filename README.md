# 🚀 Personalized Sales Message Generator

## 🎯 Transform Your Sales Strategy with AI-Powered Personalization!


Welcome to the **Personalized Sales Message Generator** repository! This cutting-edge tool is designed to help sales professionals craft engaging, customized sales messages based on detailed company insights and LinkedIn user profiles. Harnessing the power of OpenAI’s GPT models and Langchain, this tool brings a new level of personalization and efficiency to your sales outreach.

## 🔍 What is it?

Our **Personalized Sales Message Generator** takes your target company's website information and a LinkedIn user ID to generate compelling, tailored sales messages. Whether you're looking to win over potential clients or create meaningful connections, this tool provides you with the perfect message every time!

## 🚀 Features

- **AI-Powered Personalization**: Leverage OpenAI’s GPT models to create messages that resonate with your audience.
- **Dynamic Data Processing**: Extract and analyze information from company websites for relevant insights.
- **LinkedIn Integration**: Utilize LinkedIn user IDs to craft messages that address your prospects’ unique needs and interests.
- **Easy to Use**: Streamlined setup and intuitive interface for seamless integration into your sales process.

## 🤩 How it looks like?
### 🎓💻 Sales messages for an educational company / University / online courses:
<img width="668" alt="Friendly" src="https://github.com/user-attachments/assets/607f5b0d-f882-495d-864a-d933f5571b90">


### 💡🤖 Sales messages for an innovative software company:
<img width="665" alt="professional" src="https://github.com/user-attachments/assets/d40efe88-6a10-4b2e-aea5-f4713c03ede9">

### 🏋️‍♂️🧘‍♂️ Sales messages for a fitness company:
<img width="684" alt="fitness" src="https://github.com/user-attachments/assets/78a371ac-8574-4b91-8817-d524296b7117">

### 💼📈 Sales messages for a sales company:
<img width="679" alt="Intriguing" src="https://github.com/user-attachments/assets/28b3050b-0a44-4b20-b52c-0fee6efa41f8">


### 🛍️🍰 Sales messages for a retail company / cafe:
<img width="673" alt="bakery" src="https://github.com/user-attachments/assets/942e2c79-98b4-4db6-9afe-33b547010ce4">


This solution can be applied to any other business as well!


## How does it work?

![The sales automation company](https://github.com/user-attachments/assets/b9009c26-c21b-4bf8-8efe-e942453ef8f4)


### Data Mining
1. Customer Provides URL: The sales automation company's customer provides a URL.
2. Crawl Website: The sales automation company crawls the provided website to extract texts.
3. Extract Texts from Website: The extracted texts are processed and summarized using a large language model (LLM).
4. Store Summarized Data: The summarized data, including the URL, company name, summary, and top facts, is stored in the Facts DB.
5. Calculate Embeddings: The extracted texts are chunked, and embeddings are calculated and stored in a Vector DB (RAG).

### Personalized Message Generation
1. Fetch LinkedIn Data: The sales automation company fetches data from the LinkedIn profile of the customer’s lead.
2. Extract Facts from LinkedIn: Facts from the LinkedIn profile are extracted.
3. Calculate Embeddings: Embeddings for these facts are calculated.
4. Find Closest Chunks: The closest chunks from the Vector DB (RAG) are found using the embeddings.
5. Generate Prompt: Using the facts and information about the person, a summary of the company, and relevant chunks, a prompt is generated.
6. Evaluate Output: The generated message is evaluated to ensure it matches the template (mentions customer and their facts, connections, style, etc.).
7. Send to Customer: The final personalized message is sent to the customer.



## 👨‍💻 Setup

Create virtual environment:

```
python -m venv venv
```

Activate the virtual environment:

* On macOS and Linux:

```
source venv/bin/activate
```
* On Windows:
```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```
Install pre-commit hooks:
```
pre-commit install
```

Create a `.env` file in the root directory and add your API keys and other secrets:
```
OPENAI_API_KEY=
LINKEDIN_LOGIN=
LINKEDIN_PASSWORD=
```

## 🕺🏼 Run

To run streamlit frontend for the app:
```
streamlit run app.py
```
