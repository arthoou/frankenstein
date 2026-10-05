#include <iostream>
#include <string>
int main(){std::string s,line;while(std::getline(std::cin,line)){if(!s.empty())s+=" ";s+=line;}std::cout<<s<<" -> C++";}
