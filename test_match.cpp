#include <cstdio>
#include <cstring>
#include <cctype>
int main() {
    const char* query = "Explain karma yoga";
    char ql[512]; strcpy(ql, query);
    for(int i=0; ql[i]; i++) ql[i] = tolower(ql[i]);
    printf("Lowered: '%s'\n", ql);
    printf("strstr(ql, \"karma yoga\"): %p\n", (void*)strstr(ql, "karma yoga"));
    printf("strstr(ql, \"karma\"): %p\n", (void*)strstr(ql, "karma"));
    printf("strstr(ql, \"ahimsa\"): %p\n", (void*)strstr(ql, "ahimsa"));
    return 0;
}
