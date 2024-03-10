import streamlit as st
import google.generativeai as genai
import os 
import PyPDF2 as pdf
# import PyPDF2.PdfReader as pd

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    # reader = pdf.PdfReader(uploaded_file)
    # text = ""
    # for page in reader(len(reader.pages)):
    #     page = reader.pages[page-1]
    #     text+=str(page.extract_text())

    reader = pdf.PdfReader(uploaded_file)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    return text


# reader = pdf.dfReader(uploaded_file)
# number_of_pages = len(reader.pages)
# page = reader.pages[0]
# text = page.extract_text()

input_prompt = """
As an experienced AI-driven hiring software, you possess a deep understanding of the requirements for various job roles,
whether in banking, IT, education, or other sectors.
 Your task is to assess a resume's compatibility with the provided job description and provide a percentage match, 
list missing keywords, and offer suggestions for improvement. Given the competitive job market, accuracy is crucial in evaluating resumes. Provide comprehensive assistance to enhance the resumes effectively. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
You must consider the job market is very competitive and you should provide best assistance for improving the resumes.
Assign the percentage Matching  based on Job_desc and the missing keywords with high accuracy
resume:{text}
description:{Job_desc}



I want the response in one single string having the structure
{{"Job Description":"%","Missing Keywords:[]", "Profile Summary":""}}
"""

st.title("Applicant Tracking System")
st.text("Improve Your Resume ATS")
Job_desc = st.text_area("Paste The Job Description")
uploaded_file = st.file_uploader("Upload Your Resume",type='pdf',help="Please Upload The PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)