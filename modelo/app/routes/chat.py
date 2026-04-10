from flask import Blueprint, Response, request
import ollama
import modelo

chat = Blueprint("chat", __name__)
contexto = modelo.Contexto()


@chat.post("/chat")
def ollamer():
    convers = request.json
    messages = convers["messages"]
    
    query = messages[-1]['content']
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