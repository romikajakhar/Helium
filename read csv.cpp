#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "lmic.h"
#include "lmic/oslmic.h"

uint8_t randbuf[16] = { 0 };

int main() {
    int data[1024] = { 0 };   // Array to store the integers from the CSV file
    int count = 0;
    int next = 0; // add semicolon at end of line
    memset(data, 255, sizeof(data));
    FILE* file;   // Open the CSV file in read mode

    if (fopen_s(&file, "rssi.csv", "r") == 0) {   // Check if the file was successfully opened
        char line[1024]; // Buffer to store each row of data
        while (fgets(line, 1024, file)) { // Read each row from the file
            char* token = strtok(line, ","); // Parse the row using commas as delimiters
            while (token) { // Read each value from the row
                int value = atoi(token); // Convert the value to an integer
                data[count++] = value; // Add the value to the array
                token = strtok(NULL, ","); // Move to the next value
            }
        }
        fclose(file);   // Close the file
    }
    else {
        printf("Error: Unable to open file!\n");
        return 1;
    }
    for (int i = 1; i < 16; i++) { // changed starting index to 0
        for (int j = 0; j < 8; j++) {
            int b;
            // added check for end of buffer
            while ((b = data[next] & 0x01) == (data[next + 1] & 0x01)) { // use buffer[next+1] instead of buffer[next++] to prevent incrementing next twice
                
                printf("next=%d, buffer[next]=%d\n", next, data[next]);
                next++;
                next++;
            }
            randbuf[i] = (randbuf[i] << 1) | b;
            next++; // increment next after processing bit
            
            // increment next after processing bit
        }
    }

    // Print the contents of the array
    //randbuf[0] = 16; // set initial index
    randbuf[0] = 16; // set initial index
    for (int i = 0; i < 16; i++) {
        for (int j = 7; j >= 0; j--) {
            printf("%d", (randbuf[i] >> j) & 0x01);
        }
        printf(" ");
    }
    printf("\n");
   
    return 0;
}

