import nltk

nltk.download('punkt')
nltk.download('punkt_tab')


def split_into_sentences(text):

    sentences = nltk.sent_tokenize(text)

    return sentences