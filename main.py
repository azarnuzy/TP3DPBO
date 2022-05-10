import pathlib
from tkinter import *
import mysql.connector
from PIL import ImageTk, Image

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="db_praktikum"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")


# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result


# Window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)
    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=30)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")
    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=30)
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")
    # Input 3
    options = ["Filsafat Meme", "Sastra Mesin", "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(root)
    input_jurusan.set(options[0])
    label4 = Label(dframe, text="Jurusan").grid(row=2, column=0, sticky="w")
    input4 = OptionMenu(dframe, input_jurusan, *options)
    input4.grid(row=2, column=1, padx=20, pady=10, sticky='w')
    # Input 4
    input_jnsKelamin = StringVar(root)
    input_jnsKelamin.set(options[0])
    label5 = Label(dframe, text="Jenis Kelamin").grid(row=3, column=0, sticky="w")
    laki2 = Radiobutton(dframe, text="Laki-Laki", variable=input_jnsKelamin, value="Laki-Laki")
    laki2.grid(row=3,  column=1, padx=20, pady=10, sticky='w')
    perempuan = Radiobutton(dframe, text="Perempuan", variable=input_jnsKelamin, value="Perempuan")
    perempuan.grid(row=3,  column=1, padx=100, pady=10, sticky='w')
    # Input 5
    def checkBoxCek():
        hobbies = []
        if input_hobby1.get() is True:
            hobbies.append("Bernyanyi")
        if input_hobby2.get() is True:
            hobbies.append("Bermain Game")
        if input_hobby2.get() is True:
            hobbies.append("Jalan-Jalan")
        return hobbies
        
    input_hobby1 = BooleanVar(root)
    input_hobby2 = BooleanVar(root)
    input_hobby3 = BooleanVar(root)
    label6 =  Label(dframe, text="Hobi").grid(row=4, column=0, sticky="w")
    hobi_bernyanyi = Checkbutton(dframe, text="Bernyanyi", variable=input_hobby1, onvalue=True, offvalue=False)
    hobi_bernyanyi.grid(row=4, column=1, padx=20, pady=10, sticky="w")
    hobi_game = Checkbutton(dframe, text="Bermain Game", variable=input_hobby2, onvalue=True, offvalue=False)
    hobi_game.grid(row=4, column=1, padx=100, pady=10, sticky="w")
    hobi_jln2 = Checkbutton(dframe, text="Jalan-Jalan", variable=input_hobby3, onvalue=True, offvalue=False)
    hobi_jln2.grid(row=4, column=1, padx=210, pady=10, sticky="w")
    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit Data", anchor="s", command=lambda:[insertData(top, input_nama, input_nim, input_jurusan, input_jnsKelamin, checkBoxCek()), top.withdraw()])
    btn_submit.grid(row=3, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Gak jadi / Kembali", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=3, column=1, padx=10)

# Untuk memasukan data
def insertData(parent, nama, nim, jurusan, jnsKelamin, hobbies):
    top = Toplevel()
    # Get data
    nama = nama.get()
    nim = nim.get()
    jurusan = jurusan.get()
    jnsKelamin = jnsKelamin.get()
    hobby = ", ".join(hobbies)

    errorMessage = ""
    if nama == "":
        errorMessage += "Field nama tidak boleh kosong"
    if nim == "":
        errorMessage += "Field nim tidak boleh kosong"
    if jurusan == "":
        errorMessage += "Field jurusan tidak boleh kosong"
    if jnsKelamin == "":
        errorMessage += "Field jnsKelamin tidak boleh kosong"
    if hobby == "":
        errorMessage += "Field hobby tidak boleh kosong"

    if len(errorMessage) == 0:
        global mydb
        global dbcursor
        query = "INSERT INTO mahasiswa values (null, %s, %s, %s, %s, %s)"
        val = (nim, nama, jurusan, jnsKelamin, hobby)
        dbcursor.execute(query, val)
        mydb.commit()

        Label(top, text="Data telah berhasil ditambahkan!").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        # Input data disini
        btn_ok = Button(top, text="Syap!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)
    else:
        Label(top, text=errorMessage).grid(row=0, column=0, padx=20, pady=10, sticky="w")
        # Input data disini
        btn_ok = Button(top, text="Syap!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)
  
# Window Semua Mahasiswa
def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jurusan", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=3)
    title5 = Label(tableFrame, text="Jenis Kelamin", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=4)
    title6 = Label(tableFrame, text="Hobi", borderwidth=1, relief="solid", width=30, padx=5).grid(row=0, column=5)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=3)
        label5 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=4)
        label6 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid", height=2, width=30, padx=5).grid(row=i+1, column=5)
        i += 1

# Dialog konfirmasi hapus semua data
def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Melihat Fasilitas
def viewFacilities():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Fasilitas Kampus")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Fasilitas Kampus")
    head.grid(row=0, column=1, padx=20, pady=10, sticky="w")
    
    path = pathlib.Path().resolve()
    img1 = str(path) + "/images/kelas.jpg"
    img2 = str(path) + "/images/labkomputer.jpg"
    img3 = str(path) + "/images/library.jpg"
    img4 = str(path) + "/images/lobi.jpeg"

    image_list = [img1, img2, img3, img4]
    img = Image.open(img1)
    img = ImageTk.PhotoImage(img)
    panel = Label(frame, image = img)
    panel.image = img
    panel.grid(row = 1, column=0, columnspan=3)

    def forward(image_number):
        nonlocal panel
        nonlocal button_forward
        nonlocal button_back

        panel.grid_forget()
        img = Image.open(image_list[image_number])
        img = ImageTk.PhotoImage(img)
        panel = Label(frame, image = img)
        button_back.grid_forget()
        button_forward.grid_forget()
        panel.image = img
        panel.grid(row=1, column=0, columnspan=3)
        
        button_forward = Button(frame, text=">>", command=lambda: forward    (image_number + 1))
        button_back = Button(frame, text="<<", command=lambda: back(image_number - 1))

        if image_number == 3:
            button_forward = Button(frame, text=">>", state=DISABLED)

        button_back.grid(row=2, column=0)
        button_forward.grid(row=2, column=2)


    def back(image_number):
        nonlocal panel
        nonlocal button_forward
        nonlocal button_back

        panel.grid_forget()
        img = Image.open(image_list[image_number])
        img = ImageTk.PhotoImage(img)
        panel = Label(frame, image = img)
        button_back.grid_forget()
        button_forward.grid_forget()
        panel.image = img
        panel.grid(row=1, column=0, columnspan=3)
        
        button_forward = Button(frame, text=">>", command=lambda: forward    (image_number + 1))
        button_back = Button(frame, text="<<", command=lambda: back(image_number - 1))

        if image_number == 0:
            button_back = Button(frame, text="<<", state=DISABLED)

        button_back.grid(row=2, column=0)
        button_forward.grid(row=2, column=2)
    
    button_back = Button(frame, text="<<", command=lambda: back(), state=DISABLED)
    button_forward = Button(frame, text=">>", command=lambda: forward(2))
    
    button_back.grid(row=2, column=0)
    button_forward.grid(row=2, column=2)

# Dialog konfirmasi keluar GUI
def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=lambda:[top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)

def delAll():
    top = Toplevel()
    # Delete data disini
    global mydb
    global dbcursor
    query = "DELETE FROM mahasiswa"
    dbcursor.execute(query)
    mydb.commit()
    btn_ok = Button(top, text="Zeeb", command=top.destroy)
    btn_ok.pack(pady=20)

# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa", command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa", command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa", command=clearAll, width=30)
b_clear.grid(row=2, column=0, pady=5)

# View Facilities
# Clear all btn
b_clear = Button(buttonGroup, text="Fasilitas Kampus", command=viewFacilities, width=30)
b_clear.grid(row=4, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=5, column=0, pady=5)

root.mainloop()