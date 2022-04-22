https://fastapi.stevenkerautret.site/docs

APmovIes est une APi permettant de récupérer les notes et les descriptifs de films depuis les API de imdb, tmdb ainsi que metacritic.

De plus, nous permettons à nos utilisateurs de créer un compte rapidement afin de commenter et noter eux-même leur films.

Ils peuvent donc récupérer les notes de chacun des 3 sites de critiques cités précedemment mais aussi avoir une moyenne des 3 sites.

Puisque nos utilisateurs peuvent voter sur notre API, il nous a semblé interessant qu'ils puissent aussi consulter la note moyenne d'un film depuis notre Base de données (qui est bien sûr moins dense que IMDB etc...).

Les commentaires postés peuvent être supprimés et/ou mis à jour par l'utilisateur.

IMPORTANT : à la création du profil, APmovIes donne une clé API. Il est essentiel de la garder avec soi pour utiliser toutes les fonctionnalités de l'API. C'est votre credential.

Il est aussi possible de récupérer tous ses propres commentaires.

Enfin, il nous a semblé cohérent de proposer un TOP des meilleurs films. Ce TOP peut être paginé et trié en fonction de la date de sortie du film. On peut par exemple décider de voir le top des films sortis depuis mai 1995 ou entre deux dates précises.

Si un utilisateur souhaite quitter définitivement l'API, il peut supprimer son profil.

Tout est utilisable depuis l'interface swagger/fastapi.

Nos tests se trouvent dans test.py

Tout notre code est en python.

L'installation est déployée avec un conteneur docker qui est build automatiquement avec les actions github.

Le conteneur est accessible en ligne à travers Traefik (TLS Cloudflare), et une base de données mariadb est installée.

Des métriques sont disponibles sur grafana. Les données proviennent de prometheus, qui est connecté à cadvisor d'une part pour les infos des conteneurs docker et à node-exporter pour les informations du système hôte.

Merci pour votre attention.

Steven et Damien



## Configuration

un fichier config.ini est à placer dans le dosser config sous la forme:

[mysql]

host = xxxxxxxxx

user = xxxxxxxxx

password = xxxxxxxxxxxxxxx

db = xxxxxxxxxx

[tmdb]

api_key = xxxxxxxxxxxxxxxxxxxxxxxx

