#!flask/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request, session
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

#url_client = "http://127.0.0.1:5000"
url_client = "https://iwebfinal.appspot.com"

@app.route('/') #, methods=['GET', 'POST'])
def home():
    try:
        url = url_client + "/IWeb/webresources/entity.usuario/0"
        response = Connection(url)
        usuario = response.get_response().read()
        session['usuario'] = usuario

        url_weather = url_client + "/IWeb/weather/"
        response_weather = Connection(url_weather)
        data_weather = json.loads(response_weather.get_response().read())
        #print(data_weather)

    except RuntimeError as exc:
        mensaje, codigo = exc.args
        return render_template("error.html", mensaje=mensaje, codigo=codigo)
    return render_template('index.html',logUser=json.loads(usuario),weather=data_weather)

@app.route('/home/') #, methods=['GET', 'POST'])
def home_home():
    usuario = session['usuario']
    return render_template('index.html',logUser=json.loads(usuario))


@app.route('/email', methods=['GET', 'POST'])
def home_email():
    email = "Guest"
    if request.method == 'POST':
        response = request.form
        email = response['email']
        try:
            url = url_client + "/IWeb/webresources/entity.usuario/email/" + str("\""+ email + "\"")
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
        session['usuario'] = usuario
    return render_template('index.html',logUser=json.loads(usuario))


@app.route("/profile/")
def profile():
    comentarioList = list()
    if 'usuario' in session:
        usuario = session['usuario']
        userId = json.loads(usuario)
        try:
            url = url_client + "/IWeb/webresources/entity.comentario/email/" + str("\""+ userId['email'] + "\"")
            print("La url es : " + url)
            response = Connection(url)
            print("Response: " + str(response))
            if response.get_type_response() == "application/xml":
                xmlToJson = ListCommentaryXmlToJson(response.get_response())
                comentarioList = xmlToJson.get_json()
            elif response.get_type_response() == "application/json":
                comentarioList = response.get_response().read()
            print("Cantidad de comentarios: " + str(len(comentarioList)))
            url = url_client + "/IWeb/webresources/entity.comentario/count/" + str(userId['idUsuario'])
            response = Connection(url)
            quantity = response.get_response().read()
            comentarios = json.loads(quantity)['total']
            print(comentarios)
            if comentarios == 0:
                    url = url_client + "/IWeb/webresources/entity.comentario/0"
                    response = Connection(url)
                    comentarioList = response.get_response().read()
        except RuntimeError as exc:
            mensaje, codigo = exc.args
            print(mensaje)
            print(codigo)
            return render_template("error.html", mensaje=mensaje, codigo=codigo)

    return render_template("profile.html",logUser=json.loads(usuario), comentarios=json.loads(comentarioList))


@app.route("/signup/", methods=['GET','POST'])
def signup():
    if 'usuario' in session:
        usuario = session['usuario']
    return render_template("signup.html",logUser=json.loads(usuario))



@app.route('/bicilane/') #, methods=['GET', 'POST'])
def lane():
    try:
        response = Connection(url_client + '/opendata/api/bicilane/point')
    except RuntimeError as exc:
            mensaje, codigo = exc.args
            print(mensaje)
            print(codigo)
            return render_template("error.html", mensaje=mensaje, codigo=codigo)
    lane = response.get_response().read()
    if 'usuario' in session:
        usuario = session['usuario']
    return render_template('lane.html',lista=json.loads(lane),logUser=json.loads(usuario))  #, usuarios=json.loads(usuarios))

@app.route('/bicilane/lane/<int:id>') #, methods=['GET', 'POST'])
def find_lane_by_id(id):
    try:
        url = url_client + '/opendata/api/bicilane/find_by_ogc_fid/' + str(id)
        response = Connection(url)
        lane = response.get_response().read()
        url2 = url_client + '/opendata/api/bicilane/get_list_coordinates/' + str(id+1)
        response = Connection(url2)
        coordinates = response.get_response().read()
        url3 = url_client + '/opendata/api/bicilane/get_description/' + str(id+1)
        response = Connection(url3)
        description = response.get_response().read()
    except RuntimeError as exc:
            mensaje, codigo = exc.args
            print(mensaje)
            print(codigo)
            return render_template("error.html", mensaje=mensaje, codigo=codigo)
    if 'usuario' in session:
        usuario = session['usuario']
    return render_template('detail_lane.html',bicilane=json.loads(lane),coordinates=json.loads(coordinates),description=json.loads(description),logUser=json.loads(usuario))


# Aparcamientos de bici


@app.route('/bicipark/') #, methods=['GET', 'POST'])
def parking():
    try:
        response = Connection(url_client + '/opendata/api/bicipark')
    except RuntimeError as exc:
            mensaje, codigo = exc.args
            print(mensaje)
            print(codigo)
            return render_template("error.html", mensaje=mensaje, codigo=codigo)
    parking = response.get_response().read()

    if 'usuario' in session:
        usuario = session['usuario']
    return render_template('parking.html',lista=json.loads(parking),logUser=json.loads(usuario))

@app.route('/bicipark/parking/<int:id>') #, methods=['GET', 'POST'])
def find_parking_by_id(id):
    if 'usuario' in session:
        usuario = session['usuario']

    url = url_client + '/opendata/api/bicipark/find_by_ogc_fid/' + str(id)
    try:
        response = Connection(url)
    except RuntimeError as exc:
            mensaje, codigo = exc.args
            print(mensaje)
            print(codigo)
            return render_template("error.html", mensaje=mensaje, codigo=codigo)
    parking = response.get_response().read()
    return render_template('detail_parking.html',biciparking=json.loads(parking),logUser=json.loads(usuario))



if __name__ == '__main__':
    #app.run(debug=True, host='127.0.0.1', port=5001)
    app.run()
