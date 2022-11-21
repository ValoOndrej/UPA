
import os
import argparse
import zipfile

from dataset import Dataset

from kaggle.api.kaggle_api_extended import KaggleApi

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--download', action="store_true", help="Download data from website")
parser.add_argument('-a', '--analysis', action="store_true", help="Analyze datasets from downloaded .csv files")
parser.add_argument('-g', '--graphs', action="store_true", help="Generate graphs showing distribution of values from dataset")
parser.add_argument('-p', '--prepare', action="store_true", help="Prepare data for classification task")

args = parser.parse_args()
data = "data/"
names = os.listdir(data)

if args.download or not names:
    os.environ['KAGGLE_USERNAME'] = "ondrejvalo"
    os.environ['KAGGLE_KEY'] = "8b36d098faf93c8cbce40ee99225f734"

    api = KaggleApi()
    api.authenticate()


    api.dataset_download_files('parulpandey/palmer-archipelago-antarctica-penguin-data', path=".")

    zip_name = "palmer-archipelago-antarctica-penguin-data.zip"

    with zipfile.ZipFile(zip_name) as zip_ref:
        zip_ref.extractall(data)
    names = zip_ref.namelist()
    os.remove(zip_name)

dato = Dataset(data + "penguins_lter.csv")

if args.analysis:
    dato.show_atributes()

if args.graphs:
    dato.show_distribution()

if args.prepare:
    dato.prepare_for_classification()