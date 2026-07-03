import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

st.title("CSV Data Dashboard")
st.write("Upload any CSV file and explore your data instantly.")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file,encoding = 'latin1')
    st.success(f"File uploaded! {df.shape[0]} rows and {df.shape[1]} columns found.")
    

    #Raw Data
    st.subheader("Preview")
    st.dataframe(df.head(10))

    #Basic Stats
    st.subheader("Basic Statistics")
    st.dataframe(df.describe())

    #Missing Values
    st.subheader("Missing Values")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        st.dataframe(missing[missing > 0])
    else:
        st.write("No missing values found!")

    #Column info
    st.subheader("Column Types")
    st.dataframe(df.dtypes.astype(str).rename("Data Type"))

    # Download cleaned data
    st.subheader("Download Cleaned Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

    #Value counts for a selected column
    st.subheader("Explore a column")
    selected_col = st.selectbox("Choose a column",df.columns)
    st.write(df[selected_col].value_counts())

    #Visualization for selected type 
    st.subheader("Select Visualization")
    chart_types = ["Bar chart","Scatter Plot","Line Chart",
                   "Histogram","Correlation Heatmap"]
    selected_vsl = st.selectbox("Choose a chart type",chart_types)

    # Chart types
    if selected_vsl == "Bar chart":
        x_column = st.selectbox("Select X-axis",df.columns)

        numeric_df = df.select_dtypes(include = ['number'])
        y_column = st.selectbox("Select Y-axis",numeric_df.columns)

        # Group data for Bar Chart
        grouped_data = df.groupby(x_column)[y_column].sum()

        # Plotting
        plt.figure(figsize=(8,5))

        plt.bar(grouped_data.index, grouped_data.values, color="blue")

        plt.title(f"{y_column} by {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)

        plt.grid(axis="y")

        st.pyplot(plt)

        plt.clf()
    
    elif selected_vsl == "Scatter Plot":

        numeric_df = df.select_dtypes(include = ['number'])
        
        x_column = st.selectbox("Select X-axis",numeric_df.columns)
        y_column = st.selectbox("Select Y-axis",numeric_df.columns)

        #Plotting
        plt.figure(figsize=(8,5))

        plt.scatter(df[x_column],df[y_column],color = 'red',s=10)

        plt.title(f"{y_column} Vs {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)

        plt.grid(alpha=0.3)

        st.pyplot(plt)

        plt.clf()

    elif selected_vsl == "Line Chart":
        numeric_df = df.select_dtypes(include=["number"])

        x_column = st.selectbox("Select X-axis", numeric_df.columns)
        y_column = st.selectbox("Select Y-axis", numeric_df.columns)

        sorted_df = df.sort_values(by=x_column)

        #Plotting
        plt.figure(figsize=(8,5))

        plt.plot(sorted_df[x_column], sorted_df[y_column],linewidth = 2,
                marker='o',
                markersize=3)

        plt.title(f"{y_column} Vs {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)

        plt.grid(alpha=0.3)

        st.pyplot(plt)

        plt.clf()


    elif selected_vsl == "Histogram":
        numeric_df = df.select_dtypes(include=["number"])

        c_column = st.selectbox("Select Column",numeric_df.columns)

        #Plotting
        plt.figure(figsize=(8,5))

        plt.hist(df[c_column],bins = 20,color="steelblue",
    edgecolor="black")

        plt.title(f"Distribution of {c_column}")
        plt.xlabel(c_column)
        plt.ylabel("Frequency")

        plt.grid(alpha=0.3)

        st.pyplot(plt)

        plt.clf()

    elif selected_vsl == "Correlation Heatmap":

        numeric_df = df.select_dtypes(include = ['number'])
        corr_matrix = numeric_df.corr()
    
        if len(numeric_df.columns) < 2:
            st.warning("Need at least 2 numeric columns for a heatmap.")
        else:
            #Plotting
            plt.figure(figsize=(10,8))

            sns.heatmap(corr_matrix,annot = True,cmap ="coolwarm",fmt =".2f")

            plt.title("Correlation Heatmap")
            st.pyplot(plt)
            plt.clf()






        


