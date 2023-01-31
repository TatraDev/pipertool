from piper.base.executors import FastAPIExecutor
from piper.services import StringValue

from abc import abstractmethod

import torch
import requests
import PIL.Image
import clip

def download_picture(url) -> PIL.Image.Image:
    return PIL.Image.open(requests.get(url, stream=True).raw)


class CLIPExecutor(FastAPIExecutor): 
    requirements = FastAPIExecutor.requirements + ["torch", "clip-by-openai", "requests", "Pillow"]
    '''
    model args:
    -> url of the image
    -> lsit of text descriptions
    '''

    def __init__(self, **kwargs):
            self.model = "ViT-B/32"
            super().__init__(**kwargs)             

    async def run(self, url:float, text_snippets:float) -> list:   

        url, text_snippets = url.value, text_snippets.value
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, preprocess = clip.load(self.model, device=device)

        text = clip.tokenize(text_snippets).to(device)
        image_input = download_picture(url)
        image_input = preprocess(image_input).unsqueeze(0).to(device)

        with torch.no_grad():
            logits_per_image, _ = model(image_input, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy().squeeze()
            probs = [round(item, 3) for item in probs]

        return StringValue(value=str(list(zip(text_snippets, probs))))
        