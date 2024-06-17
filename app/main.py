from pydantic import BaseModel
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core.program import MultiModalLLMCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core import SimpleDirectoryReader

from decouple import config
import secrets
import pandas as pd
import streamlit as st

GOOGLE_API_KEY = config('GOOGLE_API_KEY')
MODEL_NAME = 'models/gemini-1.5-pro-latest'

prompt_template_str = """
        Give me the summary of the person in the image\
        and return the response in json format\
    """

class PersonAttributes(BaseModel):
    """Data model of the description of a person."""
    name: str
    nationality: str
    date_of_birth: str
    place_of_birth: str
    profession: str
    description: str
    height: float
    weight_in_kilo: float

def structured_response_gemini(
    output_class: PersonAttributes,
    image_documents: list,
    prompt_template_str: str,
    model_name: str = MODEL_NAME      
):
    gemini_llm = GeminiMultiModal(api_key=GOOGLE_API_KEY, model_name=model_name)

    llm_program = MultiModalLLMCompletionProgram.from_defaults(
        output_parser=PydanticOutputParser(output_cls=output_class),
        image_documents=image_documents,
        prompt_template_str=prompt_template_str,
        multi_modal_llm=gemini_llm,
        verbose=True
    )

    response = llm_program()

    return response

def get_details_from_model(uploaded_img):
    """Get response from the model."""
    for img_doc in uploaded_img:
        data=[]
        structured_response = structured_response_gemini(
            output_class=PersonAttributes,
            image_documents=[img_doc],
            prompt_template_str=prompt_template_str
        )

        for resp in structured_response:
            data.append(resp)

        data_dict = dict(data)
        return data_dict

st.title('Person Description Model')

up_file = st.file_uploader(
    label="Choose an image",
    accept_multiple_files=False,
    type=['png', 'jpg']
)

if up_file is not None:
    st.toast('File uploaded successfully!', icon="✔️")
    byte_data = up_file.read()
    st.write('Filename: ', up_file.name)

    with st.spinner('Loading... please wait!'):
        if up_file.type == 'image/jpeg':
            file_type = 'jpg'
        else:
            file_type = 'png'

        # Save the file
        filename = f"{secrets.token_hex(8)}.{file_type}"

        with open(f"./images/{filename}", "wb") as file:
            file.write(byte_data)

        filepath = f"./images/{filename}"

        # Load the image
        image_docs = SimpleDirectoryReader(
            input_files=[filepath]
        ).load_data()

        response = get_details_from_model(image_docs)

        with st.sidebar:
            st.image(image=filepath, caption=response.get('name', 'unknown'))
            st.markdown(f"""
                    :green[Name]: :red[{response.get("name", "Unknwon")}]\n
                    :green[Nationality]: :violet[{response.get("nationality", "Unknwon")}]\n
                    :green[Date Of Birth]: :gray[{response.get("date_of_birth", "Unknwon")}]\n
                    :green[Profession]: :gray[{response.get("profession", "Unknwon")}]\n
                    :green[Description]: :gray[{response.get("description", "Unknwon")}]\n
                    :green[Place Of Birth]: :orange[{response.get("place_of_birth", "Unknwon")}]\n
                    :green[Height]: :red[{response.get("height", "Unknwon")} m]\n
                    :green[Weight In Kilograms]: :red[{response.get("weight_in_kilo", "Unknwon")} kg]\n
                        """)