from fastapi import FastAPIExecutor
from piper import envs

import torch
import requests
import clip
import PIL

class ClipExecutor(FastAPIExecutor): 

    def __init__(self, url:str, text_snippets:list[str]):
            self.url = url
            self.text_snippets = text_snippets
            self.model = "ViT-B/32"

    def download_picture(self) -> PIL.Image.Image:
        return PIL.Image.open(requests.get(self.url, stream=True).raw)

    def do_clip(self) -> list:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, preprocess = clip.load(self.model, device=device)

        text = clip.tokenize(self.text_snippets).to(device)
        image_input = ClipExecutor.download_picture(self)
        image_input = preprocess(image_input).unsqueeze(0).to(device)

        with torch.no_grad():
            logits_per_image, _ = model(image_input, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

        return list(zip(self.text_snippets, probs))


with envs.DockerEnv(): 
    url = 'https://cdn.kanobu.ru/games/f8ffb106-1d6b-497c-8b12-3943d570ddc3.jpg'
    texts = ["hulk", "iron men", "black widow", "avengers"]
    res = ClipExecutor(url, texts).do_clip()
    print(res)
       