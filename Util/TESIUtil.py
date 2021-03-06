import os
import shutil
import jellyfish
import distance
import Util.SmithWaterman as SmithWaterman
import re

HONOR_STOP_WORDS = ['ser', 'lord', 'commander', 'queen', 'regent', 'king', 'princess', 
					'prince','lady', 'grand', 'maester', 'mad', 'septa', 'quickly', 'priestess',
					'aunt', 'stormborn', 'jokingly', 'great', 'khal']

def create_or_replace_dir(dir_path):
	if (os.path.isdir(dir_path)):
		shutil.rmtree(dir_path)
	os.makedirs(dir_path)

def save_file(path, filename, text):
	text_file = open(build_dir_path(path, filename), 'w')
	text_file.write(text)
	text_file.close()

def build_dir_path(*paths):
	path = "."
	for p in paths:
		path += "/" + p
	return path

def index_of(lst, value):
	try:
		n = lst.index(value)
		return n
	except ValueError:
		return -1

def string_similarity(str1, str2):
	str1 = str1.replace("'s", '').replace("ʼs", "")
	str2 = str2.replace("'s", '').replace("ʼs", "")
	str1 = " ".join(re.findall("[a-zA-Z]+", str1))
	str2 = " ".join(re.findall("[a-zA-Z]+", str2))

	if(str1 in str2 or str2 in str1):
		temp1 = str1.split(' ')
		temp2 = str2.split(' ')
		if(temp1[len(temp1)-1] == temp2[len(temp2)-1] and (len(temp1) == 1 or len(temp2) == 1)):
			cont = 0.5
		else:
			cont = 1
	else:
		cont = 0
	jaro = jellyfish.jaro_winkler(str1, str2)
	#sw = SmithWaterman.distance(str1, str2)
	
	return cont*0.4 + jaro*0.6# + sw*0.1

def dict_to_list(dic):
	result_list = []
	for key in dic:
		if(dic[key] not in result_list):
			result_list.append(dic[key])
	return result_list

def remove_honor_words(string):
	result = ''
	temp = string.split(' ')
	
	for s in temp:
		if(s.lower() not in HONOR_STOP_WORDS):
			result += s + ' '

	return result.strip()

ENGLISH_STOP_WORDS = frozenset([
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves", ""])