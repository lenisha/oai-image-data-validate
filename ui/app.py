import pandas as pd
import streamlit as st
import base64
import urllib.request
import json
from dotenv import load_dotenv
import os


st.set_page_config(
    page_title="Image to Text",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("AI Claim Image Validator 🤖✍️")


def to_base64(uploaded_file):
    file_buffer = uploaded_file.read()
    b64 = base64.b64encode(file_buffer).decode()
    return f"data:image/png;base64,{b64}"


with st.sidebar:
    st.title("Upload Your Images")
    st.session_state.images = st.file_uploader(label=" ", accept_multiple_files=True)


def generate_df():
    current_df = pd.DataFrame(
        {
            "image_id": [img.file_id for img in st.session_state.images],
            "image": [to_base64(img) for img in st.session_state.images],
            "name": [img.name for img in st.session_state.images],
            "description": [""] * len(st.session_state.images),
            "claim_type": [""] * len(st.session_state.images),
            "validation_summary": [""] * len(st.session_state.images),
        }
    )

    if "df" not in st.session_state:
        st.session_state.df = current_df
        return

    new_df = pd.merge(current_df, st.session_state.df, on=["image_id"], how="outer", indicator=True)
    new_df = new_df[new_df["_merge"] != "right_only"].drop(columns=["_merge", "name_y", "image_y", 
                                                                    "description_x","claim_type_x",
                                                                    "validation_summary_x"])
    new_df = new_df.rename(columns={"name_x": "name", "image_x": "image", 
                                    "description_y": "description",
                                    "claim_type_y":"claim_type",
                                    "validation_summary_y":"validation_summary"})
    new_df["description"] = new_df["description"].fillna("")
    new_df["claim_type"] = new_df["claim_type"].fillna("")
    new_df["validation_summary"] = new_df["validation_summary"].fillna("")

    st.session_state.df = new_df


def render_df():
    st.data_editor(
        st.session_state.df,
        column_config={
            "image": st.column_config.ImageColumn(
                "Preview Image", help="Image preview", width=100
            ),
            "name": st.column_config.Column("Name", help="Image name", width=100),
            "description": st.column_config.Column(
                "Claim Analysis", help="Claim Analysis", width=600
            ),
            "claim_type": st.column_config.Column(
                "Claim Type", help="Claim Type", width=100
            ),
            "validation_summary": st.column_config.Column(
                "Validation Summary", help="Validation Summary", width=200
            ),
        },
        hide_index=True,
        height=400,
        column_order=["image", "name", "claim_type","validation_summary","description"],
        use_container_width=True,
    )


def generate_description(image_base64):
    ''' Call PromptFlow API to generate image description '''

    data = { "image_1": image_base64 }
    body = str.encode(json.dumps(data))

    load_dotenv()

    url = os.getenv('URL')
    api_key = os.getenv('API_KEY')

    
    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key) }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        result_str = result.decode('utf-8')
        print(result_str)

        return result_str
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))


        return '{"error":"Image Analysis failed"}'


def update_df():
    indexes = st.session_state.df[st.session_state.df["description"] == ""].index
    for idx in indexes:
        description = generate_description(st.session_state.df.loc[idx, "image"])
        st.session_state.df.loc[idx, "description"] = description
        # get claim_type from json
        json_data = json.loads(description)
        st.session_state.df.loc[idx, "claim_type"] = json_data['type_of_claim']
        st.session_state.df.loc[idx, "validation_summary"] = json_data['validation_summary']


if st.session_state.images:
    generate_df()

    #st.text_input("Prompt", value="What's in this image?", key="text_prompt")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Generate Image Descriptions", use_container_width=True):
            update_df()
    
    with col2:    
        st.download_button(
                "Download descriptions as CSV",
                st.session_state.df.drop(['image', "image_id"], axis=1).to_csv(index=False),
                "descriptions.csv",
                "text/csv",
                use_container_width=True
        )

    render_df()
