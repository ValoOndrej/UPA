import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import matplotlib.pyplot as plt

class Dataset:

    def __init__(self, name):
        self.data = pd.read_csv(name)
        self.data.index = [x for x in range(1, len(self.data.values)+1)]
        self.data.index.name = 'id'
        if 'Date Egg' in self.data:
            self.data['Date Egg'] = pd.to_datetime(self.data['Date Egg'])
        if 'Sex' in self.data:
            self.data['Sex'] = self.data['Sex'].apply(
                lambda x: x if x in ['MALE', 'FEMALE'] else np.NaN)
        if 'Species' in self.data:
            self.data['Species'] = self.data['Species'].apply(
                lambda x: x.split(" ")[0] if x in [
                    'Adelie Penguin (Pygoscelis adeliae)',
                    'Chinstrap penguin (Pygoscelis antarctica)',
                    'Gentoo penguin (Pygoscelis papua)'
                ] else 'Unspecified'
            )

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
                if colum == "Sex":
                    unique_values = unique_values[:-1]
                print(f"{index: <2} colum is {colum: <20} missing {missing: <3} posible values are {', '.join(unique_values)}")
            else:
                print(f"{index: <2} colum is {colum: <20} missing {missing: <3}")

        x = (self.data.isnull().sum(axis = 1) == 2)
        print(f"{x.sum()} objects are missing more then 1 value")

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

        plt.title("Length of the Flipper (mm)")
        plt.boxplot(self.data["Flipper Length (mm)"].dropna())
        plt.savefig('graphs/flipper_l.png')
        plt.close()

        plt.title("Length of the dorsal ridge of a bird's bill between Sex")
        plt.hist(
            self.data["Culmen Length (mm)"].where(self.data["Sex"] == "MALE").dropna(), 
            histtype = 'step', 
            label = "Adelie male", 
            color = 'blue'
        )
        plt.hist(self.data["Culmen Length (mm)"].where(self.data["Sex"] == "FEMALE").dropna(), 
            histtype = 'step',
            label = "Adelie female",
            color = 'red'
        )
        plt.legend()
        plt.savefig('graphs/culmen_l_sex.png')
        plt.close()

        plt.title("Depth of the dorsal ridge of a bird's bill between Sex")
        plt.hist(self.data["Culmen Depth (mm)"].where(self.data["Sex"] == "MALE").dropna(), 
            histtype = 'step',
            label = "Adelie male",
            color = 'blue'
        )
        plt.hist(self.data["Culmen Depth (mm)"].where(self.data["Sex"] == "FEMALE").dropna(), histtype = 'step', label = "Adelie female", color = 'red')
        plt.legend()
        plt.savefig('graphs/culmen_d_sex.png')
        plt.close()

        plt.title("Length of the Flipper between Sex")
        plt.hist(self.data["Flipper Length (mm)"].where(self.data["Sex"] == "MALE").dropna(), 
            histtype = 'step',
            label = "Adelie male",
            color = 'blue'
        )
        plt.hist(self.data["Flipper Length (mm)"].where(self.data["Sex"] == "FEMALE").dropna(), 
            histtype = 'step',
            label = "Adelie female",
            color = 'red'
        )
        plt.legend()
        plt.savefig('graphs/flipper_l_sex.png')
        plt.close()

        plt.title("Body weight between Sex for Adelie Species")
        plt.hist(
            self.data["Body Mass (g)"]
            .where(self.data["Species"] == 'Adelie')
            .where(self.data["Sex"] == "MALE")
            .dropna(), histtype = 'step', label = "Adelie male", color = 'blue'
        )
        plt.hist(
            self.data["Body Mass (g)"]
            .where(self.data["Species"] == 'Adelie')
            .where(self.data["Sex"] == "FEMALE")
            .dropna(), histtype = 'step', label = "Adelie female", color = 'red'
        )
        plt.legend()
        plt.savefig('graphs/weight_A.png')
        plt.close()

        plt.title("Body weight between Sex for Chinstrap Species")
        plt.hist(
            self.data["Body Mass (g)"]
            .where(self.data["Species"] == 'Chinstrap')
            .where(self.data["Sex"] == "MALE")
            .dropna(), histtype = 'step', label = "Chinstrap male", color = 'blue'
        )
        plt.hist(
            self.data["Body Mass (g)"]
            .where(self.data["Species"] == 'Chinstrap')
            .where(self.data["Sex"] == "FEMALE")
            .dropna(), histtype = 'step', label = "Chinstrap female", color = 'red'
        )
        plt.legend()
        plt.savefig('graphs/weight_C.png')
        plt.close()

        plt.title("Body weight between Sex for Gentoo Species")
        plt.hist(
            self.data["Body Mass (g)"]
            .where(self.data["Species"] == 'Gentoo')
            .where(self.data["Sex"] == "MALE")
            .dropna(), histtype = 'step', label = "Gentoo male", color = 'blue'
        )
        plt.hist(
            self.data["Body Mass (g)"]
            .where(self.data["Species"] == 'Gentoo')
            .where(self.data["Sex"] == "FEMALE")
            .dropna(), histtype = 'step', label = "Gentoo female", color = 'red'
        )
        plt.legend()
        plt.savefig('graphs/weight_G.png')
        plt.close()

        plt.title("count samples between Species and sex")
        a_m = self.data["Body Mass (g)"].where(self.data["Species"] == 'Adelie').where(self.data["Sex"] == "MALE").dropna().size
        a_f = self.data["Body Mass (g)"].where(self.data["Species"] == 'Adelie').where(self.data["Sex"] == "FEMALE").dropna().size
        c_m = self.data["Body Mass (g)"].where(self.data["Species"] == 'Chinstrap').where(self.data["Sex"] == "MALE").dropna().size
        c_f = self.data["Body Mass (g)"].where(self.data["Species"] == 'Chinstrap').where(self.data["Sex"] == "FEMALE").dropna().size
        g_m = self.data["Body Mass (g)"].where(self.data["Species"] == 'Gentoo').where(self.data["Sex"] == "MALE").dropna().size
        g_f = self.data["Body Mass (g)"].where(self.data["Species"] == 'Gentoo').where(self.data["Sex"] == "FEMALE").dropna().size
        plt.bar(["Adelie male", "Adelie female", "Chinstrap male", "Chinstrap female", "Gentoo male", "Gentoo female"],[a_m, a_f, c_m, c_f, g_m, g_f])
        plt.savefig('graphs/count.png')
        plt.close()

    def prepare_for_classification(self):
        self.data = self.data.drop(['studyName',
                                    'Sample Number',
                                    'Region', 'Stage',
                                    'Individual ID',
                                    'Clutch Completion',
                                    'Date Egg',
                                    'Delta 15 N (o/oo)',
                                    'Delta 13 C (o/oo)',
                                    'Comments'],
                                    axis=1)

        categorical_dataset = self.data.dropna()

        categorical_dataset['Culmen Length'] = pd.qcut(categorical_dataset['Culmen Length (mm)'], 8)
        categorical_dataset = categorical_dataset.drop(['Culmen Length (mm)'], axis=1)

        categorical_dataset['Culmen Depth'] = pd.qcut(categorical_dataset['Culmen Depth (mm)'], 8)
        categorical_dataset = categorical_dataset.drop(['Culmen Depth (mm)'], axis=1)

        categorical_dataset['Flipper Length'] = pd.qcut(categorical_dataset['Flipper Length (mm)'], 8)
        categorical_dataset = categorical_dataset.drop(['Flipper Length (mm)'], axis=1)

        categorical_dataset['Body Mass'] = pd.qcut(categorical_dataset['Body Mass (g)'], 8)
        categorical_dataset = categorical_dataset.drop(['Body Mass (g)'], axis=1)



        numerical_dataset = self.data.interpolate()
        df_gender = pd.get_dummies(numerical_dataset['Sex'])
        numerical_dataset = pd.concat([numerical_dataset, df_gender], axis=1)
        numerical_dataset = numerical_dataset.drop(['Sex'], axis=1)

        df_species = pd.get_dummies(numerical_dataset['Species'])
        numerical_dataset = pd.concat([numerical_dataset, df_species], axis=1)
        numerical_dataset = numerical_dataset.drop(['Species'], axis=1)

        df_island = pd.get_dummies(numerical_dataset['Island'])
        numerical_dataset = pd.concat([numerical_dataset, df_island], axis=1)
        numerical_dataset = numerical_dataset.drop(['Island'], axis=1)

        categorical_dataset.to_csv('data/categorical_data.csv')

        numerical_dataset.to_csv('data/numerical_data.csv')
        