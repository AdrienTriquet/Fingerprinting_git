Pour faire tourner : 
* Remplir dans 'monScript' les chemins de "video_base" et "video_compar" 
* Lancer le script : python monScript.py

Ce script fait appel aux fonctions suivantes :

Recallage regarde le lien entre les 2 videos et donne une position à laquelle les fingerprints 
doivent être calculées.
Ravif calcule les fingerprint (voir README_ravif pour plus de détails, nb : fichier non mis à jour après 
mes modifications mais donne le fonctionnement global).
Correlation calcule la correlation entre 2 fingerprints.

**Attention** : Il est necessaire d'avoir un dossier 'image_travail' + '/PATH_TO_VIDEOS'
Exemple : pour video A.mp4 et B.mp4 dans 'video_travail', creer un dossier 'image_travail/video_travail'