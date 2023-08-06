import os
from .chatgpt import ChatGPT
from .bloom import Bloom


class Models:
    MODELS_DESCRIPTION = {
        "gpt-3.5-turbo": "OpenAI most capable GPT-3.5 model",
        "gpt-4": "OpenAI GPT 4.0 model",
        "mt0-xxl-mt": "Bloom's 13B parameter model finetuned on xP3",
    }

    def get_choices(self):
        return self.MODELS_DESCRIPTION.keys()

    def get_descriptions(self):
        return self.MODELS_DESCRIPTION

    def get_model(self, model_name, prompt):
        if model_name.startswith("gpt"):
            key = os.environ.get("OPENAI_API_KEY")
            if key is None or len(key) == 0:
                raise RuntimeError(
                    "You should set OPENAI_API_KEY environment variable with you OpenAI key"
                )
            model = ChatGPT(prompt, model_name)
        elif model_name == "mt0-xxl-mt":
            model = Bloom(prompt)
        else:
            raise RuntimeError(f"Unknown model {model_name}")

        return model
