from decouple import config
import os

from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core.multi_modal_llms.generic_utils import load_image_urls
from llama_index.core import SimpleDirectoryReader

os.environ['GOOGLE_API_KEY'] = config('GOOGLE_API_KEY')

image_urls = [
    "https://www.dropbox.com/scl/fi/v0l8a35fx62qnuoefdu6f/2019_Porsche_911_Carrera.jpg?rlkey=cjg374asg3u1u9deujhk2vsdo&raw=1",
]

image_docs = load_image_urls(image_urls=image_urls)

gemini_vision_pro = GeminiMultiModal(
    model_name='models/gemini-pro-vision'
)

# Read the image
image_docs = SimpleDirectoryReader(input_dir="./images/").load_data()

for image in image_docs:
    response = gemini_vision_pro.complete(
        prompt="What is the text in the image trying to infer?",
        image_documents=[image]
    )

    print(response)