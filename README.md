# Medical AI Chatbot - Dr. AI

## Overview

Dr. AI is a Python-based Medical Chatbot powered by the Cohere API.

The chatbot provides:

- Health guidance
- Symptom analysis
- Emergency detection
- Conversation history management
- Personalized responses

The project uses:
- Python
- Cohere API
- JSON
- Regular Expressions
- File Handling

---

# Features

- AI-powered medical assistant
- Emergency symptom detection
- User profile management
- Conversation history saving
- Medication tracking
- Chronic condition tracking
- Session statistics
- Smart response generation

---

# Technologies Used

- Python
- Cohere API
- JSON
- Regular Expressions (re)
- Datetime Module
- File Handling

---

# Project Structure

```bash
MedicalChatbot/
│
├── medical_chatbot.py
├── medical_chat_history.json
└── README.md
Installation
Step 1

Install Python.

Download:
https://www.python.org/downloads/

Step 2

Install Cohere library.

pip install cohere
Setup Cohere API Key

Replace:

api_key = "YOUR_COHERE_API_KEY"

with your real Cohere API key.

Get API key from:
https://dashboard.cohere.com/

How to Run
python medical_chatbot.py
Functionalities
Emergency Detection

The chatbot detects emergency symptoms such as:

Chest pain
Difficulty breathing
Stroke symptoms
Severe bleeding
Poisoning
User Information Extraction

The chatbot can automatically detect:

Age
Chronic diseases
Medications
Conversation History

All conversations are stored in:

medical_chat_history.json
Commands
Command	Function
exit	Close chatbot
stats	Show session statistics
clear	Clear conversation history
Example
You: I have fever and cough

Dr. AI:
You may be experiencing symptoms of a viral infection...
Future Improvements
GUI version using Tkinter
Voice assistant support
Symptom prediction system
Disease recommendation model
Hospital recommendation feature
Database integration
Learning Outcomes

This project helps in understanding:

API integration
AI chatbot development
Medical assistant systems
File handling
User profiling
NLP basics
Emergency detection systems
Author

Developed using Python and Cohere AI.

License

This project is for educational purposes only.
