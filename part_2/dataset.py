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

    def __export_to_png(self, fig, name):
        fig.tight_layout()
        plt_name = f"plts/{name}.png"
        fig.savefig(plt_name)
        print(f"Saving plot to '{plt_name}'")

    def show_atributes(self):
        for index, colum in enumerate(self.data.columns):
            missing = self.data[colum].isnull().sum(axis = 0)
            if self.data[colum].dtype in [np.float64, np.int64]:
                max_value = self.data[colum].max()
                min_value = self.data[colum].min()
                mean_value = self.data[colum].mean()
                print(f"{index: <2} colum is {colum: <20} missing {missing: <3} max = {max_value: <10} min = {min_value: <10} mean = {mean_value: <10}")
            elif colum in ["Date Egg"]:
                max_value = self.data[colum].max()
                min_value = self.data[colum].min()
                print(f"{index: <2} colum is {colum: <20} missing {missing: <3} earliest date is {min_value: <10}, latest date is {max_value: <10}")
            elif colum in ["studyName", "Species", "Region", "Island", "Stage", "Clutch Completion", "Sex"]:
                unique_values = self.data[colum].unique()
                print(f"{index: <2} colum is {colum: <20} missing {missing: <3} posible values are {', '.join(unique_values)}")
            else:
                print(f"{index: <2} colum is {colum: <20} missing {missing: <3}")

    def show_distribution(self):
        plt.title("Date study nest observed with 1 egg")
        plt.hist(self.data["Date Egg"], 10, label = "Dates")
        plt.legend()
        plt.savefig('graphs/date_egg.png')
        plt.close()

        plt.title("Length of the dorsal ridge of a bird's bill (mm)")
        plt.violinplot([self.data["Culmen Length (mm)"].dropna()])
        plt.savefig('graphs/culmen_l.png')
        plt.close()

        plt.title("Depth of the dorsal ridge of a bird's bill (mm)")
        plt.violinplot(self.data["Culmen Depth (mm)"].dropna())
        plt.savefig('graphs/culmen_d.png')
        plt.close()

        plt.title("Depth of the dorsal ridge of a bird's bill (mm)")
        plt.boxplot(self.data["Flipper Length (mm)"].dropna())
        plt.savefig('graphs/flipper_l.png')
        plt.close()

        plt.title("Body weight between Sex for Adelie Species")
        plt.hist(self.data["Body Mass (g)"].where(self.data["Species"] == 'Adelie').where(self.data["Sex"] == "MALE").dropna(), histtype = 'step', label = "Adelie male", color = 'blue')
        plt.hist(self.data["Body Mass (g)"].where(self.data["Species"] == 'Adelie').where(self.data["Sex"] == "FEMALE").dropna(), histtype = 'step', label = "Adelie female", color = 'red')
        plt.legend()
        plt.savefig('graphs/weight_A.png')
        plt.close()

        plt.title("Body weight between Sex for Chinstrap Species")
        plt.hist(self.data["Body Mass (g)"].where(self.data["Species"] == 'Chinstrap').where(self.data["Sex"] == "MALE").dropna(), histtype = 'step', label = "Chinstrap male", color = 'blue')
        plt.hist(self.data["Body Mass (g)"].where(self.data["Species"] == 'Chinstrap').where(self.data["Sex"] == "FEMALE").dropna(), histtype = 'step', label = "Chinstrap female", color = 'red')
        plt.legend()
        plt.savefig('graphs/weight_C.png')
        plt.close()

        plt.title("Body weight between Sex for Gentoo Species")
        plt.hist(self.data["Body Mass (g)"].where(self.data["Species"] == 'Gentoo').where(self.data["Sex"] == "MALE").dropna(), histtype = 'step', label = "Gentoo male", color = 'blue')
        plt.hist(self.data["Body Mass (g)"].where(self.data["Species"] == 'Gentoo').where(self.data["Sex"] == "FEMALE").dropna(), histtype = 'step', label = "Gentoo female", color = 'red')
        plt.legend()
        plt.savefig('graphs/weight_G.png')
        plt.close()

        plt.title("count samples between Species and sex")
        A_M = self.data["Body Mass (g)"].where(self.data["Species"] == 'Adelie').where(self.data["Sex"] == "MALE").dropna().size
        A_F = self.data["Body Mass (g)"].where(self.data["Species"] == 'Adelie').where(self.data["Sex"] == "FEMALE").dropna().size
        C_M = self.data["Body Mass (g)"].where(self.data["Species"] == 'Chinstrap').where(self.data["Sex"] == "MALE").dropna().size
        C_F = self.data["Body Mass (g)"].where(self.data["Species"] == 'Chinstrap').where(self.data["Sex"] == "FEMALE").dropna().size
        G_M = self.data["Body Mass (g)"].where(self.data["Species"] == 'Gentoo').where(self.data["Sex"] == "MALE").dropna().size
        G_F = self.data["Body Mass (g)"].where(self.data["Species"] == 'Gentoo').where(self.data["Sex"] == "FEMALE").dropna().size
        plt.bar(["Adelie male", "Adelie female", "Chinstrap male", "Chinstrap female", "Gentoo male", "Gentoo female"],[A_M, A_F, C_M, C_F, G_M, G_F])
        plt.savefig('graphs/count.png')
        plt.close()


        