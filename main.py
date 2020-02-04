#!flask/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request, session
from flask_cors import CORS
import secrets
import requests
import json
import unicodedata
from Connection import Connection
import xml.etree.ElementTree as ET
from ListUsuarioXmlToJson import ListUsuarioXmlToJson
from UsuarioXmlToJson import UsuarioXmlToJson
from ListCommentaryXmlToJson import ListCommentaryXmlToJson

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

url_server = "http://127.0.0.1:5000"
#url_server = "https://iwebfinal.appspot.com"
url_cliente = "http://127.0.0.1:5001"
#url_cliente = "https://iwebcliente.appspot.com"

title_html = '<title>Bikes in Málaga</title>'
menu_home = '<a class="brand" href="{{url_client}}/home/">Home</a>'



@app.route('/test')
def test():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        language = request.form.get('language')
        framework = request.form['framework']

        return '''<h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    return '''<form method="POST">
                  Language: <input type="text" name="language"><br>
                  Framework: <input type="text" name="framework"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''


@app.route('/') #, methods=['GET', 'POST'])
def home():
    try:
        url = url_server + "/IWeb/webresources/entity.usuario/0"
        response = Connection(url)
        usuario_session = response.get_response().read()
        usuario_json = json.loads(usuario_session)
        usuario = {'idUsuario': usuario_json['idUsuario'],
                    'nombre': usuario_json['nombre'],
                    'email': usuario_json['email'],
                    'rol': usuario_json['rol']}
        session['usuario'] = usuario
        print(usuario)

        #url_weather = url_server + "/IWeb/weather/"
        #response_weather = Connection(url_weather)
        #data_weather = json.loads(response_weather.get_response().read())
        #print(data_weather)

    except RuntimeError as exc:
        mensaje, codigo = exc.args
        return render_template("error.html", mensaje=mensaje, codigo=codigo)
    return render_template('index.html',logUser=usuario,url_client=url_cliente)#,weather=data_weather)

@app.route('/home/') #, methods=['GET', 'POST'])
def home_home():
    usuario = session['usuario']
    return render_template('index.html',logUser=usuario,url_client=url_cliente)


@app.route('/email', methods=['GET', 'POST'])
def home_email():
    email = "Guest"
    if request.method == 'POST':
        response = request.form
        email = response['email']
        try:
            url = url_server + "/IWeb/webresources/entity.usuario/email/" + str("\""+ email + "\"")
            print(url)
            response = Connection(url)
            #if response.get_type_response() == "application/xml":
            #    xmlToJson = UsuarioXmlToJson(response.get_response())
            #    usuario = xmlToJson.get_json()
            #elif response.get_type_response() == "application/json":
            usuario = response.get_response().read()
        except RuntimeError as exc:
            mensaje, codigo = exc.args
            print(mensaje)
            print(codigo)
            return render_template("error.html", mensaje=mensaje, codigo=codigo)
        usuario_json = json.loads(usuario)
        usuario_session = {'idUsuario': usuario_json['idUsuario'],
                    'nombre': usuario_json['nombre'],
                    'email': usuario_json['email'],
                    'rol': usuario_json['rol']}
        print(usuario_session)
        session['usuario'] = usuario_session
    return render_template('index.html',logUser=usuario_session,url_client=url_cliente)


@app.route("/profile/")
def profile():
    comentarioList = list()
    if 'usuario' not in session:
        try:
            url = url_server + "/IWeb/webresources/entity.usuario/0"
            response = Connection(url)
            usuario = response.get_response().read()
            usuario_json = json.loads(usuario)
            usuario_session = {'idUsuario': usuario_json['idUsuario'],
                        'nombre': usuario_json['nombre'],
                        'email': usuario_json['email'],
                        'rol': usuario_json['rol']}
            print(usuario_session)
            session['usuario'] = usuario_session
        except RuntimeError as exc:
            mensaje, codigo = exc.args
            return render_template("error.html", mensaje=mensaje, codigo=codigo)

    if 'usuario' in session:
        usuario = session['usuario']
        print(usuario)
        userId = usuario

        try:
            url = url_server + "/IWeb/webresources/entity.comentario/email/" + str("\""+ userId['email'] + "\"")
            print("La url es : " + url)
            response = Connection(url)

            print("Response: " + str(response))
            if response.get_type_response() == "application/xml":
                xmlToJson = ListCommentaryXmlToJson(response.get_response())
                comentarioList = xmlToJson.get_json()
            elif response.get_type_response() == "application/json":
                comentarioList = response.get_response().read()
            print("Cantidad de comentarios: " + str(len(comentarioList)))
            url = url_server + "/IWeb/webresources/entity.comentario/count/" + str(userId['idUsuario'])
            response = Connection(url)
            quantity = response.get_response().read()
            comentarios = json.loads(quantity)['total']
            print(comentarios)
            if comentarios == 0:
                    url = url_server + "/IWeb/webresources/entity.comentario/0"
                    response = Connection(url)
                    comentarioList = response.get_response().read()

            try:
                url = url_server + "/IWeb/webresources/entity.usuario/photo/" + str(userId['idUsuario'])
                response = Connection(url)
                photo = bytearray.fromhex(json.loads(response.get_response().read())['photo'])
                print('El tipo de photo es : ' + str(type(photo)))
            except RuntimeError as exc:
                mensaje, codigo = exc.args
                return render_template("error.html", mensaje=mensaje, codigo=codigo)


        except RuntimeError as exc:
            mensaje, codigo = exc.args
            print(mensaje)
            print(codigo)
            return render_template("error.html", mensaje=mensaje, codigo=codigo)
    return render_template("profile.html",logUser=usuario, comentarios=json.loads(comentarioList),url_client=url_cliente,url_server=url_server,photo=photo.hex())


@app.route("/signup/", methods=['GET','POST'])
def signup():
    if 'usuario' in session:
        usuario = session['usuario']
    return render_template("signup.html",logUser=usuario,url_client=url_cliente, url_server=url_server)

@app.route("/signup2/", methods=['GET','POST'])
def signup2():
    if 'usuario' in session:
        usuario = session['usuario']
    return render_template("signup2.html",logUser=usuario,url_client=url_cliente, url_server=url_server)



@app.route('/bicilane/') #, methods=['GET', 'POST'])
def lane():

    try:
        response = Connection(url_server + '/opendata/api/bicilane/point')
    except RuntimeError as exc:
            mensaje, codigo = exc.args
            print(mensaje)
            print(codigo)
            return render_template("error.html", mensaje=mensaje, codigo=codigo)
    lane = response.get_response().read()
    if 'usuario' in session:
        usuario = session['usuario']
    return render_template('lane.html',lista=json.loads(lane),logUser=usuario,url_client=url_cliente)

@app.route('/bicilane/lane/<int:id>') #, methods=['GET', 'POST'])
def find_lane_by_id(id):
    try:
        url = url_server + '/opendata/api/bicilane/find_by_ogc_fid/' + str(id)
        response = Connection(url)
        lane = response.get_response().read()
        url2 = url_server + '/opendata/api/bicilane/get_list_coordinates/' + str(id+1)
        response = Connection(url2)
        coordinates = response.get_response().read()
        url3 = url_server + '/opendata/api/bicilane/get_description/' + str(id+1)
        response = Connection(url3)
        description = response.get_response().read()
    except RuntimeError as exc:
            mensaje, codigo = exc.args
            print(mensaje)
            print(codigo)
            return render_template("error.html", mensaje=mensaje, codigo=codigo)
    if 'usuario' in session:
        usuario = session['usuario']
    return render_template('detail_lane.html',bicilane=json.loads(lane),coordinates=json.loads(coordinates),description=json.loads(description),logUser=usuario,url_client=url_cliente)


# Aparcamientos de bici


@app.route('/bicipark/') #, methods=['GET', 'POST'])
def parking():
    try:
        response = Connection(url_server + '/opendata/api/bicipark')
    except RuntimeError as exc:
            mensaje, codigo = exc.args
            print(mensaje)
            print(codigo)
            return render_template("error.html", mensaje=mensaje, codigo=codigo)
    parking = response.get_response().read()

    if 'usuario' in session:
        usuario = session['usuario']
    return render_template('parking.html',lista=json.loads(parking),logUser=usuario,url_client=url_cliente)

@app.route('/bicipark/parking/<int:id>') #, methods=['GET', 'POST'])
def find_parking_by_id(id):
    if 'usuario' in session:
        usuario = session['usuario']

    url = url_server + '/opendata/api/bicipark/find_by_ogc_fid/' + str(id)
    try:
        response = Connection(url)
    except RuntimeError as exc:
            mensaje, codigo = exc.args
            print(mensaje)
            print(codigo)
            return render_template("error.html", mensaje=mensaje, codigo=codigo)
    parking = response.get_response().read()
    return render_template('detail_parking.html',biciparking=json.loads(parking),logUser=usuario,url_client=url_cliente)



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
