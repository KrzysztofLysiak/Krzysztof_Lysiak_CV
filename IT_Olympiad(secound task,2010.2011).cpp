#include <iostream>

using namespace std;

int main(){////////////////////////////////////////MAIN
std::ifstream plik("C:\\Users\\krzys\\Downloads\\oi15-etap1-pla (1)\\etap1\\pla\\in\\pla3b.in");
ios_base::sync_with_stdio(false);
list<int> poster_list;
int i=0;
int input;
plik>>input;

//scanf("%d", &input);
for (i = 0; i < input; i++){
int b=0;
int d=0;
//scanf("%d%d", &d, &b);
plik >> d >>b;
poster_list.push_back(b);
}
int start =0;
int end= poster_list.size();
int deep = 0;
int result = szukaj_plakaty(poster_list,start,end+1,deep);
cout<<result;

return 0;
}
