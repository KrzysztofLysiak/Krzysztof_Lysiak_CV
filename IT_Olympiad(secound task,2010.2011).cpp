#include <iostream>
#include <list>
using namespace std;
#include <fstream>


int search_posters(std::list<int>& posters_list,int start, int divide, int deep){

///////////////////////////////////////////////////////////////////// We check if we have reached the end of the recursion:
/// A single block of 0s or a single block of 1s

if(start + 2 == divide){
    auto it = std::next(posters_list.begin(), start);
    if (*it == deep){return 0;}
    else {return 1;}
    }
/////////////////////////////////////////////////////////////////////// We check if the list does not consist entirely of zeros:

int j=0;
int i =0;
auto it = std::next(posters_list.begin(), start);

for(i=start+1; i< divide; it++) {  ///All zeros
    if((*it) != deep){
        j=1;
        break;
        }
    i++;

    }
if(j == 0){
    return 0;
}

///////////////////////////////////////////////////////////////////////////////////

int go_further =1;
it = std::next(posters_list.begin(), start);

for (i=start+1; i<divide;){  ///We check if there is a 0 in the list
        if ((*it) == deep){
            go_further =0;
            break;
        }
        i++;
        it++;
    }

int poster_counts = 0;
int counter=0;


/////////////////////////////////////////////////////////////////////////////////////
if(go_further == 1){

it = std::next(posters_list.begin(), start);
int smallest_value = 2147483640;
for (i=start+1; i<divide;i++,it++){            ///We search for the smallest value in the list
        if(smallest_value > (*it)){smallest_value = (*it);
        }
    }

it = std::next(posters_list.begin(), start);
for (i=start+1; i<divide;i++){            ///We decrease by the smallest value
     deep += (smallest_value-deep);
     it++;
    }

/////////////////////////////////////////////////////////////////////////////////////////////////
it = std::next(posters_list.begin(), start);
for (i=start+1; i<divide;){   /// We determine the position of the first encountered 0. We count positions like we do for arguments, meaning the first argument is numbered as 1
    i++;
    if(*it == deep){
        counter = std::distance(posters_list.begin(), it);
        counter++;
        break;
    }
    it++;
}


poster_counts++;
/////////////////////////////////////////////////////////////// We split it into two parts and call recursion on each part
if(counter + 2 == divide){
    auto it22 = std::next(posters_list.begin(), counter);
    if (*it22 != deep){poster_counts +=1;}
    }
else {poster_counts += search_posters(posters_list, counter, divide, deep);}

if(start + 2 == counter){
    auto it33 = std::next(posters_list.begin(), start);
    if (*it33 != deep){poster_counts +=1;}
    }
else {poster_counts += search_posters(posters_list, start, counter, deep);}

return poster_counts;
}



else{
///////////////////////////////////////////////////////////////////////////////////////
it = std::next(posters_list.begin(), start);
    for (i=start+1; i<divide;){   /// We determine the position of the first encountered 0. We count in the same way as for arguments, meaning the first argument is 1
        if(*it == deep){
            counter = std::distance(posters_list.begin(), it);
            counter++;
            break;
        }
        it++;
        i++;
    }

/////////////////////////////////////////////////////////////////////////////////////////////////
if(counter + 2 == divide){
    auto it52 = std::next(posters_list.begin(), counter);
    if (*it52 != deep){poster_counts +=1;}
    }
else {poster_counts += search_posters(posters_list, counter, divide, deep);}

if(start + 2 == counter){
    auto it63 = std::next(posters_list.begin(), start);
    if (*it63 != deep){poster_counts +=1;}
    }
else {poster_counts += search_posters(posters_list, start, counter, deep);}
return poster_counts;

}

}


int main(){////////////////////////////////////////MAIN
std::ifstream plik("C:\\Users\\krzys\\Downloads\\oi15-etap1-pla (1)\\etap1\\pla\\in\\pla3b.in");
ios_base::sync_with_stdio(false);
list<int> posters_list;
int i=0;
int input;
plik>>input;

//scanf("%d", &input);
for (i = 0; i < input; i++){
int b=0;
int d=0;
//scanf("%d%d", &d, &b);
plik >> d >>b;
posters_list.push_back(b);
}
int start =0;
int end= posters_list.size();
int deep = 0;
int result = search_posters(posters_list,start,end+1,deep);
cout<<result;

return 0;
}
