import streamlit as st
import os
import json
from datetime import datetime
from openai import OpenAI

st.set_page_config(page_title="AI Domain Assistant", page_icon="🤖", layout="wide")

DOMAIN_PROMPTS = {
    "Legal": """You are a knowledgeable legal assistant. You help users understand legal concepts, 
    procedures, and general legal information. You provide clear explanations but always remind users 
    to consult with a qualified attorney for specific legal advice. You are professional, accurate, 
    and cite relevant legal principles when appropriate.""",
    
    "Medical": """You are a helpful medical information assistant. You provide general health and 
    medical information, explain medical terms and conditions, and discuss wellness topics. You always 
    emphasize that your information is for educational purposes only and users should consult 
    healthcare professionals for medical advice, diagnosis, or treatment.""",
    
    "Education": """You are an enthusiastic education assistant. You help students learn new concepts, 
    explain complex topics in simple terms, provide study strategies, and encourage curiosity. You use 
    examples, analogies, and clear explanations to make learning engaging and accessible."""
}

MODEL_OPTIONS = {
    "Meta Llama 3.3 70B (Free)": "meta-llama/llama-3.3-70b-instruct:free",
    "GPT-4o": "openai/gpt-4o",
    "Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet",
    "Gemini 2.0 Flash (Free)": "google/gemini-2.0-flash-exp:free"
}

CONVERSATION_TEMPLATES = {
    "Legal": [
        "What are the key elements of a valid contract?",
        "Explain the difference between civil and criminal law.",
        "What should I know about intellectual property rights?",
        "What are my rights as a tenant?"
    ],
    "Medical": [
        "What are the symptoms and treatment options for common cold?",
        "Explain how vaccines work in the human body.",
        "What lifestyle changes can help prevent heart disease?",
        "What are the differences between bacteria and viruses?"
    ],
    "Education": [
        "Explain the concept of photosynthesis in simple terms.",
        "What are effective study techniques for memorization?",
        "How does the water cycle work?",
        "What is the Pythagorean theorem and how is it used?"
    ]
}

def initialize_client():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        st.error("OPENROUTER_API_KEY not found. Please add it to Replit Secrets.")
        st.stop()
    
    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://replit.com",
            "X-Title": "AI Domain Assistant"
        }
    )

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "domain" not in st.session_state:
        st.session_state.domain = "Legal"
    if "model" not in st.session_state:
        st.session_state.model = "Meta Llama 3.3 70B (Free)"
    if "selected_template" not in st.session_state:
        st.session_state.selected_template = None
    if "follow_up_suggestions" not in st.session_state:
        st.session_state.follow_up_suggestions = []
    if "show_suggestions" not in st.session_state:
        st.session_state.show_suggestions = True

def get_response_stream(client, messages, model_id):
    try:
        stream = client.chat.completions.create(
            model=model_id,
            messages=messages,
            stream=True,
            max_tokens=2048
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                
    except Exception as e:
        yield f"Error: {str(e)}"

def export_as_json(messages, domain, model):
    export_data = {
        "export_date": datetime.now().isoformat(),
        "domain": domain,
        "model": model,
        "conversation": messages
    }
    return json.dumps(export_data, indent=2)

def export_as_text(messages, domain, model):
    lines = [
        f"AI Domain Assistant - Conversation Export",
        f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Domain: {domain}",
        f"Model: {model}",
        f"{'=' * 60}",
        ""
    ]
    
    for msg in messages:
        role = msg["role"].upper()
        content = msg["content"]
        lines.append(f"{role}:")
        lines.append(content)
        lines.append("")
    
    return "\n".join(lines)

def generate_follow_up_suggestions(client, messages, domain, model_id):
    try:
        recent_context = messages[-4:] if len(messages) > 4 else messages
        
        suggestion_prompt = {
            "role": "system",
            "content": f"""Based on the conversation, generate exactly 3 brief follow-up questions that the user might want to ask next in the {domain} domain. 
            Make them specific, relevant, and concise (under 15 words each).
            Return only the questions, one per line, numbered 1-3."""
        }
        
        response = client.chat.completions.create(
            model=model_id,
            messages=[suggestion_prompt] + recent_context,
            max_tokens=200,
            stream=False
        )
        
        suggestions_text = response.choices[0].message.content.strip()
        suggestions = []
        
        for line in suggestions_text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                clean_line = line.lstrip('0123456789.-•) ').strip()
                if clean_line:
                    suggestions.append(clean_line)
        
        return suggestions[:3]
    except Exception as e:
        return []

def main():
    st.title("🤖 AI Domain Assistant")
    st.markdown("**Your specialized AI chatbot for Legal, Medical, and Education topics**")
    
    initialize_session_state()
    client = initialize_client()
    
    with st.sidebar:
        st.header("⚙️ Settings")
        
        selected_domain = st.selectbox(
            "Select Domain",
            options=list(DOMAIN_PROMPTS.keys()),
            index=list(DOMAIN_PROMPTS.keys()).index(st.session_state.domain)
        )
        
        selected_model = st.selectbox(
            "Select Model",
            options=list(MODEL_OPTIONS.keys()),
            index=list(MODEL_OPTIONS.keys()).index(st.session_state.model)
        )
        
        if selected_domain != st.session_state.domain or selected_model != st.session_state.model:
            if st.button("Apply Changes & Clear Chat"):
                st.session_state.domain = selected_domain
                st.session_state.model = selected_model
                st.session_state.messages = []
                st.rerun()
        
        st.divider()
        
        st.markdown(f"**Current Domain:** {st.session_state.domain}")
        st.markdown(f"**Current Model:** {st.session_state.model}")
        
        st.divider()
        
        with st.expander("💬 Conversation Templates", expanded=False):
            st.caption("Click a template to start your conversation:")
            templates = CONVERSATION_TEMPLATES.get(st.session_state.domain, [])
            for template in templates:
                if st.button(template, key=f"template_{template[:20]}", use_container_width=True):
                    st.session_state.selected_template = template
                    st.rerun()
        
        st.divider()
        
        st.session_state.show_suggestions = st.checkbox(
            "✨ Show Follow-up Suggestions",
            value=st.session_state.show_suggestions,
            help="Display AI-generated follow-up questions after each response"
        )
        
        st.divider()
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        
        if len(st.session_state.messages) > 0:
            st.subheader("📥 Export Conversation")
            
            col1, col2 = st.columns(2)
            
            with col1:
                json_data = export_as_json(
                    st.session_state.messages,
                    st.session_state.domain,
                    st.session_state.model
                )
                st.download_button(
                    label="JSON",
                    data=json_data,
                    file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col2:
                text_data = export_as_text(
                    st.session_state.messages,
                    st.session_state.domain,
                    st.session_state.model
                )
                st.download_button(
                    label="TXT",
                    data=text_data,
                    file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            st.divider()
        
        st.caption("💡 **About**")
        st.caption(f"This chatbot uses OpenRouter to access various AI models. Currently using the {st.session_state.domain} domain with specialized knowledge.")
    
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
            
            is_last_message = (i == len(st.session_state.messages) - 1)
            is_assistant = (message["role"] == "assistant")
            
            if is_last_message and is_assistant and st.session_state.show_suggestions:
                if st.session_state.follow_up_suggestions:
                    st.markdown("**💡 Suggested follow-up questions:**")
                    cols = st.columns(3)
                    for idx, suggestion in enumerate(st.session_state.follow_up_suggestions):
                        with cols[idx % 3]:
                            if st.button(suggestion, key=f"suggestion_{idx}_{len(st.session_state.messages)}", use_container_width=True):
                                st.session_state.selected_template = suggestion
                                st.session_state.follow_up_suggestions = []
                                st.rerun()
    
    prompt = None
    
    if st.session_state.selected_template:
        prompt = st.session_state.selected_template
        st.session_state.selected_template = None
    elif user_input := st.chat_input("Type your message here..."):
        prompt = user_input
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        
        system_message = {
            "role": "system",
            "content": DOMAIN_PROMPTS[st.session_state.domain]
        }
        
        messages_for_api = [system_message] + st.session_state.messages
        
        with chat_container:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                for chunk in get_response_stream(
                    client, 
                    messages_for_api, 
                    MODEL_OPTIONS[st.session_state.model]
                ):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        if st.session_state.show_suggestions:
            suggestions = generate_follow_up_suggestions(
                client,
                st.session_state.messages,
                st.session_state.domain,
                MODEL_OPTIONS[st.session_state.model]
            )
            st.session_state.follow_up_suggestions = suggestions
        
        st.rerun()

if __name__ == "__main__":
    main()
