import re

with open('vedic_agi.cpp', 'r') as f:
    code = f.read()

# New keyword list - multi-word first, then single words
new_kws = '''    {"karma yoga",46},{"bhakti yoga",47},{"jnana yoga",48},{"machine learning",16},
    {"deep learning",17},{"brahman",0},{"atman",1},{"karma",2},{"dharma",3},
    {"yoga",4},{"meditation",5},{"moksha",6},{"upanishad",7},
    {"gita",8},{"guna",9},{"pranayama",10},{"ayurveda",11},
    {"mantra",12},{"samadhi",13},{"veda",14},{"intelligence",15},
    {"quantum",18},{"light",19},{"gravity",20},{"photosynthesis",21},
    {"dna",22},{"periodic",23},{"energy",24},{"organic",25},{"farming",25},
    {"crop",26},{"irrigation",27},{"soil",28},{"monsoon",29},{"rain",29},
    {"biodiversity",30},{"india",31},{"sanskrit",32},{"indus",33},
    {"hindi",36},{"peace",37},{"education",38},{"music",39},
    {"innovation",40},{"compassion",41},{"truth",42},{"universe",43},
    {"water",44},{"math",45},{"ahimsa",49},{"satya",50},
    {"asteya",51},{"brahmacharya",52},{"aparigraha",53},'''

# Replace the old KW array
old_pattern = r'KW kws\[\] = \{.*?\};'
code = re.sub(old_pattern, 'KW kws[] = {\n' + new_kws + '\n};', code, flags=re.DOTALL)

with open('vedic_agi.cpp', 'w') as f:
    f.write(code)

print("Keywords reordered — multi-word first")
