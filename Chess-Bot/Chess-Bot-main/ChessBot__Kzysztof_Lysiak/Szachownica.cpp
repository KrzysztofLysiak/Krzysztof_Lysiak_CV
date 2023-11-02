#include <iostream>
#include <cstring>
#include <stdio.h>
#include <string.h>
#include <cassert>
#include <conio.h>

//Author: Krzysztof Lysiak

#include "Szachownica.hpp"

chessboard::chessboard (){
    for(int j=0;j<8;j++)
       {
       head[1][j] = new pawn(White,1,j,P,1);
       head[2][j] = new empty_field(Brak,2,j,_,0);
       head[3][j] = new empty_field(Brak,3,j,_,0);
       head[4][j] = new empty_field(Brak,4,j,_,0);
       head[5][j] = new empty_field(Brak,5,j,_,0);
       head[6][j] = new pawn(Black,6,j,P,1);
       }

    head[0][0]= new rook(White,0,0,W,10);
    head[0][1]= new knight(White,0,1,S,3);
    head[0][2]= new bishop(White,0,2,G,3);
    head[0][3]= new king(White,0,3,K,1000);
    head[0][4]= new queen(White,0,4,D,10);
    head[0][5]= new bishop(White,0,5,G,3);
    head[0][6]= new knight(White,0,6,S,3);
    head[0][7]= new rook(White,0,7,W,10);

    head[7][0]= new rook(Black,7,0,W,10);
    head[7][1]= new knight(Black,7,1,S,3);
    head[7][2]= new bishop(Black,7,2,G,3);
    head[7][3]= new queen(Black,7,3,D,10);
    head[7][4]= new king(Black,7,4,K,1000);
    head[7][5]= new bishop(Black,7,5,G,3);
    head[7][6]= new knight(Black,7,6,S,3);
    head[7][7]= new rook(Black,7,7,W,10);

    check = 0;
    checkmate = 0;
    whose_move = White;
    };


chessboard::chessboard(const chessboard& h):check(h.check),checkmate(h.checkmate),whose_move(h.whose_move),head(){
for(int i=0;i<8;i++)
    for(int j=0;j<8;j++)
        {
        if(h.head[i][j]->fi==0)
           head[i][j]= new king(h.head[i][j]->kolor,i,j,K,1000);
        if(h.head[i][j]->fi==1)
           head[i][j]= new queen(h.head[i][j]->kolor,i,j,D,10);
        if(h.head[i][j]->fi==2)
           head[i][j]= new rook(h.head[i][j]->kolor,i,j,W,10);
        if(h.head[i][j]->fi==3)
           head[i][j]= new knight(h.head[i][j]->kolor,i,j,S,3);
        if(h.head[i][j]->fi==4)
           head[i][j]= new bishop(h.head[i][j]->kolor,i,j,G,3);
        if(h.head[i][j]->fi==5)
           head[i][j]= new pawn(h.head[i][j]->kolor,i,j,P,1);
        if(h.head[i][j]->fi==6)
           head[i][j]= new empty_field(Brak,i,j,_,0);
        }
};


chessboard * chessboard::coppy(){
return new chessboard(*this);
}



int chessboard::count_the_points(){
int points=0;
for(int i=0;i<8;i++)
    for(int j=0;j<8;j++){
        points += (head[i][j]->points);
        }
return points;
};

void chessboard::make_move(item* r){
if (head[r->current_line][r->current_column]->fi != 6){
head[r->target_line][r->target_column]=head[r->current_line][r->current_column];
head[r->current_line][r->current_column]=new empty_field(Brak,r->current_line,r->current_column,_,0);
head[r->current_line][r->current_column]->points=0;
if(whose_move == White)
    whose_move= Black;
else
    whose_move = White;

head[r->target_line][r->target_column]->line = r->target_line;
head[r->target_line][r->target_column]->column = r->target_column;}
};

int chessboard::king_under_capture(Color kolor){
for(int i=0;i<8;i++)
    for(int j=0;j<8;j++)
        if ((head[i][j]->fi == 0)&&(head[i][j]->kolor==kolor)){
            return under_capture(i,j,kolor);
            }

return 0;
};

int chessboard::under_capture(int line, int column, Color kol){
    ////Checking rows, columns and diagols

for(int i=0;line+i<8;i++){
    if(head[line+i][column]->kolor==kol)
        break;
    if(head[line+i][column]->fi==_)
        continue;
    if((head[line+i][column]->kolor != kol) && ((head[line+i][column]-> fi== D)|| (head[line+i][column]-> fi== W))){
        return 0;}
        }

for(int i=0;line-i>0;i++){
    if(head[line-i][column]->kolor==kol)
        break;
    if(head[line-i][column]->fi==_)
        continue;
    if((head[line-i][column]->kolor != kol) && ((head[line-i][column]-> fi== D)|| (head[line-i][column]-> fi== W))){
        return 0;}
        }

for(int i=0;column-i>0;i++){
    if(head[line][column-i]->kolor==kol)
        break;
    if(head[line][column-i]->fi==_)
        continue;
    if((head[line][column-i]->kolor != kol) && ((head[line][column-i]-> fi== D)|| (head[line][column-i]-> fi== W))){
        return 0;}
        }

for(int i=0;column+i<8;i++){
    if(head[line][column+i]->kolor==kol)
        break;
    if(head[line][column+i]->fi==_)
        continue;
    if((head[line][column+i]->kolor != kol) && ((head[line][column+i]-> fi== D)|| (head[line][column+i]-> fi== W))){
        return 0;}
        }

for(int i=0;(column+i<8)&&(line+i<8);i++){
    if(head[line+i][column+i]->kolor==kol)
        break;
    if(head[line+i][column+i]->fi==_)
        continue;
    if((head[line+i][column+i]->kolor != kol) && ((head[line+i][column+i]-> fi== D)|| (head[line+i][column+i]-> fi== G))){
        return 0;}
        }

for(int i=0;(column+i<8)&&(line-i>0);i++){
    if(head[line-i][column+i]->kolor==kol)
        break;
    if(head[line-i][column+i]->fi==_)
        continue;
    if((head[line-i][column+i]->kolor != kol) && ((head[line-i][column+i]-> fi== D)|| (head[line-i][column+i]-> fi== G))){
        return 0;}
        }

for(int i=0;(column-i>0)&&(line+i<8);i++){
    if(head[line+i][column-i]->kolor==kol)
        break;
    if(head[line+i][column-i]->fi==_)
        continue;
    if((head[line+i][column-i]->kolor != kol) && ((head[line+i][column-i]-> fi== D)|| (head[line+i][column-i]-> fi== G))){
        return 0;}
        }

for(int i=0;(column-i>0)&&(line-i>0);i++){
    if(head[line-i][column-i]->kolor==kol)
        break;
    if(head[line-i][column-i]->fi==_)
        continue;
    if((head[line-i][column-i]->kolor != kol) && ((head[line-i][column-i]-> fi== D)|| (head[line-i][column-i]-> fi== G))){
        return 0;}
        }

//Under capture by the pawn

if(whose_move == Black )
    {
    if((line+1<8)&&(column+1<8)){
        if (((head[line+1][column+1]-> fi == P) && (head[line+1][column+1]-> kolor == Black)))
            return 0;
            }
    if((line+1<8)&&(column+1<8)){
        if ((head[line+1][column-1]-> kolor== Black)&&(head[line+1][column-1]->fi==P))
            return 0;
            }
    }
else
    {
    if((line-1>0)&&(column+1<8)){
        if (((head[line-1][column+1]-> fi == P) && (head[line-1][column+1]-> kolor == White)))
            return 0;
            }
    if((line-1>0)&&(column-1>0)){
        if ((head[line-1][column-1]-> kolor== White)&&(head[line-1][column-1]->fi==P))
            return 0;
            }
    }


//Under capture by the king
if(head[line][column]->kolor == White ){
        for(int i = -1; i<2;i++)
            for(int j = -1; j<2;j++)
            {
                if(((line+i)>7)||(line+i<0)||(column+j<0)||(column+j)>7)
                    continue;

                if ((head[line+i][column+j]-> fi == K ) && (head[line+i][column+j]-> kolor == Black))
                 return 0;}
}

if(head[line][column]->kolor == Black ){
        for(int i = -1; i<2;i++)
            for(int j = -1; j<2;j++)
                {
                 if(((line+i)>7)||(line+i<0)||(column+j<0)||(column+j)>7){

                    continue;}
                 if ((head[line+i][column+j]-> fi == 0 ) && (head[line+i][column+j]-> kolor == White)){

                        return 0;}
                }
}

//Under capture by the knight

if(head[line][column]->kolor != whose_move ){
        if(line+1<8&&column+2<8){
        if((head[line+1][column+2]-> fi == S ) && (head[line+1][column+2]-> kolor == White))
        return 0;}
}
if(head[line][column]->kolor != whose_move ){
        if(line+1<8&&column-2>0){
        if ((head[line+1][column-2]-> fi == S ) && (head[line+1][column+2]-> kolor == White))
        return 0;}
}
if(head[line][column]->kolor != whose_move ){
        if(line-1>0&&column+2<8){
        if ((head[line-1][column+2]-> fi == S ) && (head[line+1][column+2]-> kolor == White))
        return 0;}
}
if(head[line][column]->kolor != whose_move) {
        if(line-1>0&&column-2>0){
        if ((head[line-1][column-2]-> fi == S ) && (head[line+1][column+2]-> kolor == White))
        return 0;}
}
if(head[line][column]->kolor != whose_move ){
        if(line+1<8&&column+2<8){
        if ((head[line+1][column+2]-> fi == S ) && (head[line+1][column+2]-> kolor == Black))
        return 0;}
}
if(head[line][column]->kolor != whose_move ){
        if(line+1<8&&column-2>0){
        if ((head[line+1][column-2]-> fi == S ) && (head[line+1][column+2]-> kolor == Black))
        return 0;}
}
if(head[line][column]->kolor != whose_move ){
        if(line-1>0&&column+2<8){
        if ((head[line-1][column+2]-> fi == S ) && (head[line+1][column+2]-> kolor == Black))
        return 0;}
}
if(head[line][column]->kolor != whose_move ){
    if(line-1>0&&column-2>0){
        if ((head[line-1][column-2]-> fi == S ) && (head[line+1][column+2]-> kolor == Black))
    return 0;}
}
return 1;
};

lista *chessboard::possible_moves(){
lista* l = new lista(1);
for(int i=0;i<8;i++)
    for(int j=0;j<8;j++){
        if(((head[i][j])->kolor!=whose_move)||((head[i][j])->fi==_)){
            continue;}
        head[i][j]->possible_moves(this,l);        //In this line, chessboard::possible_moves uses mothod possible_moves of concrete figure which is in this field of chessboard
        }
  return l;
};

void chessboard::draw(){


for(int i=0;i<8;i++)
    {
    for(int j=0; j<8;j++)
        {
        if(head[i][j]->fi==0){
            std::cout<<"|";
            std::cout<<"K";
            }
        if(head[i][j]->fi==1){
            std::cout<<"|";
            std::cout<<"D";
        }
        if(head[i][j]->fi==2){
            std::cout<<"|";
            std::cout<<"W";
        }
        if(head[i][j]->fi==3){
            std::cout<<"|";
            std::cout<<"S";
        }
        if(head[i][j]->fi==4){
            std::cout<<"|";
            std::cout<<"G";
        }
        if(head[i][j]->fi==5){
            std::cout<<"|";
            std::cout<<"P";
        }
        if(head[i][j]->fi==6){
            std::cout<<"|";
            std::cout<<"_";
        }
        }
        std::cout<<"\n";
    }
};

void chessboard::make_move(int line,int column,int new_line,int new_column){
if(head[line][column]->fi!=6){
delete head[new_line][new_column];
head[new_line][new_column] = head[line][column];
head[line][column] = new empty_field(Brak,line,column,_,0);
head[line][column]->points = 0;

if(whose_move == White)
    whose_move= Black;
else
    whose_move = White;

head[new_line][new_column]->line=new_line;
head[new_line][new_column]->column=new_column;}

};


int rating(chessboard* s,int depth){ //Function of rating position, this algorithm based at the min-max schematic.We call function rating recursively which returning rating of position by the number.
// This algorithm based at the assumption that enemy makes the best move at the position and considering this return points of the best continuation.

if(depth == 0){ //When depth  == 0 function count the points and returning.
    return s->count_the_points();
}

int i=0;
lista* wti = s->possible_moves();  //Creating list of possible moves.

for(int j=1; j<(wti->size_of_list());j++){   //Inf this loop function look makes every moves from the list and returning value of this position with the min-max algorithm.
    chessboard* z= s->coppy();               //In this line we creating copy of chessboard to avoid making some changes at the main chessboard
    z->make_move(wti->return_item(j));
    if(z->whose_move==White){
        if(j==1)
            i=rating(z,(depth-1));
        if (rating(z,(depth-1)) < i){
            i = rating(z,(depth-1));
        }
    }
    if(z->whose_move==Black)
    {
        if(j==1)
            i=rating(z,(depth-1));
        if (rating(z,(depth-1)) > i){
            i = rating(z,(depth-1));
        }
    }
    delete z;
}
delete wti;

return i;

};

