import os

from dotenv import load_dotenv  # pip install python-dotenv==0.21.0
from google.cloud import translate  # pip install google-cloud-translate==3.8.2

# This is a priced translator service, you need to GoogleCloudPlatform account to use it.
# Required environment variables: PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS
# 
# You need to set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of the JSON file that contains your service account key.
# https://cloud.google.com/translate/docs/basic/setup-basic
load_dotenv()

client = translate.TranslationServiceClient()
location = "global"
# Get project id from environment variable
project_id = os.environ["PROJECT_ID"]
parent = f"projects/{project_id}/locations/{location}"

def translate(text, source_language_code, target_language_code):
    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",  # mime types: text/plain, text/html
        source_language_code=source_language_code or None, # "" = auto detect
        target_language_code=target_language_code,
        model="nmt", # "base"(PBMT) or "nmt"(NMT)
    )
    for translation in response.translations:
        return translation.translated_text
