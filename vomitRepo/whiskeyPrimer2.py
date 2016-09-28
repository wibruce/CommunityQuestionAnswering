"""
	This package pulls question and comment data from the 
	train and dev datasets found in the training repo and 
	applies the word2vec algorithm. Current implementation
	uses the skip-gram model- CBOW may be faster - skip-gram 
	is supposedly more accurate.

"""
__author__ = "whiskeyromeo"

import re, pprint
import xml.etree.ElementTree as ElementTree
#from bs4 import BeautifulSoup
from gensim.models import Word2Vec
#from nltk.corpus import stopwords
import nltk
stopwords = ['']

def getValues(tree, category):
    parent = tree.find(".//parent[@name='%s']" % category)
    return [child.get('value') for child in parent]

filePaths = [
	'../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-excluding-2016-questions-cleansed.xml',
	'../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-dev-reformatted-excluding-2016-questions-cleansed.xml',
	'../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-test-reformatted-excluding-2016-questions-cleansed.xml',
	#'../Data/dev/SemEval2016-Task3-CQA-QL-dev-subtaskA.xml',
	'../Data/train/SemEval2016-Task3-CQA-QL-train-part2-subtaskA.xml',
	'../Data/train/SemEval2016-Task3-CQA-QL-train-part1-subtaskA.xml'
]

"""
Returns an array populated with questions
The comments are nested in each question

"""
def elementParser(filepath):
	# construc the Element Tree and get the root
	tree = ElementTree.parse(filepath)
	root = tree.getroot()
	# create a list to store the pulled threads
	threadList = []
	# find each thread in the tree, starting at the root
	for Thread in root.findall('Thread'):
		# create a dict for each question
		QuestionDict = {}
		# find each question 
		relQuestion = Thread.find('RelQuestion')
		# pull the subject
		subject = relQuestion.find('RelQSubject').text
		#Pull the values from the questions into the relevant fields of the question dict
		QuestionDict['threadId'] = relQuestion.attrib['RELQ_ID']
		QuestionDict['subject'] = subject
		QuestionDict['question'] = relQuestion.find('RelQBody').text
		comments = []
		# Pull the comments from the filepath
		for relComment in Thread.findall('RelComment'):
			#create a dict for the comment
			commentDict = {}
			#populate the comment dict
			commentDict['comment'] = relComment.find('RelCText').text
			commentDict['comment_id'] = relComment.attrib['RELC_ID']
			comments.append(commentDict)
		# set the comments key to be equal to the question's comments
		QuestionDict['comments'] = comments
		#put the comments into the Question object
		threadList.append(QuestionDict)
	return threadList

thisList = []

for filePath in filePaths:
	thisList += elementParser(filePath)


questions = []
comments = []

"""
	sentence_to_wordlist
	:param question: string, question to parse
	:param remove_stopwords: boolean, default of False
	:returns: modified string
	.. note:: 
		Converts questions to words, takes bool remove_stopwords
		as an optional parameter which will remove stopwords as defined
		in nltk. Also subs out all punctuation.
	.. todo::
		Implement url, emoticon replacement as seen in SemanticZ
"""
def sentence_to_wordlist(question, remove_stopwords=False):
		question_text = BeautifulSoup(question).get_text()
		question_text = re.sub("[^a-zA-Z]", " ", question_text)
		words = question_text.lower().split()
		if remove_stopwords:
			stops = set(stopwords.words("english"))
			words = [w for w in words if not w in stops]
		return words

#tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

"""
	question_to_sentences
	:param question: string, question to tokenize
	:param tokenizer: package, nltk tokenizer to use
	:param remove_stopwords: bool, default of False
	:returns: modified string
"""
def question_to_sentences(question, tokenizer, remove_stopwords=False):
	raw_sentences = tokenizer.tokenize(question)
	sentences = []
	for raw_sentence in raw_sentences:
		if len(raw_sentence) > 0:
			sentences.append(sentence_to_wordlist( raw_sentence, remove_stopwords))
	return sentences

sentences = []
# for row in thisList:
# 	questions.append(row['question'])
# 	for comment in row['comments']:
# 		comments.append(comment['comment'])

# for question in questions:
# 	sentences += question_to_sentences(question, tokenizer)

# for comment in comments:
# 	sentences += question_to_sentences(comment, tokenizer)

#Train the model based on the kaggle input parameters, can easily be changed
# model = Word2Vec(sentences, workers=4, size=300, min_count=40, window=10, sample=1e-3)
model_name = "first_w2v_train_dev"

#Save the model so we can pull it back up at any point
# model.save(model_name)
#model = Word2Vec.load(model_name)


# Should test the accuracy of the model, currently not...
# TODO - get better output
#model.accuracy('./question-words.txt')

######################
## Cluster it up - Kaggle rip
######################
from sklearn.cluster import KMeans

# word_vectors = model.syn0
# num_clusters = word_vectors.shape[0]/5

# kmeans_clustering = KMeans(n_clusters = num_clusters)
# idx = kmeans_clustering.fit_predict( word_vectors )

# word_centroid_map = dict(zip(model.index2word, idx))

"""
	Straight from the Kaggle Bag of Popcorn Tut 3
"""
# def create_bag_of_centroids( wordlist, word_centroid_map ):
#     #
#     # The number of clusters is equal to the highest cluster index
#     # in the word / centroid map
#     num_centroids = max( word_centroid_map.values() ) + 1
#     #
#     # Pre-allocate the bag of centroids vector (for speed)
#     bag_of_centroids = np.zeros( num_centroids, dtype="float32" )
#     #
#     # Loop over the words in the review. If the word is in the vocabulary,
#     # find which cluster it belongs to, and increment that cluster count 
#     # by one
#     for word in wordlist:
#         if word in word_centroid_map:
#             index = word_centroid_map[word]
#             bag_of_centroids[index] += 1
#     #
#     # Return the "bag of centroids"
#     return bag_of_centroids

# centroids = np.zeros((len(sentences), num_clusters), dtype="float32")
# counter = 0
# for line in sentences:
# 	centroids[counter] = create_bag_of_centroids( line, word_centroid_map)
# 	counter += 1







