#ifndef SZACHOWNICA
#define SZACHOWNICA

//Author: Krzysztof Lysiak

#include <iostream>
#include <cstring>
#include <stdio.h>
#include <string.h>
#include <cassert>
#include <conio.h>

#include "Pionki.hpp"
#include "listaa.hpp"
#include "element_listy.hpp"


class chessboard{

friend class lista;
friend int rating(chessboard* s, int depth);
friend class pawn_move;

public:

    chessboard * coppy();             // This method produce independent copy of chessboard
    chessboard();                     // Constructor
    chessboard(const chessboard&h);   // Constructor by the object
    void draw();                      // Printing chessboard in the console
    void make_move(class item* r);    // This method makes a move using object class item when the move is saved
    void make_move(int line,int column,int new_line,int new_column);  //This method makes a move using column and lines given by the number(first current line and columns)
    class lista* possible_moves();      //This method returning list of possible move
    int under_capture(int line, int column,Color kol);  // This method inform if field is under capture by the figures of given color
    int count_the_points();         //Count points(black has minus points, white pluses points )
    int king_under_capture(Color kolor);   // Check if king of given color is under attack
    Color whose_move;

    class Figure *head[8][8]; // head of chessboard(head[0][0] means that this is indicator to first pawn)
    private:
    int check;
    int checkmate;
};

int rating(class chessboard* s, int depth);


#endif
