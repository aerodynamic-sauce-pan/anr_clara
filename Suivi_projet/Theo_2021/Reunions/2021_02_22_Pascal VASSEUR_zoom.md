cartes de profondeurs semblaient trop parfaites -> voir reproductibilité

Avoir des infos loin peut etre utile pour initialiser la segmentation des futures images -> initialisation de seeds. Navigation réactive donc pas besoin de données trop lointaines.


l'important = trouver les troncs, avoir l'implantation et le positionnement relatif des troncs -> force une sorte de signature exclusive de chaque forêt ou partie de forêt.
=> Le tout sur une surface donc. Mais prise en compte des aspérités sur z (hauteur) pour avoir une carte 3D dans un 2e temps et on sait pas encore comment on va faire.

La détection du feuillage pour l'éviter fait dans un autre projet : faire des cartes d'occupation (segmentation autour du drone en cubes qui dsient si les cubes ont des obstacles ou pas). Nous on veut faire une carte pour se relocaliser si cul de sac.

- Refaire une petite bibilio sur les méthodes de fusion de carte seg. sem. / depth map : soit reprendre soit dév un nouveau truc. Obj important

- Incertitude sur l'adaptation en images réelles car tout a été fait sur des img de synthèse.

- Si besoin, on pourra contacter un thésard qui maitrise bien UE4 voire des gens à nice.

- Partie object detection bbox sera mise de côté cette année. Démontré l'an dernier que comme dans les bbox on a le contenu derrière, l'app est nul.

- Espace Lab (robuste aux changements de luminosité et accepte distance eucliedienne) vieux donc surement au point mais peut etre que d'autres espaces de couleur mieux adaptés ? -> Voir s'il existe des espaces de couleurs adaptés à l'app.

Si on arrive à retrouver les résultats de l'an dernier sur seg. sem., on pourra direct s'ateler à l'instance. sem. puis passer à la cartographie. Il faudra aussi modéliser le sol -> 2D topo ou 3D. Mais d'abord réussir à extraire les arbres et les localiser et ensuite le sol.



Arrivée au labo : need badge pour entrer via l'ESIEE et salle machine
-> Envoyer numéro étudiant à P. VASSEUR
RDV 9h puis appeler P. VASSEUR

Plateforme de calcul partagé : 'Matrix'

