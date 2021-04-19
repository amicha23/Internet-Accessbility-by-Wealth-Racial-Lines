'''
Quynh Doan, Andrew Michaels, and Nolan Kim
CSE 163 Final Project
This file holds all of our functions
to produce our graphs and maps.
'''

import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
import Joining
import cleaning


def high_school_internet_to_degree(merged):
    '''
    Plot scatter plots showing high school internet
    accessibility percentages vs STEM degree attainment
    in states where the median household income was
    less than the national average.
    '''
    avgMedianIncome = merged['Median Household Income'].mean()
    income_mask = merged['Median Household Income'] < avgMedianIncome
    belowAvgMedianIncome = merged[income_mask]
    years = [2001, 2006, 2011]
    for year in years:
        sns.relplot(data=belowAvgMedianIncome,
                    x='high school',
                    y='All S&E degrees_' + str(year))
        plt.title('High School Internet Access vs STEM Degrees' +
                  'per State below Avg Median Household Income (' +
                  str(year) + ')')
        plt.xlabel('High School Student Internet Accessbility(%)')
        plt.ylabel('STEM Degrees')
        plt.savefig('high_school_internet_' + str(year) + '.png')


def income_distributions(income, race):
    '''
    Display income distributions by
    racial group 'race' on a bar chart.
    '''
    income = income.iloc[:, 3:12]
    income = income.T
    income.reset_index(inplace=True)
    income = income.iloc[:, 0:2]
    sns.catplot(x='index', y=0, data=income, palette="Blues_d", kind='bar')
    plt.xticks(fontsize=9, rotation=45)
    plt.xlabel('')
    plt.ylabel('Income Distribution(%)')
    plt.title('Income Distribution by ' + race + ' Race 2019')
    plt.savefig(race + '_income_distributions.png')


def race_internet_access(internet_access):
    '''
    Display internet access for each racial
    group on a bar chart
    '''
    white = internet_access['white'].mean()
    asian = internet_access['asian'].mean()
    black = internet_access['black'].mean()
    hispanic = internet_access['latino'].mean()
    total = internet_access['total'].mean()
    means = [white, asian, black, hispanic, total]
    races = ['White', 'Asian', 'Black', 'Hispanic', 'Total']
    x_pos = [i for i, _ in enumerate(races)]
    plt.ylim([60, 100])
    fig, ax = plt.subplots(1)
    plt.bar(x_pos, means, color='green')
    plt.xlabel("Racial Groups")
    plt.ylabel("Percentage (%)")
    plt.title("Internet Access for each Race")
    plt.xticks(x_pos, races)
    plt.savefig('internet_by_race.png')


def race_internet_access_offset(internet_access):
    '''
    Display internet access average offset for each racial
    group on a bar chart
    '''
    total = internet_access['total'].mean()
    white = internet_access['white'].mean() - total
    asian = internet_access['asian'].mean() - total
    black = internet_access['black'].mean() - total
    hispanic = internet_access['latino'].mean() - total
    means = [white, asian, black, hispanic]
    races = ['White', 'Asian', 'Black', 'Hispanic']
    x_pos = [i for i, _ in enumerate(races)]
    plt.ylim([-20, 20])
    fig, ax = plt.subplots(1)
    plt.bar(x_pos, means, color='blue')
    plt.xlabel("Racial Groups")
    plt.ylabel("Percentage (%)")
    plt.title("Internet Access for each Race Offset")
    plt.xticks(x_pos, races)
    plt.savefig('internet_by_race_offset.png')


def map_state_internet(result):
    '''
    Display internet access by state on GeoData Map of US.
    '''
    fig, ax = plt.subplots(1, figsize=(15, 7))
    result.plot(color='#CCCCCC', ax=ax)
    result.plot(column='total', legend=True, ax=ax)
    plt.title('Internet Access in each US State')
    plt.savefig('access_map.png')


def income_vs_internet(result2):
    '''
    Display regression plot of internet access vs median household income.
    '''
    sns.lmplot(x='total',
               y='Median Household Income',
               data=result2)
    plt.title('Income level vs Internet Access in US States')
    plt.xlabel('Internet Access')
    plt.ylabel('Income level')
    plt.savefig('regression_access.png')


def map_state_highest_se(country2, result3):
    '''
    Display above average S&E distributions by state on GeoData Map of US.
    '''
    fig, ax = plt.subplots(1, figsize=(15, 7))
    country2.plot(color='#CCCCCC', ax=ax)
    result3.plot(column='All S&E degrees/all higher_2011',
                 legend=True,
                 ax=ax)
    plt.title('States with highest S&E degrees distributed')
    plt.savefig('highest_STEM_map.png')


def map_state_highest_internet(country2, result5):
    '''
    Display S&E distributions by state on GeoData Map of US.
    '''
    fig, ax = plt.subplots(1, figsize=(15, 7))
    country2.plot(color='#CCCCCC', ax=ax)
    result5.plot(column='total',
                 legend=True,
                 ax=ax)
    plt.title('States with highest access to internet')
    plt.savefig('highest_internet_map.png')


def stem_vs_internet(result4):
    '''
    Display regression plot of internet access vs stem occupations by state.
    '''
    sns.jointplot(data=result4,
                  x="total",
                  y="All S&E degrees/all higher_2011",
                  kind="reg")
    plt.title('STEM occupations vs Internet Access in US States')
    plt.xlabel('Internet Access by State')
    plt.ylabel('STEM degrees/all higher degrees by State')
    plt.savefig('STEM_regression.png')


def main():
    sns.set()
    merged = Joining.joined_table()
    high_school_internet_to_degree(merged)

    white_income = pd.read_csv('files/white_income distribution.csv')
    income_distributions(white_income, 'White')
    hispanic_income = pd.read_csv('files/hispanic_income distribution.csv')
    income_distributions(hispanic_income, 'Hispanic')
    all_income = pd.read_csv('files/all_race_income_distribution.csv')
    income_distributions(all_income, 'All')
    asian_income = pd.read_csv('files/asian_income_distribution.csv')
    income_distributions(asian_income, 'Asian')
    black_income = pd.read_csv('files/black_income distribution.csv')
    income_distributions(black_income, 'Black')

    internet_access = cleaning.race_income()
    race_internet_access(internet_access)
    race_internet_access_offset(internet_access)
    country = gpd.read_file('files/gz_2010_us_040_00_5m.json')
    country2 = country[
        (country['NAME'] != 'Alaska') & (country['NAME'] != 'Hawaii')]
    result = Joining.load_country_merged2()
    map_state_internet(result)
    result2 = Joining.load_in_data2()
    income_vs_internet(result2)
    result3 = Joining.load_country_merged()
    map_state_highest_se(country2, result3)
    result4 = Joining.load_in_data()
    stem_vs_internet(result4)
    result5 = Joining.load_country_merged3()
    map_state_highest_internet(country2, result5)


if __name__ == '__main__':
    main()
