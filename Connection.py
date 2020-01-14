#!flask/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, Response, jsonify, json
from flask_cors import CORS
import urllib, json
import xml.etree.ElementTree as ET 
from urllib.error import HTTPError

class Connection:

    def __init__(self, url):
        try:
            req = urllib.request.Request(url)
            self.response = urllib.request.urlopen(req)
        except HTTPError as exc:
            content = exc.read()
            raise RuntimeError('Error with the request. Error code: ' + str(content),500)        
        if self.response.status >= 400:
            raise RuntimeError('Error with the request. Error code:' + self.response.status_code, self.response.status_code)


    def get_response(self):
        return self.response
    
    def get_info(self):
        return self.response.info()
    
    def get_type_response(self):
        return self.get_info().get_content_type()
    