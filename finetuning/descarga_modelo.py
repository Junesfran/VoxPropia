from huggingface_hub import snapshot_download

def bajar_modelo():
    snapshot_download(
        repo_id="meta-llama/Meta-Llama-3.1-8B-Instruct",
        local_dir="./Llama3/Llama-3.1",
        local_dir_use_symlinks=False,
        token=""
    )

    print("Modelo descargado")

bajar_modelo()