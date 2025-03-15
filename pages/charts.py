import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("analysis.csv")
df.columns = map(str.upper, df.columns)

# Sidebar
st.sidebar.title("Charts")

# Multi-tab setup
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Covid Cases by Age Group", 
    "Covid Cases by Gender and Age Group", 
    "Total Intubated Patients", 
    "ICU Admission Among Diseases", 
    "Total Deceased Patients in Other Diseases"
])

# ---- TAB 1: Covid Cases by Age Group ----
with tab1:
    # Group by AGE_GROUP and count cases
    age_group_counts = df['AGE_GROUP'].value_counts().sort_index()
    
    # Convert to DataFrame
    age_group_counts_df = age_group_counts.reset_index()
    age_group_counts_df.columns = ['Age Group', 'Number of Cases']

    # Plot bar chart
    fig1 = px.bar(age_group_counts_df, x='Age Group', y='Number of Cases', title='Number of Cases by Age Group')
    st.plotly_chart(fig1)

    # Description
    st.markdown(
        """
        <div style='height:100%; display:flex; align-items:flex-end;'>
            <p>The bar chart represents the number of Covid-19 cases across different age groups. The highest number of cases is observed in the 30-39 and 40-49 age groups, with a gradual decline in older populations. Younger groups, especially 0-9 and 10-19, show significantly fewer cases. The trend suggests that middle-aged individuals were the most affected, possibly due to higher exposure in workplaces and social interactions. The number of cases decreases steadily after 50-59, indicating either lower exposure or increased precautions among older age groups..</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Calculate midpoints for histogram
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    midpoints = [(bins[i] + bins[i+1]) / 2 for i in range(len(bins) - 1)]
    age_group_counts_df['Age Group Midpoint'] = midpoints

    # Plot histogram
    fig2 = px.histogram(
        age_group_counts_df,
        x='Age Group Midpoint',
        y='Number of Cases',
        title='Histogram of COVID-19 Cases by Age',
        nbins=10
    )

    fig2.update_layout(
        xaxis_title='Age Group',
        yaxis_title='Number of Cases',
        bargap=0,
        template='plotly_white',
        xaxis=dict(
            tickmode='array',
            tickvals=midpoints,
            ticktext=[str(midpoint) for midpoint in midpoints]
        )
    )

    st.plotly_chart(fig2)

    # Description
    st.markdown(
        """
        <div style='height:100%; display:flex; align-items:flex-end;'>
            <p>The histogram displays the distribution of COVID-19 cases by age. The majority of cases are concentrated between ages 30 to 50, peaking around 40-45. There is a noticeable increase in cases from younger ages up to this peak, followed by a gradual decline in older age groups. The lower number of cases in the youngest and oldest populations suggests either lower exposure or better protective measures. The shape of the histogram resembles a normal distribution, indicating that middle-aged individuals were the most affected, possibly due to higher mobility and workplace exposure.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---- TAB 2: Covid Cases by Gender and Age Group ----
with tab2:
    # Group by AGE_GROUP and SEX
    distribution_df = df.groupby(["AGE_GROUP", "SEX"]).size().reset_index(name="Number of Cases")

    # Plot histogram
    fig3 = px.histogram(
        distribution_df,
        x="AGE_GROUP",
        y="Number of Cases",
        color="SEX",
        barmode="group",
        title="Distribution of COVID-19 Cases by Gender and Age Group",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    st.plotly_chart(fig3)

    # Description
    st.write("The bar chart shows the distribution of COVID-19 cases by gender and age group. Males (orange) generally have higher case numbers than females (green) across most age groups, particularly in the 30-39, 40-49, and 50-59 age ranges. The trend indicates that middle-aged individuals, especially males, were more affected. Both genders have fewer cases in younger (0-19) and older (70+) age groups. The decline in cases among the elderly may be due to reduced exposure or protective measures. This visualization highlights gender-based differences in COVID-19 case distribution across different age groups.")

# ---- TAB 3: Total Intubated Patients ----
with tab3:
    # Group by INTUBATED
    intubation_distribution_df = df["INTUBATED"].value_counts().reset_index()
    intubation_distribution_df.columns = ["Intubation Status", "Number of Cases"]

    # Plot bar chart
    fig4 = px.bar(
        intubation_distribution_df,
        x="Intubation Status",
        y="Number of Cases",
        title="Distribution of Intubation Cases"
    )

    st.plotly_chart(fig4)

    # Description
    st.write("The bar chart illustrates the distribution of intubation cases among COVID-19 patients. The majority of cases fall under the 'DOES NOT APPLY' category, indicating that most patients did not require intubation. A significant portion of cases are labeled 'NO', meaning these patients were evaluated but did not require intubation. Only a small number of cases fall under 'YES', showing that intubation was necessary for a limited number of patients. The 'UNKNOWN' category has the fewest cases, likely representing missing or unconfirmed data. This distribution suggests that severe cases requiring intubation were relatively rare.")

# ---- TAB 4: ICU Admission Among Diseases ----
with tab4:
    diseases = ["DIABETES", "COPD", "ASTHMA", "INMUSUPR", "HYPERTENSION", "CARDIOVASCULAR", "OBESITY", "CHRONIC_KIDNEY", "TOBACCO"]
    icu_patients = df[df['ICU'] == 'YES']

    data_list = [{"Disease": disease, "Count": icu_patients[icu_patients[disease] == 'YES'][disease].count()} for disease in diseases]
    icu_counts = pd.DataFrame(data_list)

    # Plot line graph
    fig5 = px.line(
        icu_counts, 
        x="Disease", 
        y="Count", 
        title="ICU Patients based on the Diseases",
        markers=True
    )

    st.plotly_chart(fig5)

    # Description
    st.write("The line graph presents the number of ICU patients categorized by pre-existing diseases. Hypertension (1585 cases), diabetes (1545 cases), and obesity (1352 cases) have the highest ICU admissions, suggesting a strong correlation between these conditions and severe COVID-19 cases. Cardiovascular (233 cases), chronic kidney disease (189 cases), and immunosuppression (126 cases) show significantly lower ICU admissions. COPD (113 cases) and asthma (148 cases) have the least impact on ICU admissions. The variations indicate that underlying health conditions, particularly hypertension, diabetes, and obesity, may increase the risk of severe COVID-19 requiring intensive care.")

# ---- TAB 5: Total Deceased Patients in Other Diseases ----
with tab5:
    deceased_patients = df[~df['DATE_OF_DEATH'].isna()]
    diseases = ['PNEUMONIA', 'DIABETES', 'COPD', 'ASTHMA', 'INMUSUPR', 
                'HYPERTENSION', 'CARDIOVASCULAR', 'OBESITY', 'CHRONIC_KIDNEY', 'TOBACCO']

    data_list = [{"Disease": disease, "Count": deceased_patients[deceased_patients[disease] == 'YES'][disease].count()} for disease in diseases]
    disease_counts = pd.DataFrame(data_list)

    # Plot bar chart
    fig6 = px.bar(
        disease_counts, 
        x="Count", 
        y="Disease", 
        title="Common Diseases in Deceased Patients",
        text="Count",
        color="Count"
    )

    st.plotly_chart(fig6)

    # Description
    st.write("The horizontal bar graph illustrates the most common pre-existing diseases among deceased COVID-19 patients. Pneumonia (14,464 cases) and hypertension (8,042 cases) are the leading conditions associated with fatalities, followed by diabetes (7,123 cases) and obesity (4,825 cases). Other conditions like chronic kidney disease (1,314 cases), cardiovascular disease (1,059 cases), and tobacco use (1,697 cases) show lower but notable contributions. Asthma (401 cases) and immunosuppression (558 cases) are the least common among deceased patients. The data suggests that pneumonia, hypertension, and diabetes significantly increase the risk of death in COVID-19 patients.")
