from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

class LLMClient:
    def __init__(self, api_key=None, model_name="google/flan-t5-small", use_local=True):
        self.use_local = use_local
        self.model_name = model_name

        if self.use_local:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.pipe = pipeline("text2text-generation", model=self.model, tokenizer=self.tokenizer)
        else:
            self.api_key = api_key  # Keep in case you want to support remote later

    def test_connection(self):
        if self.use_local:
            return True  # Always true for local
        return False  # Disable API for now

    def generate(self, prompt: str):
        if self.use_local:
            result = self.pipe(prompt, max_length=128, do_sample=False)
            return result[0]['generated_text']
        else:
            raise NotImplementedError("API mode not supported in local-only setup.")
