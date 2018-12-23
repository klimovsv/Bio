#!/usr/bin/env python3

f = open('/home/sergey/Downloads/uniprot_sprot.fasta', 'r')

seqs = []

current_title = ''
current_seq = ''

for line in f.readlines():
    if (line.startswith('>') or line.startswith('~')) and current_seq != '':
        seqs.append([
            current_title,
            current_seq
        ])
        current_seq = ''
    if line.startswith('~'):
        break
    if line.startswith('>'):
        current_title = line.split('|')[1].strip()
    else:
        current_seq += line.rstrip()

f.close()
with open('base.json', 'w+') as f:
    import json

    json.dump(seqs, f, ensure_ascii=False)
