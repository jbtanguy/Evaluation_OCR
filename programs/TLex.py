import sys
import io
import glob
from bs4 import BeautifulSoup
import editdistance
import matplotlib.pyplot as plt

def get_lexical_entries(lex_path):
	print('Début de l\'acquisition du lexique...')
	lex = []
	inFile = io.open(lex_path, mode='r', encoding='utf-8')
	line = inFile.readline()
	while line != '':
		if '<orthography>' in line and '</orthography>' in line:
			lex_entry = line.strip().replace('\t', '').replace('<orthography>', '').replace('</orthography>', '')
			lex.append(lex_entry)
		line = inFile.readline()
	inFile.close()
	print('Fin.')
	return lex

def pourcent_tokens_in_lex(soup, lex):
	nb_tokens = 0
	nb_in = 0
	for span in soup.find_all('span'):  # tokens are in: <span class="ocrx_word">
		if span.get('class') == ['ocrx_word']:
			txt = span.get_text()
			if txt.lower() in lex:
				nb_in += 1
			nb_tokens += 1
	return nb_tokens, nb_in

def get_min_edit_distance(token, lex):
	distances = [editdistance.eval(token, l) for l in lex]
	return min(distances)


def mean_edit_distance__nearest_lex(soup, lex):
	nb_tokens = 0
	sum_ed = 0
	for span in soup.find_all('span'):  # tokens are in: <span class="ocrx_word">
		if span.get('class') == ['ocrx_word']:
			txt = span.get_text()
			sum_ed += get_min_edit_distance(txt, lex)
			nb_tokens += 1
	return nb_tokens, sum_ed

if __name__ == '__main__':
	dir_path = sys.argv[1]
	lex_path = sys.argv[2]

	lex_file = io.open(lex_path, mode='r', encoding='utf-8')
	lex = set([w.strip() for w in lex_file.readlines()])
	

	for file in glob.glob(dir_path + '*.html'):
		inFile = io.open(file, mode='r', encoding='utf-8') 
		html = inFile.read()
		soup = BeautifulSoup(html, features='html.parser') # parsing
		nb_tokens, nb_in = pourcent_tokens_in_lex(soup, lex)
		if nb_tokens != 0:
			tx = 100 * nb_in / nb_tokens
			print(file + '\t' + str(tx))
		else:
			print(file + '\t' + str(0))