# UPA
Autori: Ondrej Valo, Radoslav Páleník, Karel Fritz

VUT FIT - ukládání rozsáhlých dat v NoSQL databázích (UPA)

Projekt implementuje pipeline spracovania dát poskytnutých ministerstvo dopravy ČR, uložením do noSQL databáze a ich následnou interpretáciou.

## Príprava
Pred spustením riešenia treba spustiť `setup.sh` pomocou príkazového riadka, pre nainštalovanie potrebných knižníc a závislostí. 
```
./setup.sh
```

## Stiahnutia
``` 
python3 download.py [-h] [--download] [--url URL_LINK] [--clear] [--update] [--cancel_update]
  -h, --help Zobrazí túto pomocnú správu a ukončí sa
  -u, --url url do download from
  -up, --update update database with corections of chosen routs
  -d, --download  downloads original datasets
  -c, --clear Clears the database
  -cup, --cancel_update download collections for canceld routs and uploads them to database
```

## Spustenie
``` 
python3 lookup.py [-h] [--time TIME] [--from_city LOCATION] [--to_city LOCATION]
  -h, --help Zobrazí túto pomocnú správu a ukončí sa
  -t, --time Datetime of departure for query in format YYYY/MM/DD-HH:MM:SS
  -from, --from_city  Start city in query
  -to, --to_city Destination city in query
```