
##import cx_Oracle
import pandas as pd
import tkinter as tk
import threading
import time
import re
import tkinter.ttk as ttk
from tkinter import simpledialog
import tkinter.simpledialog


# BASED CLASS:

class General_user:
    def __init__(self,User_type,Login,Data,UsersData): 
        self.User = User_type
        self.Login = Login
        self.Data = Data
        self.UsersData = UsersData
        self.window = tk.Tk()
        self.lista = None
        self.metody = None
        self.window.title("User menu")


    def create_menu(self):

        self.frame = tk.Frame(self.window)
        self.frame.pack()

        button_list = []
        k =0
            
        for i,j in zip(self.lista,self.metody):
        
            button_list.append(tk.Button(
                self.frame,
                text = str(i),
                bd = 10,
                fg = "red",
                bg = "green",
                activeforeground = "black",
                activebackground = "silver",
                font = "Times 18 bold",
                height = 3,
                width = 25,
                padx = 10,
                pady = 10,
                relief = "groove",
                command = j
            ))
            k += 1

        for l in range (k):
            button_list[l].pack()
      
        
    def Display_data(self):                 # sorts data on a copy
        
        Data_copy = self.Data.copy()

        self.frame.destroy()
        frame = tk.Frame(self.window)
        index =0
        
        def sorting_function(event):
            if combobox.get() == "Sort by Name":
                Data_copy.sort_values(by = 'Drug',inplace=True)
                for item in tree.get_children():
                    tree.delete(item)
                for index, row in Data_copy.iterrows():
                    tree.insert('',tk.END,iid = index, text = index, values = str(row.iloc[0]) + "  " +str(row.iloc[1])+ "  "+str(row.iloc[2])+"  "+str(row.iloc[3]))
            
            else:
                Data_copy.sort_values(by = 'Numbers',inplace=True)
                for item in tree.get_children():
                    tree.delete(item)
                for index, row in Data_copy.iterrows():
                    tree.insert('',tk.END,iid = index, text = index, values = str(row.iloc[0]) + "  " +str(row.iloc[1])+ "  "+str(row.iloc[2])+"  "+str(row.iloc[3]))
            



        # Tworzenie ComboBox
        opcje = ["Sort by Name", "Sort by number of drug"]
        combobox = ttk.Combobox(frame, values=opcje)
        combobox.set("Pick an Option of sort")
        combobox.pack(side="top", pady=10)

        # Dodawanie zdarzenia po wybraniu opcji
        combobox.bind("<<ComboboxSelected>>", sorting_function)


        def Exit():
            frame.destroy()
            self.create_menu()

        def read_data():
           for index, row in Data_copy.iterrows():
                tree.insert('',tk.END,iid = index, text = index, values = str(row.iloc[0]) + "  " +str(row.iloc[1])+ "  "+str(row.iloc[2])+"  "+str(row.iloc[3]))

        Data_columns = list(Data_copy.columns)
        tree = ttk.Treeview(frame, columns = (Data_columns), height = 30)
        tree.pack()
        for colum in Data_columns:
            tree.heading(colum, text=colum)
    
        zatwierdz_button = tk.Button(frame, text="Exit", command= Exit)
        zatwierdz_button.pack(side="top")

        read_data()
        frame.pack()


    def return_data(self):
        self.frame.destroy()
        frame = tk.Frame(self.window)
        def confirm():
            pass
        text_field = tk.Entry(frame)
        text_field.pack()

        confirm_button = tk.Button(frame, text="Confirm", command=confirm)
        confirm_button.pack()
        frame.pack()


    def check_product_availability(self):

        self.frame.destroy()
        
        loaded_text = None

        def ShowData():
            loaded_text = text_field.get()
            text_field.delete(0,"end")
            row_index = self.Data.index[self.Data['Drug'] == str(loaded_text)]
            our_value = self.Data.loc[row_index]['Numbers'].iloc[0]
            label = tk.Label(frame, text= str(loaded_text) + ":" + str(our_value))
            label.pack()
        
        def Exit():
            frame.destroy()
            self.create_menu()


        frame = tk.Frame(self.window)
        frame.pack()
        
        text_field = tk.Entry(frame)
        text_field.pack()
        
        confirm_button = tk.Button(frame, text="Confirm", command= ShowData)
        confirm_button.pack()

        exit_button = tk.Button(frame, text="Exit", command= Exit)
        exit_button.pack()
                
    
    def add_item(self):
        self.frame.destroy()
        frame = tk.Frame(self.window)  
        frame.pack()       
        text_field = tk.Entry(frame)
        text_field.pack()
        text_field1 = tk.Entry(frame)
        text_field2 = tk.Entry(frame)
        text_field3 = tk.Entry(frame)

        def exit_download():

                    self.Data.at[-1,'Expiration date'] = text_field1.get()
                    self.Data.at[-1,'Numbers'] = 0 
                    self.Data.at[-1,'On prescription'] = text_field3.get()
                    
                   
                    text_field4 = tk.Entry(frame)
                    text_field4.pack()
                    exit_download_button = tk.Button(frame, text="Exit", command= Exit)
                    exit_download_button.pack()
        
                    text_field5 = tk.Entry(frame)
                    text_field5.pack()
        
                    confirm_download_button = tk.Button(frame, text="Confirm", command= ShowData)
                    confirm_download_button.pack()
            
        def ShowData():
            our_value = text_field.get()
            text_field.delete(0,"end")

            row_index = self.Data.index[self.Data['Drug'] == str(our_value)]
            #szukana_wartosc = self.Data.loc[indeksy_wierszy]['Numbers'].iloc[0]

            if self.Data['Drug'].isin([our_value]).any():
                current_value = self.Data.loc[row_index[0]]['Numbers']
                current_value += 1
                self.Data.at[row_index[0],'Numbers'] = current_value
                szukana_wartosc = self.Data.loc[row_index[0]]['Numbers']
                label = tk.Label(frame, text= str(our_value) + ":" + str(szukana_wartosc))
                label.pack()

            else:

                new_row = [our_value,0,'Yes',0]
                self.Data = self.Data._append(new_row)
                frame.pack_forget()

                text_field1.pack()
                label1 = tk.Label(frame, text= "enter the expiration date")
                label1.pack()
            
                text_field2.pack()
                label2 = tk.Label(frame, text= "enter the number of drugs")
                label2.pack()
        
                text_field3.pack()
                label3 = tk.Label(frame, text= "enter whether it requires a prescription")
                label3.pack()

                exit_button = tk.Button(frame, text="Exit_from_current_function", command= exit_download)
                exit_button.pack()
                frame.pack()


        def Exit():
            frame.destroy()
            self.create_menu()
       
            
        exit_button = tk.Button(frame, text="Exit", command= Exit)
        exit_button.pack()

        confirm_button = tk.Button(frame, text="Confirm", command= ShowData)
        confirm_button.pack()        

    
    def Browse(self):
        self.frame.destroy()
        frame = tk.Frame(self.window)
        index =0
        
        def Exit():
            frame.destroy()
            self.create_menu()

        def read_data():
           for index, row in self.Data.iterrows():
                tree.insert('',tk.END,iid = index, text = index, values = str(row.iloc[0]) + "  " +str(row.iloc[1])+ "  "+str(row.iloc[2])+"  "+str(row.iloc[3]) + "  " + str(row.iloc[4]))

        Data_columns = list(self.Data.columns)
        tree = ttk.Treeview(frame, columns = (Data_columns), height = 30)
        tree.pack()
        for colum in Data_columns:
            tree.heading(colum, text=colum)
    
        Exit_button = tk.Button(frame, text="Exit", command= Exit)
        Exit_button.pack(side="top")

        read_data()
        frame.pack()


    def subtract_the_product(self):
        self.frame.destroy()  
        frame = tk.Frame(self.window)
                
        def Exit():
            frame.destroy()
            self.create_menu()

        zatwierdz_button = tk.Button(frame, text="Exit", command= Exit)
        zatwierdz_button.pack()
        frame.pack()


    def change_price(self):
        self.frame.destroy()
        frame = tk.Frame(self.window)

        def Exit():
            frame.destroy()
            self.create_menu()
        
        exit_button = tk.Button(frame, text="Exit", command= Exit)
        exit_button.pack()
        frame.pack()

        drug_name = ''
        new_price = None

        def show_dialogue_window():
            local_frame = tk.Toplevel(frame)
            local_frame.title("Entry new price")

            # Add fields to entry text
            widget1 = tk.Label(local_frame, text="Drug name:")
            widget1.grid(row=0, column=0)
            field1 = tk.Entry(local_frame)
            field1.grid(row=0, column=1)

            widget2 = tk.Label(local_frame, text="New price")
            widget2.grid(row=1, column=0)
            field2 = tk.Entry(local_frame)
            field2.grid(row=1, column=1)

            def entry_value():
                drug_name = field1.get()
                new_price = field2.get()
                if (self.Data["Drug"] == str(drug_name)).any():
                    label1.config(text= "The name of the drug whose price has been changed:" + "  " + str(drug_name))
                    label2.config(text= "New price:" + "  " + str(new_price))
                    indeksy = self.Data[self.Data['Drug'] == drug_name].index
                    self.Data.loc[indeksy, 'Price'] = float(new_price)

                else:
                    label1.config(text= "There is no such drug in the database:")
                    label2.config(text= "0")
                
                local_frame.destroy()


            button_ok = tk.Button(local_frame, text="OK", command=entry_value)
            button_ok.grid(row=2, column=0, columnspan=2)

        kombobox_button = tk.Button(frame, text="Entry drug:", command=show_dialogue_window)
        kombobox_button.pack()
        label1 = tk.Label(frame, text="Drug price hasn't been change")
        label1.pack() 
        label2 = tk.Label(frame, text="0")
        label2.pack()

                

    def buy_something(self):
        self.frame.destroy()  
        frame = tk.Frame(self.window)
                
        def Exit():
            frame.destroy()
            self.create_menu()

        zatwierdz_button = tk.Button(frame, text="Exit", command= Exit)
        zatwierdz_button.pack()
        frame.pack()
    
    
    def list_of_things(self):
        self.frame.destroy()  
        frame = tk.Frame(self.window)
                
        def Exit():
            frame.destroy()
            self.create_menu()

        zatwierdz_button = tk.Button(frame, text="Exit", command= Exit)
        zatwierdz_button.pack()
        frame.pack()
                 

    def return_number_of_product(self):
        self.frame.destroy()

        frame = tk.Frame(self.window)

        def Exit():
            frame.destroy()
            self.create_menu()

        def Show():
            Name_of_drug = tk.simpledialog.askstring("Input", "Input an String")
            num = self.Data[self.Data['Drug'] == Name_of_drug]

            Number_of_drug = self.Data.loc[num.index,'Numbers']
            print(Number_of_drug)
            label.config(text= str(Name_of_drug) + "  " + str(Number_of_drug.values))

        exit_button = tk.Button(frame, text="Exit", command=Exit)
        exit_button.pack()

        B = tk.Button(frame, text="Click to write name of drug", command=Show)
        B.pack()
        frame.pack()
        label = tk.Label(frame, text="Initial text")
        label.pack()   


    def __del__(self):
        pass           

            
        
# DERIVED CLASSES:    
        
class Main_user(General_user):

    def __init__ (self,User_type,Login,Data,UsersData):
        super().__init__(User_type,Login,Data,UsersData)
        self.lista = ['Display_data',
                'check_product_availability',
                'change_price',
                'Browse',
                'return_number_of_product',
                'add_item',
                ]

        self.metody = [ self.Display_data,
                self.check_product_availability,
                self.change_price,
                self.Browse,
                self.return_number_of_product,
                self.add_item,
                ]
    
    def start(self):
        self.create_menu()   
        self.window.mainloop()
                 
      
class Apothecary(General_user):

    def __init__ (self,User_type,Login,Data,UsersData):
        super().__init__(User_type,Login,Data,UsersData)
        self.lista = ['Display_data',
                'check_product_availability',
                'change_price',
                'Browse',
                'return_number_of_product',
                'add_item',
                ]

        self.metody = [ self.Display_data,
                self.check_product_availability,
                self.change_price,
                self.Browse,
                self.return_number_of_product,
                self.add_item,
                ]
    
    def start(self):
        self.create_menu()   
        self.window.mainloop()     


class User(General_user):

    def __init__ (self,User_type,Login,Data,UsersData):
        super().__init__(User_type,Login,Data,UsersData)
        self.lista = ['Display_data',
                'check_product_availability',
                'change_price',
                'Browse',
                'return_number_of_product',
                'add_item',
                ]

        self.metody = [ self.Display_data,
                self.check_product_availability,
                self.change_price,
                self.Browse,
                self.return_number_of_product,
                self.add_item,
                ]
    
    def start(self):
        self.create_menu()   
        self.window.mainloop()
        

class warehouseman(General_user):

    def __init__ (self,User_type,Login,Data,UsersData):
        super().__init__(User_type,Login,Data,UsersData)
        self.lista = ['Display_data',
                'check_product_availability',
                'change_price',
                'Browse',
                'return_number_of_product',
                ]

        self.metody = [ self.Display_data,
                self.check_product_availability,
                self.change_price,
                self.Browse,
                self.return_number_of_product,
                ]
    
    def start(self):
        self.create_menu()   
        self.window.mainloop()
    






# THREAD CLASS:

class New_thread(threading.Thread):

    def __init__ (self,User_type,Login,Data,UsersData):
        threading.Thread.__init__(self)
        self.User = User_type
        self.Login = Login
        self.Data = Data
        self.UsersData = UsersData

    def run(self):

        if str(self.User) == 'Warehouseman':
            Warehouseman = Warehouseman(self.User,self.Login,self.Data,self.UsersData)
            Warehouseman.start()
        
        elif str(self.User) == 'Accountant':
            Accountant = Accountant(self.User,self.Login,self.Data,self.UsersData)
            Accountant.start()
        
        elif str(self.User) == 'Apothecary':
            Apothecary = Main_user(self.User,self.Login,self.Data,self.UsersData)
            Apothecary.start()

        else:                   #Normal user
            Userr = User(self.User,self.Login,self.Data,self.UsersData)
            Userr.start() 
        






# LOADING FROM FILE
Data = pd.read_csv("Farmacy.txt", sep=',', header=0)
UsersData = pd.read_csv("Users.txt", sep=',', header=0)
print(Data.head())


# MAIN APLICATION LOOP
print(UsersData.columns)

ThreadList = []
    
while True:
    Login = str(input("Entry Login (or type in 'exit' to close aplication): "))
    if Login == "exit":
        break

    if (UsersData['Login'] == Login).any():
        wiersz = UsersData[UsersData['Login'] == Login].index
        Users_type = UsersData.loc[wiersz, 'Login']
        Nowy_wat = New_thread(Users_type,Login,Data,UsersData)
        ThreadList.append(Nowy_wat)
        Nowy_wat.start()

    else:
        print('Unrecognized login')