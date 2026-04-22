from flask import Blueprint, Response, request
import ollama
import modelo
import toxic_class
import threading
from .aws_services import send_metric_to_cloudwatch, save_query_to_rds

chat = Blueprint("chat", __name__)
contexto = modelo.Contexto()
toxic = toxic_class.Toxic()

@chat.post("/chat")
def ollamer():
    convers = request.json
    messages = convers["messages"]
    
    query = messages[-1]['content']
    
    # [INYECCIÓN 1]: Registrar métrica de uso (asíncrono)
    threading.Thread(target=send_metric_to_cloudwatch, args=("ChatRequestCount",)).start()

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

        full_response = ""
        for chunk in stream:
            content = chunk['message']['content']
            full_response += content
            yield f"data: {content}\n\n"
            
        # [INYECCIÓN 2]: Guardar historial al finalizar (asíncrono)
        threading.Thread(target=save_query_to_rds, args=(query, full_response)).start()

    return Response(generate(), content_type='text/event-stream')