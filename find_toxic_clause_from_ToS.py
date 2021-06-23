import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from itertools import islice
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.parsing.preprocessing import preprocess_string
from sklearn.base import BaseEstimator
from sklearn import utils as skl_utils
from tqdm import tqdm
from sklearn.neural_network import MLPRegressor

import multiprocessing
import numpy as np

tos_df = pd.read_csv('./whole.csv', index_col=False, header=0)
#print(tos_df.head())
tos_df = tos_df[['Content']]

aggregate_counter = Counter()
for row_index, row in tos_df.iterrows():
    c = Counter(row['Content'].split())
    aggregate_counter += c

common_words = [word[0] for word in aggregate_counter.most_common(50)]
common_words_counts = [word[1] for word in aggregate_counter.most_common(50)]

def barplot(words, words_counts, title):
    fig = plt.figure(figsize=(18,10))
    bar_plot = sns.barplot(x=words, y=words_counts)
    for item in bar_plot.get_xticklabels():
        item.set_rotation(90)
    plt.title(title)
    plt.show()

def key_word_counter(tupple):
    return tupple[1]

all_word_counts = sorted(aggregate_counter.items(), key=key_word_counter)
uncommon_words = [word[0] for word in islice(all_word_counts, 50)]
uncommon_word_counts = [word[1] for word in islice(all_word_counts, 50)]

#barplot(words=common_words, words_counts=common_words_counts, title='Most Frequent Words used in Terms of Service')
#barplot(words=uncommon_words, words_counts=uncommon_word_counts, title='Least Frequent Words used in Terms of Service')

class Doc2VecTransformer(BaseEstimator):

    def __init__(self, vector_size=100, learning_rate=0.005, epochs=20):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self._model =None
        self.vector_size = vector_size
        self.workers = multiprocessing.cpu_count() - 1

    def fit(self, df_x, df_y=None):
        tagged_x = [TaggedDocument(str(row['Content']).split(), [index]) for index, row in df_x.iterrows()]
        model = Doc2Vec(documents=tagged_x, vector_size=self.vector_size, workers=self.workers)

        for epoch in range(self.epochs):
            model.train(skl_utils.shuffle([x for x in tqdm(tagged_x)]), total_examples=len(tagged_x), epochs=1)
            model.alpha -= self.learning_rate
            model.min_alpha = model.alpha

        self._model = model
        return self

    def transform(self, df_x):
        return np.asmatrix(np.array([self._model.infer_vector(str(row['Content']).split())
                                    for index, row in df_x.iterrows()]))

doc2vec_tr = Doc2VecTransformer(vector_size=300)
doc2vec_tr.fit(tos_df)
doc2vec_vectors = doc2vec_tr.transform(tos_df)



auto_encoder = MLPRegressor(hidden_layer_sizes=(600, 150, 600))
auto_encoder.fit(doc2vec_vectors, doc2vec_vectors)
predicted_vectors = auto_encoder.predict(doc2vec_vectors)

# print(doc2vec_vectors)
# print(predicted_vectors)
print(auto_encoder.score(predicted_vectors, doc2vec_vectors))

pd.DataFrame(auto_encoder.loss_curve_).plot()
plt.show()