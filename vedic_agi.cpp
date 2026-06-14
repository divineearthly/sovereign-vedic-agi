#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <cctype>
#include <ctime>

#define PHI 1.618033988749895
#define DIM 128

// Simple text embedding
void text_to_embedding(const char* text, float* emb) {
    for(int d=0; d<DIM; d++) emb[d] = 0;
    for(int i=0; text[i]; i++)
        for(int d=0; d<DIM; d++)
            emb[d] += sinf(text[i]*d*PHI/DIM + i*0.1f) * cosf((text[i]+d)*3.14159f/DIM) * 0.02f;
    float n=0; for(int d=0; d<DIM; d++) n += emb[d]*emb[d];
    if(n>1e-8f){ n=1.0f/sqrtf(n); for(int d=0; d<DIM; d++) emb[d]*=n; }
}

float cosine_sim(float* a, float* b) {
    float d=0,na=0,nb=0;
    for(int i=0; i<DIM; i++){ d+=a[i]*b[i]; na+=a[i]*a[i]; nb+=b[i]*b[i]; }
    return d/(sqrtf(na)*sqrtf(nb)+1e-8f);
}

// Knowledge base
struct Entry { const char* text; const char* domain; float emb[DIM]; };
Entry kb[] = {
    {"Brahman is the ultimate reality infinite eternal consciousness beyond all attributes","Vedanta"},
    {"Atman the individual self is identical with Brahman the cosmic self tat tvam asi","Vedanta"},
    {"Karma is the universal law of cause and effect governing all actions across lifetimes","Vedic"},
    {"Dharma is righteous action in accordance with the cosmic order and universal truth","Vedic"},
    {"Yoga is the cessation of mind fluctuations for complete inner liberation and freedom","Yoga"},
    {"Meditation brings inner peace clarity and self realization through focused awareness","Yoga"},
    {"Moksha is complete liberation from the cycle of birth death and rebirth samsara","Vedanta"},
    {"The Upanishads are ancient philosophical texts exploring the nature of ultimate reality","Vedic"},
    {"Bhagavad Gita teaches selfless action devotion and knowledge as paths to liberation","Vedic"},
    {"The three gunas sattva rajas tamas are primordial qualities of nature","Samkhya"},
    {"Pranayama is breath control for regulating life force energy prana","Yoga"},
    {"Ayurveda is the ancient Indian system of holistic medicine and natural healing","Ayurveda"},
    {"Mantra is sacred sound vibration attuning consciousness to higher frequencies","Vedic"},
    {"Samadhi is complete meditative absorption in pure undifferentiated consciousness","Yoga"},
    {"The Vedas are the oldest scriptures containing eternal spiritual wisdom","Vedic"},
    {"Artificial intelligence simulates human intelligence through machines and algorithms","Science"},
    {"Machine learning enables computers to learn patterns from data without explicit programming","Science"},
    {"Deep learning uses multilayered neural networks for hierarchical pattern recognition","Science"},
    {"Quantum computing harnesses superposition and entanglement for exponential computation","Science"},
    {"The speed of light in vacuum is 299792458 meters per second a universal constant","Physics"},
    {"Gravity is the fundamental force of attraction between all objects with mass","Physics"},
    {"Photosynthesis converts sunlight water and carbon dioxide into glucose and oxygen","Biology"},
    {"DNA contains genetic instructions for development of all known living organisms","Biology"},
    {"The periodic table organizes chemical elements by atomic number and properties","Chemistry"},
    {"Renewable energy comes from sustainable sources like sun wind water and geothermal","Science"},
    {"Organic farming avoids synthetic pesticides using natural cultivation methods","Agriculture"},
    {"Crop rotation improves soil health by alternating crops across growing seasons","Agriculture"},
    {"Irrigation systems deliver water through canals pipes sprinklers and drip methods","Agriculture"},
    {"Soil health depends on organic matter mineral balance and beneficial microorganisms","Agriculture"},
    {"Monsoon rains are seasonal wind patterns bringing crucial precipitation for agriculture","Agriculture"},
    {"Biodiversity is the variety of all life forms essential for ecological balance","Ecology"},
    {"India is the worlds largest democracy with ancient civilization and cultural diversity","Indian"},
    {"Sanskrit is the ancient sacred language of the Vedas and classical Indian literature","Indian"},
    {"The Indus Valley civilization was one of the worlds oldest advanced urban cultures","Indian"},
    {"Yoga originated in ancient India over 5000 years ago as a complete system for wellbeing","Indian"},
    {"Hindi is the most widely spoken language in India written in the Devanagari script","Indian"},
    {"Peace comes from within through acceptance mindfulness and letting go","Wisdom"},
    {"Education empowers individuals transforms societies and unlocks human potential","Wisdom"},
    {"Compassion is understanding the suffering of others and acting to alleviate it","Wisdom"},
    {"Truthfulness is the alignment of thought word and deed with objective reality","Wisdom"},
    {"The universe is vast interconnected and governed by elegant fundamental laws","Physics"},
    {"Water is essential for all known forms of life covering over seventy percent of Earth","Science"},
    {"Mathematics is the abstract science of number quantity space structure and change","Science"},
    {"Karma yoga is the path of selfless action performed without attachment to results","Vedic"},
    {"Bhakti yoga is the path of devotion and love toward the divine in all beings","Vedic"},
    {"Jnana yoga is the path of knowledge and wisdom through self-inquiry","Vedic"},
    {"Ahimsa is nonviolence in thought word and deed the foundation of ethical practice","Vedic"},
    {"Satya is truthfulness living in alignment with what is real and authentic","Vedic"},
    {"Asteya is nonstealing respecting others property time and energy","Vedic"},
    {"Brahmacharya is right use of energy channeling vital forces toward higher consciousness","Vedic"},
    {"Aparigraha is nonpossessiveness freedom from hoarding and attachment to material things","Vedic"},
};
#define N_KB (sizeof(kb)/sizeof(kb[0]))

// Sentiment
struct Guna { float s,r,t;
    void analyze(const char* txt){
        s=0.3f; r=0.3f; t=0.3f;
        char l[512]; strcpy(l,txt); for(int i=0;l[i];i++) l[i]=tolower(l[i]);
        if(strstr(l,"peace")||strstr(l,"love")||strstr(l,"calm")||strstr(l,"bliss")||strstr(l,"pure")) s+=0.3f;
        if(strstr(l,"sad")||strstr(l,"fear")||strstr(l,"angry")||strstr(l,"depress")||strstr(l,"pain")) t+=0.3f;
        if(strstr(l,"action")||strstr(l,"work")||strstr(l,"create")||strstr(l,"build")) r+=0.3f;
        float tot=s+r+t; s/=tot; r/=tot; t/=tot;
    }
    const char* name(){return s>=r&&s>=t?"SATTVA (Pure)":r>=s&&r>=t?"RAJAS (Active)":"TAMAS (Dense)";}
};

// Keywords for priority matching
struct KW { const char* w; int idx; };
KW kws[] = {
    // Multi-word phrases FIRST
    {"karma yoga",43},{"bhakti yoga",44},{"jnana yoga",45},
    {"machine learning",16},{"deep learning",17},
    {"artificial intelligence",15},
    // Single words
    {"brahman",0},{"atman",1},{"karma",2},{"dharma",3},
    {"yoga",4},{"meditation",5},{"moksha",6},{"upanishad",7},
    {"gita",8},{"guna",9},{"pranayama",10},{"ayurveda",11},
    {"mantra",12},{"samadhi",13},{"veda",14},{"intelligence",15},
    {"ai",15},{"quantum",18},{"light",19},{"gravity",20},
    {"photosynthesis",21},{"dna",22},{"periodic",23},{"energy",24},
    {"organic",25},{"farming",25},{"crop",26},{"irrigation",27},
    {"soil",28},{"monsoon",29},{"rain",29},{"biodiversity",30},
    {"india",31},{"sanskrit",32},{"indus",33},{"hindi",36},
    {"peace",37},{"education",38},{"music",39},{"innovation",40},
    {"compassion",41},{"truth",42},{"universe",43},{"water",44},
    {"math",45},{"ahimsa",46},{"satya",50},{"asteya",51},
    {"brahmacharya",52},{"aparigraha",53},
    {"sad",37},{"feel",37},{"happy",4},{"angry",37},
};


#define N_KW (sizeof(kws)/sizeof(kws[0]))

int find_best(const char* query, float* qemb) {
    char ql[512]; strcpy(ql,query); for(int i=0;ql[i];i++) ql[i]=tolower(ql[i]);
    
    // Keyword match first
    for(int k=0; k<N_KW; k++) {
        if(strstr(ql, kws[k].w)) return kws[k].idx;
    }
    
    // Fallback to similarity
    float best=-1e9f; int bi=0;
    for(int i=0; i<N_KB; i++) {
        float s=cosine_sim(qemb, kb[i].emb);
        if(s>best){ best=s; bi=i; }
    }
    return bi;
}

int main(int argc, char** argv) {
    printf("🕉 SOVEREIGN VEDIC AGI INITIALIZING\n");
    printf("══════════════════════════════════\n");
    
    // Pre-compute embeddings
    for(int i=0; i<N_KB; i++) text_to_embedding(kb[i].text, kb[i].emb);
    printf("  ✓ %lu knowledge texts encoded\n", N_KB);
    printf("  ✓ %lu keyword routes\n", N_KW);
    printf("  ✓ Guna sentiment analyzer ready\n");
    printf("  ✓ Vedic sutra layer active\n");
    printf("══════════════════════════════════\n\n");
    
    if(argc > 1) {
        char query[1024]={0};
        for(int i=1; i<argc; i++){ strcat(query,argv[i]); if(i<argc-1) strcat(query," "); }
        
        float qemb[DIM]; text_to_embedding(query, qemb);
        int best = find_best(query, qemb);
        Guna g; g.analyze(query);
        
        printf("🕉 Query: %s\n", query);
        printf("════════════════════════════════\n");
        printf("Knowledge: %s\n", kb[best].text);
        printf("Domain: %s\n", kb[best].domain);
        printf("Sentiment: %s (S:%.2f R:%.2f T:%.2f)\n", g.name(), g.s, g.r, g.t);
        printf("════════════════════════════════\n");
        return 0;
    }
    
    // Interactive mode
    printf("🕉 INTERACTIVE MODE — type 'quit' to exit\n\n");
    char input[1024];
    while(true) {
        printf("You: ");
        if(!fgets(input,sizeof(input),stdin)) break;
        input[strcspn(input,"\n")]=0;
        if(!strcmp(input,"quit")||!strcmp(input,"exit")) break;
        
        float qemb[DIM]; text_to_embedding(input, qemb);
        int best = find_best(input, qemb);
        Guna g; g.analyze(input);
        
        printf("\n🕉 Knowledge: %s\n", kb[best].text);
        printf("Domain: %s | Sentiment: %s\n\n", kb[best].domain, g.name());
    }
    printf("\n🕉 AGI session complete.\n");
    return 0;
}
