from openai import AzureOpenAI
import os

# Initialize Azure OpenAI client
client = AzureOpenAI()

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
