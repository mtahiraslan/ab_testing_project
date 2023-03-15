# =====================================================================================================
# Comparison of AB Test and Conversion of Bidding Methods
# =====================================================================================================

# =====================================================================================================
# Project Tasks
# =====================================================================================================
import numpy as np
import pandas as pd
from scipy.stats import shapiro, levene, ttest_ind

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 50)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.width', 500)

# Task 1: Preparing and Analyzing Data
# Step1: Step 1: Read the dataset ab_testing_data.xlsx consisting of control and test group data.
# Assign control and test group data to separate variables.

control_df = pd.read_excel("Measurement_Problems/ab_testing.xlsx", sheet_name="Control Group")
test_df = pd.read_excel("Measurement_Problems/ab_testing.xlsx", sheet_name="Test Group")

# Step 2: Analyze control and test group data.


def check_dataframe(df, row_num=5):
    print("*************** Dataset Shape ***************")
    print("No. of Rows:", df.shape[0], "\nNo. of Columns:", df.shape[1])
    print("*************** Dataset Information ***************")
    print(df.info())
    print("*************** Types of Columns ***************")
    print(df.dtypes)
    print(f"*************** First {row_num} Rows ***************")
    print(df.head(row_num))
    print(f"*************** Last {row_num} Rows ***************")
    print(df.tail(row_num))
    print("*************** Summary Statistics of The Dataset ***************")
    print(df.describe().T)
    print("*************** Dataset Missing Values Analysis ***************")
    print(missing_values_analysis(df))


def missing_values_analysis(df):
    na_columns = [col for col in df.columns if df[col].isnull().sum() > 0]
    n_miss = df[na_columns].isnull().sum().sort_values(ascending=True)
    ratio = (df[na_columns].isnull().sum() / df.shape[0] * 100).sort_values(ascending=True)
    missing_df = pd.concat([n_miss, np.round(ratio, 2)], axis=1, keys=['Total Missing Values', 'Ratio'])
    missing_df = pd.DataFrame(missing_df)
    return missing_df


check_dataframe(control_df)
check_dataframe(test_df)

# Step 3: After the analysis process, combine the control and test group data using the concat method.

test_df['group'] = 'test'
control_df['group'] = 'control'

df = pd.concat([control_df, test_df], axis=0, ignore_index=True)

df

# Task2: Defining the Hypothesis of A/B Testing
# Step 1: Define the hypothesis.

# =====================================================================================================
# Answer
# =====================================================================================================
# These are hypotheses used in statistical hypothesis testing, where we're comparing the means of two populations,
# denoted by M1 and M2.
#
# H0: M1 = M2 means that there is no significant difference between the means of the two populations.
# This is also known as the null hypothesis.
#
# H1: M1 ≠ M2 means that there is a significant difference between the means of the two populations.
# This is also known as the alternative hypothesis.
#
# In hypothesis testing, we collect data from both populations and use statistical tests to determine whether
# we can reject the null hypothesis in favor of the alternative hypothesis. If the p-value
# (the probability of obtaining the observed results or more extreme results under the null hypothesis)
# is smaller than the significance level (a pre-determined threshold), we reject the null hypothesis and
# conclude that there is evidence of a significant difference between the means of the two populations.
# Otherwise, we fail to reject the null hypothesis.

# Step 2: Analyze the purchase (earning) averages for the control and test group.

df.groupby('group').agg({'Purchase': 'mean'})
# control   550.894
# test      582.106

# Task3: Performing Hypothesis Testing
# Step 1: Perform hypothesis checks before hypothesis testing.
# These are Assumption of Normality and Homogeneity of Variance. Test separately whether the control and test groups
# comply with the assumption of normality over the Purchase variable.

#  a.Normality Assumption
# H0: Normal distribution assumption is provided.
# H1: Normal distribution assumption is not provided.
# p < 0.05 H0 REJECT , p > 0.05 H0 CANNOT REJECT
# Is the assumption of normality according to the test result provided for the control and test groups?
# Interpret the p-values obtained.

test_stat, test_pvalue = shapiro(df.loc[df['group'] == 'control', 'Purchase'])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, control_pvalue))
# Test Stat = 0.9773, p-value = 0.5891

test_stat, test_pvalue = shapiro(df.loc[df['group'] == 'test', 'Purchase'])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, test_pvalue))
# Test Stat = 0.9589, p-value = 0.1541

# Note: The p-value of the Control Group and Test Group is above 0.05. In this case, we cannot reject the H0 hypothesis.
# The assumption of normality is provided.

# b. Variance Homogeneity
# H0: Variances are homogeneous.
# H1: Variances are not homogeneous.
# p < 0.05 H0 REJECT , p > 0.05 H0 CANNOT REJECT
# Test whether the homogeneity of variance is provided for the control and test groups over the Purchase variable.
# Is the assumption of normality provided according to the test result? Interpret the p-values obtained.

test_stat, pvalue = levene(df.loc[df['group'] == 'test', 'Purchase'],
                           df.loc[df['group'] == 'control', 'Purchase'])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 2.6393, p-value = 0.1083

# Note: Since the p-value is greater than 0.05, we cannot reject the H0 hypothesis.
# In this case, the variance is homogeneous.

# Step 2: Select the appropriate test according to the Normality Assumption and Variance Homogeneity results.
# =====================================================================================================
# Answer
# =====================================================================================================
# Since both assumptions are satisfied, we will apply the independent two-sample t-test (parametric test).

# Step 3: Considering the p_value obtained as a result of the test, interpret whether there is a statistically
# significant difference between the purchasing averages of the control and test groups.

test_stat, pvalue = ttest_ind(test_df['Purchase'], control_df['Purchase'], equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9416, p-value = 0.3493

# Conclusion: The p_value is greater than 0.05. So we cannot reject the H0 hypothesis. In this case,
# there is no statistically significant difference between the purchase averages of the control and test groups.
# We can say that this difference occurred by chance.

# Task 4: Analysis of Results
# Step 1: Which test did you use, state the reasons.
# =====================================================================================================
# Answer
# =====================================================================================================
# We used the shapiro method from the scipy library in the Assumption of Normality stage,
# we used the levene method from the scipy library in the Variance Homogeneity stage, and finally we looked at
# the p_value value we obtained and decided that the independent two-sample t-test (parametric test) was appropriate.

# Step 2: Advise the customer according to the test results you have obtained.
# =====================================================================================================
# Answer
# =====================================================================================================
# As a result, in the A/B test conducted by bombabomba.com to test a new feature, there is no significant difference
# in terms of Purchase (gain) averages between the control and test groups, regarding whether average bidding leads to
# more conversions than maximum bidding. Since there is no difference, we recommend the customer to use both methods.













