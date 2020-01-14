#!flask/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import xml.etree.ElementTree as ET 
from flask.json import jsonify

class ListUsuarioXmlToJson:
    
    def __init__(self, xmlDoc):
        self.tree = ET.parse(xmlDoc)
        self.root = self.tree.getroot()
        
    def get_json(self):
        jsonList = list()
        for child in self.root:
            email = child[0].text
            id = child[1].text
            name = child[2].text
            role = child[3].text
            jsonList.append({'idUsuario':id,'nombre':name,'email':email,'rol':role})
        return json.dumps(jsonList)
            
            