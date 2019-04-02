# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

import plotly 
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='#####', api_key='#####')

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import os

psychoocean = dash.Dash(__name__)

py.sign_in(username='Wourly', api_key='ynOus3rUfBXLzn11FNII')

# LAYOUT --------------------------------------
psychoocean.layout = html.Div(children=[

	html.Label('Parameter'),
    dcc.Dropdown(
		id = 'parameter',
        options=[
            {'label': 'Age', 'value': 'age'},
            {'label': 'Education', 'value': 'education'},
            {'label': 'Gender', 'value': 'gender'}
        ],
        value='age'
    ),

    html.Label('Dimension'),
    dcc.Dropdown(
		id = 'dimension',
        options=[
            {'label': 'Agreeableness', 'value': 'agreeableness'},
            {'label': 'Conscientiousness', 'value': 'conscientiosness'},
            {'label': 'Extraversion', 'value': 'extraversion'},
			{'label': 'Neuroticism', 'value': 'neuroticism'},
            {'label': 'Openness', 'value': 'openness'}
        ],
        value='agreeableness'
    ),
	
	html.Label('Traces'),
    dcc.Checklist(
		id = 'trace',
        options=[
            	{'label': 'Mean', 'value': 'mean'},
		{'label': 'Respondents', 'value': 'res'},
		{'label': 'Progress', 'value': 'prog'}
        ],
		values=['res', 'mean', 'prog']
    ),
	
    dcc.Graph(id="graph1"),
	dcc.Graph(id="graph2"),
	
	#description
	html.Div(children=[

	html.H1("The Big Five"),
	html.H2("5 personality traits"),
	html.P("Data are obtained from Synthetic Aperture Personality Assessment (SAPA)"),
	html.P("http://sapa-project.org"),
	
	html.H2("Traits"),
	html.H3("Agreeableness"),
	html.H4("friendly/compassionate vs. challenging/detached"),
	html.P("A tendency to be compassionate and cooperative rather than suspicious and antagonistic towards others. It is also a measure of one's trusting and helpful nature, and whether a person is generally well-tempered or not. High agreeableness is often seen as naive or submissive. Low agreeableness personalities are often competitive or challenging people, which can be seen as argumentativeness or untrustworthiness."),
	html.Br(),
	html.H3("Conscientiousness"),
	html.H4("efficient/organized vs. easy-going/careless"),
	html.P(" A tendency to be organized and dependable, show self-discipline, act dutifully, aim for achievement, and prefer planned rather than spontaneous behavior. High conscientiousness is often perceived as stubbornness and obsession. Low conscientiousness is associated with flexibility and spontaneity, but can also appear as sloppiness and lack of reliability."),
	html.Br(),
	html.H3("Extraversion"),
	html.H4("outgoing/energetic vs. solitary/reserved"),
	html.P("Energy, positive emotions, surgency, assertiveness, sociability and the tendency to seek stimulation in the company of others, and talkativeness. High extraversion is often perceived as attention-seeking, and domineering. Low extraversion causes a reserved, reflective personality, which can be perceived as aloof or self-absorbed. Extroverted people tend to be more dominant in social settings, opposed to introverted people who may act more shy and reserved in this setting."),
	html.Br(),
	html.H3("Neuroticism"),
	html.H4("sensitive/nervous vs. secure/confident"),
	html.P("Neuroticism identifies certain people who are more prone to psychological stress. The tendency to experience unpleasant emotions easily, such as anger, anxiety, depression, and vulnerability. Neuroticism also refers to the degree of emotional stability and impulse control and is sometimes referred to by its low pole, \"emotional stability\". A high need for stability manifests itself as a stable and calm personality, but can be seen as uninspiring and unconcerned. A low need for stability causes a reactive and excitable personality, often very dynamic individuals, but they can be perceived as unstable or insecure. It has also been researched that individuals with higher levels of tested neuroticism, tend to have worse psychological well being."),
	html.Br(),
	html.H3("Openness"),
	html.H4("inventive/curious vs. consistent/cautious"),
	html.P(" Appreciation for art, emotion, adventure, unusual ideas, curiosity, and variety of experience. Openness reflects the degree of intellectual curiosity, creativity and a preference for novelty and variety a person has. It is also described as the extent to which a person is imaginative or independent and depicts a personal preference for a variety of activities over a strict routine. High openness can be perceived as unpredictability or lack of focus, and more likely to engage in risky behaviour or drug taking. Also, individuals that have high openness tend to lean towards being artists or writers in regards to being creative and appreciate the significance of the intellectual and artistic pursuits. Moreover, individuals with high openness are said to pursue self-actualization specifically by seeking out intense, euphoric experiences. Conversely, those with low openness seek to gain fulfillment through perseverance and are characterized as pragmatic and data-driven—sometimes even perceived to be dogmatic and closed-minded. Some disagreement remains about how to interpret and contextualize the openness factor."),
	html.Br(),
	html.P("Description is from https://en.wikipedia.org/wiki/Big_Five_personality_traits"),
	html.P("Programming by Martin Melichar")
	
	])

])
# CALLBACK Graph 1 -----------------------------
@psychoocean.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input(component_id='parameter', component_property='value'),
    Input(component_id='dimension', component_property='value'),
	Input(component_id='trace', component_property='values')]
)

def update_main_graph(parameter, dimension, trace):

	if parameter == 'age':
		lake = lake_age
		sea = sea_age
	elif parameter == 'education':
		lake = lake_edu
		sea = sea_edu
	else:
		lake = lake_gen
		sea = sea_gen

		
	if dimension == 'agreeableness':
		column = "A"
	elif dimension == 'conscientiosness':
		column = "C"
	elif dimension == 'extraversion':
		column = "E"
	elif dimension == 'neuroticism':
		column = "N"
	else:
		column = "O"
	
	trace_ocean = go.Box(
    name = "Respondents",
    x = sea[parameter],
    y = sea[column],
	)	
		
	trace_lake = go.Scatter(
    name = "Mean",
    x = lake[parameter],
    y = lake[column],
	)
	
	trace_progress = go.Scatter(
    name = "Progress",
    x = [lake.loc[0, parameter], lake.loc[len(lake.index) - 1, parameter]], 
    y = [lake.loc[0, column], lake.loc[len(lake.index) - 1, column]],
	)
	
	data = []

	if 'mean' in trace:
		data.append(trace_lake)	
		
	if 'res' in trace:
		data.append(trace_ocean)

	if 'prog' in trace:
		data.append(trace_progress)

	layout = go.Layout(
		xaxis=dict(
			title=parameter.title(),
			showgrid=True,
			zeroline=True,
			zerolinecolor='#969696',
			zerolinewidth=4


		),
		yaxis=dict(
			title=dimension.title(),
			range=[1, 6],
			showgrid=True,
			gridcolor='#bdbdbd',
			gridwidth=1
		)
	)
	
	figure = go.Figure(data = data, layout = layout)

	return figure
	
	
# CALLBACK Graph 2 -----------------------------
@psychoocean.callback(
    Output(component_id='graph2', component_property='figure'),
    [Input(component_id='parameter', component_property='value')]
)

def update_respondents_graph(parameter):

	if parameter == 'age':
		lake = lake_age
	elif parameter == 'education':
		lake = lake_edu
	else:
		lake = lake_gen

	figure={
		'data': [
			{'x': lake[parameter], 'y': lake["respondents"], 'type': 'bar', 'name': 'Respondents'},
		],
		'layout': {
		'title': 'Respondents',
		'yaxis':{'title':'Respondents'},
		'xaxis':{'title':parameter.title()}
		}
	}
	return figure
	
# DATA ----------------------------------------


#variable "ocean" is a Dataframe used in this code

#loading ocean
ocean = pd.read_csv("https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/psych/bfi.csv")
#general simplifying of ocean
ocean.drop(["Unnamed: 0"], axis = 1, inplace = True)
#low occurence of data for age lower than 16 and higher than 55, there are 10 or more participants for each age
ocean.drop(ocean.index[ocean['age'] <= 15].tolist(), inplace = True)
ocean.drop(ocean.index[ocean['age'] >= 56].tolist(), inplace = True)
ocean.dropna(axis = 0, how='any', thresh=None, subset=None, inplace = True)
#creating mean of individual questions
ocean['A'] = ocean[['A1', 'A2', 'A3', 'A4', 'A5']].mean(axis = 1)
ocean['C'] = ocean[['C1', 'C2', 'C3', 'C4', 'C5']].mean(axis = 1)
ocean['E'] = ocean[['E1', 'E2', 'E3', 'E4', 'E5']].mean(axis = 1)
ocean['N'] = ocean[['N1', 'N2', 'N3', 'N4', 'N5']].mean(axis = 1)
ocean['O'] = ocean[['O1', 'O2', 'O3', 'O4', 'O5']].mean(axis = 1)
#reorganization - cutting of unmeaned questions and resorting meaned ones
ocean.drop(['A1', 'A2', 'A3', 'A4', 'A5', 'C1', 'C2', 'C3', 'C4', 'C5', 'E1', 'E2', 'E3', 'E4', 'E5', 'N1', 'N2', 'N3', 'N4', 'N5', 'O1', 'O2', 'O3', 'O4', 'O5'], axis = 1, inplace = True)
ocean = ocean[['A', 'C', 'E', 'N', 'O', "age", "education", "gender"]].sort_values('age')
#removing values below scale
ocean = ocean[ocean['A'] > 1]
ocean = ocean[ocean['C'] > 1]
ocean = ocean[ocean['E'] > 1]
ocean = ocean[ocean['N'] > 1]
ocean = ocean[ocean['O'] > 1]
#removing decimals from 'education' column
ocean['education'] = ocean['education'].astype(int)
#final cut
ocean = ocean.reset_index(drop=True)
#sea is prepared for renaming of education and gender from ints to strings
sea = ocean




#meaner() creates means in dimensions for individual parameter (age or education or gender)
def meaner(dimension, parameter):

    start = 0
    iteration = 0
    mean = []
    
    if parameter == "a":
        end = ocean['age'].value_counts().sort_index().values.tolist()[0]
        step = ocean['age'].value_counts().sort_index().values.tolist()
    elif parameter == "e":
        end = ocean.sort_values("education")["education"].value_counts().sort_index().values.tolist()[0]
        step = ocean.sort_values("education")["education"].value_counts().sort_index().values.tolist()
    elif parameter == "g":
        end = ocean.sort_values("gender")["gender"].value_counts().sort_index().values.tolist()[0]
        step = ocean.sort_values("gender")["gender"].value_counts().sort_index().values.tolist()
    
    if dimension == "A":
        column = 0
    elif dimension == "C":
        column = 1
    elif dimension == "E":
        column = 2
    elif dimension == "N":
        column = 3
    else:
        column = 4

    for distance in step:    
    
        if iteration == 0:
            mean.append(ocean.iloc[start:end, column].mean())
            iteration += 1
            start += distance
    
        else:
            end += distance
            mean.append(ocean.iloc[start:end, column].mean())
            iteration += 1
            start += distance
            
    return [round(number, 2) for number in mean]

#end of meaner
	
#smaller dataframes made by meaner() from ocean
lake_age = pd.DataFrame()
lake_age['age'] = ocean['age'].value_counts().sort_index().index.values.tolist()
lake_age['respondents'] = ocean['age'].value_counts().sort_index().values.tolist()
lake_age['A'] = meaner("A", "a")
lake_age['C'] = meaner("C", "a")
lake_age['E'] = meaner("E", "a")
lake_age['N'] = meaner("N", "a")
lake_age['O'] = meaner("O", "a")

lake_edu = pd.DataFrame()
lake_edu['education'] = ocean.sort_values("education")["education"].value_counts().sort_index().index.values.tolist()
lake_edu['respondents'] = ocean.sort_values("education")["education"].value_counts().sort_index().values.tolist()
lake_edu['A'] = meaner("A", "e")
lake_edu['C'] = meaner("C", "e")
lake_edu['E'] = meaner("E", "e")
lake_edu['N'] = meaner("N", "e")
lake_edu['O'] = meaner("O", "e")
lake_edu.iloc[0, 0] = "Studying high school"
lake_edu.iloc[1, 0] = "Finished high school"
lake_edu.iloc[2, 0] = "College"
lake_edu.iloc[3, 0] = "College graduate"
lake_edu.iloc[4, 0] = "Graduate degree"

lake_gen = pd.DataFrame()
lake_gen['gender'] = ocean.sort_values("gender")["gender"].value_counts().sort_index().index.values.tolist()
lake_gen['respondents'] = ocean.sort_values("gender")["gender"].value_counts().sort_index().values.tolist()
lake_gen['A'] = meaner("A", "g")
lake_gen['C'] = meaner("C", "g")
lake_gen['E'] = meaner("E", "g")
lake_gen['N'] = meaner("N", "g")
lake_gen['O'] = meaner("O", "g")
lake_gen.iloc[0, 0] = "Male"
lake_gen.iloc[1, 0] = "Female"

sea_age = ocean

#Translating int values into string


sea_edu = ocean.sort_values("education")
for row in sea_edu.index:
    
    var = row - 1

    if sea_edu.iloc[var, 6] == 1:
        sea_edu.iloc[var, 6] = "Studying high school"
    elif sea_edu.iloc[var, 6] == 2:
        sea_edu.iloc[var, 6] = "Finished high school"
    elif sea_edu.iloc[var, 6] == 3:
        sea_edu.iloc[var, 6] = "College"
    elif sea_edu.iloc[var, 6] == 4:
        sea_edu.iloc[var, 6] = "College graduate"
    elif sea_edu.iloc[var, 6] == 5:
        sea_edu.iloc[var, 6] = "Graduate degree"


sea_gen = ocean.sort_values("gender")        
for row in sea_gen.index:
    
    var = row - 1
    
    if sea_gen.iloc[var, 7] == 1:
        sea_gen.iloc[var, 7] = "Male"
    elif sea_gen.iloc[var, 7] == 2:
        sea_gen.iloc[var, 7] = "Female"

server = psychoocean.server
server.secret_key = os.environ.get('SECRET_KEY', 'trevorous')

# ----------------------------------------
if __name__ == '__main__':
    psychoocean.run_server(debug=True)
