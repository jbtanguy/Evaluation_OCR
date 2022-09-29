# Evaluation_OCR

Trois évaluations non supervisées (c'est-à-dire ne nécessitant pas de vérité de terrain, ou transcription de référence) :
- TC : taux de confiance (donnés par les logiciels d'OCR) ;
- TL : taux de lexicalité (calculé en utilisant un lexique, ici : LGeRM = 3 millions de formes fléchies)
- un modèle de prédiction du CER ML_CER_apply.py


Pour lancer le modèle de prédiction du CER il faut :
- un dossier contenant toutes les pages océrisées (format enrichi HTML de Kraken)
- un fichier ressource lexicale en extension (c'est-à-dire que toutes les formes fléchies et les éventuelles variations orthotypograhiques apparaissent)
- renseigner ce dossier et cette ressource dans le fichier ML_CER_apply.py aux endroits indiqués dans le code
- lancer dans le terminal python3 ML_CER_apply.py
