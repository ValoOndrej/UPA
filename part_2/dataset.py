import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Dataset:

    def __init__(self, name):
        self.data = pd.read_csv(name)
        if 'Date Egg' in self.data:
            self.data['Date Egg'] = pd.to_datetime(self.data['Date Egg'])
        if 'Sex' in self.data:
            self.data['Sex'] = self.data['Sex'].apply(lambda x: x if x in ['MALE', 'FEMALE'] else 'Unspecified')

    def show_atributes(self):
        for index, colum in enumerate(self.data.columns):
            if self.data[colum].dtype in [np.float64, np.int64]:
                max_value = self.data[colum].max()
                min_value = self.data[colum].min()
                mean_value = self.data[colum].mean()
                print(f"name of {index}. colum is {colum}, max is {max_value}, min is {min_value}, mean is {mean_value}")
            elif colum in ["Date Egg"]:
                max_value = self.data[colum].max()
                min_value = self.data[colum].min()
                print(f"name of {index}. colum is {colum}, earliest date is {min_value}, latest date is {max_value}")
            elif colum in ["studyName", "Species", "Region", "Island", "Stage", "Clutch Completion", "Sex"]:
                unique_values = self.data[colum].unique()
                print(f"name of {index}. colum is {colum}, posible values are {', '.join(unique_values)}")
            else:
                print(f"name of {index}. colum is {colum}")

    def show_distribution(self):
        plt.title("Date study nest observed with 1 egg")
        plt.hist(self.data["Date Egg"], 10, label = "Dates")
        plt.legend()
        plt.show()

        plt.title("Lengths of the dorsal ridge of a bird's bills")
        plt.boxplot([self.data["Culmen Length (mm)"].dropna()])
        plt.show()

        plt.title("Mass of body")
        plt.violinplot(self.data["Body Mass (g)"].dropna())
        plt.show()