import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def query_llm(prompt):
    """
    Simple wrapper to call the OpenAI GPT-4 model.
    """
    try:
        print('query_llm')
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        print(response)
        return response['choices'][0]['message']['content']

    except Exception as e:
        print(e)


def analyze_text(text):
    print('analyze_text')
    prompt = f"""Summarize the following clinical note and list potential diseases or diagnoses mentioned or implied:

    {text}

    Summary:
    Potential Diseases:"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response['choices'][0]['message']['content']
    summary, *diseases = content.split("Potential Diseases:")
    return summary.strip(), diseases[0].strip().splitlines()
