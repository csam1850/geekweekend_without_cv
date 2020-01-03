import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier  # noqa: F401
from sklearn.tree import DecisionTreeClassifier  # noqa: F401
from sklearn import metrics
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from load_data import load_fruit_data, FRUITS
from model_evaluation import plot_confusion_matrix

# Get Images and Labels
X, y = load_fruit_data(FRUITS, 'Training')
X_test, y_test = load_fruit_data(FRUITS, 'Test')

# Scale Data Images
scaler = StandardScaler()
X_train = scaler.fit_transform([i.flatten() for i in X])
X_test = scaler.fit_transform([i.flatten() for i in X_test])

print('training starts now')
# SVM
svm_model = SVC(gamma='auto', kernel='linear')
svm_model.fit(X_train, y)
y_pred = svm_model.predict(X_test)
precision = metrics.accuracy_score(y_pred, y_test) * 100
print("Accuracy with SVM: {0:.2f}%".format(precision))
# save models to disk
filename = 'models/svm_model.sav'
pickle.dump(svm_model, open(filename, 'wb'))

cm, _ = plot_confusion_matrix(y_test, y_pred, normalize=True)
plt.show()

# # K-NN
# knn_model = KNeighborsClassifier(n_neighbors=5)
# knn_model.fit(X_train, y)
# y_pred = knn_model.predict(X_test)
# precision = metrics.accuracy_score(y_pred, y_test) * 100
# print("Accuracy with K-NN: {0:.2f}%".format(precision))
# # save models to disk
# filename = 'models/knn_model.sav'
# pickle.dump(knn_model, open(filename, 'wb'))

# # DECISION TREE
# dt_model = DecisionTreeClassifier()
# dt_model.fit(X_train, y)
# y_pred = dt_model.predict(X_test)
# precision = metrics.accuracy_score(y_pred, y_test) * 100
# print("Accuracy with Decision Tree: {0:.2f}%".format(precision))
# # save models to disk
# filename = 'models/dt_model.sav'
# pickle.dump(dt_model, open(filename, 'wb'))
