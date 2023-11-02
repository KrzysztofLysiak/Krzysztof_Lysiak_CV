#ifndef LISTAA
#define LISTAA

//Author: Krzysztof Lysiak
#include <iostream>
#include <cstring>
#include <stdio.h>
#include <string.h>
#include <cassert>
#include <conio.h>

#include "Pionki.hpp"
#include "element_listy.hpp"
#include "Szachownica.hpp"


class lista{

public:

    lista(int element);   //constructor, create first item of list and each value are the same
    int size_of_list();        //return size of list
    class item* return_item(int k);      //return indicator to concrete item (iteration since 1)
    void link_item(Figura fig, int k, int l, int m, int n, int p);  //create new item and link it to list
    void take_off();   //Taking off last item

private:
    class item* head;       // adres of head
    class item* tail;       // adres of last item
    int counter;            // number of item
};
#endif
