# Is education the way to earn more? LUMS Science Symposium 2026

> Team entry for the Data Science stream of the LUMS Science Symposium (August 2026). Using 48,842 records from the 1994 US Census, we asked whether education is the main route to earning over $50K, what else matters, and for whom education pays more or less.

| | |
|---|---|
| **Team** | ISL PA Team A, five students from International School Lahore |
| **Event** | LUMS Science Symposium 2026, Data Science stream (organised by SPADES, LUMS) |
| **My role** | Led the analytical framework (the hypotheses, what to control for and what not to) and the methodology defence in the panel Q&A |
| **Tools** | Python (pandas, NumPy, statsmodels, matplotlib, seaborn) in Google Colab |

## The question
The organisers asked: *"Is education the way to earn more income or does the data suggest something else, what factors can change this?"* We split it into three parts:
1. **Is education *the* way?** Rank every variable by how much of the income difference it explains.
2. **Or something else?** Is another factor, such as occupation, doing part of the work?
3. **What can change this?** For whom does education pay more, or less?

## Data
The UCI Adult ("Census Income") dataset: 48,842 employed adults from the 1994 US Census, each with 14 characteristics and whether they earn over $50K (23.9% do). Citation: Becker, B. & Kohavi, R. (1996), UCI Machine Learning Repository, [doi:10.24432/C5XW20](https://doi.org/10.24432/C5XW20), CC BY 4.0. The data is not included here; see [data/README.md](data/README.md).

Cleaning decisions worth knowing:
- **Capital gains and losses removed as leakage.** All 244 rows at the column's maximum (99,999) earn over $50K: it's a cap value, and the income label already includes capital gains.
- **Missing occupation kept, not dropped.** The 2,805 people with no recorded occupation are very different: 9.45% earn over $50K versus 24.83% (z = −18.5). Dropping them would bias the results.
- 52 duplicate rows removed, leaving 48,790.

## Findings
- **Education matters, but it isn't the whole story.** It explains 13.4% of the variation in who earns over $50K (η²). That's more than occupation (12.3%), age (9.7%), hours (7.5%), sex (4.6%) or race (1.0%). Only marital status explains more (20.1%), and that figure is distorted: the dataset leaves out most married women.
- **The first credential matters most.** The rate barely moves from preschool (1.2%) to 12th grade (7.3%), then doubles to 15.9% with a high-school diploma.
- **About a third of education's effect runs through occupation.** Bachelor's graduates out-earn high-school graduates by 25.6 percentage points. Of that, 7.0 points come from working in different jobs and 18.6 from being paid more in the same job. Depending on the baseline chosen, the job share is 27% to 40%.
- **The gender gap is constant, not widening.** In percentage points it grows from 13.9 to 31.2 as education rises. But as an odds ratio it stays near 3.7× at every level, so the growth comes from the rising base rate.
- **The payoff depends on who you are.** One more education level is worth 5.6 points for men and 3.2 for women, 6.9 for married people and 2.3 for unmarried, and 0.3 for under-25s rising to 6.6 at ages 45–55.

**Limits.** The data is from 1994 and includes only people with a job, so education's effect on getting a job at all is invisible and every estimate is a lower bound. These are associations, not causal effects. The full list is in the deck.

## Methods
Rates are reported with group sizes and 95% Wilson confidence intervals. The standard formula gave a negative lower bound for small groups, which is why we didn't use it. Gaps are checked with two-proportion z-tests. Variables are ranked by η² rather than by the range between groups, because the range can be driven by a group of 10 people. Round 2 added:
- a regression with education, age, age², sex and birth region, deliberately leaving out occupation and hours, which lie on the path from education to income
- Mantel–Haenszel odds ratios for the gender gap
- four robustness checks

## Files
- `LSS2026_deck.pdf`: the 20-slide presentation (Round 1 and Round 2).
- `lss_analysis.py`: the team's Colab notebook, exported. It covers the cleaning, the missing-occupation table, the η² ranking, the Wilson interval table, the occupation table and four figures. The Round 2 models (the regression, decomposition and odds ratios) are not in this file. Comments were tidied for publication; the code itself is unchanged.
- `data/`: where to put the dataset.

To run: `pip install pandas numpy matplotlib seaborn statsmodels`, add the CSV as `data/adult.csv`, then `python lss_analysis.py`.

## Credits
ISL PA Team A: Saad Muhammad Malik (Team Lead), Ch. Muhammad Umer Shahid, Inayah Jawad, Hania Hammad Hashmi and Minahil Rashid.

## Licence
All rights reserved by the team. The dataset is © its creators, CC BY 4.0.
