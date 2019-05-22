import xml.etree.ElementTree as ET
import csv

it = ET.iterparse("2541/2541/VUAMC.xml")
# Get rid of namespace prefix of XML tags.
for _, el in it:
    if '}' in el.tag:
        el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
root = it.root


# Open a CSV file for writing.
with open('VUAMC.csv', 'w') as f:
    writer = csv.writer(f)

    # Write header.
    header = ["ID", "word", "lemma", "sentence", "metaphor"]
    writer.writerow(header)

    word_id = 0
    for sentence in root.iter("s"):
        sentence_txt = []

        # Make sentence.
        for word_or_c in sentence:
            text = word_or_c.text
            if text is None:
                continue

            seg = word_or_c.find("seg")
            if seg is not None:
                if seg.text is None:
                    continue
                text = seg.text

            sentence_txt.append(text.strip())

        sentence_txt_str = ' '.join(sentence_txt)

        for i, word in enumerate(sentence_txt):
            # Skip single charactersf (probably punctuation).
            if sentence[i].tag == 'c':
                continue

            lemma = sentence[i].get("lemma")
            csv_row = [word_id, word, lemma, sentence_txt_str, "N/A"]
            writer.writerow(csv_row)

            word_id += 1
