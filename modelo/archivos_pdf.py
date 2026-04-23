from pypdf import PdfReader
import os
import boto3

# Necesitamos el pdf en texto plano
def extraerTexto(ruta: str):
    reader = PdfReader(ruta)
    texto = ""
    for pagina in reader.pages:
        texto += pagina.extract_text() + "\n"
    return texto


# Se divide en chucks para que el modelo no tenga que manejar líneas enteras
def dividirTexto(texto, size=500, overlap=50):
    chucks = []
    aux = 0
    while aux < len(texto):
        sigui = aux + size
        chucks.append(texto[aux:sigui])
        aux += size - overlap
        
    return chucks

def bajar_archivos_s3():
    s3 = boto3.client('s3')

    bucket_name = 'voxpropia'
    prefix = 'fuentes/'   # carpeta en S3
    local_dir = './planLector'

    os.makedirs(local_dir, exist_ok=True)

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    for obj in response.get('Contents', []):
      key = obj['Key']
    
     # evitar "carpetas" vacías
      if key.endswith('/'):
         continue

      local_path = os.path.join(local_dir, key.replace(prefix, ''))
      os.makedirs(os.path.dirname(local_path), exist_ok=True)

      s3.download_file(bucket_name, key, local_path)

def tratar_pdf(ruta= "planLector"):
    bajar_archivos_s3() 
    archivos = os.listdir(f"./{ruta}")

    pdfs = []
    for arch in archivos:
        if arch.endswith(".pdf"):
            texto = extraerTexto(f"./{ruta}/{arch}")
            split = dividirTexto(texto)
            pdfs.append(split)
            
    return pdfs

