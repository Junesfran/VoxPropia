from flask import Blueprint, Response, request, jsonify
import ollama
import modelo
import toxic_class

chat = Blueprint("chat", __name__)
contexto = modelo.Contexto()
#toxic = toxic_class.Toxic()

@chat.post("/chat")
def ollamer():
    convers = request.json
    messages = convers["messages"]
    
    query = messages[-1]['content']
    # if(toxic.predict(query)):
    #     return  Response(f"data: Esta pregunta contiene lenguaje ofensivo, por favor abstente de incluir insultos o lenguaje ofensivo \n\n", content_type='text/event-stream')
    contx = contexto.pasenContexto(query=query)
    print(contx)
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
