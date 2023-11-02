#include <iostream>
#include <cstring>
#include <stdio.h>
#include <string.h>
#include <cassert>
#include <conio.h>

#include "element_listy.hpp"

//Author: Krzysztof Lysiak


item::item(int o,int k, int l, int m, int n, int p){   //CONSTRUCTOR
    nast = NULL;
    pop = NULL;
    current_column = l;
    current_line = k;
    target_column = n;
    target_line = m;
    rodzaj_figury = o;
    kolor =p;
};

class item* item::adres(){return this;};


