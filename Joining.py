'''
Quynh Doan, Andrew Michaels, and Nolan Kim
CSE 163 Final Project
This file holds functions to
merge the necessary data tables.
'''

import cleaning
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame


def joined_table():
    '''
    Join Internet Accessibility by state, STEM degrees, and Median Household
    Incomes data tables.
    '''
    stateInternet = cleaning.accessByState()
    degrees = cleaning.degreesByState()
    houseIncomes = cleaning.householdIncomes()

    stateAndDegrees = stateInternet.merge(degrees,
                                          left_on="state",
                                          right_on="State")
    merged = stateAndDegrees.merge(houseIncomes,
                                   left_on="state",
                                   right_on="States")
    merged = merged.drop(columns=['States', 'State'])
    return merged


def load_in_data():
    """
    Takes the file name of a CSV of Internet Access by States and the file
    name of a CSV containing S&E job distribution. Return a DataFrame that
    has the two datasets merged together.
    """
    state_internet = pd.read_csv('files/state_vs_internet access.csv')
    state_se = pd.read_csv('files/degrees_vs_states.csv')
    col_name = 'All S&E degrees_2011'
    state_internet['total'] = state_internet['total'].str.rstrip('%')
    state_internet['total'] = state_internet['total'].astype(float) / 100.0
    state_se[col_name] = state_se[col_name].str.replace(',', '')
    state_se[col_name] = state_se[col_name].astype(float)
    result = state_internet.merge(state_se,
                                  left_on='state',
                                  right_on='State',
                                  how='left')
    return result


def load_in_data2():
    """
    Takes the file name of a CSV of Internet Access by States and the file
    name of a CSV containing median household income. Return a DataFrame that
    has the two datasets merged together.
    """
    state_internet = pd.read_csv('files/state_vs_internet access.csv')
    state_income = pd.read_csv('files/MedianHouseholdIncomebyState.csv')
    col_name = 'Median Household Income'
    state_internet['total'] =\
        state_internet['total'].str.rstrip('%').astype('float') / 100.0
    state_income[col_name] =\
        state_income[col_name].str.replace(',', '').astype(float)
    result2 = state_income.merge(state_internet,
                                 left_on='States',
                                 right_on='state',
                                 how='left')
    return result2


def load_country_merged():
    """
    Takes the file name of a json file of US States location and the file
    name of a CSV containing S&E job distribution. Return a GeoDataFrame that
    has the two datasets merged together. Filter for states with above
    average S&E degrees distributed.
    """
    country = gpd.read_file('files/gz_2010_us_040_00_5m.json')
    state_se = pd.read_csv('files/degrees_vs_states.csv')
    state_se = state_se[
        (state_se['State'] != 'Alaska') & (state_se['State'] != 'Hawaii')]
    country2 = country[
        (country['NAME'] != 'Alaska') & (country['NAME'] != 'Hawaii')]
    result = state_se.merge(country2,
                            left_on='State',
                            right_on='NAME',
                            how='left')
    result = result[result['All S&E degrees/all higher_2011'] >= 28]
    return GeoDataFrame(result)


def load_country_merged2():
    """
    Takes the file name of a json file of US States location and the file
    name of a CSV containing internet access by state. Return a GeoDataFrame
    that has the two datasets merged together.
    """
    country = gpd.read_file('files/gz_2010_us_040_00_5m.json')
    state_internet = pd.read_csv('files/state_vs_internet access.csv')
    state_internet['total'] = state_internet['total'].str.rstrip('%')
    state_internet['total'] = state_internet['total'].astype(float) / 100.0
    not_alaska = state_internet['state'] != 'Alaska'
    not_hawaii = state_internet['state'] != 'Hawaii'
    state_internet = state_internet[(not_alaska) & (not_hawaii)]
    country = country[
        (country['NAME'] != 'Alaska') & (country['NAME'] != 'Hawaii')]
    result = state_internet.merge(country,
                                  left_on='state',
                                  right_on='NAME',
                                  how='left')
    return GeoDataFrame(result)


def load_country_merged3():
    """
    Takes the file name of a json file of US States location and the file
    name of a CSV containing internet access by state. Return a GeoDataFrame
    that has the two datasets merged together. Filter for states with above
    average internet access.
    """
    country = gpd.read_file('files/gz_2010_us_040_00_5m.json')
    state_internet = pd.read_csv('files/state_vs_internet access.csv')
    state_internet['total'] = state_internet['total'].str.rstrip('%')
    state_internet['total'] = state_internet['total'].astype(float) / 100.0
    not_alaska = state_internet['state'] != 'Alaska'
    not_hawaii = state_internet['state'] != 'Hawaii'
    state_internet = state_internet[(not_alaska) & (not_hawaii)]
    country = country[
        (country['NAME'] != 'Alaska') & (country['NAME'] != 'Hawaii')]
    result = state_internet.merge(country,
                                  left_on='state',
                                  right_on='NAME',
                                  how='left')
    result = result[result['total'] >= 0.80]
    return GeoDataFrame(result)
