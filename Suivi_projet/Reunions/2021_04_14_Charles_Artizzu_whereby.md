# Réunion
## Objet
Cette réunion a pour objectif de clarifier les doutes et incompréhension de Théo dans l'utilisation de Visual Studio, UE4 et AirSim.
Charles, qui travaille depuis un bout de temps avec ces outils, a accepté de participer à une visio conférence pour apporter son aide.

## Traces
Un **CR écrit** sera produit à l'issu de la réunion. Un **enregistrement audio** pourra aider à la rédaction de ce CR si tous les participants donnent leur accord.

# Sujets
## Visual Studio
Microsoft Visual Studio est un IDE permettant l'édition et l'exécution de code dans un environnement géré.

- Quand un build un projet .sln on compile des _binaries_ qu'il faut déplacer dans notre projet UE4 en tant que plugin. Mais quand on veut exécuter un script via API (ex: DroneShell), on 'démarre le debogage' de 'solutions'. Quelles sont les différences entre les binaries, les solutions ? Comment communiquent-ils ?
	
	Solution = package avec ficihers sources + exécutable ?

	RPC protocol

- Peut-on exécuter un seul projet de solution (ex: HelloDrone) ou c'est forcément une solution entière (AirSim) ? Qu'est-ce qu'il se passe quand on exécute la solution AirSim entière, est-ce que Visual tente d'exécuter chaque projet ?

- Qu'est-ce que cela fait de définir un projet 'en tant que projet de démarrage' ?

- Au début j'ai du installé anaconda car le debugger disait ne pas trouve d'environnement 'Global|Continuum Analytics|...'. J'ai donc créé un environnement global sans y ajouter de package manuellement, et le debugger a pu run la solution. Comment fonctionne la gestion des paquets ? Y a-t-il un environnement local dans AirSim ?

- Au lancement de la solution PythonClient, j'ai des échec de lancement pour cause de fichiers python absents (ex: PythonClient\\computer\_vision\\character\_control.py). Une idée de pourquoi ?
	Si non : juste les lancer à la main.

## UE4
- Dans le cadre d'une manipulation par controller, l'éditeur UE4 (ou sa version NoEditor packagée) sert à la fois de serveur, de client (pour le contrôle) et de sortie vidéo. Correct ?

- Dans le cadre d'une manipulation par API, l'éditeur UE4 (ou sa version NoEditor packagée) sert uniquement de serveur et de sortie vidéo. Correct ?

- L'éditeur UE4 n'a pas tellement vocation à être utilisée pour la manipulation du plugin si ce n'est pour le paramétrage du monde. Correct ?

- J'ai du mal à comprendre la console de l'éditeur. Via le plugin python on peut exécuter des commandes ou fichiers python sous réserve qu'on ai importé les package nécessaires. Mais à quoi correspond la console de base 'cmd', est-ce qu'elle ne sert qu'à exécuter des fonctions liées à l'éditeur, indépendamment du projet ?

- Je voudrais mieux comprendre l'architecturation des assets, pour un arbre donné par ex.
	- Chaque arbre est-il identifiable individuellement ou par groupe ?
	- Peut-on attribuer une texture random à chaque arbre individuel ?

## AirSim
- Bien qu'on ne place dans notre projet UE4 que les binaries issus du build, il reste dans le dépôt les fichiers source et leurs exécutables. Le projet UE4, lorsque joué ('Play'), devient le server et les exécutables (API) deviennent le client. Le client peut envoyer des requêtes au serveur pour commander le drone. Correct ?

- Indépendamment d'où est localisé le dépôt AirSim, un fichier de config .json est initialisé à Documents/airsim/settings.json et permet de preset certains modes comme le mode ComputerVision.

- Les API C++ possèdent un terminal attendant des instructions ce qui est pratique pour une utilisation on-the-fly mais pas les scripts python. Est-ce que néanmoins c'est techniquement possible ?

- Les API C++ ne me permettent pas de faire autre chose que de me déplacer sur z (la hauteur), que je les lance à la main ou via Visual Studio. Une idée de pourquoi ?
