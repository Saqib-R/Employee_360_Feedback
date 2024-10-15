from openai import AzureOpenAI
import os
from dotenv import load_dotenv


load_dotenv()
# Initialize Azure OpenAI client
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION") 
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

client = AzureOpenAI()

# client = AzureOpenAI(api_key=AZURE_OPENAI_API_KEY, endpoint=AZURE_OPENAI_ENDPOINT, api_version=OPENAI_API_VERSION)

def exp_summarize_feedback(feedbacks, prompt):
    if not feedbacks:
        return "No feedback provided."

    summaries = []
    full_prompt = f"{prompt}:\n\n" + "\n".join(feedbacks)

    try:
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=150,
            top_p=0.9,
            frequency_penalty=0.5
        )
        summary = res.choices[0].message.content.strip()
        summaries.append(summary)

    except Exception as e:
        return f"Error during summarization: {str(e)}"

    return summaries

def cust_summarize_feedback(feedbacks, user_prompt):
    if not feedbacks:
        return "No feedback provided."

    prompt = f"{user_prompt}\n\n" + "\n".join(feedbacks)

    try:
        res = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150,
            top_p=0.9,
            frequency_penalty=0.5
        )
        summary = res.choices[0].message.content.strip()  

    except Exception as e:
        return f"Error during summarization: {str(e)}"

    return summary
