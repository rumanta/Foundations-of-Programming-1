#==============================================================================
#  ▼ M,N,K Game
#
#   -- created on Sunday 04.12.2016
#
#   -- by: William Rumanta
#          1606895461
#          Kelas B
#
#==============================================================================
'''
 Class GameMenu
 Berfungsi sebagai window main menu untuk game.
 Memiliki method:
       - windowsettings() untuk memunculkan window game settings.
       - windowshistory() untuk memunculkan window game history.
       - exitgame() untuk close program.

 Class GameBoard
 Berfungsi untuk membuat papan permainan berdasarkan input dan menjalankan fungsi game.
 Memiliki method:
       - backtomenu() untuk kembali ke main menu menggunakan menubar.
       - enter_command() menggunakan fungsi tombol Enter pada keyboard sebagai alternatif button OK.
       - gamedisplay() untuk mengiterasi dan membuat papan permainan menggunakan rectangle.
       - onclick() untuk menjalankan fungsi klik pada setiap kotak.
       - check_win() untuk mengecek kemenangan berdasarkan input kemenangan.

 Penjelasan variabel pada GameBoard:
       - self.coor = list yang memiliki kumpulan list baris dengan berisi index kolom.
       - self.row = index baris dari kotak yang diklik.
       - self.col = index kolom dari kotak yang diklik.
       - self.tanda = menyimpan tanda X atau O bergantung pada putaran player.
       - self.player = menyimpan siapa nama player pada putaran tersebut.
       - self.total = jumlah kotak keseluruhan pada board.

 Penjelasan khusus untuk method check_win():
     Method ini akan menjalankan proramnya setiap saat player menjalankan putarannya.
     Dalam method ini, terdapat pengecekan terhadap arah horizontal, vertikal, maupun diagonal
     pada setiap bidak/tanda (X atau O) yang diletakkan oleh player.

     Contohnya untuk bagian horizontal, bidak yang telah diletakkan akan secara otomatis
     mengecek sebelah kanannya, apakah ada bidak yang sama dengannya, maka akan ada variabel
     yang menghitung setiap bidak yang sama secara berturut-turut di sebelah kanannya.
     Apabila tidak ditemukan/menemukan bidak yang berbeda, maka penghitungan akan langsung
     berhenti, dan lalu bidak tersebut akan mulai mengecek arah sebelah kiri dengan proses
     penghitungan yang sama.

     Berdasarkan contoh itu, berlaku juga untuk vertikal dan juga diagonal, sehingga
     setelah melewati semua proses penghitungan, akan dilakukan pengecekan variabel yang
     menyimpan poin hitung masing-masing arah, dengan input kemenangan yang diminta oleh user.

 Module tkinter.messagebox
 Berfungsi untuk menampilkan popup message box untuk kondisi yang diinginkan

 Module winsound
 Berfungsi untuk memasukkan audio ke dalam program.
 Memiliki fungsi berupa PlaySound yang bisa memainkan audio yang diinginkan.
 Mungsi PlaySound membutuhkan parameter (<nama file audio>, <sound parameter>).
 Mada tugas ini digunakan sound parameter berupa SND_ASYNC yang memainkan audio secara
 bersamaan dengan program yang sedang dijalankan.

 Module tkinter.ttk
 Module ini dipanggil untuk membuat tabel yang menampilkan history dalam game.
 Tabel tersebut dicapai melalui widget Treeview.
'''

from tkinter import *
import tkinter.messagebox
from datetime import datetime
import winsound
from tkinter import ttk

class GameMenu:
    def __init__(self):
        self.mainmenu = Tk()  # Membuat sebuah window Main Menu
        self.mainmenu.minsize(width=400,height=380)
        self.mainmenu.title('Tic Tac Toe')
        frameUP = Frame(self.mainmenu)  # Membuat sebuah frame atas pada window
        frameUP.pack()
        logo = PhotoImage(file = 'tictactoe.gif')
        kanvas = Canvas(frameUP)
        kanvas.create_image(190, 120, image = logo)  # Meletakan sebuah gambar pada frame
        kanvas.pack(side = LEFT)
        frameLOW = Frame(self.mainmenu)  # Membuat sebuah frame bawah pada window
        frameLOW.pack()
        buttonStart = Button(frameLOW, text = 'Start Game', font = 'Arial 13', command = self.windowsettings)  # Membuat start button
        buttonHistory = Button(frameLOW, text = 'History', font = 'Arial 13', command = self.windowhistory)  # Membuat History button
        buttonExit = Button(frameLOW, text = 'Exit', font = 'Arial 13', command = self.exitgame)  # Membuat Exit button
        buttonStart.pack()
        buttonHistory.pack()
        buttonExit.pack()
        self.mainmenu.mainloop()

    def windowsettings(self):
        self.mainmenu.destroy()  # Close window main menu
        winsound.PlaySound('click_sound.wav', winsound.SND_ASYNC)
        GameBoard()  # Membuka window Settings

    def windowhistory(self):
        winsound.PlaySound('click_sound.wav', winsound.SND_ASYNC)
        self.history = Tk()  # Membuat sebuah window untuk history
        self.history.title('Game History')
        self.tree = ttk.Treeview(self.history, columns=('kolom2', 'kolom3'))  # Membuat sebuah tabel treeview dengan menambahkan 2 kolom lagi
        self.tree.heading('#0', text='Tanggal/Waktu')  # Default kolom pada treeview adalah 1
        self.tree.heading('#1', text='Pemenang')  # Kolom2
        self.tree.heading('#2', text='Jumlah Putaran')  # Kolom3
        self.tree.column('#0', stretch=YES, anchor = 'center')
        self.tree.column('#1', stretch=YES, anchor = 'center')  # Config kolom, anchor = penempatan posisi text
        self.tree.column('#2', stretch=YES, anchor = 'center')
        self.tree.grid(row=4, columnspan=4)

        infile = open('history.txt', 'r')  # Membuka file history.txt
        statistic = infile.readlines()  # Memisahkan setiap baris dalam text menjadi elemen dalam list
        for data in statistic:
            try:
                stat = data.split(' ') # Split kalimat berdasarkan spasi pada setiap baris
                # Lalu memasukkan setiap data yang sudah di split ke dalam kolom masing - masing
                self.tree.insert('', 'end', text = stat[0] + '   ' + stat[1], values = (stat[2] + ' ' + stat[3], stat[4]))
            except IndexError:
                pass
        infile.close()  # Close file history.txt

    def exitgame(self):
        winsound.PlaySound('click_sound.wav', winsound.SND_ASYNC)
        self.mainmenu.destroy()  # Close window main menu


class GameBoard:
    def __init__(self):
        self.window = Tk()  # Membuat sebuah window Settings
        self.window.minsize(width=300,height=170)
        self.window.title('Settings')
        self.baris = IntVar()
        self.kolom = IntVar()
        self.menang = IntVar()

        self.window.bind('<Return>', self.enter_command)  # Memfungsikan Enter-key pada keyboard

        menubar = Menu(self.window)  # Membuat sebuah Menu Bar pada window Settings
        self.window.config(menu = menubar)
        mainmenu = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = 'Menu', menu = mainmenu)
        mainmenu.add_command(label = 'Main Menu', command = self.backtomenu)  # Menambahkan opsi Main Menu pada Menu Bar

        Label(self.window, text = 'Jumlah Baris:').pack()
        Entry(self.window, textvariable = self.baris).pack()
        Label(self.window, text = 'Jumlah Kolom:').pack()       # Menyusun label dan entry untuk input setting game board
        Entry(self.window, textvariable = self.kolom).pack()
        Label(self.window, text = 'Jumlah Kemenangan:').pack()
        Entry(self.window, textvariable = self.menang).pack()
        Button(self.window, text = 'OK', command = self.gamedisplay).pack()
        self.window.mainloop()

    def backtomenu(self):  # Method yang digunakan oleh opsi Main Menu pada Menu Bar
        winsound.PlaySound('klik.wav', winsound.SND_ASYNC)
        self.window.destroy()
        GameMenu()  # Berfungsi untuk membuka kembali window Main Menu

    def enter_command(self, event): # Alternatif dari button OK pada window Settings
        self.gamedisplay()          # Dapat membuka board menggunakan Enter-key

    def gamedisplay(self):
        winsound.PlaySound('click_sound.wav', winsound.SND_ASYNC)
        self.board = Tk()  # Membuat sebuah window board game
        self.board.title('Game')
        self.canvas = Canvas(self.board, width = self.kolom.get() * 50, height = self.baris.get() * 50)
        self.canvas.pack()
        count = 0
        self.turn = 0
        self.total = (self.baris.get() * self.kolom.get()) - 1
        self.coor = []
        for row in range(self.baris.get()):  # Iterasi setiap baris
            self.coor.append([])  # Menambahkan list baris kosong ke dalam list self.coor
            for column in range(self.kolom.get()):  # Iterasi setiap kolom
                self.coor[row].append(column)  # Menambahkan index kolom ke dalam list baris
                '''Dibawah ini adalah fungsi untuk membuat kotak - kotak berukuran 50x50 dengan warna yang bergantian, 
                serta memberikan tags berupa index baris dan kolom pada masing - masing kotak'''
                if count % 2 == 0:
                    mark = self.canvas.create_rectangle(column * 50, row * 50, (column * 50) + 50, (row * 50) + 50, fill = 'white', tags = (row, column))    
                else:
                    mark = self.canvas.create_rectangle(column * 50, row * 50, (column * 50) + 50, (row * 50) + 50, fill = 'grey', tags = (row, column))

                self.canvas.tag_bind(mark, '<Button-1>', lambda event, target = mark: self.onclick(event, target))  # Memfungsikan setiap kotak agar dapat diklik

                if column == (self.kolom.get() - 1):  # Penghitungan variabel count
                    if self.kolom.get() % 2 == 0:     # untuk menghindari kesalahan pewarnaan
                        count += 2                    # apabila jumlah kolom genap
                    else:
                        count += 1
                else:
                    count += 1
        self.board.mainloop()

    def onclick(self, event, target):
        try:
            self.row, self.col = int(self.canvas.gettags(target)[0]), int(self.canvas.gettags(target)[1]) # Mengambil index baris dan kolom dari tags kotak yang diklik
            self.listkolom = self.coor[self.row]

            '''Dibawah ini adalah fungsi yang akan dijalankan secara bergantian tergantung dengan putaran'''
            if self.turn % 2 == 0:
                self.canvas.create_line((self.col + 1) * 50, self.row * 50, 50 + (self.col - 1) * 50, (self.row) * 50 + 50, width = 4, fill = 'red')
                self.canvas.create_line(self.col * 50, self.row * 50, 50 + self.col * 50, 50 + self.row * 50, width = 4, fill = 'red')  # Membuat tanda silang dengan 2 line
                self.canvas.itemconfig(target, tags = 'X')  # Mengganti tags pada kotak yang sudah diklik menjadi string
                self.coor[self.row][self.col] = 'X'  # Mengganti index kotak yang telah di klik menjadi X
                self.tanda = self.coor[self.row][self.col]
                self.player = 'Pemain Merah'
                self.check_win()
            else:
                self.canvas.create_oval(self.col * 50, self.row * 50, 50 + self.col * 50, 50 + self.row * 50, width = 4, outline = 'blue')
                self.canvas.itemconfig(target, tags = 'O') # Mengganti tags pada kotak yang sudah diklik menjadi string
                self.coor[self.row][self.col] = 'O'  # Mengganti index kotak yang telah di klik menjadi O
                self.tanda = self.coor[self.row][self.col]
                self.player = 'Pemain Biru'
                self.check_win()

            self.total -= 1
            self.turn += 1
            winsound.PlaySound('duck_censor', winsound.SND_ASYNC)

        except ValueError:  # Error yang akan muncul akibat konversi string berupa huruf X atau O menjadi integer, lihat line 196
            tkinter.messagebox.showerror('Error', 'Tidak bisa menekan tombol\nyang telah ditekan')

    def check_win(self):
        menang = self.menang.get()  # Mengambil nilai kemenangan dari input sebelumnya
        win_x, win_y, win_d1, win_d2 = 0, 0, 0, 0  # 4 variabel penghitung yang berbeda

        # Check Horizontal
        for i in range(self.col, len(self.listkolom)):  # Mengecek dari posisi bidak, ke arah kanan
            if self.listkolom[i] == self.tanda:
                win_x += 1
            else:
                break
        for i in reversed(range(self.col)):  # Mengecek dari posisi bidak, ke arah kiri
            if self.listkolom[i] == self.tanda:
                win_x += 1
            else:
                break

        # Check Vertical
        for i in range(self.row, len(self.coor)):  # Mengecek dari posisi bidak, ke arah bawah
            if self.coor[i][self.col] == self.tanda:
                win_y += 1
            else:
                break
        for i in reversed(range(self.row)):  # Mengecek dari posisi bidak, ke arah atas
            if self.coor[i][self.col] == self.tanda:
                win_y += 1
            else:
                break

        # Check Diagonal
        # Mengecek dari posisi bidak, serong ke arah kanan bawah
        for i, j in zip(range(self.row, len(self.coor)), range(self.col, len(self.listkolom))):
            if self.coor[i][j] == self.tanda:
                win_d1 += 1
            else:
                break
        # Mengecek dari posisi bidak, serong ke arah kiri atas
        for i, j in zip(reversed(range(self.row)), reversed(range(self.col))):
            if self.coor[i][j] == self.tanda:
                win_d1 += 1
            else:
                break

        # Mengecek dari posisi bidak, serong ke kiri bawah
        for i, j in zip(range(self.row, len(self.coor)), reversed(range(self.col + 1))):
            if self.coor[i][j] == self.tanda:
                win_d2 += 1
            else:
                break
        # Mengecek dari posisi bidak, serong ke kanan atas
        for i, j in zip(reversed(range(self.row)), range(self.col + 1, len(self.listkolom))):
            if self.coor[i][j] == self.tanda:
                win_d2 += 1
            else:
                break

        # Jika ada poin perhitungan yang SAMA dengan KEMENANGAN
        if win_x >= menang or win_y >= menang or win_d1 >= menang or win_d2 >= menang:
            tkinter.messagebox.showinfo('The End', self.player + ' wins the game!\nwith ' + str(self.turn + 1) + ' turns')
            self.canvas.config(state = DISABLED)  # Membuat board game tidak dapat diklik lagi setelah ada yang menang
            catatan = str(datetime.now()) + ' ' + self.player + ' ' + str(self.turn + 1) + '\n'  # Menyimpan hasil statistik permainan
            outfile = open('history.txt' , 'a') # Membuka file history.txt
            outfile.write(catatan)  # Mencatatkan isi statistik permainan ke dalam history.txt
            outfile.close()  # Close file

        # Jika SERI
        elif win_x != menang and win_y != menang and win_d1 != menang and win_d2 != menang and self.total == 0:
            tkinter.messagebox.showinfo('Draw', 'Permainan Seri!')
            catatan = str(datetime.now()) + ' ' + 'Permainan Seri' + ' ' + str(self.turn + 1) + '\n'  # Menyimpan hasil statistik permainan
            outfile = open('history.txt' , 'a')  # Membuka file history.txt
            outfile.write(catatan)  # Mencatatkan isi statistik permainan ke dalam history.txt
            outfile.close()  # Close file

GameMenu()