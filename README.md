# fdk-elasticsearch-etl

Følgende er et prosjekt som kommuniserer direkte med Elasticsearch sitt REST-grensesnitt.


## Forutsetninger
Rest-grensesnittet til Elasticsearch er ikke eksponert eksternt, så dette må gjøres først.

Tilgang til Google Cloud Console og clusteret der Elasticsearch kjører (fdk-dev eller fdk-prod, avhengig av hvilket miljø som skal oppdateres)


### Eksponer Elasticsearch sitt endepunkt

Logg på Google Cloud Platform og velg riktig prosjekt (fdk-dev eller fdk-prod)
Start et kommandolinjevindu
Autentiser mot riktig Kubernetes-cluster (fdk-dev eller fdk-prod)
```
gcloud config set project <project>
gcloud container clusters get-credentials <clustername> --region europe-north1-a
gcloud config set compute/region europe-north1-a
gcloud config set compute/zone europe-north1
```
List kjørende pod-er for riktig miljø/namespace (ut1, st1, it1, demo, prod)
```
kubectl --namespace=<miljø> get pods
```
Finn navnet på Elasticsearch-poden og kopier det.
Kjør port-forwarding på Elasticsearch-poden, port 9200
```
kubectl --namespace=ut1 port-forward <elasticsearch5-5d5d7484ff-4gqg8> 9200:9200
```
Åpne web preview på port 9200 (Menyvalg "vindu med et øye inni") rett over kommandolinjevinduet, velg change port. Skriv 9200 og trykk change and preview. En ny fane åpner seg i nettleseren.
Fjern /?authuser=2 fra slutten av url-en i den nye nettleserfanen. Du skal nå se statusinfo fra Elasticsearch, bl a cluster_name. Nå vet du at adressen i url-feltet er den riktige. (Noe slikt som https://9200-dot-4507209-dot-devshell.appspot.com/ - den kan være litt forskjellig fra gang til gang) Kopier denne.

For at endepunktet skal kunne brukes, må klienten (nettleser, Postman, curl etc) ha en cookie som heter devshell-proxy-session. Cookien legges automatisk inn i det nye preview-vinduet. Trykk F12 i Chrome og se på nettverkstrafikken i Network-fanen. Denne cookien må kopieres inn i cookie-store for den aktuelle klienten. Oppskrift for Postman her. Oppskrift for curl her: https://stackoverflow.com/a/21919601/767586 I dette etl-prosjektet legges cookie inn i respektive python-script.


## Eksempel
POST til Elasticsearch:
POST https://<url>/dcat/publisher/<orgnr>

Content-type skal være application/json
Accept skal være application/json (usikker på om denne må settes)
Body skal være en gyldig json-struktur vist over. Orgnr i Json og i uri-en som postes må være lik.
Serveren skal svare med http status 201 Created hvis operasjonen lykkes.
Sjekk at den nye publisheren er kommet inn



## Avslutt port-forwarding

Trykk Ctrl-c i kommandolinjevinduet i Cloud shell.

## Nyttige ekstrating:

list alle publishere
```
% curl https://<url>/dcat/publisher/_search
```
List en eksisterende publisher
```
% curl https://<url>/dcat/publisher/<orgnr>
```
