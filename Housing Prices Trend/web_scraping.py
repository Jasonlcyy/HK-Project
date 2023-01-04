#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 19:05:02 2022

@author: jasonlcyy
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import re
import numpy as np
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

# function for reading data based on different tabs
def read_data(tab):
    # list object to store data from different tabs
    tab_stat = []
    if tab == 'cost-of-living':
        # select the currency menu and select USD to standardize currency
        element = Select(browser.find_element_by_xpath('//*[@id="displayCurrency"]'))
        element.select_by_visible_text('USD')
        for i in range(2, 66):
            if i not in [10, 30, 39, 43, 47, 50, 55, 60, 63]:
                temp = browser.find_element('xpath', '/html/body/div[2]/table/tbody/tr[{}]/td[2]/span'.format(str(i)))
                tab_stat.append(check_data(temp.text))
    elif tab == 'property-investment':
        for i in range(2, 9):
            temp = browser.find_element('xpath', '/html/body/div[2]/div[2]/table/tbody/tr[{}]/td[2]'.format(str(i)))
            tab_stat.append(check_data(temp.text))
    elif tab == 'quality-of-life':
        for i in range(1, 11):
            if i != 9:
                temp = browser.find_element('xpath', '/html/body/div[2]/table/tbody/tr[{}]/td[2]'.format(str(i)))
                tab_stat.append(check_data(temp.text))
    return tab_stat

# function for reading column / row names for different tabs
def read_column(tab):
    # list object to store column names for different tabs
    tab_stat = []
    if tab == 'cost-of-living':
        for i in range(2, 66):
            if i not in [10, 30, 39, 43, 47, 50, 55, 60, 63]:
                temp = browser.find_element('xpath', '/html/body/div[2]/table/tbody/tr[{}]/td[1]'.format(str(i)))
                tab_stat.append('Cost of Living - ' + check_data(temp.text))
    elif tab == 'property-investment':
        for i in range(2, 9):
            temp = browser.find_element('xpath', '/html/body/div[2]/div[2]/table/tbody/tr[{}]/td[1]'.format(str(i)))
            tab_stat.append('Property Prices - ' + check_data(temp.text))
    elif tab == 'quality-of-life':
        for i in range(1, 11):
            if i != 9:
                temp = browser.find_element('xpath', '/html/body/div[2]/table/tbody/tr[{}]/td[1]'.format(str(i)))
                tab_stat.append('Quality of Life - ' + check_data(temp.text))
    return tab_stat

# adjust data scraped for better readability / data types
def check_data(text):
    # return nan if there is no data
    if text == '?':
        return np.nan
    # remove currency symbol and convert to float
    elif re.search('.*\$', text):
        return float(text.replace(',', '')[:len(text)-2])
    # remove ':' at the end of some column names
    elif re.search('.*:', text):
        return text[:len(text)-1]
    # try to convert numbers to float, if error directly return string
    else:
        try:
            return float(text)
        except:
            return text

# if the page is not available for that city, return an array of nan
def initialize_data(tab):
    tab_stat = []
    if tab == 'cost-of-living':
        for i in range(55):
            tab_stat.append(np.nan)
    elif tab == 'property-investment':
        for i in range(7):
            tab_stat.append(np.nan)
    elif tab == 'quality-of-life':
        for i in range(9):
            tab_stat.append(np.nan)
    return tab_stat

# chromedriver path
driver_path = "/Users/jasonlcyy/Downloads/chromedriver"

# Chrome Options preventing timeout error
ChromeOptions = webdriver.ChromeOptions()

ChromeOptions.add_argument('--disable-browser-side-navigation')

browser = webdriver.Chrome(executable_path = driver_path, chrome_options=ChromeOptions)

# first scrap cities available in the website
cities = []

# sites which have ranking available
sites = ['cost-of-living', 'property-investment', 'quality-of-life', 'crime', 'health-care', 'pollution', 'traffic']

# years available
time_list = [ x for x in range(2009, 2023) ]

# suffices for the ranking sites
suffix_list = ['-mid', '-Q1', '']

cities_lookup = "https://www.numbeo.com/{}/rankings.jsp?title={}{}"

for site in sites:
    for period in time_list:
        for suffix in suffix_list:
            browser.get(cities_lookup.format(site, str(period), suffix))
            for row in range(1, 511):
                try:
                    temp = browser.find_element('xpath', '//*[@id="t2"]/tbody/tr[{}]/td[2]'.format(str(row)))
                    # only append if the city is not already in the city list
                    if temp.text not in cities:
                        cities.append(temp.text)
                except:
                    break

# quit browser after scraping cities
browser.quit()

# open new browser to scrap city data
browser = webdriver.Chrome(executable_path = driver_path, chrome_options=ChromeOptions)

# code to directly access scraped cities to save time
# temp_df = pd.read_csv('/Users/jasonlcyy/Desktop/FINA2390/cities.csv')
# cities = list(temp_df['0'])

# split city name into city, state and country
cities_split = [ x.split(',') for x in cities ]

for x in range(len(cities_split)+1):
    for y in range(0, 3):
        try:
            # adjust city strings format to accommodate format in link text
            cities_split[x][y] = cities_split[x][y].strip()
            cities_split[x][y] = cities_split[x][y].replace('\'', '%27')
            cities_split[x][y] = cities_split[x][y].replace('(', '')
            cities_split[x][y] = cities_split[x][y].replace(')', '')
            cities_split[x][y] = cities_split[x][y].replace(' ', '-')
        except:
            pass

data_lookup = 'https://www.numbeo.com/{}/in/{}'

# tabs to scrap
tabs = ['cost-of-living', 'property-investment', 'quality-of-life']

# list to store row names
column_list = []

# for loop to scrap row names
for tab in tabs:
    browser.get(data_lookup.format(tab, 'Paris'))
    column_list.append(read_column(tab))

# list to store city data
cities_stat = []

for x in range(len(cities_split)):
    # list to store an individual city data
    city_stat = []
    for tab in tabs:
        browser.get(data_lookup.format(tab, str(cities_split[x][0])+'-'+str(cities_split[x][1])))
        try:
            # append if the page is correctly navigated to
            city_stat.append(read_data(tab))
        except NoSuchElementException:
            try:
                # suggestion will be available if the link text is incorrect, if the suggestion matches the city, click and go to the site
                city_button = browser.find_element(By.LINK_TEXT, cities[x])
                city_button.click()
                city_stat.append(read_data(tab))
            except NoSuchElementException:
                try:
                    # option for non-US cities (without state)
                    if len(cities_split[x]) == 2:
                        browser.get(data_lookup.format(tab, str(cities_split[x][0])))
                        try:
                            city_stat.append(read_data(tab))
                        except NoSuchElementException:
                            city_button = browser.find_element(By.LINK_TEXT, cities[x])
                            city_button.click()
                            city_stat.append(read_data(tab))
                    # option for US cities (with state)
                    elif len(cities_split[x]) == 3:
                        city_stat.append(initialize_data(tab))
                except:
                    # initialize the data if not available
                    city_stat.append(initialize_data(tab))
    # append the individual stat to the list of cities
    cities_stat.append(city_stat)

# quit the browser after finishing scraping
browser.quit()

# combine the rows in the 3 tabs 
columns = column_list[0]+column_list[1]+column_list[2]

# dictionary to correspond the city to its data
dict = {}

for x in range(len(cities_stat)):
    dict[cities[x]] = cities_stat[x][0]+cities_stat[x][1]+cities_stat[x][2]

df = pd.DataFrame(data = dict)

# set the column names 
df = df.set_axis(columns)

# invert rows and columns for better readability (City as rows)
df = df.transpose()

# export the result
df.to_csv('/Users/jasonlcyy/Desktop/FINA2390/project3_output.csv')

