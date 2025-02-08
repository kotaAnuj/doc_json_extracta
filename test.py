import streamlit as st
import tempfile
import os
import json
import google.generativeai as genai

# Configure the API key for Gemini.
# Either set GOOGLE_API_KEY in your environment or replace the string below.
API_KEY = "AIzaSyDpaOZq0jE6d4SdTpf1GyNk_lLkB75Kn_8"
genai.configure(api_key=API_KEY)

st.title("Gemini Vision Extractor")
st.write("Upload an image or document file and get a JSON response from Gemini Vision.")

# File uploader accepts common document/image types.
uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg", "pdf", "txt"])
# A text area to allow customization of the prompt.
prompt_text = st.text_area(
    "Enter prompt",
    "Please extract key information from this document and return valid JSON."
)

if st.button("Upload and Analyze") and uploaded_file is not None:
    # Save the uploaded file to a temporary file.
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    st.write("File saved to temporary location:", tmp_path)

    try:
        st.write("Uploading file to Gemini...")
        # Upload the file. The upload_file function expects a file path.
        myfile = genai.upload_file(tmp_path)
        st.write("File uploaded successfully!")
    except Exception as e:
        st.error(f"Error during file upload: {e}")
        os.remove(tmp_path)
        st.stop()

    try:
        st.write("Generating content with Gemini Vision...")
        # Get the Gemini model that supports JSON responses.
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Prepare the content array: first a text prompt, then the file data.
        result = model.generate_content([myfile, "\n\n", prompt_text])
        output = result.text
        st.write("Raw output from Gemini:")
        st.text_area("Output", value=output, height=300)
        # Attempt to parse the output as JSON.
        try:
            parsed = json.loads(output)
            st.write("Parsed JSON:")
            st.json(parsed)
        except Exception as parseError:
            st.error("Failed to parse output as JSON: " + str(parseError))
    except Exception as e:
        st.error(f"Error during content generation: {e}")
    
    # Remove the temporary file.
    os.remove(tmp_path)
