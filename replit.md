# AI Domain Assistant Chatbot

## Overview
An interactive AI chatbot built with Streamlit and OpenRouter that provides domain-specific assistance in Legal, Medical, and Education topics. The chatbot uses various AI models (including free options) to deliver specialized responses based on the selected domain.

## Project Goals
- Build a custom chatbot using open-source LLMs through OpenRouter API
- Provide domain-specific assistance with specialized system prompts
- Offer real-time streaming responses for better user experience
- Support multiple AI models including free options

## Current State
✅ Fully functional AI chatbot deployed on port 5000
✅ OpenRouter integration with multiple model support
✅ Three domain specializations (Legal, Medical, Education)
✅ Streaming responses with chat history
✅ Clean Streamlit UI with sidebar controls

## Recent Changes (October 24, 2025)
- Created main app.py with Streamlit chatbot interface
- Integrated OpenRouter API using OpenAI SDK format
- Implemented domain selection with custom system prompts
- Added model selection including free models (Meta Llama 3.3 70B, Gemini 2.0 Flash)
- Configured streaming responses with live cursor
- Set up session state management for chat history
- Configured workflow to run on port 5000

## Project Architecture

### Stack
- **Frontend & Backend**: Streamlit (Python)
- **AI Provider**: OpenRouter (https://openrouter.ai/api/v1)
- **SDK**: OpenAI Python SDK (compatible with OpenRouter)

### File Structure
```
.
├── app.py                      # Main Streamlit application
├── .streamlit/
│   └── config.toml            # Streamlit server configuration
└── replit.md                  # Project documentation
```

### Key Components

**app.py**:
- `initialize_client()`: Creates OpenRouter client with API key and headers
- `initialize_session_state()`: Manages chat history and user preferences
- `get_response_stream()`: Handles streaming API responses
- `main()`: Main app logic with UI components

**Domain Prompts**:
- Legal: Professional legal information assistant
- Medical: Health and medical information provider
- Education: Enthusiastic learning assistant

**Supported Models**:
- Meta Llama 3.3 70B (Free) - Default
- GPT-4o
- Claude 3.5 Sonnet
- Gemini 2.0 Flash (Free)

## Environment Variables
- `OPENROUTER_API_KEY`: Required secret for OpenRouter API access

## Features
1. **Interactive Chat Interface**: Real-time message exchange with AI
2. **Domain Selection**: Choose between Legal, Medical, or Education specializations
3. **Model Selection**: Switch between different AI models
4. **Streaming Responses**: See responses appear in real-time
5. **Chat History**: Maintains conversation context within session
6. **Clear History**: Option to reset conversation
7. **Responsive UI**: Clean Streamlit interface with sidebar controls

## User Preferences
- Prefers OpenRouter over direct OpenAI integration
- Wants access to free models
- Domain-specific assistants for specialized use cases

## Next Phase Ideas
- Conversation export functionality (save chat to file)
- Document upload for context-aware queries
- Conversation templates for different domains
- Multi-turn conversation refinement with suggestions
- Support for additional LLM providers with easy switching
