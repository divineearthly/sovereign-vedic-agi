#include <cstdio>
#include <cstring>
#include <cmath>
#include <ctime>
#include <cstdlib>

#define PHI 1.618033988749895
#define DIM 128
#define MAX_MEM 256

struct ChittaSlot {
    char key[256];
    float emb[DIM];
    time_t timestamp;
    float importance;
};

struct ChittaMemory {
    ChittaSlot slots[MAX_MEM];
    int count;
    FILE* disk;
    
    void init(const char* path = "chitta.mem") {
        count = 0;
        disk = fopen(path, "a+b");
        if(disk) {
            fseek(disk, 0, SEEK_END);
            long size = ftell(disk);
            count = size / sizeof(ChittaSlot);
            if(count > MAX_MEM) count = MAX_MEM;
            fseek(disk, 0, SEEK_SET);
            fread(slots, sizeof(ChittaSlot), count, disk);
            printf("🕉 Chitta loaded %d memories\n", count);
        }
    }
    
    void embed(const char* text, float* emb) {
        for(int d=0; d<DIM; d++) emb[d] = 0;
        for(int i=0; text[i]; i++)
            for(int d=0; d<DIM; d++)
                emb[d] += sinf(text[i]*d*PHI/DIM + i*0.1f) * cosf((text[i]+d)*3.14159f/DIM) * 0.02f;
        float n=0; for(int d=0; d<DIM; d++) n += emb[d]*emb[d];
        if(n>1e-8f){ n=1.0f/sqrtf(n); for(int d=0; d<DIM; d++) emb[d]*=n; }
    }
    
    void store(const char* text) {
        if(count >= MAX_MEM) {
            int worst=0;
            for(int i=1; i<MAX_MEM; i++)
                if(slots[i].importance < slots[worst].importance) worst=i;
            count = worst;
        }
        ChittaSlot* s = &slots[count];
        strncpy(s->key, text, 255);
        embed(text, s->emb);
        s->timestamp = time(nullptr);
        s->importance = 0.5f;
        count++;
        
        if(disk){ fseek(disk,0,SEEK_END); fwrite(s,sizeof(ChittaSlot),1,disk); fflush(disk); }
    }
    
    const char* recall(const char* query) {
        float qe[DIM]; embed(query, qe);
        float best = -1e9f;
        int bi = 0;
        for(int i=0; i<count; i++) {
            float dot=0;
            for(int d=0; d<DIM; d++) dot += qe[d]*slots[i].emb[d];
            float recency = 1.0f/(1.0f+(time(nullptr)-slots[i].timestamp)/3600.0f);
            float score = dot * slots[i].importance * recency;
            if(score > best){ best=score; bi=i; }
        }
        if(best < 0.1f) return nullptr;
        slots[bi].importance *= 1.1f;
        return slots[bi].key;
    }
    
    ~ChittaMemory() { if(disk) fclose(disk); }
};

int main(int argc, char** argv) {
    ChittaMemory chitta;
    chitta.init();
    
    if(argc > 1 && strcmp(argv[1],"recall")==0 && argc>2) {
        const char* mem = chitta.recall(argv[2]);
        printf("%s\n", mem ? mem : "[No relevant memory]");
        return 0;
    }
    if(argc > 1 && strcmp(argv[1],"store")==0 && argc>2) {
        chitta.store(argv[2]);
        printf("Stored: %s\n", argv[2]);
        return 0;
    }
    
    printf("Chitta Memory: %d slots\n", chitta.count);
    printf("Usage: %s store \"text\" | %s recall \"query\"\n", argv[0], argv[0]);
    return 0;
}
