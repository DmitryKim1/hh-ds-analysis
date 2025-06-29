import requests
import time
import yaml

def load_config():
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)

def get_full_vacancy(vacancy_id):
    url = f"https://api.hh.ru/vacancies/{vacancy_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка при получении вакансии {vacancy_id}: {e}")
        return None

def get_hh_vacancies():
    config = load_config()["api"]
    url = "https://api.hh.ru/vacancies"
    all_vacancies = []
    
    for page in range(config["max_pages"]):
        try:
            params = {
                "text": config["query"],
                "area": config["area"],
                "period": config["period"],
                "per_page": 100,
                "page": page
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            all_vacancies.extend([v for v in data.get("items", []) if v.get("id")])
            
            if page >= data.get("pages", 0) - 1:
                break
                
            time.sleep(config["request_delay"])
                
        except Exception as e:
            print(f"Ошибка на странице {page}: {e}")
            break
    
    print(f"Найдено вакансий: {len(all_vacancies)}")
    
    full_data = []
    for vacancy in all_vacancies:
        full_vac = get_full_vacancy(vacancy["id"])
        if full_vac:
            full_data.append(full_vac)
        time.sleep(config["request_delay"])
    
    return full_data