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
        if 'Species' in self.data:
            self.data['Species'] = self.data['Species'].apply(lambda x: x.split(" ")[0] if x in ['Adelie Penguin (Pygoscelis adeliae)', 'Chinstrap penguin (Pygoscelis antarctica)', 'Gentoo penguin (Pygoscelis papua)'] else 'Unspecified')

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

        plt.title("Length of the dorsal ridge of a bird's bill")
        plt.boxplot([self.data["Culmen Length (mm)"].dropna()])
        plt.show()

        plt.title("Depth of the dorsal ridge of a bird's bill")
        plt.violinplot(self.data["Culmen Depth (mm)"].dropna())
        plt.show()

        plt.title("Body weight between Species")
        plt.hist(self.data["Body Mass (g)"].where(self.data["Species"] == 'Adelie').dropna(), histtype = 'step', label = "Adelie", color = 'blue')
        plt.hist(self.data["Body Mass (g)"].where(self.data["Species"] == 'Chinstrap').dropna(), histtype = 'step', label = "Chinstrap", color = 'red')
        plt.hist(self.data["Body Mass (g)"].where(self.data["Species"] == 'Gentoo').dropna(), histtype = 'step', label = "Gentoo", color = 'sienna')
        plt.legend()
        plt.show()

        plt.title("count samples between Species and sex")
        A_M = self.data["Body Mass (g)"].where(self.data["Species"] == 'Adelie').where(self.data["Sex"] == "MALE").dropna().size
        A_F = self.data["Body Mass (g)"].where(self.data["Species"] == 'Adelie').where(self.data["Sex"] == "FEMALE").dropna().size
        C_M = self.data["Body Mass (g)"].where(self.data["Species"] == 'Chinstrap').where(self.data["Sex"] == "MALE").dropna().size
        C_F = self.data["Body Mass (g)"].where(self.data["Species"] == 'Chinstrap').where(self.data["Sex"] == "FEMALE").dropna().size
        G_M = self.data["Body Mass (g)"].where(self.data["Species"] == 'Gentoo').where(self.data["Sex"] == "MALE").dropna().size
        G_F = self.data["Body Mass (g)"].where(self.data["Species"] == 'Gentoo').where(self.data["Sex"] == "FEMALE").dropna().size
        plt.bar(["Adelie male", "Adelie female", "Chinstrap male", "Chinstrap female", "Gentoo male", "Gentoo female"],[A_M, A_F, C_M, C_F, G_M, G_F])
        plt.show()


        