import streamlit as st

class Quiz:
    def __init__(self):
        # Quiz questions for MVP; replace or extend as needed
        if 'quiz_questions' not in st.session_state:
            st.session_state.quiz_questions = [
                {
                    "question": "What is dyslexia?",
                    "options": ["A learning difficulty", "A type of food", "A sport", "A musical instrument"],
                    "answer_index": 0
                },
                {
                    "question": "Which is a common sign of dyslexia?",
                    "options": ["Difficulty reading", "Being very fast", "Easily remembering phone numbers", "Liking music"],
                    "answer_index": 0
                },
                {
                    "question": "What can help dyslexic learners?",
                    "options": ["Text simplification", "Ignoring difficulties", "Fast reading", "Skipping lessons"],
                    "answer_index": 0
                }
            ]
        # Track current question and score in session state
        if 'current_question' not in st.session_state:
            st.session_state.current_question = 0
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'quiz_completed' not in st.session_state:
            st.session_state.quiz_completed = False

    def reset_quiz(self):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.quiz_completed = False

    def render(self):
        st.markdown("## Quiz Time")

        if st.session_state.quiz_completed:
            st.success(f"Quiz Completed! Your score: {st.session_state.score} / {len(st.session_state.quiz_questions)}")
            if st.button("Retake Quiz"):
                self.reset_quiz()
            return

        question_data = st.session_state.quiz_questions[st.session_state.current_question]

        st.markdown(f"**Question {st.session_state.current_question + 1}:** {question_data['question']}")

        options = question_data['options']
        selected = st.radio("Select your answer:", options, key=f"q{st.session_state.current_question}")

        if st.button("Submit Answer"):
            correct_index = question_data['answer_index']
            if options.index(selected) == correct_index:
                st.success("Correct answer!")
                st.session_state.score += 1
            else:
                st.error(f"Wrong answer. Correct answer is: {options[correct_index]}")

            st.session_state.current_question += 1

            if st.session_state.current_question >= len(st.session_state.quiz_questions):
                st.session_state.quiz_completed = True
                st.experimental_rerun()
            else:
                st.experimental_rerun()

# To use this component inside your Streamlit app,
# instantiate and call render():
if __name__ == "__main__":
    quiz = Quiz()
    quiz.render()
