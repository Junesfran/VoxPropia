from pypdf import PdfReader
import os

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

def tratar_pdf(ruta= "planLector"):
    archivos = os.listdir(f"./{ruta}")

    pdfs = []
    for arch in archivos:
        if arch.endswith(".pdf"):
            texto = extraerTexto(f"./{ruta}/{arch}")
            split = dividirTexto(texto)
            pdfs.append(split)
            
    return pdfs

