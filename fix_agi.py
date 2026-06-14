import re

with open('vedic_agi_core.cpp', 'r') as f:
    code = f.read()

# Fix the broken sed insert - remove the goto/label hack
old = '''    // Step 3.5: Keyword priority matching
    char qlow[512];
    strcpy(qlow, query);
    for(int i=0; qlow[i]; i++) qlow[i] = tolower(qlow[i]);
    
    struct { const char* kw; int idx; } keywords[] = {
        {"brahman", 0}, {"atman", 1}, {"karma", 2}, {"dharma", 3},
        {"yoga", 4}, {"meditation", 5}, {"moksha", 6}, {"upanishad", 7},
        {"gita", 8}, {"guna", 9}, {"pranayama", 10}, {"ayurveda", 11},
        {"mantra", 12}, {"samadhi", 13}, {"veda", 14},
        {"ai", 15}, {"intelligence", 15}, {"machine learning", 16},
        {"deep learning", 17}, {"quantum", 18}, {"light", 19},
        {"gravity", 20}, {"photosynthesis", 21}, {"dna", 22},
        {"periodic", 23}, {"energy", 24}, {"renewable", 24},
        {"organic", 25}, {"farming", 25}, {"crop", 26},
        {"irrigation", 27}, {"soil", 28}, {"monsoon", 29},
        {"rain", 29}, {"biodiversity", 30}, {"india", 31},
        {"sanskrit", 32}, {"indus", 33}, {"hindi", 36},
        {"peace", 37}, {"education", 38}, {"music", 39},
        {"innovation", 40}, {"compassion", 41}, {"truth", 42},
        {"universe", 43}, {"water", 44}, {"math", 45},
        {"karma yoga", 46}, {"bhakti", 47}, {"jnana", 48},
        {"ahimsa", 49}, {"satya", 50}, {"asteya", 51},
        {"brahmacharya", 52}, {"aparigraha", 53},
    };
    int n_kw = sizeof(keywords)/sizeof(keywords[0]);
    for(int k=0; k<n_kw; k++) {
        if(strstr(qlow, keywords[k].kw)) {
            best_knowledge = keywords[k].idx;
            best_sim = 1.0f;
            goto found_by_keyword;
        }
    }
    found_by_keyword:'''

# Replace with correct version placed AFTER variable declarations
new = '''    // Step 3.5: Keyword priority matching
    {
        char qlow[512];
        strcpy(qlow, query);
        for(int i=0; qlow[i]; i++) qlow[i] = tolower(qlow[i]);
        
        struct { const char* kw; int idx; } keywords[] = {
            {"brahman", 0}, {"atman", 1}, {"karma", 2}, {"dharma", 3},
            {"yoga", 4}, {"meditation", 5}, {"moksha", 6}, {"upanishad", 7},
            {"gita", 8}, {"guna", 9}, {"pranayama", 10}, {"ayurveda", 11},
            {"mantra", 12}, {"samadhi", 13}, {"veda", 14},
            {"ai", 15}, {"intelligence", 15}, {"machine learning", 16},
            {"deep learning", 17}, {"quantum", 18}, {"light", 19},
            {"gravity", 20}, {"photosynthesis", 21}, {"dna", 22},
            {"periodic", 23}, {"energy", 24}, {"renewable", 24},
            {"organic", 25}, {"farming", 25}, {"crop", 26},
            {"irrigation", 27}, {"soil", 28}, {"monsoon", 29},
            {"rain", 29}, {"biodiversity", 30}, {"india", 31},
            {"sanskrit", 32}, {"indus", 33}, {"hindi", 36},
            {"peace", 37}, {"education", 38}, {"music", 39},
            {"innovation", 40}, {"compassion", 41}, {"truth", 42},
            {"universe", 43}, {"water", 44}, {"math", 45},
            {"karma yoga", 46}, {"bhakti", 47}, {"jnana", 48},
            {"ahimsa", 49}, {"satya", 50}, {"asteya", 51},
            {"brahmacharya", 52}, {"aparigraha", 53},
        };
        int n_kw = sizeof(keywords)/sizeof(keywords[0]);
        for(int k=0; k<n_kw; k++) {
            if(strstr(qlow, keywords[k].kw)) {
                best_knowledge = keywords[k].idx;
                best_sim = 1.0f;
                break;
            }
        }
    }'''

if old in code:
    code = code.replace(old, new)
    with open('vedic_agi_core.cpp', 'w') as f:
        f.write(code)
    print("Fixed: keyword matching now inside correct scope")
else:
    # The sed might have only partially inserted. Check.
    if 'best_knowledge = keywords[k].idx' in code:
        print("Partial insert detected. Restoring from backup...")
        import shutil
        shutil.copy('vedic_agi_core.cpp.bak', 'vedic_agi_core.cpp')
        print("Restored. Will re-insert correctly.")
        
        # Now insert properly - find Step 4 and insert before it
        old2 = '        // Step 4: Find best matching knowledge\n        float best_sim = -1e9f;\n        int best_knowledge = 0;'
        new2 = '''        // Step 3.5: Keyword priority matching
        {
            char qlow[512];
            strcpy(qlow, query);
            for(int i=0; qlow[i]; i++) qlow[i] = tolower(qlow[i]);
            
            struct { const char* kw; int idx; } keywords[] = {
                {"brahman", 0}, {"atman", 1}, {"karma", 2}, {"dharma", 3},
                {"yoga", 4}, {"meditation", 5}, {"moksha", 6}, {"upanishad", 7},
                {"gita", 8}, {"guna", 9}, {"pranayama", 10}, {"ayurveda", 11},
                {"mantra", 12}, {"samadhi", 13}, {"veda", 14},
                {"ai", 15}, {"intelligence", 15}, {"machine learning", 16},
                {"deep learning", 17}, {"quantum", 18}, {"light", 19},
                {"gravity", 20}, {"photosynthesis", 21}, {"dna", 22},
                {"periodic", 23}, {"energy", 24}, {"renewable", 24},
                {"organic", 25}, {"farming", 25}, {"crop", 26},
                {"irrigation", 27}, {"soil", 28}, {"monsoon", 29},
                {"rain", 29}, {"biodiversity", 30}, {"india", 31},
                {"sanskrit", 32}, {"indus", 33}, {"hindi", 36},
                {"peace", 37}, {"education", 38}, {"music", 39},
                {"innovation", 40}, {"compassion", 41}, {"truth", 42},
                {"universe", 43}, {"water", 44}, {"math", 45},
                {"karma yoga", 46}, {"bhakti", 47}, {"jnana", 48},
                {"ahimsa", 49}, {"satya", 50}, {"asteya", 51},
                {"brahmacharya", 52}, {"aparigraha", 53},
            };
            int n_kw = sizeof(keywords)/sizeof(keywords[0]);
            for(int k=0; k<n_kw; k++) {
                if(strstr(qlow, keywords[k].kw)) {
                    best_knowledge = keywords[k].idx;
                    best_sim = 1.0f;
                    goto skip_cosine;
                }
            }
        }
        
        // Step 4: Find best matching knowledge
        float best_sim = -1e9f;
        int best_knowledge = 0;'''
        
        if old2 in code:
            code = code.replace(old2, new2)
            # Also need to add the skip_cosine label after the cosine loop
            code = code.replace(
                '        // Step 5: Nyaya logic evaluation',
                '        skip_cosine:\n        \n        // Step 5: Nyaya logic evaluation'
            )
            with open('vedic_agi_core.cpp', 'w') as f:
                f.write(code)
            print("Inserted keyword matching correctly.")
        else:
            print("Could not find insertion point.")
else:
    print("No changes needed.")
