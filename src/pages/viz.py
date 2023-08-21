import pandas as pd
import os
import plotly.express as px
from pathlib import Path
import streamlit as st
import tableauserverclient as TSC
from io import StringIO


# Establish a filepath to the oracle_cards.csv file
filepath = os.path.join(Path(__file__).parents[1], 'data/oracle_cards.csv')
df = pd.read_csv(filepath, low_memory=False)


# # Load secrets from Streamlit's secrets manager
# tableau_secrets = st.secrets.get("tableau")

# # Check if secrets were loaded successfully
# if tableau_secrets is None:
#     st.error("Tableau secrets not found. Make sure you have added them to the Streamlit secrets manager.")
#     st.stop()

# # Set up connection to Tableau 
# tableau_auth = TSC.PersonalAccessTokenAuth(
#     st.secrets["tableau"]["token_name"],
#     st.secrets["tableau"]["token_secret"],
#     st.secrets["tableau"]["site_id"]
# )
# server = TSC.Server(st.secrets["tableau"]["server_url"], use_server_version=True)



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
            print("Error visualizing this column for scatterplot")

if type_vis == 'histogram':
    # Get the column for the histogram
    answer_hist = st.selectbox('Select a Column for the Histogram:', options=sorted(list(df.columns)))
    
    if answer_hist:
        try:
            st.plotly_chart(px.histogram(df, x=answer_hist), use_container_width=True)
        except BaseException:
            print("Error visualizing this column for historgram")

if type_vis == 'bar chart':
    # Get the columns for the bar chart
    answer_bar_x = st.selectbox('Select a Column for the X-axis:', options=sorted(list(df.columns)))
    answer_bar_y = st.selectbox('Select a Column for the Y-axis:', options=sorted(list(df.columns)))
    
    if answer_bar_x and answer_bar_y:
        try:
            st.plotly_chart(px.bar(df, x=answer_bar_x, y=answer_bar_y), use_container_width=True)
        except BaseException:
            print("Error visualizing this column for bar chart")


# Create the Plotly bar chart
fig = px.bar(df, x="country", y="monthly_revenue")

html_path = "plotly_chart.html"
fig.write_html(html_path)

# # Set up connection to Tableau Server
# tableau_server_url = 'https://prod-useast-b.online.tableau.com/#/site/alexbriody/views/streamlit_write_page/streamlit_write_page?:iid=7'
# auth = TSC.TableauAuth('alexbriody@gmail.com', 'PASSWORD')  

# # Connect to the server
# with server.auth.sign_in(auth):
#     # Create a new workbook
#     new_workbook = TSC.WorkbookItem('Streamlit Bar Chart Workbook')

#     # Add a view to the workbook
#     new_view = TSC.ViewItem()

#     # Read the HTML content
#     with open(html_path, 'r') as html_file:
#         html_content = html_file.read()

#     # Set the HTML content
#     new_view.set_html(html_content)

#     # Publish the workbook with the view
#     server.workbooks.publish(new_workbook, [new_view], overwrite=True)

# st.success("Bar chart visualization has been published to Tableau!")

