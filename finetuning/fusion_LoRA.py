import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# --- CONFIGURACIÓN ---
mi_token = ""
model_id = "meta-llama/Llama-3.1-8B-Instruct"
lora_path = "./llama3-finetuned"
output_path = "./llama3-merged"

print("Cargando tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_id, token=mi_token)

# --- CARGA DEL MODELO BASE ---
print("Cargando modelo base...")
# Usamos un device_map simple para evitar el error de recursión de capas
# Si tienes suficiente VRAM, puedes usar {"": 0}. Si no, usamos {"": "cpu"}
base_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map={"": "cpu"}, # Forzamos carga limpia en RAM para la fusión
    token=mi_token,
    trust_remote_code=True,
    low_cpu_mem_usage=True
)

# --- CARGA DEL ADAPTADOR ---
print("Acoplando adaptador LoRA...")
# Eliminamos el device_map="cpu" extra aquí para que herede el del base_model
model = PeftModel.from_pretrained(
    base_model, 
    lora_path,
    token=mi_token
)

# --- FUSIÓN ---
print("Fusionando pesos (Merge)...")
# Esta operación ocurre en la memoria donde esté el modelo (en este caso, CPU)
model = model.merge_and_unload()

# --- GUARDADO ---
print(f"Guardando modelo fusionado en {output_path}...")
model.save_pretrained(output_path, safe_serialization=True)
tokenizer.save_pretrained(output_path)

print("---------------------------------------")
print("Todo salió bien. Modelo listo para usar.")
print("---------------------------------------")