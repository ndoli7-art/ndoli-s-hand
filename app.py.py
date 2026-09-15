import os
import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(
    page_title="Ndoli's Hand | Socratic Study Buddy",
    page_icon="🖐️",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; color: #1E3A8A; font-weight: bold; }
    .sub-header { font-size: 1.1rem; color: #4B5563; }
    .stButton>button { width: 100%; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<div class='main-header'>🖐️ Ndoli's Hand</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Your Step-by-Step Socratic Tutor for Technical & Quantitative Subjects</div>", unsafe_allow_html=True)
st.divider()

# Sidebar: Settings & API Key
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Gemini API Key", type="password", help="Get your free key from Google AI Studio")
    
    st.subheader("📚 Subject Focus")
    subject = st.selectbox("Select Domain", ["Statistics", "C Programming", "Discrete Logic", "Database Systems"])
    
    st.markdown("---")
    st.caption("Developed by **Ndoli's Hand** • Interactive Learning Platform")

# Main Interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Problem Input")
    problem_text = st.text_area(
        "Enter your assignment or homework question:",
        height=180,
        placeholder="e.g., Calculate the sample variance for the data set: 12, 15, 18, 20, 25."
    )
    
    generate_btn = st.button("🚀 Break Down Problem", type="primary")

with col2:
    st.subheader("💡 Socratic Breakdown")
    
    if generate_btn:
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar to proceed.")
        elif not problem_text.strip():
            st.warning("Please enter a question or problem statement.")
        else:
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"""
                You are Ndoli's Hand, a Socratic tutor for higher education students.
                Subject: {subject}
                Problem: {problem_text}
                
                Provide a response formatted clearly with Markdown:
                1. A brief 1-sentence framing of the concept.
                2. Step 1: The foundational question to guide the user (do not give the final numerical answer).
                3. Hint Level 1 (Conceptual Hint).
                4. Hint Level 2 (Formula or Rule Hint).
                5. Step 2 & Step 3 overview to guide them toward the final solution.
                """
                
                with st.spinner("Analyzing problem and generating Socratic steps..."):
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                    st.markdown(response.text)
                    st.success("Analysis complete! Work through Step 1 first.")
            except Exception as e:
                st.error(f"Error connecting to API: {e}")

st.divider()

# Interactive Practice Sandbox
st.subheader("🧪 Practice Sandbox")
st.info("Try answering the first step of your problem below to check your logic:")

user_answer = st.text_input("Your response for Step 1:")
if st.button("Submit Step Answer"):
    if user_answer:
        st.success("Answer logged! Keep testing your logic step-by-step.")
    else:
        st.warning("Type an answer before submitting.")