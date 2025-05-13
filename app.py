import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st
import re

# Load API key
load_dotenv()
api_key = os.getenv("key")
client = Groq(api_key=api_key)

# Function to get AI response
def get_ai_response(term):
    question = f"Explain '{term}' in simple terms (1 sentence) and give a real-life analogy."
    
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{"role": "user", "content": question}],
        temperature=0.6,
        max_tokens=4096,
        top_p=0.95,
        stream=True,
    )

    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""

    # Clean up the response
    clean_response = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL).strip()
    return clean_response

# Streamlit UI
st.set_page_config(page_title="Tech Jargon Decoder (AI)", page_icon="🤖")
st.title("📘 Tech Jargon Decoder (Powered by AI)")
st.write("Enter any tech term and get a simple explanation with a real-world analogy!")

# Input field
term = st.text_input("🔍 Enter a tech term (e.g., REST API, OAuth 2.0, Kubernetes):")

# Generate response
if term:
    with st.spinner("Thinking..."):
        result = get_ai_response(term)
        if "analogy" in result.lower():
            # Try to split explanation and analogy
            parts = re.split(r'(?i)analogy\s*[:\-]?', result, maxsplit=1)
            explanation = parts[0].strip()
            analogy = parts[1].strip() if len(parts) > 1 else "No analogy found."
        else:
            explanation = result
            analogy = "No analogy provided."

        st.subheader("📘 Explanation:")
        st.success(explanation)

        st.subheader("🧠 Analogy:")
        st.info(analogy)
