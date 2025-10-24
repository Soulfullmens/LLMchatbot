# AI Domain-Specific Chatbot using OpenRouter

This project is an AI-powered chatbot capable of providing domain-specific responses in **Legal**, **Medical**, and **Education** fields. The chatbot uses **OpenRouter API** to access multiple Large Language Models (LLMs) such as Meta LLaMA, Mistral, and others.

---

## 🎯 Project Objective

- Understand how LLMs work in real applications.
- Use OpenRouter API to interact with multiple AI models.
- Build a chat interface supporting real-time conversation.
- Allow users to select or switch knowledge domains dynamically.

---

## 🧠 Features

| Feature | Description |
|--------|-------------|
| Domain Switching | Legal, Medical, Education specific responses |
| Multi-Model Support | Choose from different LLMs via OpenRouter |
| Real-Time Response Streaming | Smooth chat experience |
| Conversation Memory | Maintains previous chat context |
| Clear Chat Option | Reset conversation anytime |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python | Backend logic & chatbot pipeline |
| OpenRouter API | Access to AI language models |
| Streamlit / Web UI | Interactive chat interface (optional) |
| GitHub | Version control & project deployment |

---

## 🏗️ System Architecture
User → Chat UI → Python Backend → OpenRouter API → Selected AI Model → Response → UI Output

## 📦 Installation & Setup
1. Clone the repository:
```bash
git clone https://github.com/Soulfullmens/LLMchatbot
cd LLMchatbot
2. Install dependencies:
pip install -r requirements.txt

3. Add your OpenRouter API key in environment variable:
export OPENROUTER_API_KEY="your_key_here"

4. Run the chatbot:
python app.py

🚀 Future Enhancements

Voice-based chat input support

Save chat history to database

Deploy as web or mobile application

👤 Author

Mohammed Abdul Rahman Khan
B.E. Computer Science Engineering
Muffakham Jah Engineering College
GitHub: https://github.com/Soulfullmens


