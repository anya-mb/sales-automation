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

<img width="683" alt="example" src="https://github.com/anya-mb/sales-automation/assets/47106377/d5a77d6f-28d0-423c-8d68-6ed0ecc6f5b6">

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

To run streamlit frontend for text chat:
```
streamlit run app.py
```
