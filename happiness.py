#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 21:26:38 2022

@author: jasonlcyy
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import chart_studio
import chart_studio.plotly as py

# chart studio setup
username = 'Jasonlcyy'
api_key = 'M7tIXqtBJct4PZMO6cQJ'
chart_studio.tools.set_credentials_file(username=username,
                                        api_key=api_key)

# read file
happiness_trend = pd.read_csv('/Users/jasonlcyy/Desktop/HK Project/Happiness 2015-2022.csv')

# group by year and attain the average by year
happiness_mean = happiness_trend.groupby(by = 'Year')['Happiness score'].mean().to_numpy()

# empty list to store ranking and score 
happiness_rank = []
happiness_score = []

for year_iter in range(2015, 2023):
    # attain the data of that certain year and sort by score
    temp_year_df = happiness_trend[
        happiness_trend['Year'] == year_iter].sort_values(
            by = 'Happiness score', 
            ascending = False).reset_index(
                drop = True)
    # attain the rank of Hong Kong in that certain year
    rank_temp = temp_year_df[temp_year_df[
                    'Country'].str.startswith(
                        'Hong Kong')].index[0]+1
    # attain the score of Hong Kong in that certain year
    score_temp = happiness_trend[(happiness_trend['Year'] == year_iter) & (happiness_trend['Country'].str.startswith('Hong Kong'))]['Happiness score'].values[0]
    # append the rank and score to the lists
    happiness_rank.append(rank_temp)
    happiness_score.append(score_temp)

# create dataframe storing year, score, rank and global average data
happiness_trend_df = pd.DataFrame({'Year': np.arange(2015, 2023).tolist(),
                                   'Score (HK)': happiness_score,
                                   'Rank (HK)': happiness_rank,
                                   'Global average': happiness_mean.tolist()})

# declare and customise plotly figures                               
happiness_fig = go.Figure()

# add score data as bar chart
happiness_fig.add_trace(go.Bar(x = happiness_trend_df['Year'], y = happiness_trend_df['Score (HK)'],
                         name = 'Hong Kong', yaxis = 'y',
                         marker_color = '#000066'))

# add global average data as bar chart
happiness_fig.add_trace(go.Bar(x = happiness_trend_df['Year'], y = happiness_trend_df['Global average'],
                         name = 'Global Mean', yaxis = 'y',
                         marker_color = '#b3c6ff'))

# add rank data as line chart
happiness_fig.add_trace(go.Scatter(x = happiness_trend_df['Year'], y = happiness_trend_df['Rank (HK)'],
                             mode = 'lines+markers',
                             name = 'Global Rank (Hong Kong)', yaxis = 'y2',
                             marker_color = '#ff8000',
                             marker_size = 9))

# update layout to improve data viz readability
happiness_fig.update_layout(title = 'Happiness Score 2015-2022<br><sup>Global Average Increases Slightly, while Hong Kong Demonstrating the Opposite</sup>',
                      titlefont = dict(size = 28,
                                       family = 'Trajan'),
                      xaxis = dict(title = 'Year',
                                   tickmode = 'linear',
                                   tickfont = dict(size = 15,
                                                   family = 'Trajan'),
                                   titlefont = dict(size = 18,
                                                    family = 'Trajan'),
                                   domain = [0.01, 0.99]),
                      yaxis = dict(title = 'Happiness Score',
                                   tickfont = dict(size = 15,
                                                   family = 'Trajan'),
                                   titlefont = dict(size = 18,
                                                    family = 'Trajan'),
                                   position = 0,
                                   range = [0, 8]),
                      yaxis2 = dict(title = 'Rank',
                                    overlaying = 'y', side = 'right',
                                    showgrid = False,
                                    tickfont = dict(size = 15,
                                                    family = 'Trajan'),
                                    titlefont = dict(size = 18,
                                                     family = 'Trajan'),
                                    position = 1,
                                    range = [160, 0]),
                      bargap = 0.2,
                      bargroupgap = 0.08,
                      legend = dict(
                          x = 0.02,
                          y = 0.98,
                          bgcolor = 'rgba(255, 255, 255, 0)',
                          bordercolor = 'rgba(255, 255, 255, 0)',
                          font = dict(size = 15,
                                      family = 'Trajan')))
# source as footnote
happiness_note = 'Source:<a href="https://worldhappiness.report/">World Happiness Report</a>'

happiness_fig.add_annotation(
    showarrow=False,
    text=happiness_note,
    font=dict(size=13,
              family = 'Trajan'), 
    xref='x domain',
    x=0,
    yref='y domain',
    y=-0.2
    )

py.plot(happiness_fig, filename = "happiness_trend", auto_open = True)

happiness_fig.show()


