import pandas as pd
pd.options.mode.chained_assignment = None
import seaborn as sns
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
        sns.set_theme(style="ticks")
        sns.pairplot(self.data.drop('Sample Number', axis=1), hue="Species")
        plt.savefig('graphs/corelation_a.png')
        plt.close()

        sns.set_theme(style="darkgrid")
        sns.displot(
            self.data, x="Flipper Length (mm)", col="Species", row="Sex",
            binwidth=3, height=3, facet_kws=dict(margin_titles=True),
        )
        plt.savefig('graphs/flipper_l.png')
        plt.close()

        sns.set_theme(style="ticks", palette="pastel")
        sns.violinplot(x="Species", y="Culmen Length (mm)",
                    hue="Sex", palette=["m", "g"],
                    data=self.data)
        sns.despine(offset=10, trim=True)
        plt.savefig('graphs/culmen_l.png')
        plt.close()

        sns.set_theme(style="ticks", palette="pastel")
        sns.boxplot(x="Species", y="Culmen Depth (mm)",
                    hue="Sex", palette=["m", "g"],
                    data=self.data)
        sns.despine(offset=10, trim=True)
        plt.savefig('graphs/culmen_d.png')
        plt.close()

        sns.jointplot(
            data=self.data,
            x="Culmen Length (mm)", y="Culmen Depth (mm)", hue="Species",
            kind="kde",
        )
        plt.savefig('graphs/culmen_l_d.png')
        plt.close()
        
        sns.catplot(
            data=self.data.fillna(method="ffill"), kind="bar",
            x="Species", y="Body Mass (g)", hue="Sex",
            errorbar="sd", palette="dark", alpha=.6, height=6
        ).despine(left=True).set_axis_labels("", "Body mass (g)").legend.set_title("")
        plt.savefig('graphs/weight.png')
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
        