from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer

model_name = "OpenAssistant/falcon-7b-sft-mix-2000"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    offload_folder="offload",
    trust_remote_code=True,
    load_in_4bit=True,
)
streamer = TextStreamer(tokenizer, skip_prompt=True)
message = "<|prompter|>This is a demo of a text streamer. What's a cool fact about ducks?<|endoftext|><|assistant|>"
inputs = tokenizer(message, return_tensors="pt").to(model.device)

tokens = model.generate(
    **inputs, max_new_tokens=25, do_sample=True, temperature=0.9, streamer=streamer
)
