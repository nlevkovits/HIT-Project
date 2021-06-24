import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scraping_data import crawl_main
from ex_feaures import ex_features_main

if __name__ == "__main__":

    # try:
    #     crawl_main()
    # except Exception as e:
    #     pass
    #
    # try:
    #     ex_features_main()
    # except Exception as e:
    #     pass


    data0 = pd.read_csv('urldata.csv')
    data1 = pd.read_csv('urls_countries.csv')

    data0.head()
    data0.shape
    data0.columns
    data0.info()

    data0.describe()
    data = data0.drop(['Domain'], axis = 1).copy()
    data.isnull().sum()
    # shuffling the rows in the dataset so that when splitting the train and test set are equally distributed
    data = data.sample(frac=1).reset_index(drop=True)
    p1 = data.head()
    print(p1)
    # # Sepratating & assigning features and target columns to X & y
    y = data['Label']
    X = data.drop('Label',axis=1)
    X.shape, y.shape

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size = 0.2, random_state = 12)
    X_train.shape, X_test.shape

    from sklearn.metrics import accuracy_score

    ML_Model = []
    acc_train = []
    acc_test = []

    #function to call for storing the results
    def storeResults(model, a,b):
      ML_Model.append(model)
      acc_train.append(round(a, 3))
      acc_test.append(round(b, 3))

    from sklearn.tree import DecisionTreeClassifier

    # instantiate the model
    tree = DecisionTreeClassifier(max_depth=5)
    # fit the model
    tree.fit(X_train, y_train)


    #predicting the target value from the model for the samples
    y_test_tree = tree.predict(X_test)
    y_train_tree = tree.predict(X_train)

    #computing the accuracy of the model performance
    acc_train_tree = accuracy_score(y_train,y_train_tree)
    acc_test_tree = accuracy_score(y_test,y_test_tree)

    print("Decision Tree: Accuracy on training Data: {:.3f}".format(acc_train_tree))
    # print("Decision Tree: Accuracy on test Data: {:.3f}".format(acc_test_tree))

    #checking the feature improtance in the model
    f = plt.figure(figsize=(9,7))
    f.suptitle('Decision Tree', fontsize=20)
    n_features = X_train.shape[1]
    plt.barh(range(n_features), tree.feature_importances_, align='center')
    plt.yticks(np.arange(n_features), X_train.columns)
    plt.xlabel("Feature importance")
    plt.ylabel("Feature")
    plt.show()
    storeResults('Decision Tree', acc_train_tree, acc_test_tree)


    from sklearn.ensemble import RandomForestClassifier

    # instantiate the model
    forest = RandomForestClassifier(max_depth=5)

    # fit the model
    forest.fit(X_train, y_train)

    y_test_forest = forest.predict(X_test)
    y_train_forest = forest.predict(X_train)

    acc_train_forest = accuracy_score(y_train,y_train_forest)
    acc_test_forest = accuracy_score(y_test,y_test_forest)

    print("Random forest: Accuracy on training Data: {:.3f}".format(acc_train_forest))
    # print("Random forest: Accuracy on test Data: {:.3f}".format(acc_test_forest))

    f2 = plt.figure(figsize=(9, 7))
    f2.suptitle('Random Forest', fontsize=20)
    n_features = X_train.shape[1]
    plt.barh(range(n_features), forest.feature_importances_, align='center')
    plt.yticks(np.arange(n_features), X_train.columns)
    plt.xlabel("Feature importance")
    plt.ylabel("Feature")
    plt.show()

    def graph_categories(results, category_names):

        labels = list(results.keys())
        data = np.array(list(results.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = plt.get_cmap('RdYlGn')(
            np.linspace(0.15, 0.85, data.shape[1]))

        fig, ax = plt.subplots(figsize=(9.2, 5))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())

        for i, (colname, color) in enumerate(zip(category_names, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            rects = ax.barh(labels, widths, left=starts, height=0.5,
                            label=colname, color=color)

            r, g, b, _ = color
            text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
            ax.bar_label(rects, label_type='center', color=text_color)
        ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
                  loc='lower left', fontsize='small')

        return fig, ax

    results2 = {}

    for col in data0.keys():
        if col == 'Domain':
            continue
        results2[col] = [sum(data0[col].array), 10000 - sum(data0[col].array)]

    category_names = ['Suspected phishing', 'Legit']
    graph_categories(results2, category_names)

    data1.plot.bar(x='country', color={"url": "red"})
    plt.show()