Анализ вакансий Data Scientist с HeadHunter

Проект для автоматического сбора, обработки и визуализации данных о вакансиях Data Scientist с сайта hh.ru.

Особенности:
- Автоматический сбор данных через API hh.ru
- Очистка и обработка сырых данных
- 5 автоматически генерируемых визуализаций
- Экспорт результатов в CSV и PNG

Структура проекта:
config/
  config.yaml         - Конфигурация API и параметров поиска
data/
  processed/          - Обработанные данные (CSV)
  raw/                - Сырые данные (JSON)
results/
  figures/            - Графики и визуализации
src/
  api_client.py       - Клиент для работы с API HH.ru
  data_processor.py   - Обработка сырых данных
  main.py             - Основной скрипт
  visualizer.py       - Визуализация данных
.gitignore            - Игнорируемые файлы
LICENSE               - Лицензия MIT
README.md             - Эта документация
requirements.txt      - Зависимости

Установка:
1. Клонируйте репозиторий:
   git clone https://github.com/DmitryKim1/hh-ds-analysis.git
   cd hh-ds-analysis

2. Установите зависимости:
   pip install -r requirements.txt

3. Создайте конфигурационный файл:
   mkdir -p config
   cp config/config_example.yaml config/config.yaml
   (отредактируйте config/config.yaml под свои нужды)

Запуск:
python src/main.py

Результаты будут сохранены в:
- data/processed/processed_vacancies.csv
- results/figures/

Примеры визуализаций:
- Топ навыков: results/figures/top_skills.png
- Распределение зарплат: results/figures/salary_distribution.png

Лицензия:
Этот проект распространяется под лицензией MIT. См. файл LICENSE.
