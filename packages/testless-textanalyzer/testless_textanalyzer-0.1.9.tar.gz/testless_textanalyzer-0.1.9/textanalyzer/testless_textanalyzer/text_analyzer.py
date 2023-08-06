import nltk
import re
from textanalyzer.testless_textanalyzer.crf import LinearChainCRF

class TextAnalyzer():
    def __init__(self, path_to_model):
        self.crf = LinearChainCRF()
        self.crf.load(path_to_model)
    

    def analyze(self, sentences):

        sentences_data = []

        processed_senteces = []

        for sentence in sentences:

            processed_text = self.text_processing(sentence)

            self.tokens, self.pos = self.text_tokenization_and_pos(
                processed_text)

            sentence_data = self.get_sentence_data()
 
            sentences_data.append(sentence_data)
            
            processed_senteces.append(processed_text)

        predicted_entities = self.crf.predict(sentences_data)

        return self.mapping_entities_to_words(processed_senteces, predicted_entities)

    def text_tokenization_and_pos(self, text):

        tokens = text.split()

        pos_tuple = nltk.pos_tag(tokens)

        pos_result = [pos[1] for index, pos in enumerate(pos_tuple)]

        return tokens, pos_result

    def text_processing(self, text):

        text = re.sub('[%s]' % re.escape(
            """!"#$%&'*,،;<>؟?[]^`{|}~"""), ' ', text)  # remove punctuation
        
        if not text.endswith('.'):
            text += ' .'
            
        return text

    def get_sentence_data(self):

        sentence_data = []

        for token, word_pos in zip(self.tokens, self.pos):
            sentence_data.append((token, word_pos))
            
        return sentence_data


    def mapping_entities_to_words(self, sentences, predicted_entities):
        result = []
        for sentence, entities in zip(sentences, predicted_entities):
            senntence_words = sentence.split()
            sentence_entities = {}
            ass, act, targ, val = '', '', '', ''
            'targ', 'val'
            for word, entity in zip(senntence_words, entities):
                if entity.endswith('assert'):
                    ass += word + ' '
                elif entity.endswith('act'):
                    act += word + ' '
                elif entity.endswith('targ'):
                    targ += word + ' '
                elif entity.endswith('val'):
                    val += word + ' '

            if val != '':
                sentence_entities["value"] = val.strip()
            if targ != '':
                sentence_entities["target"] = targ.strip()
            if act != '':
                sentence_entities["action"] = act.strip()
            if ass != '':
                sentence_entities["assertion"] = ass.strip()

            result.append(sentence_entities)

        return result
