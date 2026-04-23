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
            model="qwen3b:latest",
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


        param=(query,id)
        consultas.insertar_datos(param)
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
            "telemetria": telemetrias(datos) # Aquí pasas la lista de diccionarios
        }), 200
    
    return jsonify({"success": False, "msg": "Credenciales incorrectas"}), 401


def telemetrias(query):
    if query == 1:
        telem = consultas.mostrar_tablas(f'SELECT COUNT(*) FROM chat_history GROUP BY created_at')
    else:
        telem = consultas.mostrar_tablas(f'SELECT * FROM chat_history')
    
    return telem


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
