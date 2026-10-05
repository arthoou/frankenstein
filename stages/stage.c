#include <stdio.h>
#include <string.h>
int main(){char b[8192]={0};fread(b,1,sizeof(b)-1,stdin);b[strcspn(b,"\r\n")]=0;printf("%s -> C",b);return 0;}
