from piper.base.executors import FastAPIExecutor
from piper.services import StringValue, ListOfStringsObject

from abc import abstractmethod

import torch
import requests
import PIL.Image
import clip

def download_picture(url) -> PIL.Image.Image:
    return PIL.Image.open(requests.get(url, stream=True).raw)


class CLIPExecutor(FastAPIExecutor): 

    def __init__(self, **kwargs):
            self.model = "ViT-B/32"
            super().__init__(**kwargs)

    async def run(self, url:StringValue, text_snippets:ListOfStringsObject) -> list:

        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, preprocess = clip.load(self.model, device=device)

        text = clip.tokenize(text_snippets.value).to(device)
        image_input = download_picture(url.value)
        image_input = preprocess(image_input).unsqueeze(0).to(device)

        with torch.no_grad():
            logits_per_image, _ = model(image_input, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy().squeeze()
            probs = [round(item, 3) for item in probs]
        
        return str(list(zip(text_snippets.value, probs)))
        
            
    async def __call__(self, url:StringValue, text_snippets:ListOfStringsObject) -> list:
        return await CLIPExecutor.run(self, url, text_snippets)
