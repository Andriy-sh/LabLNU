import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from openai import OpenAI

client = OpenAI(api_key='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')  # Замініть на ваш API ключ

df = pd.read_csv('2018.csv')

data_overview = {
    'Інформація про дані': str(df.info()),
    'Опис даних': str(df.describe()),
    'Кількість пропущених значень': str(df.isnull().sum())
}

correlation_matrix = df.corr(numeric_only=True)

skewness = df.select_dtypes(include=np.number).apply(lambda x: stats.skew(x.dropna()))
kurtosis = df.select_dtypes(include=np.number).apply(lambda x: stats.kurtosis(x.dropna()))

shapiro_results = {}
for column in df.select_dtypes(include=np.number).columns:
    shapiro_results[column] = stats.shapiro(df[column])

ks_results = {}
for column in df.select_dtypes(include=np.number).columns:
    ks_results[column] = stats.kstest(df[column], 'norm')

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Кореляційна матриця')
plt.savefig('correlation_heatmap.png')

report = f"""
Звіт аналізу набору даних

1. Огляд даних:
Інформація про дані:
{data_overview['Інформація про дані']}

Опис даних:
{data_overview['Опис даних']}

Кількість пропущених значень:
{data_overview['Кількість пропущених значень']}

2. Кореляційна матриця:
{correlation_matrix.to_string()}

3. Асиметрія:
{skewness.to_string()}

4. Ексцес:
{kurtosis.to_string()}

5. Тест Шапіро-Вілка:
{shapiro_results}

6. Тест Колмогорова-Смірнова:
{ks_results}
"""

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ви - аналітик даних, який пояснює результати українською мовою."},
            {"role": "user", "content": f"Поясніть ці результати: {report}"}
        ]
    )
    explanation = response.choices[0].message.content
except Exception as e:
    explanation = f"Помилка: {str(e)}"

with open('data_analysis_report.txt1', 'w', encoding='utf-8') as f:
    f.write('\n\nПояснення OpenAI українською:\n' + explanation)

print('Звіт згенеровано та збережено у файлі "data_analysis_report.txt"')