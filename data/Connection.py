#!flask/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, Response, jsonify, json
from flask_cors import CORS
import urllib, json
import xml.etree.ElementTree as ET 

class Connection:

    def __init__(self, url):
        self.response = urllib.request.urlopen(url)
        if self.response.status >= 400:
            raise RuntimeError('Error with the request. Error code:' + self.response.status_code, self.response.status_code)


    def get_response(self):
        return self.response
    
    def get_info(self):
        return self.response.info()
    
    def get_type_response(self):
        return self.get_info().get_content_type()
    