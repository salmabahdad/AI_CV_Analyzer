import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() #loads dotenv file

st.set_page_config(page_title="AI CV Analyzer", page_icon="🤖", layout="centered")

st.title("AI CV Analyzer 📝 🔍")
st.markdown("Make your CV recruiter-ready in minutes!")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your CV to get feedback (PDF)", type=["pdf"])
job_role = st.text_input("Job role you’re applying for")

analyze = st.button("Analyze")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    
    return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    

if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)
        
        if not file_content.strip():
            st.error("File is empty or could not be read. Please upload a valid PDF file.")
            st.stop()
        
        prompt = f"""You are an AI career advisor. Analyze the resume below and provide tailored feedback.

                  ### Goals
                  - Help the candidate strengthen their resume.
                  - Suggest improvements that increase chances of success in {job_role if job_role else 'general job applications'}.

                  ### Areas to Review
                  1. Clarity and readability of the content  
                  2. Effectiveness of skills presentation  
                  3. Quality and relevance of experience descriptions  
                  4. Specific, actionable improvements  

                  ### Resume
                 {file_content}

                  ### Output Format
                 Provide your analysis in a structured way:
                 - Strengths: What is done well  
                 - Weaknesses: What could be improved  
                 - Recommendations: Practical next steps"""
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI career advisor with +10 years of experience in HR ."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=800
        )
        st.markdown("### response")
        st.markdown(response.choices[0].message.content)
    
    except Exception as e:
        st.error(f" {str(e)}")