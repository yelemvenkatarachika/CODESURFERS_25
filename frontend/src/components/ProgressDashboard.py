import streamlit as st
import pandas as pd
import numpy as np

class ProgressDashboard:
    def __init__(self):
        # Initialize session state for progress data if not present
        if 'progress_data' not in st.session_state:
            # Example default data format; replace with real backend data fetching
            st.session_state.progress_data = {
                "dates": pd.date_range(end=pd.Timestamp.today(), periods=7).tolist(),
                "quiz_scores": [70, 80, 75, 85, 90, 88, 92],
                "lessons_completed": [1, 1, 2, 2, 3, 3, 4]
            }

    def render(self):
        st.markdown("## Learning Progress Dashboard")

        data = st.session_state.progress_data

        df = pd.DataFrame({
            "Date": data["dates"],
            "Quiz Score (%)": data["quiz_scores"],
            "Lessons Completed": data["lessons_completed"]
        })

        # Display summary statistics
        st.markdown("### Summary")
        avg_score = np.mean(df["Quiz Score (%)"])
        total_lessons = df["Lessons Completed"].max()
        st.write(f"**Average Quiz Score:** {avg_score:.1f}%")
        st.write(f"**Total Lessons Completed:** {total_lessons}")

        # Line chart for quiz scores over dates
        st.markdown("### Quiz Scores Over Time")
        st.line_chart(df.set_index("Date")["Quiz Score (%)"])

        # Bar chart for lessons completed over dates
        st.markdown("### Lessons Completed Over Time")
        st.bar_chart(df.set_index("Date")["Lessons Completed"])

        # Milestones visualization
        st.markdown("### Milestones Achieved")
        milestones = ["1 Lesson Completed", "3 Lessons Completed", "5 Lessons Completed", "10 Lessons Completed"]
        milestones_achieved = [m for m in milestones if int(m.split()[0]) <= total_lessons]
        if milestones_achieved:
            for milestone in milestones_achieved:
                st.success(f"🎉 {milestone}")
        else:
            st.info("No milestones achieved yet. Keep progressing!")

# To use this component, create an instance and call render() inside your Streamlit app
if __name__ == "__main__":
    dashboard = ProgressDashboard()
    dashboard.render()
