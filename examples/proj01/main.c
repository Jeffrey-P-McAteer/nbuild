
#include <stdio.h>

int main(int argc, char** argv) {
  char* name = "World";
  if (argc > 1) {
    name = argv[1];
  }
  //printf("I got %d arguments!\n", argc);
  printf("Hello %s!\n", name);
  fflush(stdout);
  //printf("Hello World!\n", name);
  return 0;
  //return 1;
}

