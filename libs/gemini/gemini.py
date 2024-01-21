import google.generativeai as genai

from libs.monad.maybe_monad import Just, Nothing, Maybe
from libs.colour_print import *

import datetime as dt


def to_markdown(text):
    text = text.replace('•', '  *')
    return text


class GeminiClient:
    def __init__(self, api_key: str, model: str):
        timestamp = dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        print(f"{timestamp} - Initialising Gemini {model} Client...")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def generate(self, prompt: str | list[str], verbose=False) -> Maybe[str]:
        if verbose:
            print(f"Generating Gemini Content for <{prompt}>")
        try:
            response = self.model.generate_content(prompt)
            response.text
            return Just(to_markdown(response.text))
        except Exception as e:
            return Nothing(f"Gemini Error: {e.__class__.__name__} {e}")
