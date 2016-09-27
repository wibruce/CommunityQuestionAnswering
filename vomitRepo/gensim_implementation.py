from gensim import corpora, models, similarities
from six import iteritems
from QuestionFileCreator import CreateFilePath
import logging
import os

# Create the uniform filepath for saving documents
new_dest = CreateFilePath('genImp1')


logging.basicConfig(filename=new_dest +'.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


######################
# Memory Friendly Implementation
######################

# This type of dictionary apparently wont eat all of your memory...ram rum ram rum....
stops = set('for a of the and to in'.split())
# collect stats about all tokens
dictionary = corpora.Dictionary(line.lower().split() for line in open('myfile.txt'))
# remove stopwords
stop_ids = [dictionary.token2id[stopword] for stopword in stops if stopword in dictionary.token2id]
# remove words only appearing once
once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)
dictionary.compactify()
dictionary.save(new_dest +'.dict')


#########################
# Create a corpus from the memory friendly dictionary implementation
#########################
class MyCorpus(object):
	def __iter__(self):
		for line in open('myfile.txt'):
			yield dictionary.doc2bow(line.lower().split())

# Create the corpus based off of myfile.txt
corpus = MyCorpus()

# Save corpus as Matrix Market file

#corpora.MmCorpus.serialize(new_dest +'.mm', corpus)

# or SVMlight format, Blei LDA-C, GibbsLDA++

#corpora.SvmLightCorpus.serialize('./tmp/corpus.svmlight', corpus)
#corpora.BleiCorpus.serialize('./tmp/corpus.lda-c', corpus)
#corpora.LowCorpus.serialize('./tmp/corpus.low', corpus)



#########################
# Implementing a Transformation
#########################

# Initialize a weighted model
tfidf = models.TfidfModel(corpus) 

# Apply transformation to an entire corpus
corpus_tfidf = tfidf[corpus]
	# for doc in corpus_tfidf:
	# 	print doc

# Initialize an LSI transformation(Latent Semantic Indexing)
# Transform the weighted tfidf corpus into latent 2-d space(num_topics = dimensions)
# num_topics should be between 200-500 as that has found to be the sweet spot...
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
corpus_lsi = lsi[corpus_tfidf]

# Save the model to disk for later
lsi.save(new_dest +'.lsi')
lsi = models.LsiModel.load(new_dest +'.lsi')

##########################
# Queries with cosine similarities
#########################

# Need to enter all documents which need comparison against subsequent queries
# !!NOTE!!: 
#	Running MatricSimilarity with a large set of documents( >= 1,000,000) coupled with a large
#	number of features will hog a lot of RAM(1M @ 256 feature_count = >2GB RAM)
# 	If RAM is an issue, use similarities.Similarity 

## TODO: Fix it
	# This is broken as the current MyCorpus clas outputs an object which has no len()
index = similarities.MatrixSimilarity(lsi[corpus])


# index.save(new_dest +'.index')
# index = similarities.MatrixSimilarity.load(new_dest +'.index')

# Perform a similarity query against the corpus( returns a bunch of 2-tuples)


sims = index[vec_lsi]

# sort the result
sims = sorted(enumerate(sims), key=lambda item: -item[1])

for key, value in sims[:10]:
	print key
	print questions[key]
	print value
	print "************"






