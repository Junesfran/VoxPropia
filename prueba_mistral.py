from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import ollama

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
        chucks.append(texto[aux:aux+sigui])
        aux += size - overlap
        
    return chucks


texto = extraerTexto("planLector/prueba.pdf")
textoSplit = dividirTexto(texto)

# Uso de chromadb para tokenizar el texto plano extraido y generar la colección de embebidos
modelo = SentenceTransformer("multi-qa-mpnet-base-cos-v1")

cliente = chromadb.PersistentClient(path="./cliPersist")
# try catch para evitar duplicados
try:
    coleccion = cliente.create_collection(name="pdf_docs")
except:
    coleccion = cliente.get_collection(name="pdf_docs")
    
# Solo indexar en caso de que este vacio
if len(coleccion.get()["ids"]) == 0:
    
    embebido = modelo.encode(textoSplit)
    
    coleccion.add(
        documents=textoSplit,
        embeddings= embebido.tolist(),
        #Los id tiene que ser Strings
        ids= [str(x) for x in range(len(textoSplit))]
    )

# IMPORTANTE, SE HA IMPLEMENTADO PERO NO SE ESTÁ SEGURO
def pasenContexto(query, k=3):
    query_embedding = modelo.encode([query])
    
    resultados = coleccion.query(
        query_embeddings = query_embedding.tolist(),
        n_results = k
    )
    
    return "\n".join(resultados["documents"][0])
    
    
    
# Con la referencia ya creada hacemos la prueba con mistral
# Necesitamos un bucle para la conversación
def main():
    contexto = pasenContexto()
    conversacion = [
        {
            "role": "system",
            "content": "Eres un bibliotecario experto en todo el contenido del plan lector del \
            centro y podrías recitar cada libro de memoria, si no es algo hacerca del plan lector \
            di 'No lo se'. Atento, aquí viene el primer alumno ..."
        }
    ]
    
    print('-' * 50)
    print("Para salir de la demo escribe 'salir'")
    print('-' * 50)
    while True:
        query = input("[Usted]: ")
        
        if query.lower() == "salir":
            break
        
        contexto = pasenContexto(query)
        
        # Contexto
        conversacion.append({
            "role": "system",
            "content": f"CONTEXTO:\n{contexto}"
        })
        
        # NO guardamos la consulta
        conversacion.append({
            "role": "user",
            "content": query
        })
        
        # El flush obliga a vaciar el buffer para que el texto salga lo más rápido posible
        print("[Bot]: ", end="", flush=True)
        consulta = ollama.chat(
            model = "mistral",
            messages = conversacion,
            stream = True  
        )
        
        respu = ""
        for c in consulta:
            token = c.message.content    
            print(token, end="", flush=True)
            respu += token
        print()
        print("-"*100)
        print()
        
        # Nos guardamos la respuesta
        conversacion.append({
            "role": "assistant",
            "content": respu
        })
        
if __name__ == "__main__":
    main()

