import streamlit as st
from blood_report import analyze_blood_report
import tempfile

st.title("Blood Report Analyzer")

uploaded_file = st.file_uploader(
    accept_multiple_files=False,
    type=["pdf"],
    label="Upload your blood report",
)

if uploaded_file is not None:
    with st.spinner("Analyzing..."):
        try:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()

            # create a temporary file
            with tempfile.NamedTemporaryFile() as tmp_file:
                tmp_file.write(bytes_data)
                temp_file_path = tmp_file.name
                answer = analyze_blood_report(temp_file_path)

                tmp_file.flush()
                tmp_file.seek(0)
                tmp_file.close()

                uploaded_file.flush()
                uploaded_file.seek(0)
                uploaded_file.close()
                st.markdown(answer)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    st.success("Done!")
