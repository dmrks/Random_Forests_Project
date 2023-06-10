import pandas as pd
import numpy as np
import codecademylib3
import matplotlib.pyplot as plt
import seaborn as sns

#Import models from scikit learn module:
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, RandomForestRegressor
from sklearn import tree
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
col_names = ['age', 'workclass', 'fnlwgt','education', 'education-num', 
'marital-status', 'occupation', 'relationship', 'race', 'sex',
'capital-gain','capital-loss', 'hours-per-week','native-country', 'income']
df = pd.read_csv('adult.data', header=None, names = col_names)

#Distribution of income

#df['income'].value_counts(normalize=True)

#Clean columns by stripping extra whitespace for columns of type "object"

for c in df.select_dtypes(include=['object']).columns:
    df[c] = df[c].str.strip()

#Create feature dataframe X with feature columns and dummy variables for categorical features
feature_cols = ['age','capital-gain', 'capital-loss','hours-per-week', 'sex','race']
X = pd.get_dummies(df[feature_cols],drop_first=True)
#Create output variable y which is binary, 0 when income is less than 50k, 1 when it is greather than 50k
y = np.where(df.income =='<=50K', 0, 1)

#Split data into a train and test set
x_train, x_test, y_train, y_test = train_test_split(X,y, random_state=1, test_size=.2)

#Instantiate random forest classifier, fit and score with default parameters  // accurancy score = 0.8185168125287886
rfc = RandomForestClassifier()
rfc.fit(x_train,y_train)
score1 =rfc.score(x_test,y_test)
print(score1)

#Tune the hyperparameter max_depth over a range from 1-25, save scores for test and train set
np.random.seed(0)
accuracy_train=[]
accuracy_test = []
depths = range(1,26)

for i in depths:
  rfc = RandomForestClassifier(max_depth = i)
  rfc.fit(x_train,y_train)
  rfc.fit(x_test,y_test)
  y_pred = rfc.predict(x_test)
  accuracy_test.append(accuracy_score(y_test, rfc.predict(x_test)))
  accuracy_train.append(accuracy_score(y_train,rfc.predict(x_train)))

#Find the best accuracy and at what depth that occurs = largest accuracy :0.8879164747428221 // depth :25

best_acc= np.max(accuracy_test)
best_depth = depths[np.argmax(accuracy_test)]

print(f"largest accuracy :{np.max(accuracy_test)}")
print(f"depth :{depths[np.argmax(accuracy_test)]}")

#Plot the accuracy scores for the test and train set over the range of depth values  
plt.plot(depths, accuracy_test,'bo--',depths, accuracy_train,'r*:')
plt.show()
plt.clf()

#Save the best random forest model and save the feature importances in a dataframe
best_rf = RandomForestClassifier(max_depth=best_depth)
best_rf.fit(x_train, y_train)
feature_imp_df = pd.DataFrame(zip(x_train.columns, best_rf.feature_importances_),  columns=['feature', 'importance'])
print('Top 5 random forest features:')
print(feature_imp_df.sort_values('importance', ascending=False).iloc[0:5])



#Create two new features, based on education and native country
df['education_bin'] = pd.cut(df['education-num'], [0,9,13,16], labels=['HS or less', 'College to Bachelors', 'Masters or more'])

feature_cols = ['age','capital-gain', 'capital-loss','hours-per-week', 'sex', 'race','education_bin']

#Use these two new additional features and recreate X and test/train split

X = pd.get_dummies(df[feature_cols],drop_first=True)
#Create output variable y which is binary, 0 when income is less than 50k, 1 when it is greather than 50k
y = np.where(df.income =='<=50K', 0, 1)

#Split data into a train and test set
x_train, x_test, y_train, y_test = train_test_split(X,y, random_state=1, test_size=.2)
rfc = RandomForestClassifier()
rfc.fit(x_train,y_train)
score1 =rfc.score(x_test,y_test)
print(score1)

#Tune the hyperparameter max_depth over a range from 1-25, save scores for test and train set
np.random.seed(0)
accuracy_train=[]
accuracy_test = []
depths = range(1,26)

for i in depths:
  rfc = RandomForestClassifier(max_depth = i)
  rfc.fit(x_train,y_train)
  rfc.fit(x_test,y_test)
  y_pred = rfc.predict(x_test)
  accuracy_test.append(accuracy_score(y_test, rfc.predict(x_test)))
  accuracy_train.append(accuracy_score(y_train,rfc.predict(x_train)))

#Find the best accuracy and at what depth that occurs

best_acc= np.max(accuracy_test)
best_depth = depths[np.argmax(accuracy_test)]

print(f"largest accuracy :{np.max(accuracy_test)}")
print(f"depth :{depths[np.argmax(accuracy_test)]}")

#Plot the accuracy scores for the test and train set over the range of depth values  
plt.plot(depths, accuracy_test,'bo--',depths, accuracy_train,'r*:')
plt.show()
plt.clf()

#Save the best random forest model and save the feature importances in a dataframe

best_rf = RandomForestClassifier(max_depth=best_depth)
best_rf.fit(x_train, y_train)
feature_imp_df = pd.DataFrame(zip(x_train.columns, best_rf.feature_importances_),  columns=['feature', 'importance'])
print('Top 5 random forest features:')
print(feature_imp_df.sort_values('importance', ascending=False).iloc[0:5])


