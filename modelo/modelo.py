import archivos_pdf as apf
from sentence_transformers import SentenceTransformer
import chromadb
import ollama


class Contexto:
    
    def __init__(self):
        self.modelo = SentenceTransformer("multi-qa-mpnet-base-cos-v1")
        self.cliente = chromadb.PersistentClient(path="./cliPersist")
        try:
            self.coleccion = self.cliente.create_collection(name="pdf_docs")
        except:
            self.coleccion = self.cliente.get_collection(name="pdf_docs")
            
        self.setColeccion()
    
    def setColeccion(self):
        textos = apf.tratar_pdf()

        textos_planos = [t for sublista in textos for t in sublista]

        if len(self.coleccion.get()["ids"]) == 0:

            embeddings = self.modelo.encode(textos_planos)
            
            for i, texto in enumerate(textos_planos):
                self.coleccion.add(
                    documents=[texto],
                    embeddings=[embeddings[i].tolist()], 
                    ids=[str(i)] 
                )

    def pasenContexto(self, query, k=3):
        query_embedding = self.modelo.encode([query])
        
        resultados = self.coleccion.query(
            query_embeddings = query_embedding.tolist(),
            n_results = k
        )
        
        return "\n".join(resultados["documents"][0])



# class chatBot():
    
#     def __init__(self):
#         self.contexto_modelo = Contexto()
        
#         self.conversacion = [
#             {
#                 "role": "system",
#                 "content": "Eres un bibliotecario experto en todo el contenido del plan lector del \
#                 centro y podrías recitar cada libro de memoria, si no es algo hacerca del plan lector \
#                 di 'No lo se'. Atento, aquí viene el primer alumno ..."
#             }
#         ]
         
#     def consulta(self, query):
#         conseguir_query = query[-1]['content']
#         contexto = self.contexto_modelo.pasenContexto(conseguir_query)
        
#         # Contexto
#         self.conversacion.append({
#             "role": "system",
#             "content": f"CONTEXTO:\n{contexto}"
#         })
        
#         self.conversacion.append({
#             "role": "user",
#             "content": query
#         })
        
#         consulta = ollama.chat(
#             model = "mistral",
#             messages = self.conversacion,
#             stream = True  
#         )
        
#         respu = ""
#         for c in consulta:
#             token = c.message.content
#             respu += token
        
#         # Nos guardamos la respuesta
#         self.conversacion.append({
#             "role": "assistant",
#             "content": respu
#         })
        
#         return self.conversacion