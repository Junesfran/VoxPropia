# ==============================================================
#   train_ray_qwen_single_file.py
# ==============================================================

import os
import json
import torch
import ray
import ray.train
from ray.train import ScalingConfig, RunConfig, CheckpointConfig
from ray.train.torch import TorchTrainer, TorchConfig
from ray.train.huggingface.transformers import prepare_trainer
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    TrainingArguments, 
    Trainer, 
    DataCollatorForLanguageModeling
)
from peft import get_peft_model, LoraConfig, TaskType
from datasets import Dataset

# ------------------------------------------------------------------
# CONFIGURACIÓN DE RUTAS (Ajusta a tu archivo único)
# ------------------------------------------------------------------
_SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
# Cambia esta ruta a donde tengas tu archivo único .jsonl
DATASET_PATH = os.path.join(_SCRIPT_DIR, "dataset_ies_comercio.jsonl") 
OUTPUT_DIR   = os.path.join(_SCRIPT_DIR, "output", "qwen_ies_comercio")

# PARÁMETROS
MODEL_NAME  = "Qwen/Qwen2.5-1.5B-Instruct"
NUM_WORKERS = 4          # Ajustado a tus 4 nodos (1 GPU por nodo)
MAX_LENGTH  = 512        # Longitud máxima por conversación
EPOCHS      = 3
BATCH_SIZE  = 1          # Por GPU
GRAD_ACCUM  = 8

# ==================================================================
# PROCESAMIENTO DEL DATASET (Con Split automático)
# ==================================================================

def cargar_y_dividir_dataset(ruta_jsonl, tokenizer, max_length):
    """Carga un archivo único y lo divide en Train y Eval."""
    datos = []
    with open(ruta_jsonl, "r", encoding="utf-8") as f:
        for linea in f:
            if linea.strip():
                datos.append(json.loads(linea))
    
    # Creamos el Dataset de HuggingFace
    full_ds = Dataset.from_list(datos)
    
    # Dividimos: 90% entrenamiento, 10% evaluación
    ds_split = full_ds.train_test_split(test_size=0.1, seed=42)
    
    def process_item(item):
        # El template de Qwen procesa perfectamente tu formato {"role": ..., "content": ...}
        tokenized = tokenizer.apply_chat_template(
            item["messages"],
            truncation=True,
            max_length=max_length,
            add_generation_prompt=False,
            return_tensors=None
        )
        return {"input_ids": tokenized}

    # Aplicamos la tokenización a ambos sets
    train_ds = ds_split["train"].map(process_item, remove_columns=full_ds.column_names)
    eval_ds  = ds_split["test"].map(process_item, remove_columns=full_ds.column_names)
    
    return train_ds, eval_ds

# ==================================================================
# LOOP DE ENTRENAMIENTO
# ==================================================================

def train_loop_per_worker(config: dict):

    model_name  = config["model_name"]
    output_dir  = config["output_dir"]
    max_length  = config["max_length"]
    epochs      = config["epochs"]
    batch_size  = config["batch_size"]
    grad_accum  = config["grad_accum"]
    
    # ... (Carga de parámetros igual al anterior) ...
    tokenizer = AutoTokenizer.from_pretrained(config["model_name"], trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Cargamos y dividimos el dataset directamente en el worker
    train_ds, eval_ds = cargar_y_dividir_dataset(
        config["dataset_path"], 
        tokenizer, 
        config["max_length"]
    )

    # Sharding para distribución entre GPUs
    rank = ray.train.get_context().get_world_rank()
    world_size = ray.train.get_context().get_world_size()
    train_ds = train_ds.shard(num_shards=world_size, index=rank)
    eval_ds  = eval_ds.shard(num_shards=world_size, index=rank)

    # --- Resto del código del modelo (LoRA, Trainer, etc.) es igual ---
    # (Asegúrate de pasar 'dataset_path' en el config del TorchTrainer)
    
    # [Aquí iría la inicialización del modelo y el Trainer explicados antes]
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map={"": "cuda"}, # Ray asigna la GPU correcta
        use_cache=False,
    )

    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    model = get_peft_model(model, lora_config)
    model.enable_input_require_grads()

    # ---- 4. Trainer ----
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=grad_accum,
        learning_rate=1e-4, # Un poco más bajo para fine-tuning instruct
        num_train_epochs=epochs,
        logging_steps=5,
        eval_strategy="epoch",
        save_strategy="no", # Ray se encarga de los checkpoints
        bf16=True,
        gradient_checkpointing=True,
        ddp_find_unused_parameters=False,
        report_to="none",
    )

    # DataCollator para Causal LM con Padding dinámico
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        data_collator=data_collator,
    )

    trainer = prepare_trainer(trainer)
    trainer.train()

    # Guardar solo en el master
    if rank == 0:
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)

# ==================================================================
# ORQUESTADOR
# ==================================================================

if __name__ == "__main__":
    # Inicialización de Ray
    _ray_env = {"USE_LIBUV": "0", "PYTHONIOENCODING": "utf-8"}
    try:
        ray.init(address="auto", runtime_env={"env_vars": _ray_env})
    except:
        ray.init(runtime_env={"env_vars": _ray_env})

    train_config = {
        "model_name" : MODEL_NAME,
        "output_dir" : OUTPUT_DIR,
        "max_length" : MAX_LENGTH,
        "epochs"     : EPOCHS,
        "batch_size" : BATCH_SIZE,
        "grad_accum" : GRAD_ACCUM,
    }

    scaling_config = ScalingConfig(
        num_workers=NUM_WORKERS,
        use_gpu=True,
        resources_per_worker={"GPU": 1, "CPU": 4},
    )

    run_config = RunConfig(
        name="qwen_chat_finetuning",
        storage_path=os.path.join(OUTPUT_DIR, "ray_results"),
        checkpoint_config=CheckpointConfig(num_to_keep=1),
    )

    trainer = TorchTrainer(
        train_loop_per_worker=train_loop_per_worker,
        train_loop_config=train_config,
        scaling_config=scaling_config,
        run_config=run_config,
        torch_config=TorchConfig(backend="gloo" if os.name == "nt" else "nccl"),
    )

    trainer.fit()