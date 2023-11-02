#include <iostream>
#include <cstring>
#include <stdio.h>
#include <string.h>
#include <cassert>
#include <conio.h>

//Author: Krzysztof Lysiak

#include "listaa.hpp"

lista::lista(int element){                //CONSTRUCTOR

item *first = new item( element, element, element, element, element, element); //creating object type "item"
head = first->adres();
tail = head;
counter=1;
}

int lista::size_of_list(){return counter;}

class item* lista::return_item(int l){
int k =0;

if(l==0)
   k=1;
else
   k=l;

item *target_indicator = head;

if (k<0 || k> counter){
    std :: cout<< "List error";
    return 0;
    }

for(;k >0;k--){
    target_indicator = target_indicator->nast;
    }

return (target_indicator->adres());
}

void lista::link_item(Figura fig,int k, int l, int m, int n, int p){

item *wsk = new item(fig,k,l,m,n,p);
(wsk->pop) = tail;
tail -> nast = wsk;
tail = wsk;
counter++;
}

void lista::take_off(){
if (counter == 1)
    ;
else{
    item* wsk1 = tail->pop;
    wsk1->nast = wsk1->adres();
    counter--;
    }
}
