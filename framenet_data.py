import nltk
import pickle
import spacy
nlp = spacy.load("en_core_web_sm")  #lg?
nltk.download('framenet_v17')
from nltk.corpus import framenet as fn


def pos2id(start, end, text):
    idx = []
    index = 1
    doc = nlp(text)
    for token in doc:
        s, e = token.idx, token.idx + len(token)
        if s >= start and e <= end:
            idx.append(index)
        index += 1

    return idx

all_sentences = dict()
# a key is a sentence, value is a list of associated frames
for doc in fn.docs():
    for sentence in doc.sentence:
        if len(sentence.annotationSet) > 1:
            # There are associated frames
            frames = []
            skip = True  # skip first element (it's POS annotation)
            for annotation in sentence.annotationSet:
                if skip:
                    skip = False
                    continue
                if not annotation.LU.name.endswith(".v"):
                    continue  # skip non verb frames

                frame = dict()
                start, end = annotation['Target'][0]
                text = annotation.text[start:end + 1]
                frame['target'] = {annotation.frameName: pos2id(start, end, annotation.text)}
                #((start, end, annotation.text[start:end + 1]))
                frame_elements = []
                for frame_element in annotation.FE[0]:
                    start, end, tag = frame_element
                    text = annotation.text[start:end + 1]
                    element = {tag: pos2id(start, end, annotation.text)}
                    frame_elements.append(element)
                frame['elements'] = frame_elements
                frames.append(frame)
            if len(frames) > 0:
                all_sentences[sentence.text] = frames

with open('annotated_sentences.pkl', 'wb') as f:
    pickle.dump(all_sentences, f)
#with open('sentences.txt', 'w') as f:
#    for key in all_sentences.keys():
#        f.write(key)
#        f.write("\n")