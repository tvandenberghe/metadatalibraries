FRANCAIS

CONTENU DU REPERTOIRE ZIPPE


Le répertoire zippé contient un dossier "Metadata" contenant les répertoires et fichiers suivants :

	-thesauri : répertoire contenant des fichiers .rdf qui correspondent aux thesauri utilisés dans le profil de métadonnées fédéral belge ;
	-templates : répertoire contenant des fichiers .xml correspondant aux templates d'une fiche ISO 19139 d'un service et de dataset. Ces templates sont spécifiques au profil de métadonnées fédéral belge;
	-dataset_ok : répertoire contenant le ou les fichiers excel contenant les informations nécessaire à la génération d'une ou plusieurs fiches de métadonnées de jeu de données ;
	-service_ok : répertoire contnenant le ou les fichiers excel contenant les informations nécessaire à la génération d'une ou plusieurs fiches de métadonnées de service ;
	-excel_dataset_simplifie_FR et excel_dataset_simplifie_NL.docx : manuel d'encodage du fichier excel dataset  en français et en néerlandais (la version française est la plus à jour) ;  ;
	-excel_service_simplifie_FR et excel_service_simplifie_NL : manuel d'encodage du fichier excel service en français et en néerlandais (la version française est la plus à jour) ;
	-dataset_FR et dataset_NL : fichier excel de collecte des informations pour créer une fiche de métadonnées de jeu de données (le fichier utilisé ne change rien le résultat, le nom des champs varient selon la langue : Nom dans un cas et Naam in andere geval)
	-service_FR et service_NL : fichier excel de collecte pour créer une fiche de métadonnées de service

En plus de cela, le répertoire zippé contient un fichier metadatarecord.py, qui correspond au code à proprement parler,  le présent fichier README.txt, ainsi que les fichiers params.py, geonetworkconnexion.py, qui contiennent des bibliothèques développées par l'IGN, ainsi que le fichier excel metada_elmt. Celui contient les XPATH des différents éléments de métadonnées.


Pour fonctionner, le répertoire dé-zippé doit toujours contenir le fichier metadarecord.py et le répertoire "Metadata" contenant tous les répertoires décrits ici.

PRESENTATION GENERALE

Le script metadarecord.py génère une fiche de métadonnées de service ou de jeu de données ISO 19139 conforme au profil fédéral belge. Ce profil est multilingue.
Pour l'utiliser, vous devez le lancer à partir d'un terminal. Le script est codé en python 2.
Le script doit iméprativement demeurer dans le répertoire. Vous devez y laisser tout ce que le répertoire contient (à part le dossier exemples).
Vous pouvez placer le répertoire où vous le désirez. La fiche que le script produit est automatiquement uploadé dans le geonetwork que vous avez défini dans geonetworkconnexion.py. 

Si vous ne souhaitez pas directement uploader la fiche, il suffit de commenter les lignes 545 à 548 du code metadatarecord.py.

OBLIGATIONS PREALABLES


Il utilise les libraires open suivantes que vous devez éventuellement ajouter :

	-lxml
	-os
	-sys
	-inspect
	-pandas
	-time
	-copy
	-uuid
	-request
	-getpass
	-

Toutes ces librairies sont open.
En plus de ça, le script utilise les deux bibliothèques python params.py, geonetworkconnexion.py, qui contiennent des bibliothèques développées par l'IGN, ainsi que le fichier excel metada_elmt

RESERVES INTELLECTUELLES

Tous les scripts python demeurent pleinement la propriété intellectuelle de l'Institut Géographique National. Ils ne peuvent ni être partagés ni vendus sans son consentement écrit et préalable.

ACTIONNEMENT DU SCRIPT

Vous devez au préalable remplir le fichier excel "dataset.xlsx" ou "service.xlsx" selon le type de fiche que vous voulez produire.
Une fois que vous avez rempli le fichier excel, vous devez l'enregistrer sous le même nom.
Une fois que c'est fait, vous pouvez lancer le script via un terminal. Le terminal va vous demander le type de fiches désirée.
Tapez "dataset" ou "service" en fonction. La fiche sera produite.


FICHIER EXCEL


Vous devez remplir correctement les différents champs, et par défaut, dans les quatre langues.
Ce sont les champs requis par lès règles INSPIRE.
Si vous souhaitez encoder plusieurs valeurs, vous devez les séparer par un "#  (comme pour les mots clés, ou les ressources couplées par exemple).
Tous les champs ne le permettent pas.

Les champs en orange sont mono-lingues : vous ne devez remplir que la colonne "content_eng".
Cela concerne également les champs des mots-clés GEMET concept et INSPIRE Theme (le script va chercher les traductions dans le répertoire thesauri).
Le contenu de balises xml doit impérativement être du texte. Veillez à ce que votre fichier excel ne contiennent que des champs texte et pas de champ date ou nombre.

/!\ Certains urls ont été hard-codés dans le script python et renvoient systématiquement vers les serveurs IGN. Vous devez donc adapter le script. Si cela vous pose un problème, n'hésitez pas à me le faire savoir.
Il s'agit des urls des champs suivants :

	-graphicOverview (aperçu graphique-thumbnail) : renvoie vers l'url http://www.ngi.be/thumbs/
	-operatesOn (ressources couplées) : renvoie vers l'url http://csw.geo.be/eng/csw?service=CSW&amp;request=GetRecordById&amp;version=2.0.2&amp;outputSchema=http://www.isotc211.org/2005/gmd&amp;elementSetName=full&amp;id=
		l'url est correcte si la fiche du jeu de données est moissonnée par l'IGN
	-linkage (lien d'accès au service) : renvoie vers l'url http://wms.ngi.be/inspire/
	

/!\ Certains champs doivent prendre leur valeur dans des domaines définis (binaire comme conformite_INSPIRE) : je vous invite à lire le document -très court- aregles_encodage_dataset_simplifie ou aregles_encodage_service_simplifie





