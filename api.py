from flask import Flask, send_file, request, redirect

app = Flask(__name__)

@app.get('/favicon.ico')
def nada():
    return 'Aqui no hay nada que ver', 418


@app.post('/recibir/<promp>')
def recibir_promp(promp):
    return f'Promp recibido: {promp} \n Respuesta: No lo se pero hay que despedir a Sebas'

@app.post('/login/')
def login():
    user = request.form.get('user')
    pwd = request.form.get('pwd')

    return f'Logeo recibido: User -> {user}, Password -> {pwd}'

