import streamlit as st
import requests
import chardet
import re
import time
from pdfminer.high_level import extract_text
from docx import Document
from io import BytesIO

import streamlit as st
from pathlib import Path
import base64

import streamlit as st
import base64
from pathlib import Path
import requests
from io import BytesIO

def set_background(image_path):
    """
    This function sets the background of a Streamlit app to a specified image.
    
    Parameters:
    image_path (str or Path): The path to the image file (local or online).
    """
    if str(image_path).startswith("http"):
        # Fetch the image from a URL
        response = requests.get(image_path)
        if response.status_code == 200:
            img_data = response.content
        else:
            st.error("Error: Unable to load the background image from the URL.")
            return
    else:
        # Read local image file
        with open(image_path, "rb") as f:
            img_data = f.read()
    
    # Encode the image to base64
    b64_encoded = base64.b64encode(img_data).decode()
    
    # Generate CSS to set background
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64_encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    
    # Inject the CSS
    st.markdown(css, unsafe_allow_html=True)

def main():
    # Use a local image or an online image
    # For local image: provide a valid relative or absolute path
    local_image_path = Path(__file__).parent / "yellow_image.png"
    
    # For online image, provide a valid URL
    online_image_url = "https://raw.githubusercontent.com/ravindranath8/resume/main/yellow_image.png"
    
    # Uncomment the preferred option
    # set_background(local_image_path)
    set_background(online_image_url)

    # Streamlit app content
    st.title("My Streamlit App with Custom Background")
    st.write("This is a sample Streamlit app with a custom background image!")

if __name__ == "__main__":
    main()

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f9fbfd;
    }
    .stApp {
        max-width: 1200px;
        padding: 2rem;
    }
    .header {
        background: linear-gradient(45deg, #4b6cb7 0%, #182848 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .success-badge {
        background: #e8f5e9;
        color: #2e7d32;
        padding: 0.5rem;
        border-radius: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="header">
        <h1 style='color: white; margin: 0;'>AI Resume Analyzer Pro</h1>
        <p style='color: #cfd8dc; margin: 0.5rem 0 0 0;'>
            Get instant feedback on your resume's ATS compatibility and job match score
        </p>
    </div>
""", unsafe_allow_html=True)
# ==============================
# Custom CSS Styling
# ==============================
def set_custom_style():
    st.markdown("""
        <style>
        .header {
            color: #2F4F4F;
            font-size: 2.5em;
            margin-bottom: 0.5em;
        }
        .feature-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .api-key-container {
            background: #e3f2fd;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .model-selector {
            border-left: 4px solid #4b6cb7;
            padding: 1rem;
            margin: 1.5rem 0;
            background: #f4f6fa;
        }
        .stProgress > div > div > div {
            background-color: #4b6cb7;
        }
        .gauge-container {
            position: relative;
            width: 100%;
            background: #ecf0f1;
            border-radius: 15px;
            margin: 1rem 0;
        }
        .gauge-labels {
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
            color: #7f8c8d;
        }
        </style>
    """, unsafe_allow_html=True)

set_custom_style()

# ==============================
# Helper Functions
# ==============================
def extract_text_from_pdf(uploaded_file):
    """Extract text from PDF files"""
    try:
        return extract_text(BytesIO(uploaded_file.read()))
    except Exception as e:
        st.error(f"PDF extraction error: {str(e)}")
        return ""

def extract_text_from_docx(uploaded_file):
    """Extract text from DOCX files"""
    try:
        doc = Document(BytesIO(uploaded_file.read()))
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        st.error(f"DOCX extraction error: {str(e)}")
        return ""

def extract_text_from_txt(uploaded_file):
    """Extract text from TXT files with encoding detection"""
    try:
        raw_data = uploaded_file.read()
        result = chardet.detect(raw_data)
        return raw_data.decode(result['encoding'])
    except Exception as e:
        st.error(f"TXT extraction error: {str(e)}")
        return ""

def calculate_ats_score(resume_text, job_desc):
    """Calculate comprehensive ATS compatibility score"""
    keyword_score = len(set(resume_text.lower().split()) & set(job_desc.lower().split())) / len(set(job_desc.split())) * 100 if job_desc else 0
    sections = ['experience', 'education', 'skills', 'projects']
    structure_score = sum(1 for section in sections if re.search(rf'\b{section}\b', resume_text, re.I)) / len(sections) * 100
    has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text))
    has_phone = bool(re.search(r'(\+?\d{1,2}[-\.\s]?)?\(?\d{3}\)?[-\.\s]?\d{3}[-\.\s]?\d{4}', resume_text))
    contact_score = 50*(has_email + has_phone)
    word_count = len(resume_text.split())
    length_score = 100 - abs(word_count - 600)/6
    return (
        keyword_score*0.4 + 
        structure_score*0.3 + 
        contact_score*0.1 + 
        length_score*0.2
    )

def create_score_gauge(score):
    """Create visual gauge for score"""
    color = "#2ecc71" if score > 75 else "#f1c40f" if score > 50 else "#e74c3c"
    return f"""
    <div style="
        background: {color};
        width: {score}%;
        height: 30px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-weight: bold;
        line-height: 30px;
        transition: all 0.3s ease;
        margin: 20px 0;
    ">{score:.1f}%</div>
    """

def analyze_with_togetherai(resume_text, job_desc, api_key):
    """Analyze resume using Together AI API"""
    prompt = f"""Analyze this resume against the job description. Provide detailed feedback in this format:
    1. Strengths: [3 bullet points]
    2. Weaknesses: [3 bullet points] 
    3. Improvements: [3 actionable suggestions]
    4. ATS Score: [0-100] with rationale
    
    RESUME:
    {resume_text[:3000]}
    
    JOB DESCRIPTION:
    {job_desc[:2000]}
    """
    
    payload = {
        "model": "togethercomputer/llama-2-70b-chat",
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 1500,
        "stop": ["</s>"]
    }
    
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    try:
        response = requests.post("https://api.together.xyz/v1/completions",
                               headers=headers,
                               json=payload,
                               timeout=30)
        return response.json()['output']['choices'][0]['text'] if response.ok else f"Error: {response.text}"
    except Exception as e:
        return f"API Error: {str(e)}"

def generate_interview_questions(resume_text, job_desc, api_key):
    """Generate interview questions using Gemini API"""
    prompt = f"""Generate 5 technical interview questions based on this resume and job description.
    Follow this format:
    1. [Role-specific technical question]
    2. [Behavioral question about experience]
    3. [Skill validation question]
    4. [Scenario-based question]
    5. [Company culture fit question]

    Resume: {resume_text[:3000]}
    Job Description: {job_desc[:2000]}"""
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
            json=payload
        )
        if response.status_code == 200:
            return response.json()['candidates'][0]['content'].split('\n')
        return ["Failed to generate questions. Please try again."]
    except Exception as e:
        return [f"Error generating questions: {str(e)}"]

def evaluate_answer(question, answer, api_key):
    """Evaluate user's answer using Gemini API"""
    prompt = f"""Act as an interview coach. Provide:
    1. Short feedback on this answer (max 50 words)
    2. Score (1-5)
    3. Improved sample answer
    
    Question: {question}
    Answer: {answer}"""
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
            json=payload
        )
        return response.json()['candidates'][0]['content'] if response.ok else "Evaluation failed"
    except Exception as e:
        return f"Evaluation error: {str(e)}"

# ==============================
# Main App Layout
# ==============================
st.title("📄 Smart Resume Analyzer AI")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload & Analysis", "🤖 AI Analysis", "📈 Score Details", "🎤 AI Interview"])

# ==============================
# Upload & Analysis Tab
# ==============================
with tab1:
    st.subheader("Upload Your Resume")
    
    uploaded_file = st.file_uploader(
        "Choose a file (PDF, DOCX, TXT)",
        type=["pdf", "docx", "txt"],
        help="Maximum file size: 5MB"
    )
    
    st.subheader("✍️ Job Description")
    job_desc = st.text_area(
        "Paste the job description here:",
        height=200,
        placeholder="Enter job description...",
        help="For best results, include key requirements and qualifications"
    )
    
    if uploaded_file and job_desc:
        file_processors = {
            "pdf": extract_text_from_pdf,
            "docx": extract_text_from_docx,
            "txt": extract_text_from_txt
        }
        file_type = uploaded_file.name.split('.')[-1]
        resume_text = file_processors[file_type](uploaded_file)
        
        if resume_text:
            st.session_state['resume_text'] = resume_text
            st.session_state['job_desc'] = job_desc
            st.success("✅ File processed successfully!")
            
            with st.expander("Preview Resume Text"):
                st.write(resume_text[:500] + "...")

# ==============================
# AI Analysis Tab
# ==============================
with tab2:
    st.subheader("AI-Powered Analysis")
    
    with st.container():
        st.markdown('<div class="model-selector">', unsafe_allow_html=True)
        analysis_type = st.radio(
            "Choose AI Service:",
            ["Gemini"],
            format_func=lambda x: f"🌟 {x}",
            horizontal=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="api-key-container">', unsafe_allow_html=True)
        api_key = st.text_input(
            f"{analysis_type} API Key",
            type="password",
            help="Get your API key from the provider's platform"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚀 Run Comprehensive Analysis", use_container_width=True):
        if not api_key:
            st.warning("🔑 Please enter your API key")
        elif 'resume_text' not in st.session_state:
            st.warning("📄 Please upload your resume first")
        else:
            with st.spinner("🔍 Analyzing resume against job description..."):
                try:
                    result = analyze_with_togetherai(
                        st.session_state['resume_text'],
                        st.session_state['job_desc'],
                        api_key
                    )
                    st.success("🎉 Analysis Complete!")
                    with st.expander("📊 Detailed Report", expanded=True):
                        st.markdown(f'<div class="feature-card">{result}</div>', 
                                  unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Analysis error: {str(e)}")

# ==============================
# Score Details Tab
# ==============================
with tab3:
    if 'resume_text' in st.session_state and 'job_desc' in st.session_state:
        st.subheader("Job Application Success Probability")
        success_probability = calculate_ats_score(
            st.session_state['resume_text'],
            st.session_state['job_desc']
        )
        
        st.markdown(create_score_gauge(success_probability), unsafe_allow_html=True)
        
        with st.expander("📊 Score Breakdown"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Keyword Match", f"{success_probability*0.4:.1f} pts")
                st.metric("Structure Score", f"{success_probability*0.3:.1f} pts")
            with col2:
                st.metric("Contact Info", f"{success_probability*0.1:.1f} pts")
                st.metric("Optimal Length", f"{success_probability*0.2:.1f} pts")
        
        st.subheader("Improvement Suggestions")
        suggestions = []
        if success_probability < 80:
            if success_probability*0.4 < 32:
                suggestions.append("🔹 Add more keywords from the job description")
            if success_probability*0.3 < 24:
                suggestions.append("🔹 Improve section organization (Add missing sections)")
            if success_probability*0.1 < 8:
                suggestions.append("🔹 Add missing contact information")
        
        if suggestions:
            for suggestion in suggestions:
                st.markdown(f'<div class="feature-card">{suggestion}</div>', unsafe_allow_html=True)
        else:
            st.success("🎉 Your resume scores well across all parameters!")
    else:
        st.info("ℹ️ Upload a resume and job description to see analysis results")

# ==============================
# AI Interview Practice Tab
# ==============================
with tab4:
    st.subheader("AI Mock Interview Practice")
    
    if 'interview_questions' not in st.session_state:
        st.session_state.interview_questions = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    gemini_key = st.text_input("Enter Gemini API Key:", 
                             type="password", 
                             key="interview_key",
                             help="Required for generating interview questions")
    
    if st.button("🔄 Generate Interview Questions") and gemini_key:
        if 'resume_text' not in st.session_state or 'job_desc' not in st.session_state:
            st.warning("Please upload resume and job description first")
        else:
            with st.spinner("🧠 Preparing customized interview questions..."):
                questions = generate_interview_questions(
                    st.session_state['resume_text'],
                    st.session_state['job_desc'],
                    gemini_key
                )
                filtered_questions = [q for q in questions if q.strip() and q[0].isdigit()]
                st.session_state.interview_questions = filtered_questions
                st.session_state.current_question = 0
                st.session_state.answers = {}
                st.rerun()
    
    if st.session_state.interview_questions:
        progress = st.session_state.current_question / len(st.session_state.interview_questions)
        st.progress(progress)
        st.caption(f"Question {st.session_state.current_question + 1} of {len(st.session_state.interview_questions)}")
    
    if st.session_state.interview_questions:
        current_q = st.session_state.interview_questions[st.session_state.current_question]
        st.markdown(f"### ❓ {current_q.split('] ')[1] if ']' in current_q else current_q}")
        
        user_answer = st.text_area("Your Answer:", 
                                 height=150, 
                                 key=f"answer_{st.session_state.current_question}",
                                 placeholder="Type your answer here...")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("⏭️ Next Question"):
                if st.session_state.current_question < len(st.session_state.interview_questions) - 1:
                    st.session_state.answers[st.session_state.current_question] = user_answer
                    st.session_state.current_question += 1
                    st.rerun()
        
        if st.button("📝 Get Feedback"):
            if user_answer.strip():
                with st.spinner("Analyzing your answer..."):
                    feedback = evaluate_answer(current_q, user_answer, gemini_key)
                    st.markdown(f'<div class="feature-card">{feedback}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please provide an answer before requesting feedback")
    
    if st.session_state.interview_questions and st.session_state.current_question >= len(st.session_state.interview_questions) - 1:
        st.success("🎉 Interview practice complete! Review your answers below:")
        for idx, q in enumerate(st.session_state.interview_questions):
            with st.expander(f"Question {idx + 1}: {q.split('] ')[1] if ']' in q else q}"):
                st.write(f"**Your Answer:** {st.session_state.answers.get(idx, 'No answer provided')}")
        if st.button("🔄 Start New Practice Session"):
            st.session_state.interview_questions = []
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.rerun()
            

if __name__ == "__main__":
    main()
