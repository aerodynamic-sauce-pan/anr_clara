# Description
Liste des commandes à excéuter depuis la racine du projet pour faire fonctionner les différents modules.

# Utils
## Reshape
- `python -m utils.reshape_img -s TestImages/tree/65.jpg -d reshaped_imgs -p 640 480 -f png jpg -v` crée un dossier à la racine nommé `reshaped_imgs` contenant l'img 65.png redimensionnées en 640x480 en affichant les détails de l'opération.

# DenseNet
## Tester le réseau DenseNet
- `python test.py --input ../reshaped_imgs/65_640x480.jpg` ATTENTION commande à lancer depuis le dossier DenseNet -> need moduliser cette partie

# AdapNet

# Mapping
## Bitterlich
`python -m mapping.adhoc.bitterlich -s /media/mis/Disque_E/python_scripts/EQUI_AIRSIM/resources/CAPTURES_785_true_origin_24fps/1624545895257_rgb.png /media/mis/Disque_E/python_scripts/EQUI_AIRSIM/resources/CAPTURES_785_true_origin_24fps/1624545895257.dep /media/mis/Disque_E/python_scripts/EQUI_AIRSIM/resources/CAPTURES_785_true_origin_24fps/1624545895257_ss.png --nsd 5 --nsw 1000 --nsh 20 --nh 5 --dmax 40 --view cartesian -v`

`python -m mapping.adhoc.bitterlich_batch -s /media/mis/Disque_E/python_scripts/EQUI_AIRSIM/resources/CAPTURES_785_true_origin_24fps/ --nsd 4 --nsw 1000 --nsh 20 --nh 5 --dmax 40`

## Display
`python -m mapping.adhoc.display_map -s mapping/distances_gt_all_meters.csv -g mapping/trees_girth.csv --display_path /media/mis/Disque_E/python_scripts/EQUI_AIRSIM/resources/CAPTURES_785_true_origin_24fps/ --display_type rgb --view cartesian --dmax 30 --compare tree_prediction.csv`

## Evaluate
`python -m mapping.adhoc.evaluate -p mapping/tree_prediction.csv -v mapping/distances_gt_all_meters.csv -g mapping/trees_girth.csv --dmax 40 -o mapping/evaluation.csv`

