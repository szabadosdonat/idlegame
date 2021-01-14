# idle játék
# Szabados Donát

import tkinter as tk
from threading import Timer


class Money:
    def __init__(self, money):
        self.money = money
        self.ertek = 1
        self.eladasi_gyorsasag = 1
        self.gyarak_szama = 0

    @property
    def get_money(self):
        return self.money

    @property
    def get_gyarak_szama(self):
        return self.gyarak_szama

    def gomb(self):
        self.money += self.ertek
        print(self.money)

    def upgrade_1(self):
        # gyár építése
        self.gyarak_szama += 1

    def upgrade_2(self):
        # termék továbbfejlesztése (2x eladási ár)
        self.ertek *= 2

    def upgrade_3(self):
        # munkások béremelése (+5% gyártási gyorsaság)
        self.eladasi_gyorsasag += self.eladasi_gyorsasag*0.05

    def upgrade_4(self):
        # termék finomhangolása (+5% eladási ár)
        self.ertek += self.ertek*0.05


def show(f):
    f.tkraise()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("360x640")
    root.title("Munkahely")

    m = Money(50)

    # framek legyártása
    frame_mainmenu = tk.Frame(root, width=360, height=640)
    frame_home = tk.Frame(root, width=360, height=640)
    frame_upgrades = tk.Frame(root, width=360, height=640)
    for frame in (frame_mainmenu, frame_home, frame_upgrades):
        frame.grid(row=0, column=0, sticky='nsew')

    # main menu
    tk.Label(frame_mainmenu, text="Idle Játék", font=('italic', 32)).place(relx=0.5, rely=0.2, anchor='center')
    tk.Button(frame_mainmenu, bd=10, relief="groove", text="Játék indítása", font=('italic', 20), command=lambda: show(frame_home)).place(relx=0.5, rely=0.4, anchor='center')
    tk.Button(frame_mainmenu, bd=10, relief="groove", text="Beállítások", font=('italic', 20), command=None).place(relx=0.5, rely=0.53, anchor='center')
    tk.Button(frame_mainmenu, bd=10, relief="groove", text="Kilépés", font=('italic', 20), command=lambda: root.quit()).place(relx=0.5, rely=0.66, anchor='center')

    # home
    tk.Label(frame_home, text='Pénzed:\n' + str(m.get_money), font=('italic', 25)).place(relx=0.5, rely=0.15, anchor='center')
    tk.Button(frame_home, width=10, bd=0, text='Fejlesztések', command=lambda: show(frame_upgrades)).place(relx=0.03, rely=0.02)
    tk.Button(frame_home, width=10, bd=0, text='Főmenü', command=lambda: show(frame_mainmenu)).place(relx=0.75, rely=0.02)
    tk.Button(frame_home, text="Kézi gyártás", bd=10, font=('italic', 25), command=lambda: m.gomb()).place(relx=0.5, rely=0.75, anchor="center")

    # upgrades
    tk.Label(frame_upgrades, text='Pénzed:\n' + str(m.get_money), font=('italic', 25)).place(relx=0.5, rely=0.15, anchor='center')

    frame_upgrades.columnconfigure(0, weight=1)
    frame_upgrades.columnconfigure(1, weight=1)
    frame_upgrades.rowconfigure(0, weight=3)
    frame_upgrades.rowconfigure(1, weight=1)
    frame_upgrades.rowconfigure(2, weight=1)
    frame_upgrades.rowconfigure(3, weight=1)
    frame_upgrades.rowconfigure(4, weight=1)
    frame_upgrades.rowconfigure(5, weight=1)
    frame_upgrades.rowconfigure(6, weight=1)

    tk.Button(frame_upgrades, bd=3, relief='ridge', text="gyár építése\n(a gyárak automatikusan\npénzt generálnak)", command=lambda: m.upgrade_1()).grid(row=1, column=0, sticky='nsew')
    tk.Button(frame_upgrades, bd=3, relief='ridge', text="termék továbbfejlesztése\n(x2 értékű áru)", command=lambda: m.upgrade_2()).grid(row=1, column=1, sticky='nsew')
    tk.Button(frame_upgrades, bd=3, relief='ridge', text="munkások béremelése\n(+5% gyártási gyorsaság)", command=lambda: m.upgrade_3()).grid(row=2, column=0, sticky='nsew')
    tk.Button(frame_upgrades, bd=3, relief='ridge', text="termék finomhangolása\n(+5% eladási ár)", command=lambda: m.upgrade_4()).grid(row=2, column=1, sticky='nsew')
    tk.Button(frame_upgrades, bd=3, relief='ridge', text="kézműves trendek\n(+100% kézzel készített áru eladási ár)").grid(row=3, column=0, sticky='nsew')
    tk.Button(frame_upgrades, bd=3, relief='ridge', text="upgrade 6").grid(row=3, column=1, sticky='nsew')
    tk.Button(frame_upgrades, bd=3, relief='ridge', text="upgrade 7").grid(row=4, column=0, sticky='nsew')
    tk.Button(frame_upgrades, bd=3, relief='ridge', text="upgrade 8").grid(row=4, column=1, sticky='nsew')
    tk.Button(frame_upgrades, width=10, bd=0, text='Főképernyő', command=lambda: show(frame_home)).place(relx=0.03, rely=0.02)
    tk.Button(frame_upgrades, width=10, bd=0, text='Főmenü', command=lambda: show(frame_mainmenu)).place(relx=0.75, rely=0.02)

    # pénz
    


    show(frame_mainmenu)

    root.mainloop()
