# Une fonction pour avoir le mean confidence global pour la page
# Une fonction pour avoir le mean confidence pour tous les caractères pour la page
# Quand on revoit, on renvoie le mean confidence et le nombre de caractère !! important pour les métriques globales

import sys
import io
import glob
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

def get_confidences__page_level(soup):
	confidences_sum, tot = 0, 0

	for span in soup.find_all('span'): # tokens are in: <span class="ocrx_word">
		if span.get('class') == ['ocrx_word']:
			txt = span.get_text()
			nbChar = len(txt)
			t = span.get('title')
			confidences = t.split(';')[1].split(' ') # ['', 'x_confs', '0.5362149']
			confidences = confidences[2:]
			for c in confidences:
				confidences_sum += float(c)
				tot += 1

	return (confidences_sum, tot)

def get_confidences__char_level(soup):
	confidences_per_char = {}
	for span in soup.find_all('span'):  # tokens are in: <span class="ocrx_word">
		if span.get('class') == ['ocrx_word']:
			txt = span.get_text()
			nbChar = len(txt)
			t = span.get('title')
			confidences = t.split(';')[1].split(' ') # ['', 'x_confs', '0.5362149']
			confidences = confidences[2:]
			for i in range(nbChar):
				cur_char = txt[i]
				cur_conf = float(confidences[i])

				if cur_char not in confidences_per_char.keys():
					confidences_per_char[cur_char] = [cur_conf, 1]
				else:
					confidences_per_char[cur_char][0] += cur_conf
					confidences_per_char[cur_char][1] += 1

	return confidences_per_char



if __name__ == '__main__':

	dir_path = sys.argv[1]

	for file in glob.glob(dir_path + '*.html'):
		inFile = io.open(file, mode='r', encoding='utf-8') 
		html = inFile.read()
		soup = BeautifulSoup(html) # parsing
		sum_, tot = get_confidences__page_level(soup)
		if tot != 0: # we do not want an empty page
			mean = sum_ / tot
			print(file + '\t' + str(mean))
		else:
			print(file + '\t' + str(0))
