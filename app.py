import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up the Streamlit page configuration
st.set_page_config(page_title='Data Visualizer', layout='centered', page_icon='📊')

# Title of the app
st.title('📊 Data Visualizer')

# Load the data
github_url = "https://raw.githubusercontent.com/Ramlavn/Data-viz/master/Brain_Stroke_Analysis.csv"
df = pd.read_csv(github_url)

# Display the first few rows of the DataFrame
st.write(df.head())

# Get the list of columns from the DataFrame
columns = df.columns.tolist()

# Layout with two columns for selecting X-axis, Y-axis, and plot type
x_axis = st.selectbox('Select the X-axis', options=["None"] + columns)
y_axis = st.selectbox('Select the Y-axis', options=["None"] + columns)
plot_type = st.selectbox('Select the type of plot', options=['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot'])

# Button to generate the plot
if st.button('Generate Plot'):
    # Function to generate the selected plot
    def generate_plot():
        fig, ax = plt.subplots(figsize=(6, 4))
        if plot_type == 'Distribution Plot':
            sns.histplot(df[x_axis], kde=True, ax=ax)
        elif plot_type == 'Count Plot':
            sns.countplot(x=df[x_axis], ax=ax)
        else:
            sns.barplot(x=x_axis, y=y_axis, data=df, ax=ax) if plot_type == 'Bar Chart' else \
            sns.lineplot(x=x_axis, y=y_axis, data=df, ax=ax) if plot_type == 'Line Plot' else \
            sns.scatterplot(x=x_axis, y=y_axis, data=df, ax=ax)
        # Adjust plot settings
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        # Set the title and axis labels
        plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
        plt.xlabel(x_axis, fontsize=10)
        plt.ylabel(y_axis, fontsize=10)
        # Display the plot
        st.pyplot(fig)
        
    generate_plot()
