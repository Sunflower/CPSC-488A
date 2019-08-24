import xml.etree.ElementTree as ET
import csv

it = ET.iterparse("2541/2541/VUAMC.xml")
# Get rid of namespace prefix of XML tags.
for _, el in it:
    if '}' in el.tag:
        el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
root = it.root


# Open a CSV file for writing.
with open('words.csv', 'w') as words_f, open ('sentences.csv', 'w') as sentences_f, \
    open('paragraphs.csv', 'w') as paragraphs_f, open('texts.csv', 'w') as texts_f:
    words_writer = csv.writer(words_f)
    sentences_writer = csv.writer(sentences_f)
    paragraphs_writer = csv.writer(paragraphs_f)
    texts_writer = csv.writer(texts_f)

    # Write headers.
    words_header = ["word_id", "word", "lemma", "word_type", 'function', "seg_type",
        "sentence_id", "paragraph_id", "text_id"]
    sentences_header = ["sentence_id", "sentence"]
    paragraphs_header = ["paragraph_id", "paragraph"]
    texts_header = ["texts_id", "text"]
    words_writer.writerow(words_header)
    sentences_writer.writerow(sentences_header)
    paragraphs_writer.writerow(paragraphs_header)
    texts_writer.writerow(texts_header)

    # IDs for CSV tables.
    word_id = 0
    sentence_id = 0
    paragraph_id = 0
    text_id = 0
    for text_element in root.iter('text'):
        text = []
        for paragraph_element in text_element.iter('p'):
            paragraph = []
            for sentence_element in paragraph_element.iter('s'):
                sentence= []
                # Make sentence.
                for i, word_char_element in enumerate(sentence_element):
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
                    # Process based on type of punctuation.
                    if word_char_element.tag == 'c' or word_type == 'POS':
                        if len(sentence) > 0:
                            sentence[-1] = sentence[-1] + word
                        else:
                            sentence.append(word)
                        continue

                    sentence.append(word)

                    csv_row = [word_id, word.lstrip(), lemma, word_type, function, seg_type,
                               sentence_id, paragraph_id, text_id]
                    words_writer.writerow(csv_row)

                    word_id += 1

                sentence = ' '.join(sentence)
                paragraph.append(sentence)

                csv_row = [sentence_id, sentence]
                sentences_writer.writerow(csv_row)

                sentence_id += 1

            paragraph = ' '.join(paragraph)
            text.append(paragraph)

            csv_row = [paragraph_id, paragraph]
            paragraphs_writer.writerow(csv_row)

            paragraph_id += 1

        text = '\n'.join(text)
        csv_row = [text_id, text]
        texts_writer.writerow(csv_row)

        text_id += 1
