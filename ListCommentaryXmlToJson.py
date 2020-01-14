#!flask/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import xml.etree.ElementTree as ET
from flask.json import jsonify

class ListCommentaryXmlToJson:


    def __init__(self, xmlDoc):
        self.tree = ET.parse(xmlDoc)
        self.root = self.tree.getroot()

    def get_json(self):
        jsonList = list()
        for child in self.root:
            jsonList.append({'contenido':child[0].text
                             ,'fechaCreacion':child[1].text
                             ,'idComentario':child[2].text})
        return json.dumps(jsonList)
