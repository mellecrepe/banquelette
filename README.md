# Banquelette 

## Description 
Banquelette est un outil pour gérer ces comptes.

## Branche couchdb_to_sqlite
Cette branche permet de migrer ces données d'une base de données couchdb vers sqlite.

Voici la procédure a suivre :

1. Assurez-vous que vous être bien dans la branche couchdb_to_sqlite via la commande
	git branch

2. Modifiez votre fichier 'projet/settings.py' en vous inspirant de 'projet/settings.py.template'
	Seules les variables sont personelles 'SECRET_KEY' et 'ALLOWED_HOSTS'

3. Installez le paquet sqlite, sous Debian/Ubuntu
	apt-get install sqlite3

4. Creation de votre base de données via la commande
	python manage.py migrate

5. Migration des données via le script couchdb_to_sqlite.py
	./couchdb_to_sqlite

6. Vous pouvez changee de branche et utilisez le projet avec une base sqlite
