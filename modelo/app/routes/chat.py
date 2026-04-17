from flask import Blueprint, Response, request, jsonify
import ollama
import modelo
import toxic_class
import json
from datetime import datetime
import logging
import uuid
import os

chat = Blueprint("chat", __name__)
contexto = modelo.Contexto()
#toxic = toxic_class.Toxic()
LOG_FILE = './logs/peticiones.json'


@chat.post("/chat")
def ollamer():
    convers = request.json
    messages = convers["messages"]
    
    id = convers.get('uuid')
    print(id)
    if id is None:
        id = str(uuid.uuid4())
        
    query = messages[-1]['content']
    
    log_entry = {
        "uuid": id,
        "tiempo": datetime.now().strftime("%d/%m/%Y-%H:%M:%S"),
        "query": query
    }


    guardar_log_json(log_entry)
    logging.info(json.dumps(log_entry))
    
    # if(toxic.predict(query)):
    #     return  Response(f"data: Esta pregunta contiene lenguaje ofensivo, por favor abstente de incluir insultos o lenguaje ofensivo \n\n", content_type='text/event-stream')
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

    return Response(generate(), headers={"uuid": id}, content_type='text/event-stream')

@chat.post("/login")
def login():
    user = request.json.get("username")
    pwd = request.json.get("password")

    if user == "Hugo" and pwd == "quesadilla":
        return jsonify({
            "success": True,
            "user": {
                "username": user,
                "email": "hugo@ejemplo.com",
                "role": "administrator"
            },
            "telemetria": telemetrias() # Aquí pasas la lista de diccionarios
        }), 200
    
    return jsonify({"success": False, "msg": "Credenciales incorrectas"}), 401


def telemetrias():
    #Temporal hasta tener datos de verdad
    return [
    {
        "uuid": "asdasdfasdfasefsxcvsdewaed12",
        "tiempo": "16/04/2026-10:00:02",
        "query": "¿Como se hace un git add?"
    },
    {
        "uuid": "b7f3a1c92d4e5f67890123456789abcd",
        "tiempo": "16/04/2026-10:05:14",
        "query": "¿Cómo hacer un commit en git?"
    },
    {
        "uuid": "c8a91e2f3b4d5c6a7e8f901234567890",
        "tiempo": "16/04/2026-10:12:33",
        "query": "¿Qué hace git push?"
    },
    {
        "uuid": "d1234abcd5678ef90123456789abcdef",
        "tiempo": "17/04/2026-10:20:45",
        "query": "¿Cómo crear una rama en git?"
    },
    {
        "uuid": "e9f8a7b6c5d4e3f2109876543210abcd",
        "tiempo": "17/04/2026-10:28:59",
        "query": "¿Cómo cambiar de rama en git?"
    },
    {
        "uuid": "f0e1d2c3b4a5968776655443322110aa",
        "tiempo": "18/04/2026-10:35:21",
        "query": "¿Cómo deshacer cambios en git?"
    }
]

def guardar_log_json(data):
    """Función auxiliar para persistir los logs en un archivo JSON"""
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, IOError):
            logs = []
    
    logs.append(data)
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)