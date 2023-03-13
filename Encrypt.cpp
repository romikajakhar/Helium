#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <lmic.h>



static osjob_t sendjob;
static uint8_t mydata[] = "Hello, world!";
//static osEvent event;
static uint8_t counter = 0;


static u1_t randbuf[16] = { 0 };


int main()
{
    FILE* fp;
    char buffer[1024];
    int rows = 0;
    int next = 0; // add semicolon at end of line

    if (fopen_s(&fp, "rssi.csv", "r") == 0) {
        while (fscanf(buffer, sizeof(buffer), fp)) {
            // process the row of data
            for (int i = 0; i < 16; i++) { // changed starting index to 0
                for (int j = 0; j < 8; j++) {
                    uint8_t b;
                    // added check for end of buffer
                    if (buffer[next] == '\0') {
                        break;
                    }
                    while ((b = buffer[next] & 0x01) == (buffer[next + 1] & 0x01)) { // use buffer[next+1] instead of buffer[next++] to prevent incrementing next twice
                        next++;
                        printf("next=%d, buffer[next]=%c\n", next, buffer[next]);
                    }
                    randbuf[i] = (randbuf[i] << 1) | b;
                    next++; // increment next after processing bit
                }
            }
             // add newline character to print statement
            rows++;
            // reset next for next row of data
        }
        fclose(fp);
    }
    randbuf[0] = 16; // set initial index
    for (int i = 0; i < 16; i++) {
        for (int j = 7; j >= 0; j--) {
            printf("%d", (randbuf[i] >> j) & 0x01);
        }
        printf(" ");
    }
    printf("\n");
    printf("Read %d rows from rssi.csv\n", rows); // corrected filename in print statement
    os_aes(AES_ENC, randbuf, 16); // encrypt seed with any key
    return 0;
}

