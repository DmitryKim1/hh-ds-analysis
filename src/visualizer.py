import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np
import re

# Определяем корень проекта
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ ПОСТРОЕНИЯ ГРАФИКОВ
# =============================================================================

def plot_experience_distribution(df, save_dir):
    """Распределение требований к опыту работы"""
    plt.figure()
    exp_counts = df['experience'].value_counts()
    exp_counts.plot(kind='bar', color='skyblue')
    plt.title('Требуемый опыт работы')
    plt.xlabel('Опыт работы')
    plt.ylabel('Количество вакансий')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'experience_distribution.png'))
    plt.close()

def plot_top_skills(df, save_dir, top_n=15):
    """Топ навыков в вакансиях"""
    # Собираем все навыки в один список
    all_skills = [skill for sublist in df['skills'].dropna() for skill in sublist]
    
    # Считаем частоту навыков
    if not all_skills:
        print("⚠️ Нет данных о навыках для построения графика")
        return
    
    skills_series = pd.Series(all_skills)
    top_skills = skills_series.value_counts().head(top_n)
    
    plt.figure()
    top_skills.sort_values().plot(kind='barh', color='lightgreen')
    plt.title(f'Топ {top_n} навыков для Data Scientist')
    plt.xlabel('Количество упоминаний')
    plt.ylabel('Навык')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'top_skills.png'))
    plt.close()

def clean_text(text):
    """Очистка текста от HTML-тегов и специальных символов"""
    if not text or not isinstance(text, str):
        return ""
    text = re.sub(r'<[^>]+>', '', text)  # Удаление HTML
    text = re.sub(r'[^\w\s]', '', text)   # Удаление пунктуации
    return text.lower().strip()

def generate_requirements_wordcloud(df, save_dir):
    """Облако слов из требований и обязанностей"""
    # Собираем текст из нескольких источников
    texts = []
    
    # Добавляем требования
    if 'requirements' in df:
        texts.extend(
            clean_text(req) for req in df['requirements'].fillna('').astype(str) 
            if clean_text(req) != ''
        )
    
    # Добавляем обязанности
    if 'responsibility' in df:
        texts.extend(
            clean_text(resp) for resp in df['responsibility'].fillna('').astype(str)
            if clean_text(resp) != ''
        )
    
    # Объединяем весь текст
    full_text = ' '.join(texts)
    
    # Проверяем наличие текста
    if not full_text.strip():
        print("⚠️ Нет текста для создания облака слов")
        return
    
    # Создаем и сохраняем облако слов
    try:
        wordcloud = WordCloud(
            width=1200, 
            height=800,
            background_color='white',
            colormap='viridis',
            max_words=100,
            collocations=False
        ).generate(full_text)
        
        plt.figure(figsize=(15, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Частые слова в описании вакансий', fontsize=18)
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'combined_wordcloud.png'))
        plt.close()
        print("✅ Облако слов успешно создано")
    except Exception as e:
        print(f"❌ Ошибка при создании облака слов: {e}")

def plot_salary_distribution(df, save_dir):
    """Распределение зарплат"""
    # Фильтруем только вакансии с указанной зарплатой
    salary_df = df.dropna(subset=['salary_from', 'salary_to'])
    
    if salary_df.empty:
        print("⚠️ Нет данных о зарплатах для построения графика")
        return
    
    plt.figure()
    
    # Средняя зарплата для визуализации
    salary_df = salary_df.copy()
    salary_df['avg_salary'] = (salary_df['salary_from'] + salary_df['salary_to']) / 2
    
    # Удаляем выбросы - верхние 5%
    threshold = salary_df['avg_salary'].quantile(0.95)
    filtered_salaries = salary_df[salary_df['avg_salary'] <= threshold]
    
    sns.histplot(filtered_salaries['avg_salary'], bins=30, kde=True, color='salmon')
    plt.title('Распределение зарплат (среднее значение)')
    plt.xlabel('Зарплата (руб.)')
    plt.ylabel('Количество вакансий')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'salary_distribution.png'))
    plt.close()

def plot_salary_by_experience(df, save_dir):
    """Зарплата в зависимости от опыта работы"""
    # Фильтруем только вакансии с указанной зарплатой
    salary_df = df.dropna(subset=['salary_from', 'salary_to'])
    
    if salary_df.empty:
        print("⚠️ Нет данных о зарплатах для построения графика")
        return
    
    # Рассчитываем среднюю зарплату
    salary_df = salary_df.copy()
    salary_df['avg_salary'] = (salary_df['salary_from'] + salary_df['salary_to']) / 2
    
    # Удаляем выбросы
    threshold = salary_df['avg_salary'].quantile(0.95)
    filtered_salaries = salary_df[salary_df['avg_salary'] <= threshold]
    
    # Группируем по опыту работы
    plt.figure()
    sns.boxplot(
        x='experience', 
        y='avg_salary', 
        data=filtered_salaries,
        palette='pastel',
        showfliers=False
    )
    plt.title('Зарплата в зависимости от опыта работы')
    plt.xlabel('Опыт работы')
    plt.ylabel('Средняя зарплата (руб.)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'salary_by_experience.png'))
    plt.close()

# =============================================================================
# ОСНОВНЫЕ ФУНКЦИИ МОДУЛЯ
# =============================================================================

def setup_visuals():
    """Создает необходимые директории для сохранения результатов"""
    try:
        # Создаем директории для графиков
        figures_dir = os.path.join(PROJECT_ROOT, "results", "figures")
        os.makedirs(figures_dir, exist_ok=True)
        print(f"✅ Директория для графиков: {figures_dir}")
        
        # Создаем директории для обработанных данных
        processed_dir = os.path.join(PROJECT_ROOT, "data", "processed")
        os.makedirs(processed_dir, exist_ok=True)
        print(f"✅ Директория для данных: {processed_dir}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка при создании директорий: {e}")
        return False

def analyze_and_visualize(df):
    """Анализирует данные и создает визуализации"""
    try:
        # 1. Сохранение обработанных данных
        processed_dir = os.path.join(PROJECT_ROOT, "data", "processed")
        csv_path = os.path.join(processed_dir, "processed_vacancies.csv")
        df.to_csv(csv_path, index=False)
        print(f"💾 Данные сохранены: {csv_path}")
        
        # 2. Настройка стиля графиков
        sns.set_style("whitegrid")
        plt.rcParams.update({
            'figure.figsize': (12, 6),
            'font.size': 14,
            'axes.titlesize': 16,
            'axes.titleweight': 'bold'
        })
        
        # 3. Создаем графики
        figures_dir = os.path.join(PROJECT_ROOT, "results", "figures")
        
        # График 1: Распределение опыта работы
        plot_experience_distribution(df, figures_dir)
        
        # График 2: Топ навыков
        plot_top_skills(df, figures_dir)
        
        # График 3: Облако слов требований и обязанностей
        generate_requirements_wordcloud(df, figures_dir)
        
        # График 4: Распределение зарплат
        plot_salary_distribution(df, figures_dir)
        
        # График 5: Зарплата по опыту работы
        plot_salary_by_experience(df, figures_dir)
        
        print(f"📊 Все визуализации сохранены в: {figures_dir}")
        return True
    except Exception as e:
        print(f"❌ Ошибка при визуализации: {e}")
        return False