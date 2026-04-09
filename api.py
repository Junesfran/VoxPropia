from flask import Flask, send_file, request, redirect
import modelo

app = Flask(__name__)
chatbot = modelo.chatBot()

@app.get('/favicon.ico')
def nada():
    return 'Aqui no hay nada que ver', 418


@app.post('/recibir/<promp>')
def recibir_promp(promp):
    respuesta = chatbot.consulta(query= promp)

    return respuesta

@app.post('/login/')
def login():
    user = request.form.get('user')
    pwd = request.form.get('pwd')

    return f'Logeo recibido: User -> {user}, Password -> {pwd}'

