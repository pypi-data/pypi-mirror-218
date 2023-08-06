import ctranslate2
import transformers
import huggingface_hub


class Bloom:
    def __init__(self, prompt):
        self.prompt = prompt

        # Models: https://huggingface.co/bigscience/bloomz-p3
        # https://github.com/bigscience-workshop/xmtf

        model_name = "mt0-xxl-mt"
        snapshot_folder = self._download_model_if_need(model_name)
        model = f"{snapshot_folder}/{model_name}"

        self.model = ctranslate2.Translator(model, compute_type="int8", intra_threads=8)
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(model)

    def _download_model_if_need(self, model_name):
        repo_id = "jordimas/bloom-ctranslate2"
        snapshot_folder = huggingface_hub.snapshot_download(
            repo_id=repo_id, allow_patterns=f"*{model_name}*"
        )
        return snapshot_folder

    def query_thread(self, text, translations, index):
        start_tokens = self.tokenizer.convert_ids_to_tokens(
            self.tokenizer.encode(f"{self.prompt} {text}")
        )

        results = self.model.translate_batch([start_tokens])

        output_tokens = results[0].hypotheses[0]
        result = self.tokenizer.decode(
            self.tokenizer.convert_tokens_to_ids(output_tokens)
        )

        result = result.replace(self.prompt, "")
        translations[index] = result
        # print(f"result: {index} - t:'{result}' - s:'{self.prompt}'")
