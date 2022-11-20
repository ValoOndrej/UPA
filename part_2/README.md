# UPA_2
Autori: Ondrej Valo, Radoslav Páleník, Karel Fritz

VUT FIT - příprava dat a jejich popisná charakteristika (UPA)

## Príprava
Pred spustením riešenia treba spustiť `setup.sh` pomocou príkazového riadka, pre nainštalovanie potrebných knižníc a závislostí. 
```
source ./setup.sh
```

## Spustenie
``` 
python3 run.py [-h] [--download] [--analysis] [--graphs] [--prepare]
  -h, --help Zobrazí túto pomocnú správu a ukončí sa
  -d, --download, Download data from website
  -a, --analysis, Analyze datasets from downloaded .csv files
  -g, --graphs, Generate graphs showing distribution of values from dataset
  -p, --prepare, Prepare data for classification task
```