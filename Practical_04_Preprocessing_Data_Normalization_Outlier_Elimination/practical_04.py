"""
Practical 4: Preprocessing, Data Normalization & Outlier Elimination
Name: Shivam Singh | Roll No. 56 | Student ID 5135873 | T.Y. Data Science
"""

# ===== Part A – Missing Values, Duplicates & Min-Max Normalization =====
import pandas as pd

data = {
    'Name': ['Amit', 'Riya', 'Amit', 'Neha', None, 'Riya'],
    'Age': [22, 24, 22, None, 26, 24],
    'Marks': [85, 90, 85, 78, None, 90]
}

df = pd.DataFrame(data)

df['Age'] = df['Age'].fillna(df['Age'].mean())
df['Marks'] = df['Marks'].fillna(df['Marks'].mean())
df['Name'] = df['Name'].fillna('Unknown')
df = df.drop_duplicates()

df['Marks_Normalized'] = (df['Marks'] - df['Marks'].min()) / (df['Marks'].max() - df['Marks'].min())
df['Age_Normalized'] = (df['Age'] - df['Age'].min()) / (df['Age'].max() - df['Age'].min())

print(df[['Name', 'Age_Normalized', 'Marks_Normalized']])



# ===== Part B – Outlier Elimination (IQR), Low Variance Selection & Feature Histograms =====
from sklearn.feature_selection import VarianceThreshold

Q1, Q3 = df['Age'].quantile(0.25), df['Age'].quantile(0.75)
IQR = Q3 - Q1

df_clean = df[(df['Age'] >= Q1 - 1.5*IQR) & (df['Age'] <= Q3 + 1.5*IQR)]

selector = VarianceThreshold(threshold=0.0)
numeric_df = df_clean.select_dtypes(include='number')
selected_columns = numeric_df.columns[selector.fit(numeric_df).get_support()]

print("Selected Features:", selected_columns.tolist())

