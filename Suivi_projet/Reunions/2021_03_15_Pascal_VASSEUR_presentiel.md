# Avancée du travail
- Script pour resize des images automatiquement fini
- Pb avec le launcher epic games persistant (laissé en standby) : le problème vient peut etre du GPU, peut etre de la CM
	- Essayer de ré-instaler le launcher sans le GPU. SI encore pb -> il faudra changer de poste
- Need changer le mode de paramétrage des modèles AdapNet
	- Réduire à 1 fichier de config au lieu de 2, + le tf.record.
		- Référencer un dossier pour train et test/val mais implique modifier `convert_to_tfrecords.py` (méthode 'decode')
	- Rendre les arguments d'appel plus compréhensibles
- Need ajouter une doc intra code sur AdapNet et une partie de DenseNet
	- Pour clustering : voir avec Dao pour traduction du chinois
- On va partir sur de la stéréo pour la profondeur avec seg sem sur chaque image
- Une fois arrivé à la partie fisheye -> voir avec doctorant qui l'a simulé sous UE4

# Deadlines
- Précisions sur la réunion avec l'équipe de nice
	- Nope
- Autres dates
	- Nope
	- A partir du 15 avril, un doc sera sur Nice et devra utiliser mes travaux -> reconstruction 3D
- Possibilité de se libérer plus tôt le vendredi 30/04 pour un événement perso.

# Organisation
- Télétravail possible via VPN + SSH. Il faut déterminer quand je serai en télétravail maintenant qu'il y a Mathieu 2-3 jours par semaine
	- Voir avec Christophe pour le planning

