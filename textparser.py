import nltk
from nltk.tokenize import PunktSentenceTokenizer


class textparser(object):
    def parse(self, input):
        sentences = nltk.sent_tokenize(input)
        tags = []
        for sent in sentences:
            tags += nltk.pos_tag(nltk.word_tokenize(sent))
        return tags

    def findorgs(self, input):
        tags = self.parse(input)
        orgs = [i[0] for i in list(filter(lambda x: x[1] == "NNP", tags))]
        return orgs


# textparser = textparser()
# textparser.findorgs(
#     'Whether you\'re new to programming or an experienced developer, it\'s easy to learn and use Python. My Name is Utkarsh Chauhan')
    