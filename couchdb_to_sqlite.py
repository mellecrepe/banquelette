#!/usr/bin/python
#-*- coding: utf-8 -*-

from couchdbkit import *
import sqlite3

# server object
server = Server()

# connexion a la base de donnes account
db = server.create_db('account')

# connexion a la base sqlite
conn = sqlite3.connect('db.sqlite3.account')
cursor = conn.cursor()

# on recupere tous les doc
all_docs = db.all_docs()
i = 2

for d in all_docs :
    id_doc = d['id']
    if id_doc == '_design/all' :
        continue
    if id_doc == '_design/average' :
        continue
    if id_doc == '_design/sum' :
        continue

    # on recupere un document
    doc = db.get(id_doc)
    if doc['category'] == None: 
        doc['category'] = 'autre' 
        doc['subcategory'] = 'autre' 
    if doc['comment'] == None: 
        doc['comment'] = "" 

    data = (i, doc['date'], doc['description'], doc['expense'], doc['category'], doc['bank'], doc['check'], doc['halve'], doc['comment'], doc['subcategory'])

    cursor.execute("""
        INSERT INTO account_account VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)
    i = i + 1

conn.commit()
conn.close()
