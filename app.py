import streamlit as st
from blood_report import read_blood_report, standardize_blood_report,collect_reasons, generate_llm_answer
import tempfile
import time


st.title("Blood Report Analyzer")

gender_option = st.selectbox(
    "Gender",
    ("Male", "Female"),
)

uploaded_file = st.file_uploader(
    accept_multiple_files=False,
    type=["pdf"],
    label="Upload your blood report",
)

answer = ""

if uploaded_file is not None:
    with st.status("Progressing...", expanded=True) as status:
        try:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()

            # Create a temporary file
            with tempfile.NamedTemporaryFile() as tmp_file:
                tmp_file.write(bytes_data)
                temp_file_path = tmp_file.name
                
                llm_input_token_count = 0
                llm_output_token_count = 0

                # Read blood report content
                st.write("Extracting test results...")
                read_blood_report_result = read_blood_report(temp_file_path)
                llm_input_token_count += read_blood_report_result["usage"].get("input_tokens", 0)
                llm_output_token_count += read_blood_report_result["usage"].get("output_tokens", 0)
                if read_blood_report_result["invalid_response"]:
                    status.update(label="Analyze failed!", state="error", expanded=True)
                    st.markdown(read_blood_report_result["content"])
                else:
                    report = read_blood_report_result["content"]

                    # Standardize blood report to have same unit as the base structure
                    st.write("Standardizing test results...")
                    standardize_report_response = standardize_blood_report(report)
                    standardized_report = standardize_report_response["standardized_blood_test_json"]
                    llm_input_token_count += standardize_report_response["usage"].get("input_tokens", 0)
                    llm_output_token_count += standardize_report_response["usage"].get(
                        "output_tokens", 0
                    )

                    # Collect reasons for each test
                    st.write("Analyzing test results...")
                    derived_reasons = collect_reasons(standardized_report, gender_option)

                    # Generate answer
                    st.write("Generating answer...")
                    llm_answer_response = generate_llm_answer(derived_reasons)
                    answer = llm_answer_response["content"]
                    llm_input_token_count += llm_answer_response["usage"].get("input_tokens", 0)
                    llm_output_token_count += llm_answer_response["usage"].get("output_tokens", 0)                    
                    status.update(label="Analyze complete!", state="complete", expanded=True)

                tmp_file.flush()
                tmp_file.seek(0)
                tmp_file.close()

                uploaded_file.flush()
                uploaded_file.seek(0)
                uploaded_file.close()
        except Exception as e:
            status.update(label="Analyze failed!", state="error", expanded=True)
            st.error(f"An error occurred: {e}")
        finally:
            st.write(f"LLM input tokens: {llm_input_token_count}")
            st.write(f"LLM output tokens: {llm_output_token_count}")
    st.markdown(answer)
    st.button("Rerun")
