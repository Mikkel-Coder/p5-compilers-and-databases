/*
 * Opgave 1. b)
 *
 * implementer den opstillede automat i selvvalgt sprog fx. C.
 */

#include <stdio.h>
#include <string.h>

enum State
{
    STATE_0,
    STATE_1,
    STATE_2,
    STATE_3,
    STATE_4,
    STATE_5,
    STATE_6
};

int main(int argc, char *argv[])
{
    enum State myState = STATE_0;
    unsigned char *input = argv[1];

    for (int i = 0; i < strlen(input); i++)
    {
        switch (myState)
        {
        case STATE_0:
            if (input[i] == 'a' || input[i] == 'b')
            {
                myState = STATE_1;
                break;
            }

            myState = STATE_6;
            break;

        case STATE_1:
            if (input[i] == 'a')
            {
                myState = STATE_2;
                break;
            }

            myState = STATE_6;
            break;

        case STATE_2:
            if (input[i] == 'b')
            {
                myState = STATE_3;
                break;
            }

            myState = STATE_6;
            break;

        case STATE_3:
            if (input[i] == 'c')
            {
                myState = STATE_4;
                break;

            }

            myState = STATE_6;
            break;
            
        case STATE_4:
            if (input[i] == 'd')
            {
                myState = STATE_5;
                break;
            }

            myState = STATE_6;
            break;

        case STATE_5:
            myState = STATE_6;
            break;

        case STATE_6:
            myState = STATE_6;
            break;
        }
    };

    printf("My state is: %d\n", myState);

    return 0;
}