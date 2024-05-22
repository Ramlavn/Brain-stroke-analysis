import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import StringIO

# Set the page config
st.set_page_config(page_title='Data Visualizer',
                   layout='centered',
                   page_icon='📊')

# Title
st.title('📊  Data Visualizer')

# Specify the GitHub URL of the CSV file
github_url = "https://raw.githubusercontent.com/Ramlavn/Data-viz/master/Brain_Stroke_Analysis.csv"

# Function to download the CSV file from GitHub
def download_csv_from_github(url):
    csv_content = requests.get(url).content.decode('utf-8')
    return pd.read_csv(StringIO(csv_content))

# Dropdown to select an option
select_option = st.selectbox('Select an option', ['Choose an option ', 'Brain Stroke Analysis'])

# Download the CSV file if option is 'Automatically select file'
if select_option == 'Brain Stroke Analysis':
    # Download the CSV file
    df = download_csv_from_github(github_url)

    # Display the DataFrame
    st.write(df.head())

    # Function to generate plot
    def generate_plot(df, x_axis, y_axis, plot_type):
        fig, ax = plt.subplots(figsize=(6, 4))
        if plot_type == 'Line Plot':
            sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Bar Chart':
            sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Scatter Plot':
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Distribution Plot':
            sns.histplot(df[x_axis], kde=True, ax=ax)
            y_axis='Density'
        elif plot_type == 'Count Plot':
            sns.countplot(x=df[x_axis], ax=ax)
            y_axis = 'Count'

        # Adjust label sizes
        ax.tick_params(axis='x', labelsize=10)  # Adjust x-axis label size
        ax.tick_params(axis='y', labelsize=10)  # Adjust y-axis label size

        # Adjust title and axis labels with a smaller font size
        plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
        plt.xlabel(x_axis, fontsize=10)
        plt.ylabel(y_axis, fontsize=10)

        # Show the results
        st.pyplot(fig)

    # Generate Plot button
    if st.button('Generate Plot'):
        col1, col2 = st.columns(2)
        columns = df.columns.tolist()

        with col1:
            st.write("")
            st.write(df.head())

        with col2:
            # Allow the user to select columns for plotting
            x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
            y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])

            plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
            # Allow the user to select the type of plot
            plot_type = st.selectbox('Select the type of plot', options=plot_list)

        # Generate the plot based on user selection
        generate_plot(df, x_axis, y_axis, plot_type)

# If option is 'Select a file', display the dropdown to select the file
elif select_option == 'Select a file':
    # Display the dropdown to select a file
    st.write("Please select 'Automatically select file' option to display the file.")
