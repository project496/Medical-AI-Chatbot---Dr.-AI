import cohere
import json
import os
from datetime import datetime
import re


class MedicalChatbot:

    def __init__(self, api_key):

        self.co = cohere.Client(api_key)

        self.conversation_history = []

        self.user_profile = {
            "name": None,
            "age": None,
            "chronic_conditions": [],
            "medications": [],
            "session_start": datetime.now()
        }

        self.emergency_keywords = [
            'chest pain',
            'can\'t breathe',
            'difficulty breathing',
            'shortness of breath',
            'severe pain',
            'unconscious',
            'bleeding heavily',
            'heavy bleeding',
            'severe headache',
            'vision loss',
            'stroke',
            'heart attack',
            'suicide',
            'overdose',
            'poisoning',
            'allergic reaction',
            'broken bone',
            'severe burn',
            'choking'
        ]

        self.load_conversation_history()

    def save_conversation_history(self):

        try:
            data = {
                "conversations": self.conversation_history,
                "user_profile": self.user_profile,
                "last_updated": datetime.now().isoformat()
            }

            with open("medical_chat_history.json", "w") as f:
                json.dump(data, f, indent=2, default=str)

        except Exception as e:
            print(f"Could not save conversation history: {e}")

    def load_conversation_history(self):

        try:
            if os.path.exists("medical_chat_history.json"):

                with open("medical_chat_history.json", "r") as f:

                    data = json.load(f)

                    self.conversation_history = data.get(
                        "conversations", []
                    )

                    self.user_profile = data.get(
                        "user_profile",
                        self.user_profile
                    )

                print("Previous conversation history loaded.")

        except Exception as e:
            print(f"Could not load conversation history: {e}")

    def detect_emergency(self, message):

        message_lower = message.lower()

        return [
            keyword
            for keyword in self.emergency_keywords
            if keyword in message_lower
        ]

    def extract_user_info(self, message):

        message_lower = message.lower()

        age_match = re.search(
            r'\b(\d{1,2})\s*(?:years?\s*old|yr|age)\b',
            message_lower
        )

        if age_match and not self.user_profile["age"]:
            self.user_profile["age"] = age_match.group(1)

        conditions = [
            'diabetes',
            'hypertension',
            'asthma',
            'arthritis',
            'depression',
            'anxiety'
        ]

        for condition in conditions:

            if condition in message_lower and \
                    condition not in self.user_profile["chronic_conditions"]:

                self.user_profile["chronic_conditions"].append(condition)

        med_keywords = [
            'taking',
            'medication',
            'medicine',
            'pills',
            'prescribed'
        ]

        if any(keyword in message_lower for keyword in med_keywords):

            words = message.split()

            for i, word in enumerate(words):

                if word.lower() in med_keywords and i + 1 < len(words):

                    potential_med = words[i + 1].strip('.,!?')

                    if len(potential_med) > 3 and \
                            potential_med not in self.user_profile["medications"]:

                        self.user_profile["medications"].append(potential_med)

    def build_medical_context(self):

        context = """
You are Dr. AI, a compassionate and knowledgeable medical assistant.

Provide:
- Helpful health guidance
- Symptom analysis
- General wellness advice
- Encouragement to seek professional help when necessary

Never replace a real doctor.
"""

        if self.user_profile["age"]:
            context += f"\nUser Age: {self.user_profile['age']}"

        if self.user_profile["chronic_conditions"]:
            context += (
                f"\nConditions: "
                f"{', '.join(self.user_profile['chronic_conditions'])}"
            )

        if self.user_profile["medications"]:
            context += (
                f"\nMedications: "
                f"{', '.join(self.user_profile['medications'])}"
            )

        return context

    def get_conversation_context(self):

        if not self.conversation_history:
            return "\nThis is the beginning of the consultation."

        context = "\nRecent Conversation:\n"

        for exchange in self.conversation_history[-3:]:

            context += f"Patient: {exchange['user']}\n"

            context += (
                f"Dr. AI: "
                f"{exchange['assistant'][:200]}...\n\n"
            )

        return context

    def clean_response(self, response):

        response = re.sub(
            r'^(Dr\.?\s*AI:?\s*|Assistant:?\s*|Bot:?\s*)',
            '',
            response,
            flags=re.IGNORECASE
        )

        response = re.sub(r'\n{3,}', '\n\n', response)

        return response.strip()

    def generate_response(self, user_message):

        self.extract_user_info(user_message)

        emergencies = self.detect_emergency(user_message)

        if emergencies:

            return f"""
MEDICAL EMERGENCY DETECTED

The symptoms described ({', '.join(emergencies)})
may indicate a serious condition.

Please contact emergency services immediately
or visit the nearest hospital.
"""

        medical_context = self.build_medical_context()

        conversation_context = self.get_conversation_context()

        cohere_prompt = f"""
{medical_context}

{conversation_context}

Patient: {user_message}

Dr. AI:
"""

        try:

            print("Dr. AI is thinking...")

            cohere_response = self.co.generate(
                model='command',
                prompt=cohere_prompt,
                max_tokens=400,
                temperature=0.7,
                k=0,
                stop_sequences=[
                    "Patient:",
                    "User:",
                    "Human:"
                ],
                return_likelihoods='NONE'
            )

            bot_response = (
                cohere_response.generations[0]
                .text
                .strip()
            )

            bot_response = self.clean_response(bot_response)

            if not any(
                    word in bot_response.lower()
                    for word in ['doctor', 'consult']
            ):

                bot_response += (
                    "\n\nRemember: "
                    "This is general health information. "
                    "Always consult a healthcare professional."
                )

            return bot_response

        except Exception as e:

            return f"Cohere API Error: {str(e)}"

    def chat(self, user_message):

        if not user_message.strip():

            return "Please describe your health concern."

        bot_response = self.generate_response(user_message)

        self.conversation_history.append({
            "user": user_message,
            "assistant": bot_response,
            "timestamp": datetime.now().isoformat()
        })

        self.save_conversation_history()

        return bot_response

    def get_stats(self):

        total_messages = len(self.conversation_history)

        session_duration = (
                datetime.now() -
                self.user_profile["session_start"]
        )

        return f"""
Session Statistics

Total exchanges: {total_messages}
Session duration: {str(session_duration).split('.')[0]}
Known conditions: {len(self.user_profile['chronic_conditions'])}
Medications mentioned: {len(self.user_profile['medications'])}
"""


def main():

    print("=" * 60)
    print("MEDICAL AI ASSISTANT - Dr. AI")
    print("=" * 60)

    print("Welcome! I'm Dr. AI.")
    print("I am not a replacement for professional healthcare.")
    print("Type 'exit', 'stats', or 'clear' anytime.")

    print("=" * 60)

    api_key = "YOUR_COHERE_API_KEY"

    try:

        chatbot = MedicalChatbot(api_key)

        print("Dr. AI is ready to help!")

        age_input = input(
            "Enter your age (optional): "
        ).strip()

        if age_input.isdigit():
            chatbot.user_profile["age"] = age_input

        print("\nStart chatting now!")
        print("=" * 60)

        while True:

            user_input = input("You: ").strip()

            if user_input.lower() in [
                'quit',
                'exit',
                'bye'
            ]:

                print("\nDr. AI: Take care! Goodbye!")

                print(chatbot.get_stats())

                break

            elif user_input.lower() == 'stats':

                print(chatbot.get_stats())

            elif user_input.lower() == 'clear':

                chatbot.conversation_history = []

                chatbot.user_profile = {
                    "name": None,
                    "age": chatbot.user_profile.get("age"),
                    "chronic_conditions": [],
                    "medications": [],
                    "session_start": datetime.now()
                }

                if os.path.exists("medical_chat_history.json"):
                    os.remove("medical_chat_history.json")

                print("Conversation history cleared!")

            else:

                print("\n" + "-" * 50)

                response = chatbot.chat(user_input)

                print(f"Dr. AI: {response}")

                print("-" * 50 + "\n")

    except Exception as e:

        print(f"Error initializing Dr. AI: {e}")


if __name__ == "__main__":
    main()
