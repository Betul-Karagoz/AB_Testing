Comparison of the AB Test and Conversion of Bidding Methods
#####################################################

#####################################################
# Business Problem
#####################################################

# Facebook recently launched an alternative to the existing "maximumbidding" type of bidding
# introduced a new type of bidding, "average bidding". One of our clients is bombabomba.com,
# decided to test this new feature and found that averagebidding converts more than maximumbidding
#He wants to do an A/B test to see if it brings # A/B testing has been going on for 1 month and
# bombabomba.com is now waiting for you to analyze the results of this A/B test for Bombabomba.com
# the ultimate success metric is Purchase. Therefore, statistical tests should focus on the Purchase metric.

#####################################################
# Data Set Story
#####################################################

# What users see and click on in this data set containing a company's website information
# includes information such as the number of ads, as well as information about the earnings from them. Check and Test
#There are two separate data sets, the # group. These data sets are on separate sheets of ab_testing.xlsxexcel
# takes. Maximum Bidding was applied to the control group and Average Bidding to the test group.

# impression: Number of ad views
# Click: Number of clicks on the displayed ad
# Purchase Number of products purchased after clicked ads
# Earning: Earnings from purchased products

#####################################################
# Project Tasks
#####################################################

######################################################
# AB Testing (Independent Two Sample T Test)
######################################################

# 1. Set up Hypotheses
# 2. Assumption Check
# - 1st Normality Assumption (shapiro)
# Homogeneity of Variance (levene)
# Implementation of the Hypothesis
# Independent two sample t-test if assumptions are met
# Mannwhitneyu test if assumptions are not met
# 4. Interpret results according to p-value
# Note:
# - Direct number 2 if normality is not ensured. If variance homogeneity is not ensured, enter argument in number 1.
# - It may be useful to perform outlier inspection and correction before normality inspection.

#####################################################
# Task 1: Preparing and Analyzing Data
#####################################################

import numpy as np
import pandas as pd
# *pip install statsmodels import in terminal 
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

####################################################
# Step 1: Read the data set named ab_testing_data.xlsx which consists of control and test group data.
# Assign control and test group data to separate variables.
####################################################

df1= pd.read_excel("DataScience/datasets/ab_testing.xlsx", sheet_name="Control Group")
df2= pd.read_excel("DataScience/datasets/ab_testing.xlsx", sheet_name="Test Group")

#####################################################
# Step 2: Analyze the control and test group data.
#####################################################

df1.info()
df1.head()
df1.describe().T
df1.quantile([0,0.05,0.50,0.95,0.99,1]).T
df1.shape
df1.dtypes
df1.isnull().sum()


df2.info()
df2.head()
df2.describe().T
df2.quantile([0,0.05,0.50,0.95,0.99,1]).T
df2.shape
df2.dtypes
df2.isnull().sum()

#####################################################
# Step 3: After the analysis,
# combine the control and test group data using the concat method.
#####################################################

df1["Group"]="Control"
df2["Group"]="Test"
df1.head()
df2.head()

pd.concat([df1, df2])
df= pd.concat([df1, df2])
df.head()
df.tail()
df["Group"].unique()

#####################################################
# Task 2: Defining the Hypothesis of the A/B Test
#####################################################

#####################################################
# Step 1: Define the hypothesis.
#####################################################

#H0: M1=M2 (between the control group with Maximumbidding and the test group with Averagebidding
# there is no statistically significant difference in the mean number of purchases)

#H1: M1!=M2 (between the control group offered Maximumbidding and the test group offered Averagebidding
# there is a statistically significant difference in the mean number of purchases)

#####################################################
# Step 2: Analyze the mean purchase (gain) for the control and test group
#####################################################

df.groupby("Group").agg({"Purchase": "mean"})

#####################################################
# TASK 3: Performing Hypothesis Testing
#####################################################

######################################################
# AB Testing (Independent Two Sample T Test)
######################################################

######################################################
# Step 1: Make assumption checks before conducting hypothesis testing. These are the Assumption of Normality and Homogeneity of Variance.
######################################################

# Test whether the control and test groups meet the normality assumption separately on the Purchase variable

# H0: The assumption of normal distribution is satisfied.( H0 CANNOT BE REJECTED if p-value < 0.05)
# H1:.The assumption of normal distribution is not satisfied.(HO RED if p-value < 0.05.)

test_stat, pvalue = shapiro(df.loc[df["Group"] == "Control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#p-value=0.5891
##p-value < 0.05, so HO cannot be rejected, the values of the control group fulfill the normality assumption.

test_stat, pvalue = shapiro(df.loc[df["Group"] == "Test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#p-value = 0.1541
##p-value < 0.05, so H0 cannot be rejected, the values of the test group satisfy the normality assumption.

##In this case it is necessary to evaluate whether the homogeneity of variance is satisfied.

##### HOMOGENEITY OF VARIANCE
#H0 : Homogeneity of variance is ensured.
#H1 : Homogeneity of variance is not achieved.

test_stat, pvalue = levene(df.loc[df["Group"] == "Control", "Purchase"],
                           df.loc[df["Group"] == "Test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value < 0.05, so H0 cannot be rejected, the values of the control and test group satisfy homogeneity of variance
# (Variances are homogeneous)

######################################################
# Step 2: Select the appropriate test based on the Assumption of Normality and Homogeneity of Variance results
######################################################

### Since both assumptions are met, an independent two-sample t-test (parametric test) is used.

test_stat, pvalue = ttest_ind(df.loc[df["Group"] == "Control", "Purchase"],
                              df.loc[df["Group"] == "Test", "Purchase"],
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value = 0.3493
#Since the condition #p-value < 0.05 is not met, the hypothesis established at the beginning of the study cannot be rejected.

######################################################
# Step 3: Considering the p_value obtained as a result of the test, the control and test group purchase
## Interpret whether there is a statistically significant difference between the averages.
######################################################

###The hypothesis established at the beginning of the study cannot be rejected because the condition of p-value < 0.05 is not met.
## That is, there is no statistically significant difference between the experimental and control groups in terms of purchase averages.
# The difference between the mean sales (Purchase) of the two groups is random.

######################################################
# TASK 4 : Analysis of Results
#####################################################

#######################################################
# Step 1: Indicate which test is used and why.
#######################################################


##In order to analyze the variable "Purchase" by control and test groups, first use the "Shapira Method" we evaluated the normality assumption.
# p-value <0.05 condition is not met, so the normality assumption is met.
#As a next step, we checked the homogeneity variance with "Levene's Method".
#We found that the variances were homogeneous since the p-value <0.05 condition was not met.
#Since both assumptions were correct, an independent two sample t-test (parametric test) was used. As a result,
#the hypothesis cannot be rejected since the p<0.05 condition is not met again.
#We have reached our conclusion.

# Our hypothesis is :
# "#H0: There is no statistically significant difference in the mean number of purchases between the control group with Maximumbidding
# and the test group with Averagebidding)", so we assume that the difference in the mean number of purchases is random.

########################################################
# Step 2: Make a recommendation to the customer based on the obtained test results .
########################################################

####Averagebidding and Maximumbidding bidding types were analyzed and the results showed no significant difference
# in terms of number of purchases and revenue return. While there is always the possibility that changes offered to customers
#can often bring novelty and dynamism and help to increase sales in the long run, there does not appear to be a statistical necessity
#to make a forced choice between the two at this time.
#After examining the visuals and prices, either one can be chosen at will.
# However, as mentioned before, it is advisable to compare again by recording data (clicks, interactions, etc.) as the products spread
# in the market and prove themselves socially. For this purpose, differences in the proportions of these data
# the duration of the test may have to be prolonged while it is being evaluated.
