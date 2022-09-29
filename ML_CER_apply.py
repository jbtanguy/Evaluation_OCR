from glob import glob
import numpy as np
import fastwer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from TLex import TLEX_page
from TConf import TCON_page
from matplotlib import pyplot
from scipy.stats.stats import pearsonr
import pickle
import io

dir_path = 'path/to/corpus/html/KRAKEN/'

# Lexicon 
lex_path = 'path/to/lexical/resource/in/extension'
lex_file = io.open(lex_path, mode='r', encoding='utf-8')
lex = set([w.strip() for w in lex_file.readlines()])

X = {}
TC, TL = [], []

for html_path in glob(dir_path + '*'):
	if '.html' in html_path:
		txt_path = html_path.replace('/html/', '/txt/').replace('.html', '.txt')
	else:
		txt_path = html_path.replace('/alto/', '/txt/').replace('.alto', '.txt')
	OCR_txt = open(txt_path).read()
	# variables descriptives -> X
	nb_chars = len(OCR_txt)
	nb_words = len(OCR_txt.split())
	nb_spaces = OCR_txt.count(' ')
	prop_spaces = nb_spaces / nb_chars if nb_chars != 0 else 0
	nb_MAJ = sum(1 for c in OCR_txt if c.isupper())
	prop_MAJ = nb_MAJ / nb_chars if nb_chars != 0 else 0
	nb_min = sum(1 for c in OCR_txt if c.islower())
	prop_min = nb_min / nb_chars if nb_chars != 0 else 0
	nb_punct = sum(1 for c in OCR_txt if c in ',?;.:/!§*%$£^¨=}+)]°@\\_`|-[(\'#"~&€«»¶ŧ←↓“”')
	prop_ponct = nb_punct / nb_chars if nb_chars != 0 else 0
	nb_s = OCR_txt.count('s') # erreur s long 1
	nb_S = OCR_txt.count('f') # erreur s long 2
	prop_s = nb_s / nb_chars if nb_chars != 0 else 0
	prop_S = nb_S / nb_chars if nb_chars != 0 else 0
	val_con = TCON_page(html_path)
	val_lex = TLEX_page(html_path, lex)
	TC.append(val_con)
	TL.append(val_lex)
	descriptors = [nb_chars, nb_words, nb_spaces, nb_MAJ, nb_min, nb_punct, prop_spaces, prop_MAJ, prop_min, prop_ponct, nb_s, nb_S, prop_s, prop_S, val_lex, val_con]
	X[html_path] = descriptors

loaded_model = pickle.load(open('CER_predictor.mlmodel', 'rb'))

predictions = []
for html_path, descriptors in X.items():
	html_name = html_path.split('/')[-1]
	CER_pred = loaded_model.predict([descriptors])
	predictions.append(CER_pred[0])

print(str(sum(predictions)/len(predictions)))
print(str(sum(TC)/len(TC)))
print(str(sum(TL)/len(TL)))