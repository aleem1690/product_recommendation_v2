

import streamlit as st
from audio_recorder_streamlit import audio_recorder
import modal
import json
import os
import whisper
import pandas as pd



def main():
    # Enthusiastic welcome message
    st.title("Welcome to the Product Needs Portal!")
    st.write("Hello there! 🌟 We're excited to hear about your product needs. You can share your thoughts with us through text or voice!")

    # Radio button to select input type
    input_type = st.radio("Select input type:", ["Text", "Voice"])

    # Initialize variables
    product_needs_text = ""
    product_needs_audio = None

    #setting whisper model
    model = whisper.load_model("base")

    data_di = {"product_name":"mobile_phone","requirement_list":["1.under Rs 35000", "2. calls", "3. texts"]}
    data = pd.DataFrame(data_di)

    req_df = st.experimental_data_editor(data["requirement_list"],num_rows=”dynamic”)
    

    if input_type == "Text":
        # Text box for sharing product needs
        user_input_text = st.text_area("What do you want to buy today?:", "")
    else:
        # Voice recording option
        st.write("We would love to hear from you!")
        audio_bytes = audio_recorder()
        product_needs_voice = st.audio(audio_bytes, format="audio/wav")
        user_input_text = model.transcribe("audio.mp3")

    if st.button("Submit"):
        if input_type == "Text" and user_input_text.strip() != "":
          st.success("🚀 Thanks for sharing your thoughts through text!")
          user_input = user_input_text
        elif input_type == "Voice" and user_input_voice is not None:
          st.success("🎤 Thanks for sharing your thoughts through voice!")
          user_input = user_input_text
        else:
          st.warning("Oops! Please share your product needs, either through text or voice recording.")
        
        result = request_summary(user_input_text)
        # result_name = result['product_name']
        # result_requirements = result['requirement_list'][0]

        # Display the product name and requirements from ML model
        st.success("Product Information from ML Model:")
        
        # Extract product name and requirements
        # edited_product_name = st.text_input("Confirm product:", result['product_name'])
        req_df = st.experimental_data_editor(result['product_name'])

        st.write("Product Requirements:")
        # req_df = st.experimental_data_editor(result['requirement_list'])
        # for idx, req in enumerate(result['requirement_list']):
        #     with st.beta_expander(f"Requirement {idx + 1}"):
        #         edited_req = st.text_input("Edit requirement:", req)
        #         delete_button = st.button("Delete")
        #         if delete_button:
        #             ml_output['requirement_list'].remove(req)

        # Allow user to manipulate requirement list
        # st.write("Product Requirements:")
        # edited_requirements = []
        # for idx, req in enumerate(result['requirement_list']):
        #     edited_req = st.text_input(f"Requirement {idx + 1}:", req)
        #     edited_requirements.append(edited_req)

        # # Rearrange, add, or delete values in requirements list
        # rearranged_requirements = st.text_area("Rearrange, add, or delete values:", "\n".join(edited_requirements))
        
        # result_name = result['product_name']
        # result_requirements = result['requirement_list'][0]
        # #product_name = lines[0]
        # product_requirements = [line.strip() for line in lines[1:] if line.strip()]


def request_summary(user_input):
    f = modal.Function.lookup("corise-prod_recommendation-project", "summary_breakdown")
    output = f.call(user_input)
    return output

if __name__ == '__main__':
    main()
