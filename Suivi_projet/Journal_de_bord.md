# Semaine 1
## Lundi 01/03
- Présentation des locaux et de l'équipe, réu de lancement, prise en main des ressources informatiques, installations. Dual boot et customization OK.
- Installation UE4 : Sous linux fail car need 100+Go pour la compilaton et la partition home n'a pas été crée à côté de l'espace windows donc flemme de réinstaller linux -> UE4 sous windows (installé à partir de la session mis)
	- La machine sur laquelle je me suis installé ne possède pas de GPU : les ressources du PC sont très limitées quand il est lancé et il y a sans arrêts des crashs de UE4. -> Solutions : l'installer sur pc portable (non), l'installer sur pc fixe mais il faudra le faire venir + attendre le bureau, utiliser une machine avec GPU, quitte à prendre un MAC, voir si on peut le faire travailler sur matrix (à mon avis non)
- Recherche d'articles
- Recherche de tuto UE4

## Mardi 02/03
- Récupération du dépôt Git + prise de contact avec Dao
- Recherche d'ordinateur avec GPU + prise de contact avec Christophe poix
- Exploration du Git
- Construction d'une RoadMap du travail établi
- Recherche d'articles
- Absence aprem car installation internet

## Mercredi 03/03
- Recherche de solutions GPU avec Christophe
- Complétion de la RoadMap du travail établi
- Refonte du README à la racine
- Recherche d'articles / datasets / pistes
- Récupération des modèles

## Jeudi 04/03
- Installation de l'environnement virtuel et des outils de développement
- Point avec Pascal
- Reprise du code

## Vendredi 05/03
- Reprise du code : pb rencontrés
	- Communication avec Dao pour la reprise et correction des certaines choses
- Confirmation que le DenseNet brut fonctionne (sans suprise car reprise du git officiel)
	
# Semaine 2
## Lundi 08/03
- Réunion hebdomadaire
- Reprise du code avec mises à jour Dao
	- DenseDepth : fonctionne mais sensible à la luminosité forte qui peut tromper l'estimation de profondeur. Inquiétant pour la vraie vie.
	- AdapNet : marche mais je n'arrive pas à changer le dossier d'input d'images
- Installation du nouveau GPU : Quadro M6000
	- Pb Epic Games Launcher -> crash par memory leak (sur le PC GPU + le Dell all-in-one)
	
## Mardi 09/03
- Tentative de debuggage du launcher Epic Games (Epic fail)
- Run de seg. sem et depth map sur images réelles
	- Documentation sur les TFRecords
	
## Mercredi 10/03
- Amélioration du script de test d'AdapNet
- Création d'un script de redimensionnement d'images dans un dossier

## Jeudi 11/03
- Création script reshape img from file/folder

## Vendredi 12/03
- Paufinage script reshape
- MàJ du README
- MàJ config linters & testers
- MàJ rapport de stage

# Semaine 3
## Lundi 15/03
- Réunion avec Pascal
- Nettoyage des fichiers AdapNet
- Bataille avec le fonctionnement des modules python
- Problème constaté avec le VPN : impossible d'accéder à des ressources extérieures en fonction de la co
	- Discussion par mail en cours

## Mardi 16/03
- Nettoyage des fichiers AdapNet
- Résolution du problème VPN
- Configuration du planning

## Mercredi 17/03
- Nettoyage des fichiers AdapNet
- Tentatives de résolution du problème GPU
	- 'Réparation' au niveau bios pour le boot.
	- A faire : tenter UE4 sous linux
- Tentatives nouveaux entraînements -> problèmes
	- Prise de contact avec Dao
	
## Jeudi 18/03
- Nettoyage des fichiers AdapNet
- Reprise en profondeur du code dans AdapNet/
- Nettoyage des fichiers Clustering
- Test de gabor.py
- Installation complète d'UE4 sur Ubuntu : OK

## Vendredi 19/03
- Annonce confinement : absence la matinée
- Aprem : 
	- Mise en place de l'accès à distance du poste avec GPU contenant UE4 + accès graphique sur le poste de dev + accès direct via clefs ssh
	- Corrections AdapNet suite à la réponse de Dao
	
# Semaine 4
## Lundi 22/03
- Ajout code et ressources suite à update du git après la réponse de Dao : de nouvelles images (les anciennes dans TrainImages/SS n'étaient pas des labels mais des masques pour la visualisation), du nouveau code pour générer les bons datasets et leurs labels via UnrealCV.
- Tentative installation unrealcv -> bugs
	- Tentative correction manuelle dans code C++ mais échec, projet très gros
- Installation UE4 sur pc fixe perso (lent car pas encore de cable ethernet pour relier à livebox)
- Documentation UE4 & unrealcv

## Mardi 23/03
- Réunion Pascal
- Fixed installation unrealcv en plugin sous UE4 (aucune des branche de build correctement, sur recommandation de Dao j'ai pris les version déjà compilées dans les releases). /!\ Peut-etre d'autres pb de compatibilité avec UE4, à voir inside IDE /!\
	- UnrealCV n'est pas loadé dans UE4 car pb de version (destiné à UE4.16), dit de compiler dans l'IDE mais crash après (?)
- Ré-entrainement à neuf en restaurant le modèle pré-entrainé AdapNet :
	- ré-entrainé avec le ficheir train.py de Dao (y a des formes qui approchent les arbres mais y a encore cet aspect 'points'). En attente du miens 'clean' pour comparer
- Basculement de l'environnement de travail sur le psote à GPU car plus possible d'attendre des années sur le all-in-one. Prend un temps monstrueux à ré-installer conda, aucune idée de pourquoi. En attente.
	- evaluate.py 'clean' confirmé bien marcher comme celui de Dao.

## Mercredi 24/03
- Ré-installation UE4.16 sur fixe appart
- Tentative résolution problème de compatibilité de version unrealcv/UE4.26 sur poste GPU. Si échec -> ré-installation 4.16
- Quelques résultats plus intéressants avec entrainement, attente confirmation Dao + basculement environnement de travail sur poste GPU pour lancer des entraînement plus conséquents
- Basculement de l'environnement de travail sur le poste GPU
	- 1 journée entière + soirée pour faire marcher tensorflow sur le GPU (entre la bonne version de CUDA pour tensorflow-gpu 1.14.0, la création d'un compte pour cuDNN, **le parametrage de gpu_id dans les fichier a passer à 0 (pour set os.environ['CUDA_VISIBLE_DEVICES'] à 0 car single-GPU set)**, la résolution de conflit de versions...
	
## Jeudi 25/03
- Finition transfert environnement de travail :
	- finition paramétrage accès à distance poste GPU au niveau du boot et de la sessions
	- wipe Ubuntu du poste all-in-one.
	- Déménagement du poste dans le coin
- Lecture d'articles

## Vendredi 26/03
- Réunion Pascal
- Lecture d'articles

# Semaine 5
## Lundi 29/03
- Lecture d'articles
- Tentatives de fix Epic Games sur poste GPU
	- Succès : install avant màj du launcher
## Mardi 30/03

- Lecture d'articles
- Recherches config stéréo UE4
	- En fait pas possible nativement, quelques plugins ont l'air d'exister mais pas très connus. 
	- A voir si ce n'est pas plus facile de faire parcourir un chemin à la caméra 2 fois avec des offsets définis
- Entraînement utilisation unrealcv sous UE4 :
	- Pas de GUI, que commande et la plupart crash... peut etre des configs manquantes
- Contact Dao car lien de téléchargement environnement UE4 mort
- Récupération ressources article depth stéréo 360

## Mercredi 31/03
- Tests du code article depth stéréo 360
- Relance Dao
- Réunion Pascal

## Jeudi 01/04
- Récupération environnements :
	- [x] Dao
	- [ ] Guillaume Allibert -> impossible
- Chargement environnements :
	- [ ] Dao
	- [ ] Guillaume Allibert
	
## Vendredi 02/04
- UE4
	- Pas de problème si pas de connexion internet, mais dès qu'on la (re)met : RAM overflow.
	- Fonctionne correctement sous VirtualBox - Win10
- Tentative de résolution bug launcher epic games pour récupérer environnement Guillaume
- Rapport + Récupération info labo auprès de David

# Semaine 6
## Lundi 05/04
- Férié

## Mardi
- Problème majeur sur les distributions à cause d'une mauvaise manipulation des partitions sur Windows : perte d'une grosse demi-journée
- Recherche sur les techniques de synchronisation de caméra
- Import de l'environnement de Dao : viewport complètement noir
- Rapport

## Mercredi 07/04
- Récupération et chargement environnement de Guillaume Allibert sur le fixe à l'appart
- Engagement via Christophe avec les respo réseau pour débloquer l'Epic Games launcher au labo
	- Résolu : désactivation de la détection automatique de sparamètres de proxy auto dans windows...
	- Ré-installation des UE4 16 et 26
- **News sur les présentations : possibilité de tenir un séminaire en mai/juin sur le travail réalisé**
- Séminaire demain jeudi 08/04 9h30 sur la vision (cf. mails)
- Mise en place accès à distance windows
- Recherche sur les techniques de synchronisation de caméra

## Jeudi 08/04
- Séminaire Yufan Kang (University of Tokyo)
- Installation AirSim

## Vendredi 09/04
- Réunion Pascal
- Installation et prise en main du plugin AirSim
	- Tutorials
	- Génération directe d'images equirectangulaires impossible
	- Contrôle du drone impossible au clavier : need une manette compatible suivant cette [liste](https://github.com/Microsoft/AirSim/blob/master/docs/remote_control.md)
	
# Semaine 7
## Lundi 12/04
- AirSim :
	- Tentative de faire fonctionner les API pour prendre des screenshots stereo : échec, dans l'attente de la réponse de Charles Artizzu pour un call Zoom
	- Problème de compréhension de Visual Studio + gestion environnements python sous windows
	- Manque de tutoriels vidéos en ligne

## Mardi 13/04
- Contact Guillaume et Dao. Réunion Guillaume demain 14h + préparation visio
- Airsim :
	- Manipulations et apprentissage.
	- Premières sorties d'image par API
	- 1ère demande s'il y a des manettes ou des télécommandes dans le labo pour controller le drone qui ne peut pas être dirigé au clavier. Peut etre intéressant pour prendre des images perspectives mais pas forcément pour de la stéréo
	- Les APIs sont parfois buggées avec des issues très récentes (ex: les types python non reconnus dans PythonClient/airsim/types.py qu'il faut remplacer par leur int correspondant pour le moment)
	- Peut-être problème avec la seg. sem. si on n'arrive pas à attribuer une couleur différente à chaque arbre individuellement car ce n'est pas le cas par défaut. D'où l'intérêt de garder la solution de Dao sous le coude.
	
- Environnement Dao :
	- Confirmation de corruption de sauvegarde ou en tout cas d'un problème, d'où la prise de contact
	
## Mercredi 14/04
- Réunion Pascal matin + Charles aprem
- Expérimentations UE4 + AirSim
- Rédaction CR

## Jeudi 15/04
- Expérimentations UE4 + AirSim
- Expérimentation environnement Dao
- Expérimentations plugin stereo 360 intégré à UE4

## Vendredi 16/04
- Expérimentations avec sorties du plugin stereo 360 intégré à UE4 utilisées dans 360SD Net
	- Précision en environnement forestier très moyen voire mauvais. Mais il n'y avait pas de différence entre les images top et bot. Donc j'ai ré-essayé avec de la vraie stereo top/bot de foret trouvé sur internet, et ce n'était pas tellement mieux. => voir avec Charles si ce serait pertinent qu'il partage ses scripts perspective -> cubemap -> spherique -> equirectangulaire
- Rapport

# Semaine 8
## Lundi 19/04
- Réunion Pascal
	- Voir avec Charles pour récupérer au moins ses données d'images equirectangulaire UE4, au mieux son code en plus
	- Comprendre avec certitude ce que caractérise l'entrée 'polar angle' du 360SD-Net
	- Idem pour le Learnable Cost Volume
	- Si besoin pour 360SD-Net, demander accès aux données du papier via leur formulaire en ligne
- Contact Charles pour échange de code et données
- Rapport
- Ré-entraînement modèle Dao sur sa base d'app

## Mardi 20/04
- AdapNetpp
	- Adressage des warnings d'apprentissage et test : tous n'ont pas pu être suprimés mais une bonne partie
	- Correction de l'id GPU dans les fichiers .config. Attention à l'avenir à bien mettre 0
- Investigation en profondeur de l'article
- Rapport

## Mercredi 21/04
- Recherches fusion
- Recherches Cartographie
	- Voir avec Pascal pour des mots-clefs précis sinon ça n'existe peut-être pas
	- Beaucoup des projets travaillent en vue aérienne + photogrammetry
	- RL en simulation dans un micro-proc embarqué  ?
- Investigation en profondeur du code de 350SD-Net

## Jeudi 22/04
- Idem (cf. notes mercredi)

## Vendredi 23/04
- Manipulations UE4.26 pour créer une 'copie label' de l'env de Charles càd où toutes les textures sont remplacées par des couleurs unies et où l'éclairage est simplifié comme dans le monde de Dao
	- Reste à comprendre comment correctement régler l'éclairage des textures + voir avec Charles comment on peut changer l'aspect des éléments qui ne sont pas sélectionnables dans le monde mais qui sont dans le monde display.
- Rapport

# Semaine 9
## Lundi 26/04
- Réunion Pascal
- Documentation Cartographie supplémentaire w/ conseils Pascal
- Présentation Mise en Commun (+ base présentation bilan mi-parcours)

## Mardi 27/04
- Modification Redwood Forest :
	- Textures unlit sans effet d'optique
	- Enregistrement d'un parcours (images + pos & orientation dans le même dossier)
- Etude article [Visual Appearance Analysis of Forest Scenes for Monocular SLAM]
- Préparation réunions d'équipe

## Mercredi 28/04
- Préparation réunions d'équipe

## Jeudi 29/04
- Réunion mise en commun des ressources
	- Flightmare : simulateur différent avec environnement foret dispo sur lequel il y aura un challenge ICRA bientôt. Fonctionne sous Unity.
	- Synchro caméras ricoh theta : Guillaume et Renato s'en chargent, ils ont de pistes
	- Dès la semaine, se rapprocher de Charles sur l'aspect Seg Sem et l'épauler pour qu'on arrive à trouver un (ou des) modèle(s) qui nous convienne(nt) à nous 2

## Vendredi 30/04
- Préparation réunion techinque d'équipe
- Lecture d'articles

# Semaine 10
## Lundi 03/05
- Réunion Pascal
- Préparation réunion techinque d'équipe

## Mardi 04/05
- Réunion techinque d'équipe

# Mercredi 05/05
- Lecture article
- Prise en main script Charles :
	- Bug non solvés

# Jeudi 06/05
- Debuggage script Charles avec son aide
- Contact Rida
- Lecture article

# Vendredi 07/05
- Reunion Rida
- Tests script Charles

# Semaine 11
## Lundi 10/05
- Travail sur le script de Charles
	- A faire : partager le script à Rida, il est prêt pour le benchmarking
- Paramétrage Redwood Forest pour tenter de régler le pb de reconstruction equi (gestion de la lumière) : échec
	- Rida et Charles en soutien mais ça se termine par du tatonnage. Voir si on peut exporter des paramètres. Sinon au pire : télécharger les fichiers de config ou tout l'env de Charles (lourd)

## Mardi 11/05
- Paramétrage de Redwood Forest (again) : toujours échec
	- Demande visio Charles pour comparer les settings à la main, quitte à télécharger son environnement (comparer les fichier Config/DefaultEngine.ini aussi)
- Debuggage + nettoyage script Charles capture\_dataset\_6.py
	- Partage Rida pour benchmark + proposition intégration Look Up Table pour warp cube -> equi de Rida
	
## Mercredi 12/05
- Etude d'articles

# Semaine 12
## Lundi 17/05
- Etude d'articles
- Réunion Pascal
- Rédaction résumé d'articles
- Definition et étude de la solution de Bitterlich sur papier en préparation de l'implémentation (destiné au cahier de recherche)

## Mardi 18/05
- Développement 1ère approche de cartogrpahie inspirée par la méthode de Bitterlich
- Réunion avec Charles pour régler les problèmes d'éclairage du monde UE4
	- Certaines dimensions (trop grandes) de perspectives -> equi font apparaitre le problème d'illumination. les dimensions < 1500x1500 -> 1500x750 ont l'air ok
	- La visionneuse d'images de windows "Photos" crée des déchirures dans l'image qu'il n'y a pas vraiment en réalité

## Mercredi 19/05
- Conception + Dev bitterlich

## Jeudi 20/05
- Dev bitterlich

## Vendredi 20/05
- Rdv médical matin + urgence PC Daniel aprem

# Semaine 13
## Lundi 24/05
- férié

## Mardi 25/05
- Dev bitterlich

## Mercredi 26/06
- Paufinage bitterlich

## Jeudi 27/06
- Réunion pascal
  - Présentation Bitterlich v1, définition des évolutions et objectifs prochains
- Correction comportements innatendus bitterlich v1
- Construction papier de la prise en compte des vraies depth map.

## Vendredi 28/06
- Rapport
- Dev prise en compte vraies depth map

# Semaine 14
## Lundi 31/05
- Amélioration de bitterlich
  - Adaptation pour les .dep
  - Amélioration de l'affichage
  - Correction de bugs mineurs
  - Nettoyage du code (sauf lignes trop longues)
  - Debut amélioration de la précision : pas de conclusion en l'état. Problème d'estimation de la profondeur à la source car il faut remonter jusqu'à une aggregation de pixels

## Mardi 01/06
- Inspection nouveau script Charles avec les Look Up Table
- Contact Charles pour savoir comment récupérer les métriques des arbres d'une scène (pos + girth) afin d'évaluer bitterlich par métrique quantitative.
- Visio Charles
- Prise en main nouveau script Charles qui intègre les LUT

## Mercredi 02/06
- Réunion Pascal
  - Projet
  - Thèses
- Début v2 bitterlich
  - Amélioration estimation de grosseur
- Nouveau script Charles
  - Construction analyse descendante nouveau script Charles + modification
  - Essai : ultra rapide

## Jeudi 03/06
- UE4
  - Tentative d'accès aux meshes d'arbres : fail car tout est 'absorbé' dans une entité PFS_RW_Redwood_Trees qui les représente tous. Documentation sur l'accès aux objets générés de manière procédurale sous UE4 : aucune réponse. Cela signifie que pour l'instant on ne peut pas établir de métrique et one st en 'non supervisé'.
  - Contact par **mail** de l'entreprise créatrice du monde. Sur leur page UE4 ils répondent encore de nos jours et assez rapidement, hopefully par mail aussi.
- Développement v2 bitterlich
- Paramétrage autologin linux (à distance)

## Vendredi
- Amélioration bitterlich par depth à la source + superposition d'affichage pour estimer la précision de notre script visuellement.
- Aide Farah mise en place accès à distance sous demande de sa tutrice.
- Installation Orb Slam 3
  - Difficultés à la conciliation des dépendences et librairies. Aide de Sarah.

# Semaine 15
## Lundi 07/06
- Tests Orb Slam 3
  - Exemples impressionants, précision de l'ordre du centimètre, cas d'utilisation à la fois perspective et fisheye, mono et stereo.
- Réunion Pascal concernant sujets de thèse trouvés
- Tests solution UE4

## Mardi 08/06
- Tests solution UE4
- Génération dataset equi via nouveau script avec LUT
- Nouvelle prise de contact avec le créateur de l'environnement UE4

## Mercredi 09/06

## Jeudi 10/06
- Intégration dataset à orb slam 3
	- recherche de comment intégrer des vues equi à la place de vues fisheye ou perspective
	- contact reda paramètres caméra
- Documentation caméra et calibration
- Choix thèses

## Vendredi 11/06
- Intégration dataset à orb slam 3
- RDV médical

## Dimanche 13/06
- Intégration dataset à orb slam 3
	- Résiste encore, erreur openCV comme s'il y avait des problèmes de dimension ou des chargements de fichiers vides. Mais CSV et dataset corrects.
	- Mono TUMV_vi cassé : il n'y a plus de points descripteurs

# Semaine 16
## Lundi 14/06
- Re-build complet de ORB-SLAM3
	- Mono sur TUM-vi ne produit toujours pas de points descripteurs. -> Tjrs comme ça ???
	- Données UE4 à la place de celle d'euroc en cam0 mono : bloqué sur la phase d'initialisation "trying to initialize" mais pas étonnant car vues equi resized en 752x480 -> le modèle de caméra pinhole paramétré ne colle pas.
	- Update : sans resize on est toujours bloqué sur l'initialisation.
		- IDEE : refaire des captures plus longues avec une phases stationnaire au début à l'instar de EuRoC_MH01 ou TUM_vi_room1
- Le retour du build en mauvaise version de airsim et forestwood...
- 2e retour du créateur de Redwood Forest : n'a pas les compétences pour répondre à notre question
	- Demande à la communauté d'UE4 via post sur forum
- Génération nouveau dataset avec phase stationnaire qu début ou petits déplacements selon les axes de liberté pour faciliter la phase d'initialisation d'ORB-SLAM3²	
	- Au mieux AirSim est capable de produire 3.4 im/s.

## Mardi 15/06
- La phase semi-stationnaire au début du dataset aide à la phase d'initialisation, on voit que l'algo a des débuts de matching mais il n'y a pas assez d'images similaires générées par airsim, tout va trop vite, les fps ne sont pas assez élevés.
  - L'application d'un flou gaussien à kernel 3x3 facilite l'initialisation des descripteurs comparés aux images brutes dont l'approximation des valeur est 'plus proche voisin'.
	- Refaire le même dataset en prenant plus son temps.
	- Il y avait un problème d'ordre dans les images après renommage : ça marche ! mais la capture a une sacade trop forte : il faut augmenter les fps ou diminuer la vitesse de déplacement

## Mercredi 16/06
- Développement script d'augmentation artificielle du nombre de positions de airsim_rec.csv par interpolation pour avoir plus de captures selon un tracé grossier défini, sans avoir à enregistrer de nouveau tracé où il faudrait diminuer la vitesse de déplacement pour avoir plus de frames proches.
- Réponse sur le forum de UE4 concernant l'extraction des instances d'arbres

## Jeudi 17/06
- Dev script augmenteur de csv
- Discussion avec Charles + lecture source pour les transformations géométriques entre equi et fisheye/perspective
- Documentation blueprints par rapport à la 1ère réponse sur le forum UE4

## Vendredi 18/06
- Finitions script augmenteur de csv + tests unitaires
- Génération d'un nouveau dataset plus précis (1174 éléments pour un équivalent ~12fps airsim)
	- Meilleure robustesse d'ORBSLAM3 mais encore des pertes de cartes lors des grands déplacements (toujours trop grands). Lorsque les cartes sont répéres : 600+ points d'intérêts en moyenne pour 3000 descripteurs demandés.
	- Meilleurs résultats sur un modèle de caméra perspective PinHole que sur fisheye KannalaBrandt8 car dans le 1er cas les descripteurs sont cherchés partout alors que dans le 2e cas seule une partie de l'image (gauche) est cherchée car correspond à une vue en déformation fisheye. En fait une equi est comme la concaténation de 2 vues fisheye à 180° degrés : devant et derrière.

# Semaine 17
## Lundi 21/06
- Rapport
- Documentation SLAM
- Entretien thèse Huawei

## Mardi 22/06
- Exploration solutions blueprint UE4 pour récupérer les vérité terrains
	- Pas encore ce qu'on veut, équivalent des requêtes via airsim
- Reprise de la solution C++ : de nouveau le problème de compilation du monde
	- Proposition à Charles de la tenter de son côté car pour résoudre le problème de compilation, je devrais réinitialiser mon monde alors que j'esplore la piste blueprint qui est prometteuse
- Génération dataset réduit concentré sur la phase d'initialisation avec plus de fps

## Mercredi 23/06
- Mise à jour solution blueprint
- Nouveau dataset à équivalent 24fps bien adapté à ORBSLAM, pas de cassure de la map une fois établie, entre 400 et 600 matches et une quinzaine de keyframes, récupération des positions et quaternions (supposés) des frames et keyframes
	- Reste à déterminer avec précision ce que ça qualifie

## Jeudi 24/06
- Finition de la solution blueprint, confirmation de la conformité des données ressorties et exportation des données.
- Nouvelle capture à partir du PlayerStart placé à l'origine du monde pour les coordonnées AirSim soient raccord avec celles des arbres

## Vendredi 25/06
- Récupération des grosseurs des 12 prototypes d'arbres dans le viewport : vue side + mouse middle button