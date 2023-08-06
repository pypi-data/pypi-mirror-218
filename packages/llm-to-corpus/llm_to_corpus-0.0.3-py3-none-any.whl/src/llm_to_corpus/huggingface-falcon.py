from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer

model_name = "OpenAssistant/falcon-7b-sft-mix-2000"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="cpu",
    offload_folder="offload",
    trust_remote_code=True,
    load_in_4bit=False,
)
streamer = TextStreamer(tokenizer, skip_prompt=True)
message = (
    '<|prompter|>Translate to Catalan: "how are you today?"<|endoftext|><|assistant|>'
)
inputs = tokenizer(message, return_tensors="pt", return_token_type_ids=False).to(
    model.device
)

print("A")
tokens = model.generate(
    **inputs, max_new_tokens=25, do_sample=False, temperature=0, streamer=streamer
)
print("B")
# print(tokens)
