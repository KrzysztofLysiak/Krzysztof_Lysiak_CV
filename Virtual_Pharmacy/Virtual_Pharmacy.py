
##import cx_Oracle
import pandas as pd
import tkinter as tk
import threading
import time
import re
import tkinter.ttk as ttk
from tkinter import simpledialog
import tkinter.simpledialog



class Keep_order_in_DataFrame(threading.Thread):
    def __init__ (self, Data, lock):
        threading.Thread.__init__(self)
        self.Data = Data
        self.lock = lock
    def run(self):

        while True:
            self.lock.acquire()
            Data_frame_of_exhausted_drug = self.Data.query('Numbers <= 0 ')
            self.Data.drop(Data_frame_of_exhausted_drug.index,inplace=True)
            self.Data.reset_index(drop = True,inplace = True)

            self.lock.release()
            time.sleep(2)




# BASED CLASS:

class General_user:
    def __init__(self,User_type,Login,Data,UsersData,datalock): 
        self.User = User_type
        self.Login = Login
        self.Data = Data
        self.UsersData = UsersData
        self.window = tk.Tk()
        self.lista = None
        self.metody = None
        self.window.title("User menu")
        self.datalock = datalock


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

        shopping_cart_list = []
        buy_frame = tk.Frame(self.window)
        buy_frame.pack(side = "bottom")
        Bought_things = tk.Label(buy_frame, text = "Nothing has been bought")
        Bought_things.pack()
        Price_of_the_drugs = tk.Label(buy_frame, text = "0")
        Price_of_the_drugs.pack()

        self.frame.destroy()
        frame = tk.Frame(self.window)
        button_frame = tk.Frame(self.window)
        index =0
        
        def buy_drug(arg):

            row = self.Data[self.Data['Drug'] == str(arg)].index[0]

            self.datalock.acquire()
            if self.Data.loc[row , 'Numbers'] != 0:
                self.Data.loc[row , 'Numbers'] -= 1
                self.datalock.release()
            
            else:
                print("Product is not available")
                self.datalock.release()
                return

            shopping_cart_list.append(arg)

            Bought_things.config(text = "You bought:  " + str(shopping_cart_list))
            total_price = 0
            
            for i in shopping_cart_list:
                row = self.Data.loc[self.Data['Drug'] == i].iloc[0]
                total_price += row['Price']


            Price_of_the_drugs.config(text = "Total price:  " + str(total_price))

            read_data_one_more_time()


        def Exit():
            frame.destroy()
            button_frame.destroy()
            self.create_menu()
            buy_frame.destroy()

        def read_data():
            for index, row in self.Data.iterrows():
                tree.insert('',tk.END,iid = index, text = index, values = str(row.iloc[0]) + "  " +str(row.iloc[1])+ "  "+str(row.iloc[2])+"  "+str(row.iloc[3]) + "  " + str(row.iloc[4]))
                button = tk.Button(button_frame, text="Buy:  "+ str(row.iloc[0]), command=lambda arg=str(row.iloc[0]): buy_drug(arg), font=("Helvetica", 8) , width = 23)
                button.pack(side="top")

        def read_data_one_more_time():
            for index, row in self.Data.iterrows():
                tree.item(index, text = index, values = str(row.iloc[0]) + "  " +str(row.iloc[1])+ "  "+str(row.iloc[2])+"  "+str(row.iloc[3]) + "  " + str(row.iloc[4]))

        Data_columns = list(self.Data.columns)

        tree = ttk.Treeview(frame, columns = (Data_columns ), height = 30)
        tree.pack()
        for colum in Data_columns:
            tree.heading(colum, text=colum)
            
    
        Exit_button = tk.Button(frame, text="Exit", command= Exit)
        Exit_button.pack(side="top")

        read_data()
        frame.pack(side="left")
        button_frame.pack(side = "right")
 
    
    def add_list_of_things(self):
        self.frame.destroy()  
        frame = tk.Frame(self.window)

        def add_items():
            path_to_file = entry.get()
            Data_temporary = pd.read_csv(str(path_to_file), sep=',', header=0)
            MainDatatemporary = self.Data.copy()
            MainDatatemporary = MainDatatemporary._append(Data_temporary, ignore_index=True)
            self.Data = MainDatatemporary
            label.config(text = "File: " + str(path_to_file) + " has been load")
            entry.delete(0, 'end')


        label = tk.Label(frame, text = "Write path to your list of things:")
        label.pack()

        button = tk.Button(frame, text =  "accept", command = add_items)
        button.pack()

        entry = tk.Entry(frame)
        entry.pack()



        def Exit():
            frame.destroy()
            self.create_menu()

        exit_button = tk.Button(frame, text="Exit", command= Exit)
        exit_button.pack()
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

    def __init__ (self,User_type,Login,Data,UsersData,datalock):
        super().__init__(User_type,Login,Data,UsersData,datalock)
        self.lista = ['Display_data',
                'check_product_availability',
                'change_price',
                'Browse',
                'return_number_of_product',
                'add_item',
                'buy_something',
                'add_list_of_things',
                ]

        self.metody = [ self.Display_data,
                self.check_product_availability,
                self.change_price,
                self.Browse,
                self.return_number_of_product,
                self.add_item,
                self.buy_something,
                self.add_list_of_things,
                ]
    
    def start(self):
        self.create_menu()   
        self.window.mainloop()
                 
      
class Apothecary(General_user):

    def __init__ (self,User_type,Login,Data,UsersData,datalock):
        super().__init__(User_type,Login,Data,UsersData,datalock)
        self.lista = ['Display_data',
                'check_product_availability',
                'change_price',
                'Browse',
                'return_number_of_product',
                'add_item',
                'buy_something'
                ]

        self.metody = [ self.Display_data,
                self.check_product_availability,
                self.change_price,
                self.Browse,
                self.return_number_of_product,
                self.add_item,
                self.buy_something
                ]
    
    def start(self):
        self.create_menu()   
        self.window.mainloop()     


class User(General_user):

    def __init__ (self,User_type,Login,Data,UsersData,datalock):
        super().__init__(User_type,Login,Data,UsersData,datalock)
        self.lista = ['Display_data',
                'check_product_availability',
                'Browse',
                'return_number_of_product',
                'buy_something',
                ]

        self.metody = [ self.Display_data,
                self.check_product_availability,
                self.Browse,
                self.return_number_of_product,
                self.buy_something
                ]
    
    def start(self):
        self.create_menu()   
        self.window.mainloop()
        

class warehouseman(General_user):

    def __init__ (self,User_type,Login,Data,UsersData,datalock):
        super().__init__(User_type,Login,Data,UsersData,datalock)
        self.lista = ['Display_data',
                'check_product_availability',
                'change_price',
                'Browse',
                'return_number_of_product',
                'add_list_of_things',
                ]

        self.metody = [ self.Display_data,
                self.check_product_availability,
                self.change_price,
                self.Browse,
                self.return_number_of_product,
                self.add_list_of_things,
                ]
    
    def start(self):
        self.create_menu()   
        self.window.mainloop()
    




# THREAD CLASS:

dataLock = threading.Lock()


class New_thread(threading.Thread):

    def __init__ (self,User_type,Login,Data,UsersData,datalock):
        threading.Thread.__init__(self)
        self.User = User_type
        self.Login = Login
        self.Data = Data
        self.UsersData = UsersData
        self.datalock =datalock

    def run(self):
        print(self.User)
        if str(self.User) == "Warehouseman":
            Warehouseman_object = warehouseman(self.User,self.Login,self.Data,self.UsersData,self.datalock)
            Warehouseman_object.start()
        
        elif str(self.User) == "Main_user":
            Main_user_object = Main_user(self.User,self.Login,self.Data,self.UsersData,self.datalock)
            Main_user_object.start()
        
        elif str(self.User) == "Apothecary":
            Apothecary_object = Apothecary(self.User,self.Login,self.Data,self.UsersData,self.datalock)
            Apothecary_object.start()

        else:                   #Normal user
            User_object = User(self.User,self.Login,self.Data,self.UsersData,self.datalock)
            User_object.start() 
        




# LOADING FROM FILE
Data = pd.read_csv("Farmacy.txt", sep=',', header=0)
UsersData = pd.read_csv("Users.txt", sep=',', header=0)
print(Data.head())
#KeepOrder = Keep_order_in_DataFrame(Data, dataLock)
#KeepOrder.start()

# MAIN APLICATION LOOP
print(UsersData.columns)

ThreadList = []


Order_thread = Keep_order_in_DataFrame(Data,dataLock)
Order_thread.start()

while True:
    Login = str(input("Entry Login (or type in 'exit' to close aplication): "))
    if Login == "exit":
        break

    if (UsersData['Login'] == Login).any():
        row = UsersData[UsersData['Login'] == Login].index[0]
        Users_type = UsersData.loc[row, 'User_type']
        print(Users_type)
        New_th = New_thread(Users_type,Login,Data,UsersData,dataLock)
        ThreadList.append(New_th)
        New_th.start()

    else:
        print('Unrecognized login')