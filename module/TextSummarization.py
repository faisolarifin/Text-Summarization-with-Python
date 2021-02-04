import re
import numpy as np
from networkx import from_scipy_sparse_matrix, pagerank
from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from Sastrawi.StopWordRemover.StopWordRemoverFactory import ArrayDictionary, StopWordRemoverFactory, StopWordRemover

class TextSummarization():
    def __init__(self):
        with open('./stopwords.txt') as f:
            more_stopword=f.read().split('\n')
        
        SWfactory = StopWordRemoverFactory()
        stopword_data = ArrayDictionary(more_stopword+SWfactory.get_stop_words())
        self.stopword = StopWordRemover(stopword_data)

    def Preprocessing(self, text):        
        clean = re.sub("#[^\W]+|@[^\W]+|http[^*\s]+|<[^>]*>|[0-9]", '', text) #cleansing data
        emoticons = re.findall('(?::|;|=)()(?:-)?(?:\)|\(|D|P)', clean)
        text = (re.sub('[\W]+', ' ', clean.lower()) +  #Case folding
                ' '.join(emoticons).replace('-', ''))
        result=''
        for kata in text.split(): 
            stop = self.stopword.remove(kata) #Stopword 
            result += f"{stop} " if stop else ''
        return result

    def Summary(self, doc, preprocess=False):
        doc_tokenizer = PunktSentenceTokenizer()
        sentences_list = doc_tokenizer.tokenize(doc)

        clean_sentences_list=[] 
        for sentence in sentences_list:
            clean_sentences_list.append(self.Preprocessing(sentence)) 

        cv = CountVectorizer()
        cv_matrix = cv.fit_transform(clean_sentences_list if preprocess else sentences_list)
        normal_matrix = TfidfTransformer().fit_transform(cv_matrix)

        tfidf=normal_matrix.toarray()
        res_graph = normal_matrix * normal_matrix.T # similaritas /adjacency matrix

        nx_graph= from_scipy_sparse_matrix(res_graph)
        pageranks = pagerank(nx_graph)

        sentence_array = sorted(((pageranks[i], s) for i, s in enumerate(sentences_list)), reverse=True)
        sentence_array = np.asarray(sentence_array)

        rank_max = float(sentence_array[0][0])
        rank_min = float(sentence_array[len(sentence_array) - 1][0])

        temp_array = []

        # Jika semua rank sama
        # taking any sentence will give the summary, say the first sentence
        flag = 0
        if rank_max - rank_min == 0:
            temp_array.append(0)
            flag = 1

        # If the sentence has different ranks
        if flag != 1:
            for i in range(0, len(sentence_array)):
                temp_array.append((float(sentence_array[i][0]) - rank_min) / (rank_max - rank_min))
        
        # Calculation of threshold:
        # We take the mean value of normalized scores
        # any sentence with the normalized score 0.2 more than the mean value is considered to be 
        threshold = (sum(temp_array) / len(temp_array))# + 0.2

        # Separate out the sentences that satiasfy the criteria of having a score above the threshold
        sentence_list = []
        if len(temp_array) > 1:
            for i in range(0, len(temp_array)):
                if temp_array[i] > threshold:
                        sentence_list.append(sentence_array[i][1])
        else:
            sentence_list.append(sentence_array[0][1])

        summary = " ".join(str(x) for x in sentence_list)

        return summary