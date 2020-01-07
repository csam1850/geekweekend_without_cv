"""
this module is used for training the classifier
"""
# pylint: disable=unused-import, invalid-name

import pickle
import os
from time import time
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier  # noqa: F401
from sklearn.tree import DecisionTreeClassifier  # noqa: F401
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
from load_data import load_fruit_data, FRUITS
from model_evaluation import plot_confusion_matrix


start = time()

# create folder to save model and scaling weights
root_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(root_dir, 'models')
if not os.path.isdir(path):
    os.mkdir(path)

# Get Images and Labels
X_train, y_train = load_fruit_data(FRUITS, data_type='Training')
X_test, y_test = load_fruit_data(FRUITS, 'Test')

print('scaling images')

# Scale Data Images
scaler = StandardScaler()
X_train = scaler.fit_transform([i.flatten() for i in X_train])
X_test = scaler.fit_transform([i.flatten() for i in X_test])

# Save scaler to disk
scalerfile = 'models/scaler.sav'
pickle.dump(scaler, open(scalerfile, 'wb'))

print('training starts now')

# feature extraction with principal components analysis
pca = PCA(n_components=50, whiten=True, random_state=42)

# Support vector machine model - kernel choices were linear / rbf
svm = SVC(kernel='rbf', C=150, gamma=0.0002)

# pipeline
model = make_pipeline(pca, svm)

# grid search for hyperparameters
# param_grid = {'svc__C': [150, 350],
#               'svc__gamma': [0.00005, 0.0001, 0.001],
#               'pca__n_components': [25, 50, 100]}

# param_grid = {'svc__C': [50, 100, 150],
#               'svc__gamma': [0.00005, 0.0001, 0.0002]}
# print('performing grid search of parameters')

# param_grid = {'pca__n_components': [25, 50, 75]}

param_grid = {'svc__C': [150],
              'svc__gamma': [0.0002]}

grid = GridSearchCV(model, param_grid, cv=5)

# fitting of model
grid.fit(X_train, y_train)
print(grid.best_params_)

model = grid.best_estimator_

# predicting values
y_pred = model.predict(X_test)
precision = metrics.accuracy_score(y_pred, y_test) * 100

print("Accuracy with SVM: {0:.2f}%".format(precision))

# save model to disk
filename = 'models/svm_model.sav'
pickle.dump(model, open(filename, 'wb'))

print('total training time was: ', str(time()-start), 'seconds')

# plot confusion matrix and show table
cm, _ = plot_confusion_matrix(y_test, y_pred, normalize=True)
plt.show()

print(metrics.classification_report(y_test, y_pred,
                                    target_names=FRUITS))

# # K-NN
# knn_model = KNeighborsClassifier(n_neighbors=5)
# knn_model.fit(X_train, y_train)
# y_pred = knn_model.predict(X_test)
# precision = metrics.accuracy_score(y_pred, y_test) * 100
# print("Accuracy with K-NN: {0:.2f}%".format(precision))
# # save models to disk
# filename = 'models/knn_model.sav'
# pickle.dump(knn_model, open(filename, 'wb'))

# # DECISION TREE
# dt_model = DecisionTreeClassifier()
# dt_model.fit(X_train, y_train)
# y_pred = dt_model.predict(X_test)
# precision = metrics.accuracy_score(y_pred, y_test) * 100
# print("Accuracy with Decision Tree: {0:.2f}%".format(precision))
# # save models to disk
# filename = 'models/dt_model.sav'
# pickle.dump(dt_model, open(filename, 'wb'))
