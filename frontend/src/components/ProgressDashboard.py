import streamlit as st

class ProgressDashboard:
    def __init__(self):
        # Initialize any data or state needed for the dashboard
        # For demonstration, let's use some placeholder data
        if "progress_data" not in st.session_state:
            st.session_state.progress_data = {
                "lessons_completed": 5,
                "quizzes_taken": 3,
                "avg_quiz_score": 85,
                "reading_time_hours": 10
            }

    def render(self):
        st.subheader("📊 Your Learning Progress")

        st.write(f"Hello, **{st.session_state.username}**! Here's how you're doing:")

        # Display progress metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(label="Lessons Completed", value=st.session_state.progress_data["lessons_completed"])
        with col2:
            st.metric(label="Quizzes Taken", value=st.session_state.progress_data["quizzes_taken"])
        with col3:
            st.metric(label="Average Quiz Score", value=f"{st.session_state.progress_data['avg_quiz_score']}%")
        with col4:
            st.metric(label="Total Reading Time", value=f"{st.session_state.progress_data['reading_time_hours']} hrs")

        st.markdown("---")

        st.write("### Recent Activity")
        # Example of dynamic content, e.g., showing recent quiz scores or simplified texts
        if st.session_state.progress_data["quizzes_taken"] > 0:
            st.info(f"You scored {st.session_state.progress_data['avg_quiz_score']}% on your last quiz!")
        else:
            st.info("No quiz data yet. Take a quiz to see your progress!")

        st.write("Keep up the great work!")

        # You might add interactive elements here, like a button to refresh data or view detailed reports
        if st.button("Refresh Progress"):
            # In a real app, this would fetch updated data from a database or API
            st.session_state.progress_data["lessons_completed"] += 1
            st.session_state.progress_data["quizzes_taken"] += 1
            st.session_state.progress_data["avg_quiz_score"] = min(100, st.session_state.progress_data["avg_quiz_score"] + 5)
            st.session_state.progress_data["reading_time_hours"] += 0.5
            st.success("Progress updated!")
            st.experimental_rerun() # Rerun to reflect the new state immediately