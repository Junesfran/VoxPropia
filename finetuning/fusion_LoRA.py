from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)

model = PeftModel.from_pretrained(base_model, "./llama3-finetuned")

model = model.merge_and_unload()

model.save_pretrained("./llama3-merged")
tokenizer.save_pretrained("./llama3-merged")