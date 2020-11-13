
#include <stdio.h>

int main(int argc, char** argv) {
  char* name = "World";
  char user_input[24];

  if (argc > 1) {
    name = argv[1];
  }
  else {
    // Prompt user interactively
    printf("What is your name? ");
    fflush(stdout);

    scanf("%s", &user_input);

    name = user_input;
  }
  
  printf("Hello %s!\n", name);
  fflush(stdout);
  
  return 0;
}

