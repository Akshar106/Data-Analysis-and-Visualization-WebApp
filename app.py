import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import requests
container = st.container()
col1,col2 = st.columns(2)



@st.cache_resource
def load_data(file):

    file_extension = file.name.split(".")[-1]
    if file_extension == "csv":
        data = pd.read_csv(file)
    elif file_extension in ["xls", "xlsx"]:
        data = pd.read_excel(file)
    else:
        st.warning("Unsupported file format. Please upload a CSV or Excel file.")
        return None
    return data

def group_data(data, aggregation):
    def select_group_column(df):
        group_columns = st.sidebar.multiselect("Select columns for Analysis", df.columns, key="group_cols")
        return group_columns

def select_columns(df):
    st.write("### Select Columns")
    all_columns = df.columns.tolist()
    options_key = "_".join(all_columns)
    selected_columns = st.multiselect("Select columns", options=all_columns)
    
    if selected_columns:
        sub_df = df[selected_columns]
        st.write("### Sub DataFrame")
        st.write(sub_df.head())
    else:
        st.warning("Please select at least one column.")

          
def analyze_data(data):
    
    show_file_header(data)
    st.write("### Select Columns to make your Data Set for Analysis")
    all_columns = data.columns.tolist()
    options_key = "_".join(all_columns)
    selected_columns = st.multiselect("Select columns", options=all_columns)
    
    if selected_columns:
        sub_df = data[selected_columns]
        st.write("### Sub DataFrame")
        st.write(sub_df.head())

        def show_data_shape(data):
            st.write("Number of rows")
            st.write(data.shape[0])
            st.write("Number of columns")
            st.write(data.shape[1])
        show_data_shape(sub_df)

        st.write("Description")
        st.write(sub_df.describe())


        show_columns_info(sub_df)
        show_missing_values(sub_df)
        show_unique_values(sub_df)
        show_standard_deviation(sub_df)
        


    else:
        st.warning("Please select at least one column.")


def show_file_header(data):
    st.write("File Header")
    st.write(data.head())

def sort_data(data):
    # Sort the data by a selected column
    sort_column = st.selectbox("Select column to sort by", data.columns)
    sorted_df = data.sort_values(by=sort_column)
    return sorted_df


def show_sorted_data(sorted_df):
    st.write("Sort Data")
    st.write(sorted_df)



def show_columns_info(data):
  
    st.write("Columns Names")
    st.write(data.columns)
    st.write("Columns Data Types")
    st.write(data.dtypes)


def show_missing_values(data):
    st.write("Missing Values")
    st.write(data.isnull().sum())


def show_unique_values(data):
    st.write("Unique Values")
    st.write(data.nunique())


def show_standard_deviation(data):
    st.write("Standard Deviation")
    st.write(data.std(numeric_only=True))





def create_chart(chart_type, data, x_column, y_column):

    container.write(" # Data Visualization # ")
    if chart_type == "Bar":
    
        st.header("Bar Chart")
        
        color_column = st.sidebar.selectbox("Select column for color ", data.columns,key="color_name")
        #pattern_column = st.sidebar.selectbox("Select column for pattern ", data.columns)
        if color_column:
           fig = px.bar(data, x=x_column, y=y_column,color=color_column,barmode="group")
           st.plotly_chart(fig)
        else:
           fig = px.bar(data, x=x_column, y=y_column,barmode="group")
           st.plotly_chart(fig)   

    elif chart_type == "Line":
        st.header("Line Chart")
        fig = px.line(data, x=x_column, y=y_column)
        st.plotly_chart(fig)

    elif chart_type == "Scatter":
        st.header("Scatter Chart")
        size_column = st.sidebar.selectbox("Select column for size ", data.columns)
        color_column = st.sidebar.selectbox("Select column for color ", data.columns)
        if color_column:
            
           fig = px.scatter(data, x=x_column, y=y_column,color=color_column,size=size_column)

        else:
            fig = px.scatter(data, x=x_column, y=y_column) 
        st.plotly_chart(fig)        

    elif chart_type == "Histogram":
        st.header("Histogram Chart")
        color_column = st.sidebar.selectbox("Select column for color ", data.columns)
        fig = px.histogram(data, x=x_column, y=y_column,color = color_column)
        st.plotly_chart(fig)
        

    elif chart_type == "Pie":
        st.header("Pie Chart")

        color_column = st.sidebar.selectbox("Select column for color ", data.columns)
        if color_column:
            fig = px.pie(data, names=x_column, values=y_column, color=color_column)
            st.plotly_chart(fig)
        else:
            fig = px.pie(data, names=x_column, values=y_column)
            st.plotly_chart(fig)
    
    

def main():

    
    image = Image.open("pandasFuny.jpg")
    container.image(image, width=200)
    container.write(" # Data Analysis and Visualization # ")
    
    st.sidebar.image(image, width=50)
    file_option = st.sidebar.radio("Data Source", options=["Upload Local File", "Enter Online Dataset"])
    file = None
    data = None

    if file_option == "Upload Local File":
        file = st.sidebar.file_uploader("Upload a data set in CSV or EXCEL format", type=["csv", "excel"])

    elif file_option == "Enter Online Dataset":
        online_dataset = st.sidebar.text_input("Enter the URL of the online dataset")
        if online_dataset:
            try:
                response = requests.get(online_dataset)
                if response.ok:
                    data = pd.read_csv(online_dataset)
                else:
                    st.warning("Unable to fetch the dataset from the provided link.")
            except:
                st.warning("Invalid URL or unable to read the dataset from the provided link.")

    options = st.sidebar.radio('Pages', options=['Data Analysis', 'Data visualization'])

    if file is not None:
        data = load_data(file)

    if options == 'Data Analysis':
        if data is not None:
            analyze_data(data)
        else:
            st.warning("No file or empty file")

    if options == 'Data visualization':
        if data is not None:
            # Create a sidebar for user options
            st.sidebar.title("Chart Options")


            st.write("### Select Columns")
            all_columns = data.columns.tolist()
            options_key = "_".join(all_columns)
            selected_columns = st.sidebar.multiselect("Select columns", options=all_columns)
            if selected_columns:
                sub_df = data[selected_columns]


                chart_type = st.sidebar.selectbox("Select a chart type", ["Bar", "Line", "Scatter", "Histogram", "Pie"])

                x_column = st.sidebar.selectbox("Select the X column", sub_df.columns)

                y_column = st.sidebar.selectbox("Select the Y column", sub_df.columns)

                create_chart(chart_type, sub_df, x_column, y_column)


if __name__ == "__main__":
    main()