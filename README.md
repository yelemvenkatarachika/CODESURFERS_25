# AI-Powered Dyslexic Learner Support App

## Project Overview

This project is a **web-based application** designed to support dyslexic learners by leveraging AI and NLP technologies. The app provides a dyslexia-friendly interface to help users read, write, and learn more effectively through personalized, adaptive features. Key capabilities include text-to-speech, speech-to-text, AI-based text simplification, a friendly conversational chatbot, and adaptive quizzes.

***

## Features

- **Text-to-Speech (TTS):** Converts text input into clear, slow-paced audio tailored for dyslexic learners.
- **Speech-to-Text (STT):** Allows users to dictate answers and notes which are transcribed into editable text.
- **Text Simplification:** Uses AI to rewrite complex text into simpler, easy-to-understand language along with keyword highlighting.
- **Conversational Chatbot:** An empathetic AI chatbot helps with learning guidance, encouragement, and interaction.
- **Adaptive Quiz System:** Generates quizzes from learning content with difficulty adjusting based on user performance.
- **Progress Dashboard:** Visualizes learner progress with personalized recommendations and motivational feedback.

***

## Tech Stack

- **Frontend:** ReactJS / Streamlit  
- **Backend:** FastAPI / Flask  
- **AI & NLP:** Hugging Face Transformers, OpenAI GPT, Google Cloud Text-to-Speech & Speech-to-Text APIs  
- **Database:** SQLite / Firebase  
- **Deployment:** Heroku / Render / Vercel / Netlify  

***

## Installation & Setup

1. Clone the repository  
2. Create and activate a Python virtual environment  
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```
3. Install backend dependencies  
   ```
   pip install -r backend/requirements.txt
   ```
4. Install frontend dependencies (if using React)  
   ```
   cd frontend
   npm install
   ```
5. Configure environment variables (.env file)  
   - API keys for Google Cloud, OpenAI, etc.  
6. Run backend server  
   ```
   uvicorn backend.app:app --reload
   ```
7. Run frontend app  
   - React: `npm start`  
   - Streamlit: `streamlit run frontend/app.py`  

***

## Usage

- Open the app URL in a web browser  
- Paste or upload text for reading or simplification  
- Use the microphone to dictate notes or answers  
- Interact with the chatbot for help and encouragement  
- Take adaptive quizzes and view progress on the dashboard  

***

## Contribution

This repository welcomes contributions! Please open issues for bugs or features, fork and submit pull requests.

***

## License

Specify license details here (e.g., MIT License)

***

## Contact

For questions or support, reach out to the project team at [email@example.com].

***

This README gives a clear, concise summary of the project, setup instructions, and usage guidance for developers and users engaged with the AI-powered dyslexic learner support app.
