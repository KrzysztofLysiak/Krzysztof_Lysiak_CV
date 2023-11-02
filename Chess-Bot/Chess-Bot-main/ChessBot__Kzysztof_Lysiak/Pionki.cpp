#include <iostream>
#include <cstring>
#include <stdio.h>
#include <string.h>
#include <cassert>
#include <conio.h>

#include "Pionki.hpp"

//Author: Krzysztof Lysiak

void Figure::possible_moves( chessboard*s, lista*l){};

Figure::Figure(){};

Figure:: Figure(Color color,int wier,int kol,Figura Fig,int point){
line = wier;
column = kol;
kolor = color;
fi = Fig;

if (color == Black)
    points = (-point);
else
    points =point;

};


int pawn_move:: GG(chessboard* chessboard, lista* lista,int line_pos,int col_pos, int wier,int kol,Color kolor){

class chessboard* wti= chessboard->coppy();

if(wier <0 || wier>7 ||kol > 7||kol<0){
     return 0;}

if (wti->head[wier][kol]->kolor != kolor){
    wti->make_move(line_pos,col_pos,wier,kol);
    }
else
{
    return 0;
}

if(wti->king_under_capture(kolor)==0){
   return 0;}
lista->link_item(wti->head[wier][kol]->fi,line_pos ,col_pos ,wier, kol,kolor);
return 1;
};

int pawn_move:: check(chessboard* chessboard, lista* lista, int line, int column,Color kolor){
if((column+1)>7)
    return 0;
if((chessboard->head[line][column+1]->fi)==6)
        return 1;
if ((chessboard->head[line][column+1]->kolor == kolor) || (line <0) || (line >7) || (column <0) || (column+1 >7)){
    lista->take_off();
}

return 1;
};

pawn:: pawn(Color color,int wier,int kol,Figura Fig,int punkt):Figure(color,wier,kol,Fig,punkt){};

void pawn:: possible_moves(chessboard* s, lista* l){

if(kolor == White){
        GG(s, l,line,column,(line+1),column,kolor);
        check(s,l,(line+1),column,kolor);
    }
else
    {
        GG(s, l,line,column,line-1,column,kolor);
        check(s,l,line-1 ,column,kolor);
    }
};

rook::rook(Color color,int wier,int kol,Figura Fig,int punkt):Figure(color,wier,kol,Fig,punkt){};

void rook::possible_moves(chessboard* s, lista* l){

for(int i = line; i<8; i++){
    if(GG(s,l,line,column,i+1,column,kolor)==0){
        break;}
    }
for(int i = column; i<8; i++){
    if (GG( s, l,line,column,line,i+1,kolor)==0){
        break;}
    }
for(int i = line; i<8; i--){
    if(GG( s, l,line,column,i-1,column,kolor)==0){
        break;}
    }
for(int i = column; i<8; i--){
    if(GG(s, l,line,column,line,i-1,kolor)==0){
        break;}
    }

};

knight::knight(Color color,int wier,int kol,Figura Fig,int punkt):Figure(color,wier,kol,Fig,punkt){};

void knight::possible_moves(chessboard* s, lista* l){

    GG(s,l,line,column,line+2,column+1,kolor);
    GG(s,l,line,column,line+1,column+2,kolor);
    GG(s,l,line,column,line+2,column-1,kolor);
    GG(s,l,line,column,line+1,column-2,kolor);
    GG(s,l,line,column,line-2,column+1,kolor);
    GG(s,l,line,column,line-1,column-2,kolor);
    GG(s,l,line,column,line-2,column-1,kolor);
    GG(s,l,line,column,line-1,column+2,kolor);
};

bishop::bishop(Color color,int wier,int kol,Figura Fig,int punkt):Figure(color,wier,kol,Fig,punkt){};

void bishop::possible_moves(chessboard* s, lista* l){

for(int j = 1; ;j++)
    if (GG(s, l,line,column,line+j,column+j,kolor)==0){
          goto next1;}
next1:

for(int j = 1; ;j++)
    if (GG(s, l,line,column,line+j,column-j,kolor)==0){
          goto next2;}
next2:

for(int j = 1; ;j++)
    if (GG(s, l,line,column,line-j,column+j,kolor)==0){
          goto next3;}
next3:

for(int j = 1; ;j++)
    if (GG(s, l,line,column,line-j,column-j,kolor)==0){
          goto next4;}
next4:
;
};

queen::queen(Color color,int wier,int kol,Figura Fig,int punkt):Figure(color,wier,kol,Fig,punkt){};

void queen::possible_moves(chessboard* s, lista* l){

for(int j = 1; ;j++)
    if (GG(s, l,line,column,line+j,column+j,kolor)==0){
          goto next1;}
next1:

for(int j = 1; ;j++)
    if (GG(s, l,line,column,line+j,column-j,kolor)==0){
          goto next2;}
next2:

for(int j = 1; ;j++)
    if (GG(s, l,line,column,line-j,column+j,kolor)==0){
          goto next3;}
next3:

for(int j = 1; ;j++)
    if (GG(s, l,line,column,line-j,column-j,kolor)==0){
          goto next4;}
next4:


for(int i = line; i<8; i++){
    if(GG(s,l,line,column,i+1,column,kolor)==0){
        break;}
    }
for(int i = column; i<8; i++){
    if (GG( s, l,line,column,line,i+1,kolor)==0){
        break;}
    }
for(int i = line; i<8; i--){
    if(GG( s, l,line,column,i-1,column,kolor)==0){
        break;}
    }
for(int i = column; i<8; i--){
    if(GG(s, l,line,column,line,i-1,kolor)==0){
        break;}
    }
};

king::king(Color color,int wier,int kol,Figura Fig, int punkt):Figure(color,wier,kol,Fig,punkt){};

void king::possible_moves(chessboard* s, lista* l){
    for(int i= -1; i< 2;i++)
        for(int j=-1; j<2;j++){
         if(i==0 && j==0)
            break;
         GG(s,l,line,column,line+i,column+j,kolor);
        }
};

empty_field::empty_field(Color color,int wier,int kol,Figura Fig, int punkt):Figure(color,wier,kol,Fig,punkt){};

void empty_field::possible_moves(chessboard* s, lista* l){};


