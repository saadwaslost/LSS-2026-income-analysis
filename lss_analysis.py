# -*- coding: utf-8 -*-
"""LSS 2026 Data Science - "Is education the way?" (ISL PA Team A)

Exported from the team's Google Colab notebook. Cleaning, descriptive tables and figures.
Data: UCI Adult / Census Income (Becker & Kohavi, 1996), CC BY 4.0, not included in this repo.
Put the CSV at data/adult.csv (see README) and run:  python lss_analysis.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.proportion import proportion_confint


# load the data (in Colab this was read from Google Drive)
path = 'data/adult.csv'

data = pd.read_csv(path, skipinitialspace=True)  # strips the leading spaces in the raw values
print(data)

"""Cleaning the Data"""

# cleaning the data
# value counts, kept for checking categories
#percentages = data['marital-status'].value_counts(normalize=True) * 100
#print(percentages)

# leakage evidence for capital-gain
top_coded = data[data['capital-gain'] == 99999]
print(f"rows at capital-gain 99999: {len(top_coded)}")
print(f"share of them earning >50K: {(top_coded['income'] == '>50K').mean():.1%}")

# '?' marks a missing value in this dataset
data = data.replace('?', np.nan)
#print(data.isnull().sum())

# making native country us, non-us, or unknown if nan ****(we do this later now, after table 2)****
#data['native-country'] = np.where(data['native-country'].isna(), 'Unknown', np.where(data['native-country'] == 'United-States', 'US', 'Non-US'))

# married flag, made before marital-status is dropped
data['married'] = np.where(data['marital-status'].isin(['Married-civ-spouse', 'Married-spouse-absent', 'Married-AF-spouse']), 1, 0)

# remove duplicates
data = data.drop_duplicates()
print(data.duplicated().sum())

# dropping columns which aren't needed
#data = data.drop(columns=['fnlwgt', 'capital-gain', 'capital-loss', 'marital-status', 'relationship', 'race'])
data = data.drop(columns=['fnlwgt', 'capital-gain', 'capital-loss', 'relationship'])

data['occupation-status'] = np.where(data['occupation'].isna(), 'occupation missing', 'occupation present')
data['occupation'] = np.where(data['occupation'].isna(), 'Unknown', data['occupation'])

# drop rows missing education (there are none, kept as a safeguard)
data = data.dropna(subset=['educational-num'])

# grouping of levels of education into education bands and writing the orders as well for both, for our graphs
data['education-band'] = data['education']
data['education-band'] = np.where(data['education-band'].isin(['11th', '9th', '10th', '12th', '7th-8th', '5th-6th', '1st-4th', 'Preschool']), '< HS diploma', data['education-band'])  # edu-num 1-8, hs-grad is 9
data['education-band'] = np.where(data['education-band'].isin(['Some-college', 'Assoc-voc', 'Assoc-acdm']), 'Some college / Assoc.', data['education-band']) # edu-num 10-12, bachelors is 13
data['education-band'] = np.where(data['education-band'].isin(['Masters', 'Prof-school', 'Doctorate']), 'Postgraduate', data['education-band']) # edu-num 14-16
education_band_order = ['< HS diploma', 'HS-grad', 'Some college / Assoc.', 'Bachelors', 'Postgraduate']
education_order = ['Preschool', '1st-4th', '5th-6th', '7th-8th', '9th', '10th', '11th', '12th', 'HS-grad', 'Some-college', 'Assoc-voc', 'Assoc-acdm', 'Bachelors', 'Masters', 'Prof-school', 'Doctorate']

# age and hours bands
data['age-band'] = pd.cut(data['age'], bins=[16, 25, 35, 45, 55, 65, 90])
data['hours-band'] = pd.qcut(data['hours-per-week'], q=5, duplicates='drop')

# text categories to 0/1
data['gender'] = np.where(data['gender'] == 'Male', 1, 0)  # 1 for male, 0 for female
data['income'] = np.where(data['income'] == '>50K', 1, 0)  # 1 for >50K, 0 for <=50K
#print(data)

"""Graphs & Analysis"""

# graph 1:
counts = data['education-band'].value_counts()
labels = [f"{band}\nn={counts[band]:,}" for band in education_band_order]

occupation_rates = data.groupby('occupation')['income'].mean().sort_values()
sorted_occupations = occupation_rates.index.tolist()

ct = pd.crosstab(data['education-band'], data['occupation'])

ct = ct.div(ct.sum(axis=1), axis=0) * 100

ct = ct.reindex(index=education_band_order)

ct = ct[sorted_occupations]

fig, ax = plt.subplots(figsize=(12, 6))
colors = plt.cm.RdYlBu(np.linspace(0.1, 0.95, len(sorted_occupations)))

ct.plot(kind='bar', stacked=True, ax=ax, color=colors, width=0.7, edgecolor='white', linewidth=0.5)

ax.set_title('Occupation mix by Education Bands', fontsize=12, pad=15)
ax.set_xlabel('Education Band (n shown below each bar)', fontsize=11, labelpad=10)
ax.set_ylabel('Share of people in each occupation (%)', fontsize=11)
ax.set_ylim(0, 100)

ax.set_xticklabels(labels, rotation=0, fontsize=10)

handles, labels = ax.get_legend_handles_labels()
ax.legend(list(reversed(handles)), list(reversed(labels)), title='Occupations', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)

plt.tight_layout()
plt.show()

# graph 2
data['income-percent'] = data['income'] * 100  # as a percentage

fig_data = data.groupby('education')['income-percent'].mean().reindex(education_order)

fig, ax = plt.subplots(figsize=(12, 6))

fig_data.plot(kind='bar', ax=ax, color='#3B6FB6', width=0.8)

ax.set_title('Share earning >$50K by education level', pad=15)
ax.set_ylabel('Share earning >$50K (%)')
ax.set_xlabel('Education Level')

ax.set_xticklabels(education_order, rotation=45, ha='right')

plt.tight_layout()
plt.show()

# graph 3
gender_colors = {1: "#1f77b4", 0: "#e377c2"}

fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(
    data=data,
    x='education',
    y='income-percent',
    hue="gender",
    palette=gender_colors,
    order=education_order,
    errorbar=None,
    ax=ax
)

ax.set_title('Share earning >$50K by educational level and gender', pad=15)
ax.set_ylabel('Share earning >$50K (%)')
ax.set_xlabel('Education Level')
ax.set_xticklabels(education_order, rotation=45, ha='right')

handles, labels = ax.get_legend_handles_labels()
ax.legend(list(handles), ["Female", "Male"], title='Gender', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)

plt.tight_layout()
plt.show()

# table 1
print(data.shape[0])
table = data.groupby('occupation-status').agg(
    n=('occupation-status', 'size'),
    rate_50K=('income', lambda x: x.mean() * 100),
    mean_age=('age', 'mean'),
    mean_education=('educational-num', 'mean'),
    mean_hours=('hours-per-week', 'mean')
).round({
    'rate_50K': 2,
    'mean_age': 1,
    'mean_education': 2,
    'mean_hours': 1
})

table.columns = ['n', 'rate >$50K', 'mean age', 'mean education', 'mean hours']

print(table)

# table 2
overall_rate = data['income'].mean()
total_squared_deviation = ((data['income'] - overall_rate) ** 2).sum()

variables = {
    'Marital status': 'marital-status',
    'Education': 'education',
    'Occupation': 'occupation',
    'Age Band': 'age-band',
    'Hours Band': 'hours-band',
    'Gender': 'gender',
    'Workclass': 'workclass',
    'Race': 'race',
    'Native Country': 'native-country'
}

results = []
for display_name, col_name in variables.items():
    series = data[col_name].dropna()  # occupation already has 'Unknown' filled in

    stats = data.groupby(series, observed=False)['income'].agg(n='count', rate='mean')

    rate_range = (stats['rate'].max() - stats['rate'].min()) * 100

    # eta-squared= sum of [n * (category_rate - overall_rate)^2] / total squared deviation
    explained_variance = (stats['n'] * (stats['rate'] - overall_rate) ** 2).sum()
    eta_squared = (explained_variance / total_squared_deviation) * 100

    results.append({
        'Variable': display_name,
        'categories': len(stats),
        'range': rate_range,
        'η²': eta_squared
    })

# final table
table = pd.DataFrame(results)

# add rankings
table['rank by range'] = table['range'].rank(ascending=False).astype(int)
table['rank by η²'] = table['η²'].rank(ascending=False).astype(int)

table = table.sort_values('rank by η²').reset_index(drop=True)

# formatting
table['range'] = table['range'].round(1).astype(str) + 'pp'
table['η²'] = table['η²'].round(2).astype(str) + '%'

table = table[['Variable', 'categories', 'range', 'rank by range', 'η²', 'rank by η²']]

print(table.to_string(index=False))

# group into 3 countries here (which we commented earlier in data cleaning)
data['native-country'] = np.where(data['native-country'].isna(), 'Unknown', np.where(data['native-country'] == 'United-States', 'US', 'Non-US'))

# table 3: rate by education level with 95% Wilson intervals
stats = data.groupby(['educational-num', 'education'])['income'].agg(
    n='count',
    n_50K='sum'
).reset_index()

stats['rate_calc'] = stats['n_50K'] / stats['n']

lower, upper = proportion_confint(
    count=stats['n_50K'],
    nobs=stats['n'],
    alpha=0.05,
    method='wilson'
)
stats['rate'] = (stats['rate_calc'] * 100).round(1).astype(str) + '%'
stats['95% CI (Wilson)'] = '[' + (lower * 100).round(1).astype(str) + ', ' + (upper * 100).round(1).astype(str) + ']'

table = stats[['education', 'n', 'n_50K', 'rate', '95% CI (Wilson)']].copy()
table.columns = ['education level', 'n', 'n >50K', 'rate', '95% CI (Wilson)']

print(table.to_string(index=False))

target_occupations = ['Exec-managerial', 'Prof-specialty']
data['top_occ'] = data['occupation'].isin(target_occupations).astype(int)

data['education-band'] = pd.Categorical(data['education-band'], categories=education_band_order, ordered=True)

table = data.groupby('education-band', observed=False).agg(
    n=('education-band', 'count'),
    occ_rate=('top_occ', 'mean'),
    income_rate=('income', 'mean')
).reset_index()

table['% in Exec-managerial or Prof-specialty'] = (table['occ_rate'] * 100).round(1).astype(str) + '%'
table['>$50K rate'] = (table['income_rate'] * 100).round(1).astype(str) + '%'

final_table = table[['education-band', 'n', '% in Exec-managerial or Prof-specialty', '>$50K rate']]

print(final_table.to_string(index=False))

# graph 4
stats = data.groupby(['educational-num', 'education'])['income'].agg(
    n='count',
    n_50K='sum',
    rate='mean'
).reset_index()

stats['rate_pct'] = stats['rate'] * 100

p = stats['rate']
n = stats['n']
z = 1.95996

denominator = 1 + (z**2 / n)
center = p + (z**2 / (2 * n))
std_dev = np.sqrt((p * (1 - p) / n) + (z**2 / (4 * (n**2))))

lower_bound = (center - z * std_dev) / denominator
upper_bound = (center + z * std_dev) / denominator

lower_err = stats['rate_pct'] - (lower_bound * 100)
upper_err = (upper_bound * 100) - stats['rate_pct']

sns.set_theme(style="ticks")
fig, ax = plt.subplots(figsize=(12, 5))

ax.errorbar(
    x=stats['education'],
    y=stats['rate_pct'],
    yerr=[lower_err, upper_err],
    fmt='-o',
    color='#1f497d',
    ecolor='#8c96a0',
    capsize=4,
    elinewidth=1.5,
    markeredgewidth=1.5,
    linewidth=2
)

base_rate = data['income'].mean() * 100
ax.axhline(base_rate, color='#c0504d', linestyle='--', linewidth=1.2)
ax.text(
    x=0.5, y=base_rate + 1.5,
    s=f"base rate {base_rate:.1f}%",
    color='#c0504d', fontsize=11
)

#ax.annotate(
 #   "credential jump\n7.3% → 15.9%",
  #  xy=(8.2, 12),
   # xytext=(4.5, 33),
    #arrowprops=dict(arrowstyle="->", color="#555555", lw=1.2),
   # fontsize=11,
    #color="black"
#)

ax.set_ylabel("% earning >$50K", fontsize=12)
ax.set_xlabel("")
ax.set_ylim(-2, 85)
plt.xticks(rotation=45, ha='right', fontsize=11)

plt.figtext(
    0.5, -0.15,
    "Bars are 95% Wilson intervals. Prof-school vs Doctorate: p = 0.55, not distinguishable.",
    ha="center", fontsize=11, color="#555555"
)

sns.despine()
plt.tight_layout()
plt.show()