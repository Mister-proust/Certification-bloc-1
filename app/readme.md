Pour lancer l'application, veuillez écrire dans le terminal la commande suivante dans le dossier app : uvicorn main:app --reload 

Le dossier app va contenir les routes utilisées pour le projet.

Dans le dossier Database, vous pourrez retrouver les fonctions qui vont appelés la Database Postgres ainsi que le fichier permettant de faire la connexion avec la base de données. Vous retrouverez également un dossier SQL qui correspond aux requêtes SQL utilisées dans les fonctions. 

Dans le dossier services, vous retrouverez le module permettant l'authentification, la connexion aux templates ainsi que le fichier permettant la connexion à la base mongoDB. 

Dans le dossier static, vous retrouverez le CSS ainsi que la carte de France. 

Dans le dossier templates, vous retrouverez les fichiers HTML permettant un affichage graphique de l'application. 