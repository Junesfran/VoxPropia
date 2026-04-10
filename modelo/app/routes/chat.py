from flask import Blueprint, Response, request
import ollama
import modelo
import toxic_class

chat = Blueprint("chat", __name__)
contexto = modelo.Contexto()
toxic = toxic_class.Toxic()

@chat.post("/chat")
def ollamer():
    convers = request.json
    messages = convers["messages"]
    
    query = messages[-1]['content']
    if(toxic.predict(query)):
        return  Response(f"data: Esta pregunta contiene lenguaje ofensivo, por favor abstente de incluir insultos o lenguaje ofensivo \n\n", content_type='text/event-stream')
    contx = contexto.pasenContexto(query=query)
    
    def generate():
        context = {
            "role": "system",
            "content": f"CONTEXTO:\n{contx}"
        }
        
        stream = ollama.chat(
            model="mistral:7b",
            messages=[context, *messages],
            stream=True,
            think=None
        )

        for chunk in stream:
            content = chunk['message']['content']
            yield f"data: {content}\n\n"

    return Response(generate(), content_type='text/event-stream')