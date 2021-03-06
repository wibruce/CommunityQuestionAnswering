"""
Worse perfomance than standard model
"""

from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from nltk.corpus import stopwords
from random import shuffle
import sys
import os

sys.path.insert(0, os.path.absPath('..'))
from utils.QuestionFileCreator import getQuestions, getComments, QuestionCleaner, prepModelFolder, initializeLog
from utils.sourceFiles import thisList, origQfilePath
from D2V.doc2vec1 import createPredictionFile

initializeLog()

stops = set(stopwords.words('english'))


def prepLabeledSentList(questions = [], withStops = False):
	mod_questions = []
	for q in questions:
		#print('idx: ' + str(idx) + ' , question: ' + question)
		mod_questions.append(TaggedDocument([i for i in q['question'] if i not in stops], q['id']))
	return mod_questions

def altDoc2Vec(questions):
	mod_questions = prepLabeledSentList(questions)
	model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=8)
	model.build_vocab(mod_questions)
	shuffle(mod_questions)
	for epoch in range(10):
		model.train(mod_questions)
	return model

questions = getQuestions(thisList)
model = altDoc2Vec(questions)

createPredictionFile(origQfilePath, model)
