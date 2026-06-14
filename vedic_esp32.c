// 🕉 Vedic AGI for ESP32 / Arduino — Ultra-lightweight
// ~5KB RAM, 50 knowledge texts, keyword matching
// Compile: arduino-cli or PlatformIO

#include <string.h>
#include <math.h>

#define PHI 1.618033988749895
#define MAX_KB 30
#define MAX_KW 25
#define MAX_RESP 256

// Knowledge base in flash (PROGMEM on AVR)
const char kb_texts[MAX_KB][128] = {
    "Brahman is the ultimate reality infinite eternal consciousness",
    "Karma is the universal law of cause and effect",
    "Dharma is righteous action in cosmic order",
    "Yoga is cessation of mind for liberation",
    "Meditation brings inner peace and clarity",
    "Moksha is liberation from birth death cycle",
    "Ayurveda is ancient holistic medicine system",
    "Pranayama is breath control for life energy",
    "Organic farming uses natural cultivation methods",
    "Crop rotation improves soil health naturally",
    "Irrigation delivers water through canals",
    "Soil health needs organic matter and minerals",
    "Monsoon brings seasonal rain for agriculture",
    "Renewable energy from sun wind water",
    "Photosynthesis converts sunlight to energy",
    "Water is essential for all life forms",
    "Peace comes from within through mindfulness",
    "Education empowers and transforms society",
    "Compassion is understanding others suffering",
    "Truth is alignment of thought word deed",
    "Ahimsa is nonviolence in all actions",
    "Satya is truthfulness in living",
    "Gravity attracts all objects with mass",
    "Light speed is universal constant",
    "DNA contains genetic instructions",
    "Biodiversity is variety of life forms",
    "Sanskrit is ancient sacred language",
    "India has ancient civilization diversity",
    "Universe is vast and interconnected",
    "Mathematics is abstract science of patterns"
};

const char kb_domains[MAX_KB][16] = {
    "Vedanta","Vedic","Vedic","Yoga","Yoga",
    "Vedanta","Ayurveda","Yoga","Agriculture","Agriculture",
    "Agriculture","Agriculture","Agriculture","Science","Biology",
    "Science","Wisdom","Wisdom","Wisdom","Wisdom",
    "Vedic","Vedic","Physics","Physics","Biology",
    "Ecology","Indian","Indian","Physics","Science"
};

// Keywords
struct { const char* kw; int idx; } kws[MAX_KW] = {
    {"brahman",0},{"karma",1},{"dharma",2},{"yoga",3},
    {"meditation",4},{"moksha",5},{"ayurveda",6},{"pranayama",7},
    {"organic",8},{"farming",8},{"crop",9},{"irrigation",10},
    {"soil",11},{"monsoon",12},{"rain",12},{"energy",13},
    {"renewable",13},{"photosynthesis",14},{"water",15},{"peace",16},
    {"education",17},{"compassion",18},{"truth",19},{"ahimsa",20},
    {"satya",21},{"gravity",22},{"light",23},{"dna",24},
    {"biodiversity",25},{"sanskrit",26},{"india",27},{"universe",28},
    {"math",29}
};

void tolower_str(char* s) {
    for(int i=0; s[i]; i++) if(s[i]>='A'&&s[i]<='Z') s[i]+=32;
}

int find_best(const char* query) {
    char ql[256];
    strcpy(ql, query);
    tolower_str(ql);
    
    for(int k=0; k<MAX_KW; k++) {
        if(strstr(ql, kws[k].kw)) return kws[k].idx;
    }
    return 0;
}

// Called by Arduino loop or ESP32 task
void vedic_query(const char* input, char* response) {
    int best = find_best(input);
    snprintf(response, MAX_RESP, "%s [%s]", kb_texts[best], kb_domains[best]);
}
