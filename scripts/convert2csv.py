# import xml.etree.ElementTree as ET
import lxml.etree as ET
import csv
import os

XML_NAMESPACE = '{http://www.w3.org/XML/1998/namespace}'

it = ET.iterparse("../data/VUAMC3.xml")
# Get rid of namespace prefix of XML tags.
for _, el in it:
    if '}' in el.tag:
        el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
root = it.root


os.chdir('../data/raw')
# Open a CSV file for writing.
with open('words.csv', 'w') as words_f, open ('sentences.csv', 'w') as sentences_f, \
    open('paragraphs.csv', 'w') as paragraphs_f, open('texts.csv', 'w') as texts_f:
    words_writer = csv.writer(words_f)
    sentences_writer = csv.writer(sentences_f)
    texts_writer = csv.writer(texts_f)

    # Write headers.
    words_header = ["word_id", "word", "lemma", "word_type", 'function', "seg_type",
        "sentence_id","text_id"]
    sentences_header = ["sentence_id",  "paragraph_id", "sentence"]
    texts_header = ["text_id", "text"]
    words_writer.writerow(words_header)
    sentences_writer.writerow(sentences_header)
    texts_writer.writerow(texts_header)

    # IDs for CSV tables.
    word_id = 0
    sentence_id = 0
    paragraph_id = 0
    text_id = None
    num_text_ids = 0
    text_ids = set()
    for root_text_element in root.find('text'):
        for text_element in root_text_element.iter('text'):
            text_id = text_element.get(XML_NAMESPACE + 'id', default='')
            text_ids.add(text_id)
            print(text_id)
            num_text_ids += 1

            text = []
            for sentence_element in text_element.iter('s'):
                # Check if sentence belongs to a paragraph.
                paragraph_id = -1
                parent = sentence_element.getparent()
                if parent.tag == 'p':
                    paragraph_id = parent.get('n')

                sentence = []
                # Make sentence.
                for word_char_element in sentence_element:
                    # Initialize word attributes for the row..
                    word, lemma, word_type, function, seg_type = '', '', '', '', ''

                    if word_char_element.text is None:
                        continue

                    word = word_char_element.text.rstrip()

                    # If contains a seg, include seg function and seg type values.
                    seg = word_char_element.find("seg")
                    if seg is not None:
                        if seg.text is None:
                            continue
                        word = seg.text.rstrip()

                        function = seg.get('function', default='')
                        seg_type = seg.get('type', default='')

                    lemma = word_char_element.get('lemma', default='')
                    word_type = word_char_element.get('type', default='')

                    # Don't write punctuation into words CSV.
                    if word_char_element.tag == 'c' or word_type == 'POS':
                        if len(sentence) > 0:
                            sentence[-1] = sentence[-1] + word
                        else:
                            sentence.append(word)
                        continue

                    if not word:
                        continue
                    sentence.append(word)

                    csv_row = [word_id, word.lstrip(), lemma, word_type, function, seg_type,
                                sentence_id, text_id]
                    words_writer.writerow(csv_row)

                    word_id += 1

                sentence = ' '.join(sentence)

                if not sentence:
                    continue
                text.append(sentence)

                csv_row = [sentence_id, paragraph_id, sentence]
                sentences_writer.writerow(csv_row)

                sentence_id += 1

            text = '\n'.join(text)
            csv_row = [text_id, text]
            texts_writer.writerow(csv_row)

print(len(text_ids))

print("Num texts: {}".format(num_text_ids))
print("Num sentences: {}".format(sentence_id))
