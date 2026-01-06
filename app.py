import streamlit as st #imports the streamlit library
import re #imports the regular expression library

st.set_page_config(page_title="Application Companion AI", layout="wide") #sets the page title and layout
st.title("Application Companion AI") #sets the title of the page
st.write("Analyze your resume and job description to generate a tailored application.") #sets the description of the page

STOPWORDS = { #sets the stopwords for the keyword extraction
    "the","and","to","of","in","a","for","on","with","as","is","are","be","this","that","it","an",
    "or","by","from","at","will","you","your","we","our","their","they","can","able","using"
}

def extract_keywords(text): #extracts the keywords from the text
    text = text.lower() #converts the text to lowercase
    text = text.replace("power bi", "powerbi") #replaces power bi with powerbi
    words = re.findall(r"\b[a-z0-9]+\b", text) #finds all the words in the text
    ALLOW_1_CHAR = {"r"} #allows the word r to be included
    return {w for w in words if w not in STOPWORDS and (len(w) > 1 or w in ALLOW_1_CHAR) #returns the keywords
    }

def read_text_file(uploaded_file): #reads the text file
    return uploaded_file.read().decode("utf-8") #returns the text file

col1, col2 = st.columns(2) #creates two columns
with col1:
    st.subheader("Upload your resume") #sets the subheader of the first column
    resume_file = st.file_uploader("Upload your resume", type=["txt"]) #creates a file uploader for the resume
with col2:
    st.subheader("Upload the job description") #sets the subheader of the second column
    job_description_file = st.file_uploader("Upload the job description", type=["txt"]) #creates a file uploader for the job description

if resume_file and job_description_file:
    resume_text = read_text_file(resume_file) #reads the resume text
    job_text = read_text_file(job_description_file) #reads the job description text

    st.success("Files uploaded successfully. Analyzing content...") #shows a success message

    with st.expander("Debug: show raw text"):
        st.write("Resume preview:", resume_text[:500]) #shows the preview of the resume text
        st.write("Job preview:", job_text[:500]) #shows the preview of the job description text

    resume_keywords = extract_keywords(resume_text) #extracts the keywords from the resume text
    job_keywords = extract_keywords(job_text) # extracts the keywords from the job description text

    matching = resume_keywords.intersection(job_keywords) #finds the matching keywords
    missing_from_resume = job_keywords.difference(resume_keywords) #finds the missing keywords from the resume text
    extra_in_resume = resume_keywords.difference(job_keywords) #finds the extra keywords in the resume text

    job_coverage = round(len(matching) / max(len(job_keywords), 1) * 100, 1) #calculates the job coverage
    resume_relevance = round(len(matching) / max(len(resume_keywords), 1) * 100, 1) #calculates the resume relevance

    st.subheader("Keyword Matching") #sets the subheader of the keyword matching section

    colA, colB = st.columns(2)
    colA.metric("Job coverage", f"{job_coverage}%") #shows the job coverage
    colB.metric("Resume relevance", f"{resume_relevance}%") #shows the resume relevance

    st.write("Matching keywords (sample):", ", ".join(sorted(list(matching))[:40])) #shows the matching keywords
    st.write("Missing keywords from your resume (sample):", ", ".join(sorted(list(missing_from_resume))[:40])) #shows the missing keywords from the resume text
    st.write("Extra keywords in your resume (sample):", ", ".join(sorted(list(extra_in_resume))[:40])) #shows the extra keywords in the resume text

    st.write("Total unique keywords across both:", len(resume_keywords.union(job_keywords))) #shows the total unique keywords across both the resume and job description

    st.subheader("Preview")
    st.write("Resume length:", len(resume_text.split()), "words") #shows the length of the resume text
    st.write("Job description length:", len(job_text.split()), "words") #shows the length of the job description text
else:
    st.info("Upload both files to see the keyword match.") #shows a info message

