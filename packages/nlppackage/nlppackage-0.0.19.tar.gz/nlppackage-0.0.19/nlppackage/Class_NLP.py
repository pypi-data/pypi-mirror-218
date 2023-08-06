import spacy
import pandas as pd
import re
from unidecode import unidecode
import treetaggerwrapper
tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR='C:\TreeTagger')


class NLP:
    def __init__(self):
        # Initialisation de la classe NLP 
        # On utilise spacy, on charge le modèle fr_core_news_sm et on initialise le tokenizer et les stopwords
        self.nlp = spacy.load('fr_core_news_sm', disable=['parser', 'ner'])
        self.tokenizer = self.nlp.tokenizer
        self.stopwords = spacy.lang.fr.stop_words.STOP_WORDS

    def tokenize(self, text):
        return [token.text for token in self.tokenizer(text)]

    def cleanStopWord(self, text, add_stopwords=[], remove_stopwords=[]):
        stopwords = [
            word for word in self.stopwords if word not in remove_stopwords]
        stopwords.extend(add_stopwords)
        if isinstance(text, str):
            tokens = text.split(' ')
        elif isinstance(text, list):
            tokens = text
        else:
            raise ValueError("Invalid input type for text.")
        return ' '.join([token for token in tokens if token.lower() not in stopwords])

    def lowercaseText(self, text):
        # Cette méthode permet de mettre un texte en minuscule
        return text.lower()

    def cleanText(self, text, keep_numbers=True, exception=''):
        # Cette méthode permet de nettoyer un texte en supprimant tous les caractères spéciaux, sauf ceux spécifiés dans l'argument exception
        if keep_numbers and exception:
            pattern = re.compile('[^A-Za-z0-9\xe0-\xff '+exception+']')
        elif keep_numbers:
            pattern = re.compile('[^A-Za-z0-9\xe0-\xff]')
        elif exception:
            pattern = re.compile('[^A-Za-z\xe0-\xff '+exception+']')
        else:
            pattern = re.compile('[^A-Za-z\xe0-\xff]')

        cleaned_text = pattern.sub(' ', text)
        return cleaned_text

    def cleanAccent(self, text):
        # Cette méthode permet de supprimer les accents d'un texte en les remplaçant par les lettres correspondantes sans accent
        cleaned_text = unidecode(text)
        return cleaned_text

    def lemmatisation(self, text, lemma_exclu, keep_numbers=True, exlu_type_word=[]):
        tokenisation_majuscule = list()
        majuscule_tokenised = ''
        tags = tagger.tag_text(str(text), nosgmlsplit=True)
        for tag in tags:
            word, mottag, lemma = tag.split()
            if len(lemma.split('|')) > 1:
                lemma = lemma.split('|')[0]
            if word in lemma_exclu.keys():
                lemma = lemma_exclu[word]
            if keep_numbers:
                if mottag == 'NUM':
                    lemma = word
            pos = mottag.split(':')[0]
            if pos not in exlu_type_word:
                majuscule_tokenised = majuscule_tokenised + ' ' + lemma

        tokenisation_majuscule.append(majuscule_tokenised)
        return (' '.join(tokenisation_majuscule))


