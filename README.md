# Banquelette 

## Description 
Banquelette est un outil pour gérer ces comptes.

## Lancement via Docker
Banquelette est packagée pour Docker. Vous pouvez directement télécharger une
image Docker fonctionnelle ou construire vous-même votre image (si vous
souhaitez être certain d'avoir les tous derniers commits, par exemple).

Des variables d'environnement principales peut être définies au moment de lancer
l'image:

- ***SECRET_KEY*** est la clef secrète Django. Si vous ne la définissez pas
  elle sera générée aléatoirement ;
- ***VIRTUAL_HOST*** est le virtual host par le quel on accède à banquelette. Par défaut, localhost est autorisé.

### Image docker préconstruite

L'image à télécharger sur le Docker Hub est
[mellecrepe/banquelette](https://hub.docker.com/r/mellecrepe/banquelette).

```
	docker pull mellecrepe/banquelette

	docker run \
		--name banquelette \
		-e "SECRET_KEY=12345678abcdef" \
		-e "VIRTUAL_HOST=banquelette.test.com" \
		-p 8000:8000
		-v /path/ou/stocker/db/sur/host:/home/banquelette/config
		mellecrepe/banquelette
```
Deux fichiers de configuration : settings.py et categories.yaml peuvent être
personnaliser. Il suffit de les placer dans le dossier de volume 
'/path/ou/stocker/db/sur/host' sur votre host.


### Construire votre image Docker

Tous les fichiers nécessaires sont déjà présents dans le repo git, qu'il va
vous falloir cloner.

```
	git clone https://github.com/mellecrepe/banquelette.git

	cd banquelette

	docker build -t test/banquelette .

	docker run \
		--name banquelette \
		-e "SECRET_KEY=12345678abcdef" \
		-e "VIRTUAL_HOST=banquelette.test.com" \
		-p 8000:8000
		-v /path/ou/stocker/db/sur/host:/home/banquelette/config
		test/banquelette
```

## Lancement manuel
### Installation 
Paquets à installer : *python3.5*, *django*, *sqlite*"
Par exemple, sous debian/ubuntu :
```
	apt-get install python3-django sqlite
```

NOTE: Banquelette a été testé avec django v1.10. Vous pouvez vérifier la
version de django grâce à cette commande :
```
	django-admin --version
```

### Configuration
#### Configuration du schema de la base de données
Django crée lui-même la base de données et les modifications de schéma.
Afin d'appliquer les modifications de schéma, exécutez cette commande
```
        python manage.py migrate
```


#### configuration de l'application banquelette
Il existe trois fichiers de configuration :

- *projet/settings.py*  définit les paramètres génériques, notamment la clef
  secrète Django et la connexion à CouchDB ;
- *account/settings.py* definit les parametres liés aux banques ;
- *account/categories.yaml* permet d'automatiser la modification de certains
  descriptifs ou de definir à quel categorie appartient la depense.
 

