#!flask/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import xml.etree.ElementTree as ET 
from flask.json import jsonify

class UsuarioXmlToJson:
    
    def __init__(self, xmlDoc):
        self.tree = ET.parse(xmlDoc)
        self.root = self.tree.getroot()
        
    def get_json(self):
        email = self.root[0].text
        id = self.root[1].text
        name = self.root[2].text
        role = self.root[3].text
        jsonList = {'idUsuario':id,'nombre':name,'email':email,'rol':role}
        return json.dumps(jsonList)
            
            