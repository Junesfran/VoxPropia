import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

model_id = "meta-llama/Llama-3.1-8B-Instruct"
# Ruta donde Ray guardó el checkpoint (sustituye por la real)
adapter_path = "./results/checkpoint-XX" 

# 1. Cargar Tokenizer y Modelo Base
tokenizer = AutoTokenizer.from_pretrained(model_id)
base_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)

# 2. Cargar el "Adapter" entrenado (tus conocimientos del IES Comercio)
model = PeftModel.from_pretrained(base_model, adapter_path)
model.eval()

# 3. Preparar la consulta
messages = [
    {"role": "system", "content": "Eres un asistente virtual del IES Comercio experto en la biblioteca."},
    {"role": "user", "content": "¿Qué libro me recomiendas para 1º ESO?"}
]

# Aplicar el chat template oficial de Llama 3.1
inputs = tokenizer.apply_chat_template(
    messages, 
    add_generation_prompt=True, 
    return_tensors="pt"
).to("cuda")

# 4. Generar respuesta
with torch.no_grad():
    outputs = model.generate(
        inputs, 
        max_new_tokens=150, 
        temperature=0.7, # Creatividad moderada
        top_p=0.9,
        eos_token_id=tokenizer.eos_token_id
    )

# Decodificar y mostrar
response = tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True)
print(f"Respuesta del modelo:\n{response}")