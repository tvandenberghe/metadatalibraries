FRANCAIS

CONTENU DU REPERTOIRE ZIPPE


Le r�pertoire zipp� contient un dossier "Metadata" contenant les r�pertoires et fichiers suivants :

	-thesauri : r�pertoire contenant des fichiers .rdf qui correspondent aux thesauri utilis�s dans le profil de m�tadonn�es f�d�ral belge ;
	-templates : r�pertoire contenant des fichiers .xml correspondant aux templates d'une fiche ISO 19139 d'un service et de dataset. Ces templates sont sp�cifiques au profil de m�tadonn�es f�d�ral belge;
	-dataset_ok : r�pertoire contenant le ou les fichiers excel contenant les informations n�cessaire � la g�n�ration d'une ou plusieurs fiches de m�tadonn�es de jeu de donn�es ;
	-service_ok : r�pertoire contnenant le ou les fichiers excel contenant les informations n�cessaire � la g�n�ration d'une ou plusieurs fiches de m�tadonn�es de service ;
	-excel_dataset_simplifie_FR et excel_dataset_simplifie_NL.docx : manuel d'encodage du fichier excel dataset  en fran�ais et en n�erlandais (la version fran�aise est la plus � jour) ;  ;
	-excel_service_simplifie_FR et excel_service_simplifie_NL : manuel d'encodage du fichier excel service en fran�ais et en n�erlandais (la version fran�aise est la plus � jour) ;
	-dataset_FR et dataset_NL : fichier excel de collecte des informations pour cr�er une fiche de m�tadonn�es de jeu de donn�es (le fichier utilis� ne change rien le r�sultat, le nom des champs varient selon la langue : Nom dans un cas et Naam in andere geval)
	-service_FR et service_NL : fichier excel de collecte pour cr�er une fiche de m�tadonn�es de service

En plus de cela, le r�pertoire zipp� contient un fichier metadatarecord.py, qui correspond au code � proprement parler,  le pr�sent fichier README.txt, ainsi que les fichiers params.py, geonetworkconnexion.py, qui contiennent des biblioth�ques d�velopp�es par l'IGN, ainsi que le fichier excel metada_elmt. Celui contient les XPATH des diff�rents �l�ments de m�tadonn�es.


Pour fonctionner, le r�pertoire d�-zipp� doit toujours contenir le fichier metadarecord.py et le r�pertoire "Metadata" contenant tous les r�pertoires d�crits ici.

PRESENTATION GENERALE

Le script metadarecord.py g�n�re une fiche de m�tadonn�es de service ou de jeu de donn�es ISO 19139 conforme au profil f�d�ral belge. Ce profil est multilingue.
Pour l'utiliser, vous devez le lancer � partir d'un terminal. Le script est cod� en python 2.
Le script doit im�prativement demeurer dans le r�pertoire. Vous devez y laisser tout ce que le r�pertoire contient (� part le dossier exemples).
Vous pouvez placer le r�pertoire o� vous le d�sirez. La fiche que le script produit est automatiquement upload� dans le geonetwork que vous avez d�fini dans geonetworkconnexion.py. 

Si vous ne souhaitez pas directement uploader la fiche, il suffit de commenter les lignes 545 � 548 du code metadatarecord.py.

OBLIGATIONS PREALABLES


Il utilise les libraires open suivantes que vous devez �ventuellement ajouter :

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
En plus de �a, le script utilise les deux biblioth�ques python params.py, geonetworkconnexion.py, qui contiennent des biblioth�ques d�velopp�es par l'IGN, ainsi que le fichier excel metada_elmt

RESERVES INTELLECTUELLES

Tous les scripts python demeurent pleinement la propri�t� intellectuelle de l'Institut G�ographique National. Ils ne peuvent ni �tre partag�s ni vendus sans son consentement �crit et pr�alable.

ACTIONNEMENT DU SCRIPT

Vous devez au pr�alable remplir le fichier excel "dataset.xlsx" ou "service.xlsx" selon le type de fiche que vous voulez produire.
Une fois que vous avez rempli le fichier excel, vous devez l'enregistrer sous le m�me nom.
Une fois que c'est fait, vous pouvez lancer le script via un terminal. Le terminal va vous demander le type de fiches d�sir�e.
Tapez "dataset" ou "service" en fonction. La fiche sera produite.


FICHIER EXCEL


Vous devez remplir correctement les diff�rents champs, et par d�faut, dans les quatre langues.
Ce sont les champs requis par l�s r�gles INSPIRE.
Si vous souhaitez encoder plusieurs valeurs, vous devez les s�parer par un "#  (comme pour les mots cl�s, ou les ressources coupl�es par exemple).
Tous les champs ne le permettent pas.

Les champs en orange sont mono-lingues : vous ne devez remplir que la colonne "content_eng".
Cela concerne �galement les champs des mots-cl�s GEMET concept et INSPIRE Theme (le script va chercher les traductions dans le r�pertoire thesauri).
Le contenu de balises xml doit imp�rativement �tre du texte. Veillez � ce que votre fichier excel ne contiennent que des champs texte et pas de champ date ou nombre.

/!\ Certains urls ont �t� hard-cod�s dans le script python et renvoient syst�matiquement vers les serveurs IGN. Vous devez donc adapter le script. Si cela vous pose un probl�me, n'h�sitez pas � me le faire savoir.
Il s'agit des urls des champs suivants :

	-graphicOverview (aper�u graphique-thumbnail) : renvoie vers l'url http://www.ngi.be/thumbs/
	-operatesOn (ressources coupl�es) : renvoie vers l'url http://csw.geo.be/eng/csw?service=CSW&amp;request=GetRecordById&amp;version=2.0.2&amp;outputSchema=http://www.isotc211.org/2005/gmd&amp;elementSetName=full&amp;id=
		l'url est correcte si la fiche du jeu de donn�es est moissonn�e par l'IGN
	-linkage (lien d'acc�s au service) : renvoie vers l'url http://wms.ngi.be/inspire/
	

/!\ Certains champs doivent prendre leur valeur dans des domaines d�finis (binaire comme conformite_INSPIRE) : je vous invite � lire le document -tr�s court- aregles_encodage_dataset_simplifie ou aregles_encodage_service_simplifie





