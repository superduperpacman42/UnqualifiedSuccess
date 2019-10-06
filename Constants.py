import random

WIDTH = 560+300 # Screen width (pixels)
HEIGHT = 560 # Screen height (pixels)
TIME_STEP = 60 # Frames per second
GRID_SPACE = 40 # Grid square dimensions (pixels)
SCALE = 2 # Ratio of pixel art to screen pixels
GRID_X = 12 # Number of columns
GRID_Y = 12 # Number of rows
SPEED = 8/1000 # Grid squares per millisecond
FRAME_DURATION = 5
FONT_SIZE = 24

MALE = ["Bob", "Joe", "Carl", "Gregor", "Steven", "Howard", "Sam", "Luke","James","Oliver","Logan","Liam","Jake","Dylan"]
FEMALE = ["Julia", "Ella", "Rebecca", "Sally", "Rachel", "Lauren", "Lucy", "Laurel","Amelia","Sophia","Evelyn","Alice"]
NAMES = MALE + FEMALE # candidate names
random.shuffle(NAMES)

NOUNS = ["squizzle", "octolog", "drizzle", "obvorp", "corkscrew", "snik-snak", "plogger", "daxle", "clacker", "bellomatic", "zorp", "yik-yak", "glub-blub", "gabbergorn", 
"pentapack", "neezle", "jixle", "alegaxy", "logoplex", "glactor", "smallock", "hectoplast", "reezoid", "max-mox", "antipax", "razzle", "zim-zam", "rerailer", "pentact",
"unalloy", "glactave", "slich", "mesomode", "vaxle", "flazer", "minimack", "optate", "twivock", "cryoct","smect","mellery","tele-toc"]

ADJECTIVES = ["ralleable", "slovoid", "relemetric", "volular", "oblactic", "glovoid", "sneadly", "reractic","antectic","revoidal"]

EXTREMES = ["ralliest", "beeliest", "squiddle-most", "valliest", "meshiest", "zilliest", "sneelest", "clalliest"]

VERBS = ["revalate", "unplume", "slike", "squeedle", "blue-blate", "derazzle", "callivate", "quillify", "ellevize"]

JARGON = ["Python", "Java", "polynomials", "bits","leet","recursion",
		 "byte", "merge-sort", "quick-sort", "integer", "float"] # common answer choices

VOCAB = ["Python", "Java", "C++", "language", "sort", "list", "leet", "smart", "innovative", "fastest", "factor", "polynomials","recursion", "bits",
		 "byte", "developer", "merge-sort", "quick-sort", "closure", "integer", "float", "datatype", "biggest", "compiler", "cloud", "speed", "efficiency", "performance"]

alt = [["BaNaNa", "KiWi", "CoCoNUT", "FrUIT", "dice", "SALad", "innovative", "creative", "dextrous", "juiciest","slice", "GrapeFruit","spoons", "grapes",
		"bunch", "SALadSmith", "MiXER", "CuttingBoard", "BoWL", "ChErRy", "BluBERRY", "BERRY", "sweetest", "juicer", "produce", "tastiness", "firmness", "sweetness"]]

BITS_PER_BYTE = 4

W = {} # dictionary of vocab

def randomize():
	nouns = NOUNS[:]
	verbs = VERBS[:]
	adjectives = ADJECTIVES[:]
	extremes = EXTREMES[:]
	wordtypes = "nnnnvnaaaevnnnnnnnnnnnennnnn"
	for t, key in zip(wordtypes, VOCAB):
		if t == "n":
			word = random.choice(nouns)
			nouns.remove(word)
		elif t == "v":
			word = random.choice(verbs)
			verbs.remove(word)
		elif t == "e":
			word = random.choice(extremes)
			extremes.remove(word)
		elif t == "a":
			word = random.choice(adjectives)
			adjectives.remove(word)
		W[key] = "*"+word
	BITS_PER_BYTE = random.randint(2,8)
	W["Python"] = W["Python"].title()
	W["Java"] = W["Java"].title()


# for key, word in zip(VOCAB,alt[0]):
# 	if not key in W.keys():
# 		# print((key,word))
# # 		W[key] = "*"+word
# BITS_PER_BYTE = random.randint(2,8)