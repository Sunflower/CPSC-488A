import os
import glob
import subprocess
import csv

os.chdir('../ELKB')

with open('../data/longest_chains.csv', 'w', encoding='utf-8') as f:
    csv_writer = csv.writer(f, delimiter=',')
    csv_writer.writerow(('paragraph_id', 'longest_chain'))

    for file_name in glob.glob('../data/paragraphs/paragraph*.txt'):
        paragraph_id = os.path.splitext(os.path.basename(file_name))[
            0].split('_')[-1]

        with open(file_name, 'r', encoding='utf-8') as g:
            result = subprocess.run('java applications/LexicalChain -f {}'.format(file_name),
                stdout=subprocess.PIPE)

            result = result.stdout.decode('utf-8')

            result = result.strip().split('\n')

            # Does not contain a lexical chain.
            if len(result) < 4:
                continue

            longest_chain = result[3]
            longest_chain = [word.strip() for word in longest_chain.split('[')[0].split(',')]
            longest_chain = ' '.join(longest_chain)

            # line = '{},{}'.format(paragraph_id, longest_chain)
            # f.write(line + '\n')
            row = [paragraph_id, longest_chain]
            csv_writer.writerow(row)
