/*
 * A small program that counts the number of occurrens of a word in a text.
 *
 *  ./main "Mikkel" "This is Mikkel, and this is a test Mikkel."
 *  2
 *
 * echo "Mikkel is awesome" | grep -o "Mikkel" | wc -l
 * 1
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
  // We ignore sanity checks for better readability!

  const char *word_to_find = argv[1];
  const char *text = argv[2];

  char *founded_word;
  unsigned int number_of_occurrences = 0;

  // Loop over ever occurrences of the word to find.
  while ((founded_word = strstr(text, word_to_find)) != NULL)
  {
    /* As strstr returns a pointer to the first occurrences of the word to
     * find, we must then update our search scope by moving the text pointer
     * to only include our new search scope + the length of the word to find.
     *
     * Example
     * founded_word = "Mikkel, and this is a test Mikkel."
     * -> text = ", and this is a test Mikkel."
     */
    text = founded_word + strlen(word_to_find);
    number_of_occurrences++;
  }

  printf("%d\n", number_of_occurrences);

  return EXIT_SUCCESS;
}