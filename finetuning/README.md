Meter el llama3.gguf en la misma carpeta del Modelfile (/finetuning)
Ejecutar
    
    ollama create llama3-finetuned -f Modelfile
En caso de que solo tengamos la carpeta /Llama3-merged ejecutar esto:
        
    python convert_hf_to_gguf.py ./llama3-merged --outfile llama3.gguf
