import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def clean_description(html_text):
    if not html_text or not isinstance(html_text, str):
        return ""
    
    try:
        soup = BeautifulSoup(html_text, "html.parser")
        text = soup.get_text()
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
        return text
    except:
        return html_text

def process_vacancies(vacancies):
    processed = []
    for vacancy in vacancies:
        # Проверка наличия объекта зарплаты
        salary = vacancy.get("salary")
        
        row = {
            "id": vacancy.get("id"),
            "name": vacancy.get("name"),
            "salary_from": salary.get("from") if salary else None,
            "salary_to": salary.get("to") if salary else None,
            "salary_currency": salary.get("currency") if salary else None,
            "experience": vacancy.get("experience", {}).get("name"),
            "schedule": vacancy.get("schedule", {}).get("name"),
            "employment": vacancy.get("employment", {}).get("name"),
            "requirements": vacancy.get("snippet", {}).get("requirement"),
            "responsibility": vacancy.get("snippet", {}).get("responsibility"),
            "skills": [skill.get("name") for skill in vacancy.get("key_skills", [])],
            "published_at": vacancy.get("published_at")
        }
        processed.append(row)
    return pd.DataFrame(processed)
