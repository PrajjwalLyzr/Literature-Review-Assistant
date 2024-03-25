import streamlit as st
import os
import shutil



def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")


def get_files_in_directory(directory):
    # This function help us to get the file path along with filename.
    files_list = []

    if os.path.exists(directory) and os.path.isdir(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                files_list.append(file_path)

    return files_list

def save_uploaded_file(directory, uploaded_file):
    remove_existing_files(directory=directory)
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.read())
    st.success("File uploaded successfully")


def reviewer(agent):
    results = {}
    prompts = {
        "Summary": "Write 2 lines of summary about this research paper in the simplest manner",
        "Research Objectives": "What is the main research question the paper investigates? What are the specific objectives or hypotheses outlined in the paper? Use 3-5 bullet points to show the response",
        "Methodology": "What research methodology was used in the study (e.g., survey, experiment, case study)? What is the population or sample size used in the research? How was the data collected and analyzed? Use 3-5 bullet points to show the response",
        "Findings and Results": "What are the key findings or results presented in the paper? Are there any specific statistics, figures, or tables that highlight the results? How do the findings relate to the research question and objectives? Use 3-5 bullet points to show the response",
        "Discussion and Conclusions": "What are the main conclusions drawn by the authors based on the findings? What are the limitations of the study or areas for future research? How do the paper's conclusions contribute to the existing body of knowledge in the field? Make a 4-5 line of response",
        "Related Research": "Write down 5 research topics along with their titles based on this research paper",
        "Prototype": "The user wants to write an extended research paper on the provided research paper, so what are the key points I should take care of and how can I proceed with this?"
    }

    for heading, prompt in prompts.items():
        response = agent.query(prompt)
        results[heading] = response.response

    return results


def get_response(response:dict):
    for heading, response in response.items():
        st.subheader(heading)
        st.write(response)
        st.markdown("---")  
