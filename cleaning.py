'''
Quynh Doan, Andrew Michaels, and Nolan Kim
CSE 163 Final Project
The file hold functions to clean excel
and csv files.
'''

import pandas as pd


def accessByState():
    '''
    Clean internet access by state table
    '''
    filepath = 'files/state_vs_internet access.xls'
    stateInternet = pd.read_excel(filepath)
    return stateInternet


def degreesByState():
    '''
    Clean STEM degrees by state table and
    remove excel formatting.
    '''
    filepath = 'files/college-19-1.xls'
    df = pd.read_excel(filepath)
    col_name = 'Science and engineering degrees as a percentage of higher' +\
               ' education degrees conferred, by state: 2001, 2006, and 2011'
    df = df.rename(columns={
        col_name: 'State',
        'Unnamed: 1': 'All S&E degrees_2001',
        'Unnamed: 2': 'All S&E degrees_2006',
        'Unnamed: 3': 'All S&E degrees_2011',
        'Unnamed: 5': 'All higher education degrees_2001',
        'Unnamed: 6': 'All higher education degrees_2006',
        'Unnamed: 7': 'All higher education degrees_2011',
        'Unnamed: 9': 'All S&E degrees/all higher_2001',
        'Unnamed: 10': 'All S&E degrees/all higher_2006',
        'Unnamed: 11': 'All S&E degrees/all higher_2011'})
    degrees = df.iloc[4:55, ]
    degrees = degrees.drop(columns=["Unnamed: 4",
                                    "Unnamed: 8"])
    return degrees


def householdIncomes():
    '''
    Clean Median Household Income Table and
    remove excel formatting.
    '''
    filepath = 'files/stateonline_13.xls'
    df = pd.read_excel(filepath)

    df = df.iloc[5:7, :].T
    df = pd.DataFrame(data=df)
    df.reset_index(drop=True, inplace=True)
    df = df.iloc[4:, 0:2]
    houseIncomes = df.rename(columns={5: 'States',
                                      6: 'Median Household Income'})
    return houseIncomes


def race_income():
    '''
    Cleans the State vs Internet Access data
    to read in floats rather than strings for
    each desired percentage column
    '''
    file_name = 'files/state_vs_internet access.csv'
    internet_access = pd.read_csv(file_name)
    internet_access = internet_access.dropna()
    internet_access['white'] = list(map(lambda x: x[:-1],
                                        internet_access['white'].values))
    internet_access['black'] = list(map(lambda x: x[:-1],
                                        internet_access['black'].values))
    internet_access['asian'] = list(map(lambda x: x[:-1],
                                        internet_access['asian'].values))
    internet_access['latino'] = list(map(lambda x: x[:-1],
                                         internet_access['latino'].values))
    internet_access['total'] = list(map(lambda x: x[:-1],
                                        internet_access['total'].values))
    internet_access['white'] = [
        float(x) for x in internet_access['white'].values]
    internet_access['black'] = [
        float(x) for x in internet_access['black'].values]
    internet_access['asian'] = [
        float(x) for x in internet_access['asian'].values]
    internet_access['latino'] = [
        float(x) for x in internet_access['latino'].values]
    internet_access['total'] = [
        float(x) for x in internet_access['total'].values]
    return internet_access
