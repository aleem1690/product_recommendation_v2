

import streamlit as st
from audio_recorder_streamlit import audio_recorder
import modal
import json
import os
import whisper
import pandas as pd
# from st_draggable_list import DraggableList
import speech_recognition as sr

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
    r = sr.Recognizer()
    
    if input_type == "Text":
        # Text box for sharing product needs
        user_input_text = st.text_area("What do you want to buy today?:", "")
    else:
        # Voice recording option
        st.write("We would love to hear from you!")
        audio_bytes = audio_recorder()
        product_needs_voice = st.audio(audio_bytes, format="audio/wav")
        st.write(type(products_needs_voice))
        # user_input_text = model.transcribe(product_needs_voice)

        # with sr.AudioFile(product_needs_voice) as source:
        #     # listen for the data (load audio to memory)
        #     audio_data = r.record(source)
        #     # recognize (convert from speech to text)
        #     text = r.recognize_google(audio_data)
        #     print(text)

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
        
        try:
            # check if the key exists in session state
            _ = st.session_state.result
        except AttributeError:
            # otherwise set it to false
            st.session_state.result = False

        # Display the product name and requirements from ML model
        st.success("Product Information from ML Model:")
        
        # Extract product name and requirements
        # edited_product_name = st.text_input("Confirm product:", result['product_name'])
        result_df = pd.DataFrame(result)
        data_prod_name = result_df["product_name"].drop_duplicates()
        # data_prod_name = data_prod_name.rename(columns={"product_name":"product identified"})
        # name_df = st.experimental_data_editor(data_prod_name,num_rows="dynamic")
        name_df = st.experimental_data_editor(data_prod_name, num_rows="dynamic")
        # if st.button("Save Changes"):
        #     st.table(name_df)
    
    
        st.write("Product Requirements:")
        data_req_name = result_df.drop("product_name",axis=1)
        data_req_name["Rank"] = ""
        req_df = st.experimental_data_editor(data_req_name,num_rows="dynamic")
        if st.button("Save Changes"):
            st.session_state.result["product_name"] = name_df
            st.session_state.result["requirements_list"] = req_df
            st.session_state.result = True
            st.success("Changes saved!")
            
            st.table(name_df,req_df)

def request_summary(user_input):
    f = modal.Function.lookup("corise-prod_recommendation-project", "summary_breakdown")
    output = f.call(user_input)
    return output

if __name__ == '__main__':
    main()
