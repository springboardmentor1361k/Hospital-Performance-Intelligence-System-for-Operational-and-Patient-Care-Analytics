import streamlit as st
import pandas as pd
import plotly.express as px

# ====================================
# PAGE CONFIG
# ====================================
st.set_page_config(
    page_title="Hospital Analytics Dashboard",
    page_icon="🏥",
    layout="wide"
)

# ====================================
# LOAD DATA
# ====================================
df = pd.read_csv("Data/hospital_data_cleaned.xlsx.csv")


# ====================================
# SIDEBAR
# ====================================
st.sidebar.title("🏥 Hospital Filters")

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

specialty_filter = st.sidebar.multiselect(
    "Select Specialty",
    options=df["Specialty"].unique(),
    default=df["Specialty"].unique()
)

doctor_filter = st.sidebar.multiselect(
    "Doctor Status",
    options=df["Doctor Status"].unique(),
    default=df["Doctor Status"].unique()
)

case_filter = st.sidebar.multiselect(
    "Case Type",
    options=df["Case type"].unique(),
    default=df["Case type"].unique()
)

# ====================================
# APPLY FILTERS
# ====================================
filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Specialty"].isin(specialty_filter)) &
    (df["Doctor Status"].isin(doctor_filter)) &
    (df["Case type"].isin(case_filter))
]

# ====================================
# TITLE
# ====================================
st.title("🏥 Hospital Analytics Dashboard")
st.markdown("### Healthcare Performance & Resource Utilization")
tab1, tab2, tab3, tab4 = st.tabs([
    "🏥 Overview",
    "👨‍⚕️ Patient Flow",
    "📊 Department Analytics",
    "🛏 Resource Utilization"
])
# ====================================
# KPI CALCULATIONS
# ====================================
total_admissions = len(filtered_df)
total_revenue = filtered_df["Revenue"].sum()
avg_los = filtered_df["LOS"].mean()
active_doctors = len(
    filtered_df[filtered_df["Doctor Status"] == "Active"]
)
avg_cmi = filtered_df["CMI Value"].mean()

# ====================================
# KPI CARDS
# ====================================
with tab1:

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total Admissions", total_admissions)
    c2.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    c3.metric("Average LOS", f"{avg_los:.2f}")
    c4.metric("Active Doctors", active_doctors)
    c5.metric("Average CMI", f"{avg_cmi:.2f}")

    st.divider()

    st.subheader("📋 Executive Summary")

    st.success(f"""
    Total Admissions: {total_admissions}

    Revenue Generated: ₹{total_revenue:,.0f}

    Average LOS: {avg_los:.2f}

    Active Doctors: {active_doctors}
       """)

    st.subheader("🤖 Quick Insights")

    top_specialty = (
        filtered_df.groupby("Specialty")["Revenue"]
        .sum()
        .idxmax()
    )

    st.info(
        f"Highest Revenue Department: {top_specialty}"
    )
with tab2:

    st.subheader("👨‍⚕️ Patient Flow Analysis")

    col1, col2 = st.columns(2)

    with col1:

        revenue_specialty = (
            filtered_df.groupby("Specialty")["Revenue"]
            .sum()
            .reset_index()
            .sort_values("Revenue", ascending=False)
        )

        fig1 = px.bar(
            revenue_specialty,
            x="Specialty",
            y="Revenue",
            title="Revenue by Specialty"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:

        gender_data = (
            filtered_df["Gender"]
            .value_counts()
            .reset_index()
        )

        gender_data.columns = [
            "Gender",
            "Count"
        ]

        fig2 = px.pie(
            gender_data,
            names="Gender",
            values="Count",
            title="Gender Distribution"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )
with tab3:

    st.subheader("📊 Department Analytics")

    col3, col4 = st.columns(2)

    with col3:

        severity_data = (
            filtered_df["Severity"]
            .value_counts()
            .reset_index()
        )

        severity_data.columns = [
            "Severity",
            "Count"
        ]

        fig3 = px.bar(
            severity_data,
            x="Severity",
            y="Count",
            title="Severity Analysis"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    with col4:

        doctor_data = (
            filtered_df["Doctor Status"]
            .value_counts()
            .reset_index()
        )

        doctor_data.columns = [
            "Doctor Status",
            "Count"
        ]

        fig4 = px.pie(
            doctor_data,
            names="Doctor Status",
            values="Count",
            title="Doctor Status Analysis"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    st.divider()

    st.subheader("🏆 Top Specialties by Revenue")

    top_specialties = (
        filtered_df.groupby("Specialty")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    st.dataframe(
        top_specialties,
        use_container_width=True
    )

    st.subheader("📈 Department Revenue Ranking")

    fig_dept = px.bar(
        top_specialties,
        x="Specialty",
        y="Revenue",
        color="Revenue",
        text_auto=True,
        title="Department Revenue Ranking"
    )

    st.plotly_chart(
        fig_dept,
        use_container_width=True
    )

    st.divider()

    
with tab4:

    st.subheader("🛏 Resource Utilization")

    col5, col6 = st.columns(2)

    # Case Type Distribution
    with col5:

        case_data = (
            filtered_df["Case type"]
            .value_counts()
            .reset_index()
        )

        case_data.columns = [
            "Case Type",
            "Count"
        ]

        fig5 = px.bar(
            case_data,
            x="Case Type",
            y="Count",
            title="Case Type Distribution"
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )

    # LOS Distribution
    with col6:

        fig6 = px.histogram(
            filtered_df,
            x="LOS",
            nbins=15,
            title="Length of Stay Distribution"
        )

        st.plotly_chart(
            fig6,
            use_container_width=True
        )

    st.divider()

    # Revenue by Payer Mix
    st.subheader("💰 Revenue by Payer Mix")

    payer_mix = (
        filtered_df.groupby("Payer Mix")["Revenue"]
        .sum()
        .reset_index()
    )

    fig7 = px.bar(
        payer_mix,
        x="Payer Mix",
        y="Revenue",
        title="Revenue by Payer Mix",
        text_auto=True
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )

    st.divider()

    # Dataset Preview
    st.subheader("📋 Hospital Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400
    )

    # Download Button
    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="⬇ Download Filtered Dataset",
        data=csv,
        file_name="hospital_filtered_data.csv",
        mime="text/csv"
    )




# ====================================
# FOOTER
# ====================================
st.markdown("---")
st.markdown(
    "### Developed using Streamlit | Hospital Analytics Dashboard"
)