from tkinter import *  
from tkinter import messagebox
import math,random,os
import tkinter as tk
import sqlite3
# import mysql.connector
# from mysql.connector.cursor import MySQLCursor
mydb = sqlite3.connect('D:travel.db')
mycursor = mydb.cursor()
try:    
    mycursor.execute("CREATE TABLE  package_choice( user_name varchar(50), package_choice INT)")
    mycursor.execute("CREATE TABLE  package_info( package_id INT PRIMARY KEY, package_name varchar(100), package_price INT, package_desc varchar(255))")
    mycursor.execute("CREATE TABLE  user_info( user_info_name varchar(50), user_name varchar(50),user_password varchar(50))")
    mycursor.execute("INSERT INTO package_info VALUES(111,'India',210000,'VISIT THE MAJOR CITIES IN 14 DAYS')")
    mycursor.execute("INSERT INTO package_info VALUES(222,'Thailand',110000,'ENJOY THE BEAUTY OF THAILAND')")
    mycursor.execute("INSERT INTO package_info VALUES(333,'Russia',250000,'HAVE A GREAT TIME IN MOSCOW WITH 5-STAR SUITE')")
    mycursor.execute("INSERT INTO package_info VALUES(444,'America',200000,'ENJOY YOUR STAY AT LAS VEGAS')")
    mycursor.execute("INSERT INTO package_info VALUES(555,'France',250000,'EXPLORE NEW HEIGHTS WITH YOUR LOVED ONES IN PARIS')")
    mycursor.execute("INSERT INTO package_info VALUES(666,'London',150000,'Get your Chance to Steal the Stolen Kohinoor')")
except Exception as e:
    print(e)
mydb.commit()

def myclick1():
    #  register window

       root = Tk()
       root.geometry('500x650')
       root.title("Registration Form")

       


       def printent1():
           global uname1
           first=entry_1.get()
           uname1=entry_2.get()
           var1=entry_3.get()
           sql = f"INSERT INTO user_info (user_info_name,user_name,user_password) VALUES ('{first}','{uname1}','{var1}')"
           mycursor.execute(sql)
           mydb.commit()
           root.destroy()
           
           
           

       label_0 = Label(root, text="Registration form",relief="solid",width=20,font=("arial", 19,"bold"))
       label_0.place(x=90,y=150)


       label_1 = Label(root, text="Name :",width=20,font=("bold", 10))
       label_1.place(x=80,y=240)

       entry_1 = Entry(root)
       entry_1.place(x=240,y=242)


       label_2 = Label(root, text="Username :",width=20,font=("bold", 10))
       label_2.place(x=80,y=280)

       entry_2 = Entry(root)
       entry_2.place(x=240,y=282)

       label_3 = Label(root, text="Password :",width=20,font=("bold", 10))
       label_3.place(x=80,y=320)

       entry_3 = Entry(root)
       entry_3.place(x=240,y=320)


       but_login=Button(root, text='Signup',width=12,bg='brown',fg='white',command=printent1).place(x=130,y=515)
       but_login=Button(root, text='Close',width=12,bg='brown',fg='white',command=root.destroy).place(x=250,y=515)

def myclick2():
    #    login window
    
       root = Tk()
       root.geometry('500x650')
                     
       root.title("login")
       #root.config(background="white")

       def abtt():
           window=Tk()
           window.title("INCORRECT CREDITIALS ")
           window.geometry("350x180")
           label_1=Label(window,text="WRONG USERNAME OR PASSWORD",relief="solid",font=("arial", 12,"bold")).place(x=30,y=70)
           b1=Button(window,text="close",width=12,bg='brown',fg='white',command=window.destroy).place(x=120,y=120)
           window.mainloop()           
           

     



       
       def printent2():
           global uname1
           uname1=username.get()
           var1=password.get()
           mycursor.execute(f'SELECT user_password FROM user_info WHERE user_name ="{uname1}"')
           record=mycursor.fetchone()
           if record and var1==record[0]:
               myclick3()
           else:
               abtt()
               root.destroy()                       
                                   
                                   
           mydb.commit()

           
           
           

       label_0 = Label(root, text="login",relief="solid",width=20,font=("arial", 19,"bold"))
       label_0.place(x=90,y=150)



       label_1 = Label(root, text="UserName :",width=20,font=("bold", 10))
       label_1.place(x=80,y=280)

       username = Entry(root)
       username.place(x=240,y=282)

       label_2 = Label(root, text="Password :",width=20,font=("bold", 10))
       label_2.place(x=80,y=320)

       password = Entry(root)
       password.place(x=240,y=320)


       but_login=Button(root, text='Login',width=12,bg='brown',fg='white',command=printent2).place(x=130,y=515)
       but_login=Button(root, text='close',width=12,bg='brown',fg='white',command=root.destroy).place(x=250,y=515)

def myclick3():
#package choosing window
       root = Tk()
       root.geometry('650x850')
       root.title("package")
       #root.config(background="white")

          
       def second_win(dis):
            
            window=Tk()
            window.title("Welcome ")
            window.geometry("550x400")
            label_1=Label(window,text="WELCOME  "+uname1,relief="solid",font=("arial", 12,"bold")).place(x=30,y=70)
            label_1=Label(window,text="DETAILS OF CHOOSEN PACKAGE ARE:  ",relief="solid",font=("arial", 12,"bold")).place(x=30,y=100)
            
            label_2=Label(window,text="place name : "+dis[1],relief="solid",font=("arial", 12,"bold")).place(x=30,y=130)
            label_3=Label(window,text="package price : "+str(dis[2]),relief="solid",font=("arial", 12,"bold")).place(x=30,y=160)
            label_4=Label(window,text="DESCRIPTION : "+dis[3],relief="solid",font=("arial", 12,"bold")).place(x=30,y=190)
            
            b1=Button(window,text="close",width=12,bg='brown',fg='white',command=window.destroy).place(x=120,y=270)
            window.mainloop()           
                  
       def result():
           
           userch=ch1.get()
           print(userch)
           mycursor.execute(f"Select * from package_info WHERE package_name='{userch}'")
           dis=mycursor.fetchone()
        
           second_win(dis)
           
               
       label_0 = Label(root, text="CHOOSE  PLACE TO VISIT",relief="solid",width=25,font=("arial", 19,"bold"))
       label_0.place(x=90,y=150)


       ch1=StringVar(root,"India") 
       Radiobutton(root,text="India - 2,10,000 rupees",variable=ch1,value="India").place(x=230,y=330)
       Radiobutton(root,text="Thailand - 1,10,000 rupees",variable=ch1,value="Thailand").place(x=230,y=360)
       Radiobutton(root,text="Russia - 2,50,000 rupees",variable=ch1,value="Russia").place(x=230,y=390)
       Radiobutton(root,text="America - 2,00,000 rupees",variable=ch1,value="America").place(x=230,y=420)
       Radiobutton(root,text="France - 2,50,000 rupees",variable=ch1,value="France").place(x=230,y=450)
       Radiobutton(root,text="London - 1,50,000 rupees",variable=ch1,value="London").place(x=230,y=480)

       
             

       but_login=Button(root, text='select',width=12,bg='brown',fg='white',command=result).place(x=180,y=515)
       but_login=Button(root, text='close',width=12,bg='brown',fg='white',command=root.destroy).place(x=290,y=515)
       
       
    
root=Tk()       


root.geometry("500x500")
root.title(' User ')
root.configure(bg='WHITE')
label_0 =Label(root,text="Travel agency",bd=9,relief=GROOVE,width=20,bg='WHITE',fg="black",font=("times new roman",30,"bold")).place(x=0,y=35)
          
mybutton1=Button(root,text="SIGN IN",font=("times new roman",30,"bold"),width=15,bg="WHITE",fg='green',command=myclick1).place(x=78,y=220)
mybutton1=Button(root,text="LOGIN",font=("times new roman",30,"bold"),width=15,bg="WHITE",fg='green',command=myclick2).place(x=78,y=320)

root.mainloop()
