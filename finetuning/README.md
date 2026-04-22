Primero hacer el merge de LoRA con el modelo finetuneado.
Para ello:
* En la carpeta finetuning necesitas la carpeta del modelo finetuneado y el modelo original.
para el modelo original ejecutar:

      py ./descarga_modelo.py
* Hacer el Merged

      py ./fusionar_LoRA
---
* Hacer un git clone de llama.cpp

        git clone https://github.com/ggerganov/llama.cpp
* Entrar

        cd llama.cpp
* Recordar hacer un enviroment con el requeriment que trae el repo
---
En caso de que solo tengamos la carpeta /Llama3-merged ejecutar esto:
        
    python convert_hf_to_gguf.py ./llama3-merged --outfile llama3.gguf
Recuerda llevarte el llama3.gguf resultante a la carpeta de finetuning
---
Meter el llama3.gguf en la misma carpeta del Modelfile (/finetuning)
Ejecutar
    
    ollama create llama3-finetuned -f Modelfile

