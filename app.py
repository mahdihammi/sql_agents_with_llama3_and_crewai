import streamlit as st
from crew import crew
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px

load_dotenv()
st.set_page_config(layout="wide")
# Set the title of the app

color_palette = px.colors.qualitative.Pastel2  # You can change this to any color palette you prefer

# Add bottom chart
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Agents Analysis", "Dataset", "Visuals"])
st.sidebar.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        color: grey;
       
    }
    </style>
    <div class="footer">
        Developed by <strong>Mahdi Hammi</strong>
    </div>
    """,
    unsafe_allow_html=True
)

if page == "Agents Analysis":
    st.title('Multi-Agents Employee Salaries Analysis')

    user_input = st.text_input("What do you want to analyze ?")

    if st.button("Analyze"):
        # Perform the task when the button is clicked
        inputs = {
        "query": user_input
            }
        result = crew.kickoff(inputs=inputs)
        
        st.write(result.raw)
        
        st.download_button(
        label="Download Result as Text File",
        data=result.raw,  # the raw result from the task
        file_name="result.txt",  # default filename
        mime="text/plain",  # mime type for text files
        )
########################################################################################       
elif page == "Dataset":
    st.title('Employee salary dataset')

    df = pd.read_csv('./ds-salaries.csv')
    st.write(df)
    
    st.markdown("-----------------------------------------------")
    st.write("## Filtering the Dataset")
    experience_level = st.multiselect("Experience Level", options=df["experience_level"].unique())
    employment_type = st.multiselect("Employment Type", options=df["employment_type"].unique())
    remote_ratio = st.multiselect("Remote Ratio", options=df["remote_ratio"].unique())

    # Apply filters to the DataFrame
    filtered_data = df[
    (df["experience_level"].isin(experience_level) if experience_level else df["experience_level"].notna()) &
    (df["employment_type"].isin(employment_type) if employment_type else df["employment_type"].notna()) &
    (df["remote_ratio"].isin(remote_ratio) if remote_ratio else df["remote_ratio"].notna())
    ]
    st.write("#### Filtered Dataset")
    st.write(filtered_data)
####################################################################
    
elif page == "Visuals":
    df = pd.read_csv('./ds-salaries.csv')
    col1, col2 = st.columns(2)

    with col2:
        fig1 = px.bar(df, 
                      x='remote_ratio',
                      y='salary',
                      title="Salary By Job Title",
                        #color_discrete_sequence=color_palette
                        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col1:
        grouped_data = df.groupby(["employment_type", "remote_ratio"]).size().reset_index(name="count")

        fig = px.bar(
        grouped_data,
        x="employment_type",
        y="count",
        color="remote_ratio",
        title="Distribution of Remote Work by Employment Type",
        labels={"count": "Number of Employees", "remote_ratio": "Remote Ratio"},
        #color_discrete_sequence=color_palette 
        )

    # Customize layout for better readability
        fig.update_layout(barmode="stack", xaxis_title="Employment Type", yaxis_title="Number of Employees")
        st.plotly_chart(fig, use_container_width=True)


        
    col3, col4 = st.columns(2)
    
    with col3:
        
        grouped_data = df.groupby(["experience_level", "company_size"]).salary_in_usd.mean().reset_index(name="total_salary")

        # Create the grouped bar chart (not stacked)
        fig3 = px.bar(
            grouped_data,
            x="experience_level",
            y="total_salary",
            color="company_size",
            title="Average Salary by Experience Level and Company Size",
            labels={"total_salary": "Total Salary (USD)", "experience_level": "Experience Level", "company_size": "Company Size"},
            #color_discrete_sequence=color_palette
        )

        # Ensure the bars are grouped (not stacked)
        fig3.update_layout(barmode="group", xaxis_title="Experience Level", yaxis_title="Total Salary (USD)")

        # Display the chart

        # Display the chart
        st.plotly_chart(fig3, use_container_width=True, use_container_height=True)
    with col4:
        employment_counts = df["remote_ratio"].value_counts().reset_index()
        employment_counts.columns = ["remote_ratio", "count"]

    # Create a pie chart
        fig4 = px.pie(
            employment_counts,
            names="remote_ratio",
            values="count",
            title="remote_ratio Proportion",
            #color_discrete_sequence=color_palette
        )
        st.plotly_chart(fig4, use_container_width= True, use_container_height=True)