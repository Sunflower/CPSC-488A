import os
import glob
import subprocess
import csv

# Go to ELKB directory from the parent directory of this file.
dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(os.path.join(dir, '../ELKB'))

with open('../data/train/longest_chains.csv', 'w', encoding='utf-8') as f:
    csv_writer = csv.writer(f, delimiter=',')
    csv_writer.writerow(('paragraph_id', 'longest_chain'))

    for file_name in glob.glob('../data/train/paragraphs/paragraph*.txt'):
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

            longest_chain = []
            len_longest_chain = 0
            for r in result:
                chain = [word.strip()
                         for word in r.split('[')[0].split(',')]
                if len(chain) >= len_longest_chain:
                    longest_chain.extend(chain)
            # longest_chain = result[3]
            # longest_chain = [word.strip() for word in longest_chain.split('[')[0].split(',')]
            longest_chain = ' '.join(longest_chain)

            # line = '{},{}'.format(paragraph_id, longest_chain)
            # f.write(line + '\n')
            row = [paragraph_id, longest_chain]
            print('Writing longest chain for paragraph {}\n'.format(paragraph_id))
            csv_writer.writerow(row)
