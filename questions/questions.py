import nltk
import sys
import os
import string
from collections import defaultdict
import math
nltk.download('stopwords')
FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    print("Loading Data: ")
    files = {}
    for file in os.listdir(directory):
        with open(os.path.join(directory, file)) as f:
            files[file] = f.read()
    return files



def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.word_tokenize(document)
    filtered_words = []
    for word in words:
        word = word.lower()
        punctuation = word in string.punctuation
        stopword = word in nltk.corpus.stopwords.words("english")
        if not punctuation and not stopword:
            filtered_words.append(word)
    return filtered_words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = {}
    occurances = {}
    for filename, words in documents.items():
        found_words = set()
        for word in words:
            if word not in found_words:
                found_words.add(word)
                try:
                    occurances[word] += 1
                except KeyError:
                    occurances[word] = 1
    for word in occurances:
        idfs[word] = math.log(len(documents.items())/occurances[word])
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    scores = {}
    returnFiles = []
    for word in query:
        idf = idfs[word]
        for file, words in files.items():
            if word in words:
                count = 0
                for fileWord in words:
                    if fileWord == word:
                        count += 1
                try:
                    scores[file] += idf * count
                except KeyError:
                    scores[file] = idf * count
    for k, v in sorted(scores.items(), key=lambda item: item[1], reverse = True):
        returnFiles.append(k)
    return returnFiles[:n:]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_scores = {}
    returnSentences = []
    for word in query:
        for sentence, words in sentences.items():
            count = 0
            if word in words:
                try:
                    sentence_scores[sentence] += idfs[word]
                except KeyError:
                    sentence_scores[sentence] = idfs[word]
            for sentenceword in words:
                if sentenceword in query:
                    count += 1
            termDensity = count / len(words)
            if termDensity > 0:
                try:
                    sentence_scores[sentence] += termDensity
                except KeyError:
                    sentence_scores[sentence] = termDensity

    for k, v in sorted(sentence_scores.items(), key=lambda item: item[1], reverse = True):
        returnSentences.append(k)
    return returnSentences[:n:]


if __name__ == "__main__":
    main()
