import pandas as pd
import os
import plotly.express as px
from pathlib import Path
import streamlit as st
import tableauserverclient as TSC
from io import StringIO



# Set the path to the secrets.toml file
filepath = Path(__file__).resolve().parents[3] / ".streamlit" / "secrets.toml"

# Load the secrets using dictionary-like access
try:
    tableau_secrets = st.secrets["tableau"]
except KeyError:
    st.error("Error loading secrets. This thing sucks.")

# Set up connection to Tableau 
tableau_auth = TSC.PersonalAccessTokenAuth(
    st.secrets["tableau"]["toke_name"],
    st.secrets["tableau"]["toke_secret"],
    st.secrets["tableau"]["site_id"],
)
server = TSC.Server(st.secrets["tableau"]["server_url"], use_server_version=True)

# Take in a user input:
vis_to_use = ['scatterplot', 'histogram', 'bar chart']
type_vis = st.selectbox('Select the type of Visualization you would like to see:', options=vis_to_use)

if type_vis == 'scatterplot':
    answer = st.selectbox('Select a Column to Visualize on the X-axis:', options=sorted(list(df.columns)))
    answer2 = st.selectbox('Select a column to visualize on the Y-axis:', options = sorted(list(df.columns)))
# answer = st.selectbox('Select a Column to Visualize:', options=list(df.columns))
    if answer:
        try:
            st.plotly_chart(px.scatter(df, x=answer, y=answer2, hover_data=['name']), use_container_width=True)
        except BaseException:
            print("Error visualizing this column")

if type_vis == 'histogram':
    # Get the column for the histogram
    answer_hist = st.selectbox('Select a Column for the Histogram:', options=sorted(list(df.columns)))
    
    if answer_hist:
        try:
            st.plotly_chart(px.histogram(df, x=answer_hist), use_container_width=True)
        except BaseException:
            print("Error visualizing this column")

if type_vis == 'bar chart':
    # Get the columns for the bar chart
    answer_bar_x = st.selectbox('Select a Column for the X-axis:', options=sorted(list(df.columns)))
    answer_bar_y = st.selectbox('Select a Column for the Y-axis:', options=sorted(list(df.columns)))
    
    if answer_bar_x and answer_bar_y:
        try:
            st.plotly_chart(px.bar(df, x=answer_bar_x, y=answer_bar_y), use_container_width=True)
        except BaseException:
            print("Error visualizing this column")

          
# Create the Plotly bar chart
fig = px.bar(df, x="country", y="monthly_revenue")
            
# Create a workbook and add the visualization to it
try:
    with server.auth.sign_in(tableau_auth):
        workbook = TSC.WorkbookItem(name='Streamlit Bar Chart')
        workbook = server.workbooks.publish(workbook)

        view_item = TSC.ViewItem(workbook.id)
        server.views.populate_image(view_item, content=fig.to_image(format='png'))

    st.success("Bar chart visualization has been published to Tableau!")

except BaseException as e:
    st.error("Error:", e)