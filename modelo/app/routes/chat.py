from flask import Blueprint, Response, request, jsonify
import ollama
import modelo
import toxic_class
import threading
from .aws_services import send_metric_to_cloudwatch, save_query_to_rds

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
            model="llama3-finetuned:latest",
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

    return Response(generate(), headers={"uuid": id}, content_type='text/event-stream')

@chat.post("/login")
def login():
    user = request.json.get("username")
    pwd = request.json.get("password")
    
    datos = request.json.get("query")
    
    if user == "Hugo" and pwd == "quesadilla":
        return jsonify({
            "success": True,
            "user": {
                "username": user,
                "email": "hugo@ejemplo.com",
                "role": "administrator"
            },
            "tablas": tablas(),
            "telemetria": telemetrias(datos) # Aquí pasas la lista de diccionarios
        }), 200
    
    return jsonify({"success": False, "msg": "Credenciales incorrectas"}), 401

    
def tablas():
    #Esto para que no pete mientras no alla RDS
    return ''

    #Así sería
    tablas = consultas.mostrar_tablas("SHOW TABLES;")
    return tablas

def telemetrias(query):
    if query is not None:
        telem = consultas.mostrar_tablas(f'SELECT * FROM {query}')
    else:
        "Tabla con todos los logs"
        telem = consultas.mostrar_tablas(f'SELECT * FROM Logs')
        
    #Temporal hasta tener datos de verdad
    #Cambiarlo cuando alla RDS
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