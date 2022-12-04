# UPA_1
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
  -h, --help show this help message and exit
  -u, --url url do download from
  -up, --update update database with corections of chosen routs
  -d, --download  downloads original datasets
  -c, --clear Clears the database
  -cup, --cancel_update download collections for canceld routs and uploads them to database
```

## Spustenie
``` 
python3 lookup.py [-h] [--time TIME] [--from_city LOCATION] [--to_city LOCATION]
  -h, --help show this help message and exit
  -t, --time Datetime of departure for query in format YYYY/MM/DD-HH:MM:SS
  -from, --from_city  Start city in query
  -to, --to_city Destination city in query
```

# UPA_2
VUT FIT - příprava dat a jejich popisná charakteristika (UPA)

## Príprava
Pred spustením riešenia treba spustiť `setup.sh` pomocou príkazového riadka, pre nainštalovanie potrebných knižníc a závislostí. 
```
source ./setup.sh
```

## Spustenie
``` 
python3 run.py [-h] [--download] [--analysis] [--graphs] [--prepare]
  -h, --help show this help message and exit
  -d, --download, Download data from website
  -a, --analysis, Analyze datasets from downloaded .csv files
  -g, --graphs, Generate graphs showing distribution of values from dataset
  -p, --prepare, Prepare data for classification task
```

# UPA_3
VUT FIT - webove stránky jako zdroje dat

## Spustenie
``` 
python3 get_urls.py [-h] [--base-url URL_LINK] [--product-url URL_LINK] [--save]
  -h, --help show this help message and exit
  -b, --base-url Base page of eshop
  -p, --product-url page with products in eshop
  -s, --save Save list of links as file
```

## Spustenie
``` 
python3 get_data.py [-h]
  -h, --help show this help message and exit
```