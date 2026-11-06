import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
import plotly.express as px

#Step 9: Update Page Configuration
st.set_page_config(
    page_title="EduRisk Analytics - Lab 05",
    page_icon="🎓",
    layout="wide"
)

# Step 10: Keep CSV Loading from Lab 04
def load_student_data():
    try:
        data = pd.read_csv("students.csv")
        return data
    except FileNotFoundError:
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()
        
# Step 12: Keep the Risk Level Function
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"
    
# Step 11: Keep Loading the Student Data
student_df = load_student_data()
total_students = len(student_df)
average_score = student_df["Score"].mean()
average_attendance = student_df["Attendance"].mean()
low_score_students = student_df[student_df["Score"] < 60].shape[0]

# Step 13: Keep the Risk Level Column
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(
        row["Score"],
        row["Attendance"]
    ),
    axis=1
)

# Step 14: Keep Session State from Lab 04
if "risk_history" not in st.session_state:
    st.session_state["risk_history"] = []

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

# Step 15: Keep Sidebar Navigation
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
    st.subheader("Interactive Dashboard with Visualization and Filters")
    st.write("Welcome to Lab 05.")
    st.write(
        "In this lab, the app improves the Dashboard page using "
        "grouped summaries, interactive filters, Streamlit charts, and Plotly charts."
    )
    st.success("Lab 05 app is running successfully!")

# Dashboard page
# Step 17: Replace the Old Dashboard Page
elif selected_page == "Dashboard":
    st.title("Interactive Student Performance Dashboard")

    st.write(
        "Use filters to explore student performance by course, risk level, "
        "and attendance. The dashboard updates based on your selections."
    )
    # Step 19: Add Dashboard Filters Section
    st.subheader("Dashboard Filters")

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    # Step 20: Add Course Filter
    with filter_col1:
        course_options = ["All"] + sorted(student_df["Course"].unique())
        selected_course = st.selectbox(
            "Filter by Course",
            course_options
        )
    # Step 21: Add Risk Level Filter
    with filter_col2:
        risk_options = ["All"] + sorted(student_df["Risk Level"].unique())
        selected_risk = st.selectbox(
            "Filter by Risk Level",
            risk_options
        )
    # Step 22: Add Attendance Slider
    with filter_col3:
        minimum_attendance = st.slider(
            "Minimum Attendance",
            0,
            100,
            0
        )
    #Step 23: Create filtered_df
        filtered_df = student_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[
            filtered_df["Course"] == selected_course
        ]

    if selected_risk != "All":
        filtered_df = filtered_df[
            filtered_df["Risk Level"] == selected_risk
        ]

    filtered_df = filtered_df[
        filtered_df["Attendance"] >= minimum_attendance
    ]
    # Step 24: Handle Empty Filter Results
    if filtered_df.empty:
        st.warning("No students match the selected filters. Please adjust the filters.")
    # Step 25: Add Filtered Metrics
        st.subheader("Filtered Dashboard Metrics")

    filtered_total_students = len(filtered_df)

    if filtered_total_students > 0:
        filtered_average_score = filtered_df["Score"].mean()
        filtered_average_attendance = filtered_df["Attendance"].mean()
        filtered_high_risk_students = filtered_df[
            filtered_df["Risk Level"] == "High Risk"
        ].shape[0]
    else:
        filtered_average_score = 0
        filtered_average_attendance = 0
        filtered_high_risk_students = 0
    # Step 26: Display Filtered Metric Cards
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric("Students", filtered_total_students)

    with metric_col2:
        st.metric("Average Score", round(filtered_average_score, 2))

    with metric_col3:
        st.metric(
            "Average Attendance",
            f"{round(filtered_average_attendance, 2)}%"
        )

    with metric_col4:
        st.metric("High Risk", filtered_high_risk_students)
    # Step 27: Add Course Summary Table
    st.subheader("Course Summary")

    if filtered_total_students > 0:
        course_summary = filtered_df.groupby("Course").agg(
            Students=("Student Name", "count"),
            Average_Score=("Score", "mean"),
            Average_Attendance=("Attendance", "mean"),
            Average_Study_Hours=("Study Hours", "mean")
        ).reset_index()

        st.dataframe(course_summary)
    else:
        st.info("No course summary available for the selected filters.")    
    # Step 28: Add Risk Level Summary Table
        st.subheader("Risk Level Summary")

    if filtered_total_students > 0:
        risk_summary = filtered_df["Risk Level"].value_counts().reset_index()
        risk_summary.columns = ["Risk Level", "Students"]

        st.dataframe(risk_summary)
    else:
        st.info("No risk summary available for the selected filters.")
    #Step 29: Add Streamlit Charts Section
        st.subheader("Streamlit Charts")

    chart_col1, chart_col2 = st.columns(2)
    # Step 30: Add Student Score Chart
    with chart_col1:
        st.write("Student Scores")

        if filtered_total_students > 0:
            score_chart = filtered_df.set_index("Student Name")["Score"]
            st.bar_chart(score_chart)
        else:
            st.info("No score chart available.")
    # Step 31: Add Course Count Chart
    with chart_col2:
        st.write("Students by Course")

        if filtered_total_students > 0:
            course_count = filtered_df["Course"].value_counts()
            st.bar_chart(course_count)
        else:
            st.info("No course count chart available.")
    # Step 32: Add Plotly Charts Section
    st.subheader("Interactive Plotly Charts")

    plotly_col1, plotly_col2 = st.columns(2)
    # Step 33: Add Plotly Risk Distribution Chart
    with plotly_col1:
        st.write("Risk Level Distribution")

        if filtered_total_students > 0:
            risk_summary_chart = filtered_df["Risk Level"].value_counts().reset_index()
            risk_summary_chart.columns = ["Risk Level", "Students"]

            fig_risk = px.bar(
                risk_summary_chart,
                x="Risk Level",
                y="Students",
                color="Risk Level",
                title="Risk Level Distribution",
                color_discrete_map={
                    "Low Risk": "#16A34A",
                    "Medium Risk": "#F59E0B",
                    "High Risk": "#DC2626"
                }
            )

            st.plotly_chart(fig_risk, use_container_width=True)
        else:
            st.info("No risk distribution chart available.")
    # Step 34: Add Plotly Score by Student Chart
    with plotly_col2:
        st.write("Student Scores by Risk Level")

        if filtered_total_students > 0:
            fig_score = px.bar(
                filtered_df,
                x="Student Name",
                y="Score",
                color="Risk Level",
                title="Student Scores by Risk Level",
                color_discrete_map={
                    "Low Risk": "#16A34A",
                    "Medium Risk": "#F59E0B",
                    "High Risk": "#DC2626"
                }
            )

            st.plotly_chart(fig_score, use_container_width=True)
        else:
            st.info("No score chart available.")
    # Step 35: Add Filtered Student Records Table
    st.subheader("Filtered Student Records")

    if filtered_total_students > 0:
        st.dataframe(filtered_df)
    else:
        st.info("No student records to display.")
    # Step 36: Add Ethical Visualization Reminder
    st.warning(
        "Ethics Reminder: Visualizations should support students and guide "
        "academic support decisions, not label or punish students."
    )

# Step 37: Keep the Student Data Page from Lab 04
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

# Step 17: Replace the Old Risk Checker Page
# Step 18: Add Risk Checker Page Title and Instruction
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

    st.write(
        "Enter student information to check risk level. "
        "The result is based on score and attendance."
    )

    st.info(
        "This tool is for academic support. Risk results should help students, "
        "not label or punish them."
    )

# Step 19: Add a Streamlit Form
    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)

        submitted = st.form_submit_button("Check Risk")

# Step 20: Add Form Submission Logic
    if submitted:
        st.write("Form submitted.")

# Step 21: Validate Empty Student Name
        if input_name.strip() == "":
            st.warning("Please enter the student name.")
# Step 22: Add Risk Calculation After Validation
        else:
            risk_result = get_risk_level(
                input_score,
                input_attendance
            )
            # Step 23: Create a Result Dictionary
            result = {
                "Student Name": input_name.strip(),
                "Score": input_score,
                "Attendance": input_attendance,
                "Risk Level": risk_result
            }

#Step 24: Save Result to Session State
            st.session_state["risk_history"].append(result)

#Step 25: Show Supportive Risk Feedback
            if risk_result == "Low Risk":
                st.success("Risk Level: Low Risk")
                st.write("Student appears on track.")
            elif risk_result == "Medium Risk":
                st.warning("Risk Level: Medium Risk")
                st.write("Monitor progress and provide guidance.")
            else:
                st.error("Risk Level: High Risk")
                st.write("Student may need additional support.")
# Step 26: Display the Submitted Input
            st.write("Student Name:", input_name.strip())
            st.write("Score:", input_score)
            st.write("Attendance:", input_attendance)
# Step 27: Add Recent Risk Checks Section
        st.subheader("Recent Risk Checks")
# Step 28: Display Risk History Table
    if len(st.session_state["risk_history"]) > 0:
        history_df = pd.DataFrame(
            st.session_state["risk_history"]
        )

        #Step 29: Add Clear History Button
        if st.button("Clear History"):
            st.session_state["risk_history"] = []
            st.success("Risk check history cleared.")
            st.session_state["risk_history"]
        st.dataframe(history_df)
    else:
        st.info("No risk checks yet.")
# Step 30: Add Ethics Reminder to Risk Checker
    st.warning(
        "Ethics Reminder: Risk results should be used as guidance for support, "
        "not as final judgment about a student."
    )

# Step 39: Update the About Page
else:
    st.title("About")

    st.write("This app is part of Lab 05.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Visualization and Interactivity")

    st.info(
        "This version improves the Dashboard page using grouped summaries, "
        "interactive filters, Streamlit charts, and Plotly charts."
    )

    st.warning(
        "Ethics Reminder: Student performance visualizations should be used "
        "responsibly to support learning and student success."
    )
    