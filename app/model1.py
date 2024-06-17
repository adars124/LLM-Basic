from decouple import config
import os
import asyncio

from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core.multi_modal_llms.generic_utils import load_image_urls

os.environ['GOOGLE_API_KEY'] = config('GOOGLE_API_KEY')

image_urls = [
    "https://www.dropbox.com/scl/fi/v0l8a35fx62qnuoefdu6f/2019_Porsche_911_Carrera.jpg?rlkey=cjg374asg3u1u9deujhk2vsdo&raw=1",
]

image_docs = load_image_urls(image_urls=image_urls)

gemini_vision_pro = GeminiMultiModal(
    model_name='models/gemini-pro-vision'
)

async def generate_resp(): 
    response = await gemini_vision_pro.astream_complete(
        prompt="Give me a brief description of the vehicle displayed in the image.",
        image_documents=image_docs
    )

    async for resp in response:
        print(resp.text)


asyncio.run(generate_resp())