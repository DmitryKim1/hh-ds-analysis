from api_client import get_hh_vacancies
from data_processor import process_vacancies
from visualizer import analyze_and_visualize, setup_visuals
import traceback
import sys
import os

print("=== ДИАГНОСТИКА ЗАПУСКА ===")

try:
    print("Попытка импорта api_client...")
    from api_client import get_hh_vacancies
    print("✅ api_client импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта api_client: {str(e)}")
    traceback.print_exc()

try:
    print("Попытка импорта data_processor...")
    from data_processor import process_vacancies
    print("✅ data_processor импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта data_processor: {str(e)}")
    traceback.print_exc()

try:
    print("Попытка импорта visualizer...")
    from visualizer import analyze_and_visualize, setup_visuals
    print("✅ visualizer импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта visualizer: {str(e)}")
    traceback.print_exc()

print("\n=== ЗАПУСК ОСНОВНОЙ ПРОГРАММЫ ===\n")

def main():
    # Создаём необходимые папки при запуске
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("results/figures", exist_ok=True)
    print("🔄 Запуск анализа вакансий Data Scientist")
    setup_visuals()
    
    try:
        print("1. Получение данных с hh.ru...")
        vacancies = get_hh_vacancies()
        
        if vacancies:
            print(f"✅ Получено {len(vacancies)} вакансий")
            print("2. Обработка данных...")
            df = process_vacancies(vacancies)
            
            if not df.empty:
                print(f"✅ Обработано {len(df)} записей")
                print("3. Анализ и визуализация...")
                analyze_and_visualize(df)
            else:
                print("⚠️ После обработки данные отсутствуют")
        else:
            print("⚠️ Не удалось получить данные с hh.ru")
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {str(e)}")
        traceback.print_exc()
    
    print("🏁 Завершено!")

if __name__ == "__main__":
    main()