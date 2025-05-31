# app/services/summarizer.py

from openai import OpenAI

client = OpenAI()


def summarize_text(text: str) -> str:
    """Summarizes the given clinical note."""
    print('summarize_text')
    response = client.chat.completions.create(
        model="gpt-4",  # or 'gpt-3.5-turbo' if you're using that instead
        messages=[
            {"role": "system", "content": "You are a clinical note summarizer."},
            {"role": "user", "content": f"Summarize the following clinical note:\n\n{text}"}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

