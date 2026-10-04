import tkinter as tk
from tkinter import ttk, messagebox
import json, os
from datetime import datetime

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin123"
DATA_FILE = "salon_history.json"

STAFF = [
    ["1","Maria Santos","Hair Stylist","09123456789"],
    ["2","Anna Cruz","Nail Technician","09234567890"],
    ["3","Jessica Garcia","Hair Colorist","09345678901"],
    ["4","Sofia Reyes","Beauty Specialist","09456789012"],
    ["5","Angela Flores","Hair Stylist","09567890123"],
    ["6","Patricia Ramos","Nail Technician","09678901234"],
    ["7","Catherine Lopez","Hair Colorist","09789012345"],
    ["8","Isabella Torres","Beauty Specialist","09890123456"],
    ["9","Michelle Aquino","Hair Stylist","09901234567"],
    ["10","Rachel Mendoza","Nail Technician","09012345678"],
]

PROMOS = [
    ["Rebond","₱1,499","Hair rebonding promo"],
    ["Manicure","₱299","Classic manicure promo"],
    ["Spa","₱799","Relaxing spa promo"],
]

SERVICES = {"Rebond":1499,"Manicure":299,"Spa":799,"Haircut":350,"Hair Color":1200}

def load_history():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE,"r",encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return []

history = load_history()

def save_history():
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(history,f,indent=4,ensure_ascii=False)

def login():
    if email_entry.get().strip() == ADMIN_EMAIL and password_entry.get() == ADMIN_PASSWORD:
        login_window.destroy()
        open_dashboard()
    else:
        messagebox.showerror("Login Failed","Incorrect email or password.")

login_window = tk.Tk()
login_window.title("GLAM SALON - Admin Login")
login_window.geometry("450x350")
login_window.resizable(False,False)

tk.Label(login_window,text="GLAM SALON",font=("Arial",28,"bold")).pack(pady=(45,10))
tk.Label(login_window,text="Admin Login",font=("Arial",16)).pack()
tk.Label(login_window,text="Email").pack(pady=(20,3))
email_entry = tk.Entry(login_window,width=35)
email_entry.pack()
tk.Label(login_window,text="Password").pack(pady=(10,3))
password_entry = tk.Entry(login_window,width=35,show="*")
password_entry.pack()
tk.Button(login_window,text="LOGIN",width=20,bg="#d88aaa",fg="white",
          font=("Arial",11,"bold"),command=login).pack(pady=25)

def open_dashboard():
    global root, content
    root = tk.Tk()
    root.title("GLAM SALON - Salon Appointment and Management System")
    root.geometry("1100x700")
    root.minsize(900,600)

    header = tk.Frame(root,bg="#d88aaa",height=75)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header,text="GLAM SALON",bg="#d88aaa",fg="white",
             font=("Arial",25,"bold")).pack(side="left",padx=25)
    tk.Label(header,text="Salon Appointment and Management System",
             bg="#d88aaa",fg="white",font=("Arial",11)).pack(side="left")

    main = tk.Frame(root)
    main.pack(fill="both",expand=True)

    side = tk.Frame(main,bg="#f5e5ec",width=210)
    side.pack(side="left",fill="y")
    side.pack_propagate(False)

    for text,cmd in [
        ("Dashboard",dashboard_page),
        ("Appointments",appointment_page),
        ("Staff",staff_page),
        ("Promos",promo_page),
        ("History / Reports",history_page),
        ("Exit",root.destroy)
    ]:
        tk.Button(side,text=text,command=cmd,width=22,height=2,
                  relief="flat",bg="#f5e5ec",font=("Arial",11)).pack(pady=5)

    content = tk.Frame(main,bg="white")
    content.pack(side="right",fill="both",expand=True)
    dashboard_page()
    root.mainloop()

def clear():
    for w in content.winfo_children():
        w.destroy()

def page_title(text,sub=""):
    tk.Label(content,text=text,font=("Arial",25,"bold")).pack(pady=(25,5))
    if sub:
        tk.Label(content,text=sub,font=("Arial",12)).pack(pady=(0,20))

def dashboard_page():
    clear()
    page_title("Welcome to GLAM SALON","Salon Appointment and Management System")
    box=tk.Frame(content,bg="#f8eef2")
    box.pack(fill="x",padx=40,pady=15)
    for name,num in [("STAFF",len(STAFF)),("PROMOS",len(PROMOS)),("APPOINTMENTS",len(history))]:
        card=tk.Frame(box,bg="white",width=200,height=120)
        card.pack(side="left",padx=15,pady=20,expand=True,fill="both")
        card.pack_propagate(False)
        tk.Label(card,text=str(num),font=("Arial",28,"bold"),bg="white").pack(pady=(20,3))
        tk.Label(card,text=name,font=("Arial",11,"bold"),bg="white").pack()
    tk.Label(content,text="Available Services",font=("Arial",18,"bold")).pack(pady=(25,10))
    tk.Label(content,text="   ".join(f"{n} - ₱{p:,}" for n,p in SERVICES.items()),
             font=("Arial",11)).pack()

def appointment_page():
    clear()
    page_title("Appointments","Create a new salon appointment")
    form=tk.Frame(content); form.pack(pady=10)
    fields=["Customer Name","Contact","Date","Time"]
    entries=[]
    for i,label in enumerate(fields):
        tk.Label(form,text=label,font=("Arial",11)).grid(row=i,column=0,sticky="w",padx=10,pady=7)
        e=tk.Entry(form,width=35); e.grid(row=i,column=1,padx=10,pady=7); entries.append(e)
    customer,contact,date,time=entries

    tk.Label(form,text="Service",font=("Arial",11)).grid(row=4,column=0,sticky="w",padx=10,pady=7)
    service=ttk.Combobox(form,values=list(SERVICES),width=32,state="readonly")
    service.grid(row=4,column=1,padx=10,pady=7); service.current(0)

    tk.Label(form,text="Staff",font=("Arial",11)).grid(row=5,column=0,sticky="w",padx=10,pady=7)
    staff=ttk.Combobox(form,values=[s[1] for s in STAFF],width=32,state="readonly")
    staff.grid(row=5,column=1,padx=10,pady=7); staff.current(0)

    def book():
        if not customer.get().strip():
            messagebox.showwarning("Missing","Enter customer name."); return
        history.append({
            "customer":customer.get().strip(),"contact":contact.get().strip(),
            "date":date.get().strip(),"time":time.get().strip(),
            "service":service.get(),"staff":staff.get(),
            "price":SERVICES[service.get()],
            "created":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status":"Booked"
        })
        save_history()
        messagebox.showinfo("Success","Appointment saved successfully.")
        for e in entries: e.delete(0,tk.END)
        dashboard_page()

    tk.Button(content,text="BOOK APPOINTMENT",command=book,width=25,
              bg="#d88aaa",fg="white",font=("Arial",11,"bold")).pack(pady=20)

def staff_page():
    clear(); page_title("Staff Management","Salon staff information")
    frame=tk.Frame(content); frame.pack(fill="both",expand=True,padx=30,pady=10)
    cols=("ID","Name","Position","Contact")
    tree=ttk.Treeview(frame,columns=cols,show="headings",height=16)
    for c in cols:
        tree.heading(c,text=c); tree.column(c,width=190)
    for row in STAFF: tree.insert("", "end", values=row)
    tree.pack(fill="both",expand=True)

def promo_page():
    clear(); page_title("Promos","Current GLAM SALON promotions")
    frame=tk.Frame(content); frame.pack(pady=20)
    for name,price,desc in PROMOS:
        card=tk.Frame(frame,bg="#f8eef2",width=600,height=100)
        card.pack(pady=8); card.pack_propagate(False)
        tk.Label(card,text=name,bg="#f8eef2",font=("Arial",18,"bold")).pack(pady=(12,2))
        tk.Label(card,text=f"{price}  -  {desc}",bg="#f8eef2",font=("Arial",11)).pack()

def history_page():
    clear(); page_title("History / Reports","Previous salon appointment records")
    frame=tk.Frame(content); frame.pack(fill="both",expand=True,padx=10,pady=10)
    cols=("Customer","Contact","Date","Time","Service","Staff","Price","Status")
    tree=ttk.Treeview(frame,columns=cols,show="headings",height=18)
    widths=[120,100,90,80,100,130,80,80]
    for c,w in zip(cols,widths):
        tree.heading(c,text=c); tree.column(c,width=w)
    for x in history:
        tree.insert("", "end", values=(
            x.get("customer",""),x.get("contact",""),x.get("date",""),
            x.get("time",""),x.get("service",""),x.get("staff",""),
            f"₱{x.get('price',0):,}",x.get("status","")))
    tree.pack(fill="both",expand=True)

login_window.mainloop()