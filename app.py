#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

# Load dataset
url = "http://archive.ics.uci.edu/ml/machine-learning-databases/00374/energydata_complete.csv"
data = pd.read_csv(url)

# Data Cleaning
data['date'] = pd.to_datetime(data['date'])

# Initialize the app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Appliances Energy Prediction Dashboard"),
    
    dcc.DatePickerRange(
        id='date-range',
        start_date=data['date'].min(),
        end_date=data['date'].max(),
        display_format='YYYY-MM-DD'
    ),
    
    dcc.Graph(id='energy-consumption'),
    
    dcc.Graph(id='temp-humidity')
])

# Callback for updating the plots
@app.callback(
    [Output('energy-consumption', 'figure'),
     Output('temp-humidity', 'figure')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_graphs(start_date, end_date):
    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    
    # Energy Consumption Plot
    fig1 = px.line(filtered_data, x='date', y='Appliances', title='Appliances Energy Consumption Over Time')
    
    # Temperature and Humidity Plot
    fig2 = px.line(filtered_data, x='date', y=['T1', 'RH_1'], title='Temperature and Humidity in Kitchen Over Time')
    
    return fig1, fig2

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




