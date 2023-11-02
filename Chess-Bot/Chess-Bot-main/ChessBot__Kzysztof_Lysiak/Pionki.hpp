
#ifndef PIONKI
#define PIONKI

//Author: Krzysztof Lysiak


enum Figura{K,D,W,S,G,P,_};
enum Color{White,Black,Brak};


#include <iostream>
#include <cstring>
#include <stdio.h>
#include <string.h>
#include <cassert>
#include <conio.h>


#include "Szachownica.hpp"
#include "listaa.hpp"
#include "element_listy.hpp"

// Class Figure and pawn_move are primary classes

class Figure{

public:
Figure();
Figure(Color color,int wier,int kol,Figura Fig,int point);
virtual void possible_moves(class chessboard*s,class lista*l);  //This is virtual method of concrete method in derived class
Figura fi;                      //Type of figure
Color kolor;                    //Figure's color

int line;       //Figures's position and points
int column;
int points;
};


class pawn_move{
protected:
int GG(class chessboard* chessboard, lista* lista,int line_pos,int col_pos, int line,int column,Color kolor); // This method check the legality of this move, and when everything is ok return 1 or when move isn't ok return 0
int check(chessboard* chessboard, lista* lista, int i, int j,Color kolor);  //This method is using by pawn to check if before field is empty
};

// Derived class after pawn_move and Figure. This is representation of every type of figure and empty field. Pawns can return list of possible move, this requires chessboard and list when the moves will be add

class knight :public pawn_move ,public Figure{
public:
knight(Color,int,int,Figura,int punkt);
void possible_moves(chessboard*, lista*);
};

class king :public pawn_move ,public Figure{
public:
king(Color,int,int,Figura,int punkt);
void possible_moves(chessboard*, lista*);
};

class queen :public pawn_move ,public Figure{
public:
queen(Color,int,int,Figura,int punkt);
void possible_moves(chessboard*, lista*);
};

class bishop :public pawn_move ,public Figure{
public:
bishop(Color,int,int,Figura,int punkt);
void possible_moves(chessboard*, lista*);
};

class rook :public pawn_move ,public Figure{
public:
rook(Color,int,int,Figura,int punkt);
void possible_moves(chessboard*, lista*);
};

class pawn : public pawn_move , public Figure{
public:
pawn(const pawn& p);
pawn(Color,int,int,Figura,int punkt);
void possible_moves(chessboard*, lista*);
};

class empty_field :public pawn_move ,public Figure{ //This class represents empty field
public:
empty_field(Color,int,int,Figura,int punkt);
void possible_moves(chessboard*, lista*);
};


#endif
