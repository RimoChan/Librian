#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdio>
#include <cassert>

char *join(const char *s1, const char *s2) {
    char *result = (char *)malloc(strlen(s1) + strlen(s2) + 1);
    strcpy(result, s1);
    strcat(result, s2);
    return result;
}

int main(int argc, char *argv[]) {
    char *s = argv[0];
    printf("%s\n", s);
    char *a = strrchr(s, '\\') + 1, *b = strrchr(s, '.');
    b[0] = 0;
    printf("<%s>\n", a);
    char *name = join(join("_", a), ".kuzu");
    printf("[%s]\n", name);

    FILE *f = fopen(name, "r");
    assert(f != 0);

    int length;
    char *data;
    fseek(f, 0, SEEK_END);
    length = ftell(f);
    data = (char *)malloc((length + 1) * sizeof (char));
    rewind(f);
    length = fread(data, 1, length, f);
    data[length] = 0;
    fclose(f);

    printf("%s\n", data);

    system(data);
}
