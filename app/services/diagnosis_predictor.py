# app/services/diagnosis_predictor.py

from openai import OpenAI

client = OpenAI()


def predict_diagnosis(text: str) -> dict:
    """
    Predicts possible diseases from a clinical note and maps them to ICD-10 codes.
    Returns a dictionary of {"disease": "ICD-10 code"}.
    """
    prompt = (
        "Extract the most probable diseases from the following clinical note and map each one "
        "to an ICD-10 code. Return the result as a JSON dictionary with diseases as keys and ICD-10 codes as values.\n\n"
        f"{text}"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a clinical NLP assistant that returns diagnoses with ICD-10 codes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    # Try to parse JSON response safely
    try:
        import json
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        return {"error": "Failed to parse ICD-10 response", "details": str(e)}

#
#
#
# from app.services.llm_agent import query_llm
#
# # Simple hardcoded ICD-10 mapping
# ICD10_MAP = {
#     "Diabetes": "E11",
#     "Hypertension": "I10",
#     "Asthma": "J45",
#     "Chronic kidney disease": "N18",
#     "Coronary artery disease": "I25"
# }
#
#
# def predict_diseases_with_icd10(text):
#     prompt = f"""
#     You are a medical AI assistant. From the following clinical note, identify possible diagnoses and provide
#     their most likely ICD-10 codes. Format:
#     - Disease Name: ICD-10 Code
#
#     {text}
#     """
#     response = query_llm(prompt)
#     diseases = {}
#     for line in response.splitlines():
#         if ":" in line:
#             name, code = line.split(":", 1)
#             diseases[name.strip()] = code.strip()
#     return diseases
#
#
# def predict_diseases(text):
#     prompt = f"""Analyze the following clinical note and list the potential diseases (one per line):
#
# {text}
#
# Diseases:"""
#     response = query_llm(prompt)
#     lines = response.split("\n")
#     diseases = [line.strip("-• ").strip() for line in lines if line.strip()]
#
#     mapped = [{"disease": d, "icd10": ICD10_MAP.get(d, "Unknown")} for d in diseases]
#     return mapped