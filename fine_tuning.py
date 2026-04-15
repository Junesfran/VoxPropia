from transformers import AutoTokenizer
import ray.train.torch
from ray.train.huggingface.transformers import RayTrainReportCallback, prepare_trainer
from transformers import TrainingArguments, Trainer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
import ray

model_id = "meta-llama/Llama-3.1-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Definimos las dependencias
runtime_env = {
    "pip": [
        "transformers>=4.43.0", # Versión mínima para Llama 3.1
        "peft",
        "accelerate",
        "datasets",
        "bitsandbytes", # Si usas QLoRA
        "sentencepiece"
    ],
    "working_dir": "./llama_3.1" # Sincroniza tus archivos locales con el cluster
}

# Ray instala esto automáticamente en todos los workers al conectar
ray.init(address="auto", runtime_env=runtime_env)

def preprocess_function(examples):
    # Aplicamos el template oficial de Llama 3.1
    texts = [tokenizer.apply_chat_template(msg, tokenize=False, add_generation_prompt=False) for msg in examples["messages"]]
    return tokenizer(texts, padding="max_length", truncation=True, max_length=512)


def train_func(config):
    # 1. Cargar modelo y tokenizador
    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Llama-3.1-8B-Instruct",
        device_map={"": ray.train.torch.get_device()},
        # load_in_4bit=True, # Opcional para QLoRA
    )
    
    # 2. Configurar LoRA
    lora_config = LoraConfig(
        r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"], 
        lora_dropout=0.05, task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_config)

    # 3. Argumentos de entrenamiento
    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        num_train_epochs=3,
        fp16=True, # O bf16 si tus GPUs lo soportan (A100+)
        logging_steps=10,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=load_dataset("json", data_files="biblioteca_comercio.json", split="train"), # Tu dataset procesado
        callbacks=[RayTrainReportCallback()]
    )
    
    # 4. Adaptar el trainer para Ray
    trainer = prepare_trainer(trainer)
    trainer.train()

# Configurar el escalado en el cluster
scaling_config = ray.train.ScalingConfig(num_workers=2, use_gpu=True)
trainer = ray.train.torch.TorchTrainer(
    train_func,
    scaling_config=scaling_config
)
result = trainer.fit()

# Obtener la ruta del checkpoint
checkpoint_path = result.checkpoint.path
print(f"Modelo guardado en: {checkpoint_path}")