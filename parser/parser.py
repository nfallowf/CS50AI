import nltk
import sys
nltk.download('punkt')
import string
TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP | S P S | S NP | S P NP
NP -> N | Det N | AP N | N PP | NP ADP | Det AP N
VP -> V | V NP | V NP PP | V PP | ADP V | V ADP
PP -> P NP
AP -> Adj | Adj AP
ADP -> Adv | Adv ADP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))

def alphabetic(word):
    for char in word:
        if char in string.ascii_lowercase:
            return True
    return False

def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    filtered_words = []
    words = nltk.word_tokenize(sentence)
    for word in words:
        word = word.lower()
        if alphabetic(word):
            filtered_words.append(word)
    return filtered_words



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    np_chunks = []
    filtered_chuncks = []
    for node in tree.subtrees():
        if node.label() == "NP":
            for child_node in node.subtrees(lambda t: t.label() == 'NP'):
                if child_node not in np_chunks:
                    for subtree in child_node.subtrees():
                        if subtree.label() == "NP" and subtree != child_node:
                            break
                    else:
                        np_chunks.append(child_node)
    return np_chunks


if __name__ == "__main__":
    main()
