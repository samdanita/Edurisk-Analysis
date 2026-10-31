import streamlit as st
import pandas as pd

#Step 9: Update Page Configuration
st.set_page_config(
    page_title="EduRisk Analytics - Lab 03",
    page_icon="🎓",
    layout="wide"
)

# Step 10: Remove the Hard-Coded Student Dataset
# Step 11: Add a CSV Loading Function
def load_student_data():
    try:
        data = pd.read_csv("students.csv")
        return data
    except FileNotFoundError:
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()
        
# step 9 add risk level calculation
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

student_df = load_student_data()
total_students = len(student_df)
average_score = student_df["Score"].mean()
average_attendance = student_df["Attendance"].mean()
low_score_students = student_df[student_df["Score"] < 60].shape[0]
# Step 14: Add the Risk Level Column
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(
        row["Score"],
        row["Attendance"]
    ),
    axis=1
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f5f7ff 0%, #ffffff 55%, #f0fdf9 100%);
        border-right: 1px solid #e5e7eb;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }
    .sidebar-brand {
        padding: 1rem;
        margin: 0 0 1rem;
        border: 1px solid #dbeafe;
        border-radius: 18px;
        background: linear-gradient(135deg, #eff6ff, #ecfdf5);
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.08);
    }
    .sidebar-brand-icon {
        font-size: 2rem;
        line-height: 1;
        margin-bottom: 0.65rem;
    }
    .sidebar-brand-title {
        color: #172554;
        font-size: 1.15rem;
        font-weight: 800;
    }
    .sidebar-brand-caption {
        color: #64748b;
        font-size: 0.82rem;
        margin-top: 0.2rem;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 0.35rem 0.45rem;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# step 11 update sidebar navigation
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">🎓</div>
            <div class="sidebar-brand-title">EduRisk Analytics</div>
            <div class="sidebar-brand-caption">Student risk monitoring</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("##### MENU")
    selected_page = st.radio(
        "Navigate",
        ["Home", "Dashboard", "Student Data", "Risk Checker", "About"],
        format_func=lambda page: {
            "Home": "🏠  Home",
            "Dashboard": "📊  Dashboard",
            "Student Data": "👥  Student Data",
            "Risk Checker": "⚠️  Risk Checker",
            "About": "ℹ️  About",
        }[page],
        label_visibility="collapsed",
    )

# Step 16: Update the Home Page
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Frontend Prototype with CSV Data Loading")
    st.write("Welcome to Lab 03.")
    st.write(
        "In this lab, the app loads student data from students.csv "
        "using Pandas instead of storing data directly inside app.py."
    )
    st.success("Lab 03 app is running successfully!")

# Dashboard page
# Step 17: Update the Dashboard Page
elif selected_page == "Dashboard":
    st.markdown(
        """
        <style>
        .dashboard-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #1f2937;
            margin-bottom: 0.25rem;
        }
        .dashboard-subtitle {
            font-size: 1.1rem;
            color: #4b5563;
            background: linear-gradient(135deg, #f3f6ff, #eefaf5);
            border: 1px solid #dfe7ff;
            border-radius: 16px;
            padding: 1rem 1.1rem;
            margin: 0 0 1rem;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        }
        .stat-card {
            background: linear-gradient(135deg, #2563eb, #3b82f6);
            border-radius: 18px;
            padding: 1.1rem 1rem;
            height: 150px;
            color: white;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
            margin-bottom: 1rem;
        }
        .stat-icon {
            font-size: 1.8rem;
            margin-bottom: 0.6rem;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.1;
        }
        .stat-label {
            margin-top: 0.2rem;
            font-size: 0.9rem;
            opacity: 0.95;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .section-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #111827;
            margin-top: 1rem;
            margin-bottom: 0.7rem;
        }
        .data-panel {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 0.8rem;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="dashboard-title">Dashboard Prototype</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="dashboard-subtitle">This dashboard gives a quick overview of student performance using data loaded from students.csv.</div>',
        unsafe_allow_html=True,
    )

    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()
    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    st.markdown(
        '<div class="section-title">📌 Dashboard Metrics</div>',
        unsafe_allow_html=True,
    )
    metric_cols = st.columns(4)
    metrics = [
        {"icon": "👨‍🎓", "label": "Students", "value": str(total_students)},
        {
            "icon": "📊",
            "label": "Average Score",
            "value": f"{average_score:.2f}",
        },
        {
            "icon": "📅",
            "label": "Average Attendance",
            "value": f"{average_attendance:.2f}%",
        },
        {"icon": "⚠️", "label": "High Risk", "value": str(high_risk_students)},
    ]
    for col, metric in zip(metric_cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-icon">{metric['icon']}</div>
                    <div class="stat-value">{metric['value']}</div>
                    <div class="stat-label">{metric['label']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">📋 Student Records</div>',
        unsafe_allow_html=True,
    )
    st.write("This table shows student data loaded from students.csv.")
    st.markdown('<div class="data-panel">', unsafe_allow_html=True)
    st.dataframe(student_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">📈 Charts</div>',
        unsafe_allow_html=True,
    )
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown("#### Student Score Chart")
        score_chart = student_df.set_index("Student Name")["Score"]
        st.bar_chart(score_chart, use_container_width=True)
    with chart_col2:
        st.markdown("#### Course Count")
        course_count = student_df["Course"].value_counts()
        st.bar_chart(course_count, use_container_width=True)

    st.info(
        "Ethics Reminder: Academic monitoring should support students, "
        "not label or punish them."
    )

# Step 18: Update the Student Data Page
elif selected_page == "Student Data":
    st.title("Student Data")

    st.write(
        "This page displays and inspects the dataset loaded from students.csv."
    )

    st.subheader("Data Inspection")

    st.write("Rows and Columns:", student_df.shape)

    st.write("Column Names:")
    st.write(student_df.columns.tolist())

    st.write("First 5 Rows:")
    st.dataframe(student_df.head())

    st.subheader("Full Student Dataset")
    st.dataframe(student_df)

# Step 19: Keep the Risk Checker Page
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

    st.write(
        "Use this page to check the risk level of one student based on "
        "score and attendance."
    )

    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)
        submitted = st.form_submit_button("Check Risk")

    if submitted:
        risk_result = get_risk_level(input_score, input_attendance)

        st.write("Student Name:", input_name)
        st.write("Score:", input_score)
        st.write("Attendance:", input_attendance)

        if risk_result == "Low Risk":
            st.success("Risk Level: Low Risk")
        elif risk_result == "Medium Risk":
            st.warning("Risk Level: Medium Risk")
        else:
            st.error("Risk Level: High Risk")

#Step 20: Update the About Page
else:
    st.title("About")

    st.write("This app is part of Lab 03.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Data Loading, Layout, and Frontend Prototype")

    st.info(
        "This frontend prototype loads real data from students.csv "
        "and displays it using Streamlit and Pandas."
    )

    st.warning(
        "Ethics Reminder: Student risk information should be used responsibly "
        "to support learning and student success."
    )

    