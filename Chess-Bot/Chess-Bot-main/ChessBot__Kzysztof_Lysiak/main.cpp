#include <iostream>
#include <cstring>
#include <stdio.h>
#include <string.h>
#include <cassert>
#include <conio.h>

//Author: Krzysztof Lysiak

#include "element_listy.hpp"
#include "listaa.hpp"
#include "Szachownica.hpp"
#include "Pionki.hpp"

// You have to write current row, next current column, after target row and target column to play

int main()
{     // Auxiliary variables:
int k=0;
int l=0;
int m=0;
int n=0;
int i =1;
int j = 0;
int number_of_the_best_move=0;
int points=0;
chessboard c;

// This "while" ending work when one of king is out of game:
    while((c.count_the_points()<300) && (c.count_the_points()>-300)){  // checking the check-mate
        lista* list_of_move = c.possible_moves(); // Producing list of legal move

        for(i=1; i < list_of_move->size_of_list();i++){
            chessboard* a= c.coppy();      // This loop executing move and after that using evaluatin function. Move which has the most points is remembering with "number_of_the_best_move" variables.
            a->make_move(list_of_move->return_item(i));
            j = rating(a,3);
            if(j > points){
                number_of_the_best_move=i;
                }
            }
            // Execute move which was chosen in "for" loop:
            c.make_move(list_of_move->return_item(number_of_the_best_move));
            //Printing computer's move:
            std::cout<<"\n";
            std::cout<<"My move:";
            std::cout<<"\n";
            std::cout<<list_of_move->return_item(number_of_the_best_move)->current_line;
            std::cout<<list_of_move->return_item(number_of_the_best_move)->current_column;
            std::cout<<"::";
            std::cout<<list_of_move->return_item(number_of_the_best_move)->target_line;
            std::cout<<list_of_move->return_item(number_of_the_best_move)->target_column;
            std::cout<<"\n";

            //This code is responsible for fetching movement from the player and executing:
            c.draw();
            std::cout<<"Your move:";
            std::cout<<"\n";
            std::cin>>k;
            std::cin>>l;
            std::cin>>m;
            std::cin>>n;
            std::cout<<"Your move has been made:";
            std::cout<<"\n";
            c.make_move(k,l,m,n);
    }

    return 0;
}
