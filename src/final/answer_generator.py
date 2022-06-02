import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer


class AnswerGenerator:
    def __init__(self):
        self._tokenizer = T5Tokenizer.from_pretrained("cointegrated/rut5-small-chitchat")
        self._model = T5ForConditionalGeneration.from_pretrained("cointegrated/rut5-small-chitchat")

    def generate(self, history: list[str]) -> str:
        text = "\n\n".join(history)
        inputs = self._tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            hypotheses = self._model.generate(
                **inputs,
                do_sample=True,
                top_p=0.6,
                num_return_sequences=1,
                repetition_penalty=2.5,
                max_length=64,
            )
        return self._tokenizer.decode(hypotheses[0], skip_special_tokens=True)
