import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import chi2
from sklearn import metrics
from sklearn.model_selection import cross_validate as cv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
import seaborn as sns
import re
from sklearn.externals import joblib
#Importing labeled data--------------------------------------------------------------------------------------------
df = pd.read_csv('labeled.csv', sep=";",names=['Tweets', 'category_id'])
df.drop_duplicates()
category_name =  {'1':'Events','2':'Career','3':'Sport','4':'Science','5':'Politics','6':'Education','7':'Culture','8':'Freebies'}
#Creating chart of the categories----------------------------------------------------------------------------------
def plot():	
	COLOR = 'white'
	plt.rcParams['text.color'] = COLOR
	plt.rcParams['axes.labelcolor'] = COLOR
	plt.rcParams['xtick.color'] = COLOR
	plt.rcParams['ytick.color'] = COLOR
	plt.rc('axes',edgecolor=COLOR)
plot()
fig = plt.figure(figsize=(8,6))
fig.suptitle('Number of tweets in each category', fontsize=16)
df.groupby('category_id').Tweets.count().plot.bar(ylim=0,tick_label=category_name.values()).set_facecolor((0.12, 0.12, 0.09))
fig.set_facecolor((0.12, 0.12, 0.09))
plt.show()
#Vectorizing tweets---------------------------------------------------------------------------------------------
my_stop_words = text.ENGLISH_STOP_WORDS.union(["qmul"],["student"],["queen"],["mary"],["elaine"],["university"])
tfidf = TfidfVectorizer(min_df=2,ngram_range=(1, 2), stop_words=my_stop_words)
features = tfidf.fit_transform(df.Tweets.values.astype('U'))
labels = df.category_id
features.shape
#Printing top features per class--------------------------------------------------------------------------------
N = 4
for category_id in range(1,9):
  features_chi2 = chi2(features, labels == category_id)
  indices = np.argsort(features_chi2[0])
  feature_names = np.array(tfidf.get_feature_names())[indices]
  unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
  bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
  print("Most correlated for {}:".format(category_name[str(category_id)]))
  print("Unigrams:\n {}".format('\n '.join(unigrams[-N:])))
  print("Bigrams:\n {}".format('\n '.join(bigrams[-N:])))
#Naive bayes cross-validation----------------------------------------------------------------------------------
X1, X2, y1, y2 = train_test_split(features, labels, random_state = 19, test_size=0.5)
model1 = MultinomialNB().fit(X1, y1).predict(X2)
model2 = MultinomialNB().fit(X2, y2).predict(X1)
print(accuracy_score(y1, model2))
print(accuracy_score(y2, model1))
#Naive bayes model training------------------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(features, labels, random_state = 19, test_size=0.2)
model = MultinomialNB().fit(X_train, y_train)
expected = y_test
predicted = model.predict(X_test)
#Sample prediction and evaluation of the model-----------------------------------------------------------------
print(model.predict(tfidf.transform(['Free giveaway will take place on the library square tomorow at 5 pm!'])))
print (metrics.confusion_matrix(expected, predicted))
print(metrics.classification_report(expected, predicted))
#Creating confusion matrix diagram-----------------------------------------------------------------------------
sns.set()
plt.clf()
plot()
mat = confusion_matrix(y_test, predicted)
plt.suptitle('Confusion matrix', fontsize=16)
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
            xticklabels=category_name.values(), yticklabels=category_name.values())
plt.xlabel('true label')
plt.ylabel('predicted label');
plt.show()
#Sampling from the full dataset-------------------------------------------------------------------------------
alldata = pd.read_csv('dict.csv', sep=";",names=['Tweets', 'category_id'])
print(len(alldata))
regex = re.compile('[^a-zA-Z]')
for i in range(1,30000, 5999):
	print(alldata.Tweets.iloc[i])
	idl=str(model.predict(tfidf.transform([alldata.Tweets.iloc[i]]))).replace('[', '').replace(']', '')
	print('  '+category_name[idl], end='\n\n')
#Saving the model----------------------------------------------------------------------------------------------
filename1 = 'model.sav'
filename2 = 'tfidf.sav'

joblib.dump(model, filename1)
joblib.dump(tfidf, filename2)
