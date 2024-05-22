import streamlit as st
import pandas as pd
import requests
from io import StringIO
from datetime import date

# Set up the Streamlit page configuration
st.set_page_config(page_title='Data Visualizer',
                   layout='centered',
                   page_icon='📊')

# Author name
author_name = "Ramlavan"
# Current date
current_date = date.today().strftime("%B %d, %Y")

# Author name and current date above the title
st.write(f"Author: {author_name} | Date: {current_date}")

# Title of the app
st.title('📊 Data Visualizer')

# Dropdown to select a file
github_url = "https://raw.githubusercontent.com/Ramlavn/Data-viz/master/Brain_Stroke_Analysis.csv"
selected_file = st.selectbox('Select a file', ['Choose a file', github_url])

# Check if a file is selected
if selected_file != 'Choose a file':
    # Function to download the CSV file from GitHub
    @st.cache
    def download_csv_from_github(url):
        csv_content = requests.get(url).content.decode('utf-8')
        return pd.read_csv(StringIO(csv_content))

    # Download the CSV file
    df = download_csv_from_github(selected_file)

    # Display the first few rows of the DataFrame
    st.write(df.head())

    # Get the list of columns from the DataFrame
    columns = df.columns.tolist()

    # Layout with two columns for selecting X-axis, Y-axis, and plot type
    col1, col2 = st.columns(2)

    with col1:
        # Dropdown for selecting X-axis
        x_axis = st.selectbox('Select the X-axis', options=["None"] + columns, key='x_axis')
        # Dropdown for selecting Y-axis
        y_axis = st.selectbox('Select the Y-axis', options=["None"] + columns, key='y_axis')

    with col2:
        # Dropdown for selecting the type of plot
        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
        plot_type = st.selectbox('Select the type of plot', options=plot_list, key='plot_type')

    # Button to generate the plot
    if st.button('Generate Plot'):
        # Function to generate the selected plot
        def generate_plot(df, x_axis, y_axis, plot_type):
            if plot_type == 'Line Plot':
                st.line_chart(df[[x_axis, y_axis]])
            elif plot_type == 'Bar Chart':
                st.bar_chart(df[[x_axis, y_axis]])
            elif plot_type == 'Scatter Plot':
                st.scatter_chart(df[[x_axis, y_axis]])
            elif plot_type == 'Distribution Plot':
                if x_axis != "None":
                    st.line_chart(df[x_axis].value_counts())
                else:
                    st.error("Please select a column for the X-axis.")
                    return
            elif plot_type == 'Count Plot':
                if x_axis != "None":
                    st.bar_chart(df[x_axis].value_counts())
                elif y_axis != "None":
                    st.bar_chart(df[y_axis].value_counts())
                else:
                    st.error("Please select a column for either the X-axis or Y-axis.")
                    return

        # Generate the plot based on user selection
        generate_plot(df, x_axis, y_axis, plot_type)
