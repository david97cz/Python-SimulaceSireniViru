import tkinter as tk
from tkinter import ttk
from random import randint


class VirusSimulationApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x900")
        self.master.title("Simulace šíření viru")

        self.nakazenych = 1
        self.zdravych = 0
        self.celkem = self.zdravych + self.nakazenych
        self.r = 10
        self.pravdepodovnost_nakazeni = 70
        self.rychlost_vykreslovani = 10
        self.start_zmacknuto = False

        self.populace = Populace(self)

        self.create_widgets()

    def create_widgets(self):
        self.root = ttk.Notebook(self.master)
        self.oblast = ttk.Frame(self.root)
        self.root.add(self.oblast)
        self.canvas = tk.Canvas(self.oblast, height=600, width=600)
        self.canvas.grid(row=1, column=1)
        self.canvas2 = tk.Canvas(self.oblast, height=60, width=60)
        self.canvas2.grid(row=2, column=1)

        self.start_button = tk.Button(self.canvas2, text="Start", command=self.start)
        self.start_button.grid(row=0, column=0)
        self.stop_button = tk.Button(self.canvas2, text="Exit", command=self.stop)
        self.stop_button.grid(row=0, column=1)
        self.pauza_button = tk.Button(self.canvas2, text="Stop", command=self.pauza)
        self.pauza_button.grid(row=1, column=0)
        self.reset_button = tk.Button(self.canvas2, text="Reset", command=self.reset)
        self.reset_button.grid(row=1, column=1)

        self.label0_F2 = tk.Label(self.canvas2, text="Zvol počet zdravých jedinců:")
        self.label0_F2.grid(row=2, column=0)
        self.slider0Var = tk.IntVar()
        self.slider0_F2 = tk.Scale(self.canvas2,from_=0, to=10, variable=self.slider0Var, command=self.populace.nastav_pocet_zdravych)
        self.slider0_F2.grid(row=2, column=1)

        self.root.pack(expand=1, fill="both")

    def start(self):
        if not self.start_zmacknuto:
            self.populace.zastavit_pohyb()
            self.populace.nastav_pocet_zdravych(self.slider0Var.get())
            self.canvas.delete("all")
            self.populace.list_zdravych.clear()
            self.populace.list_nakazenych.clear()

            self.start_zmacknuto = True
            self.populace.pridat_zdravych(self.zdravych)
            self.populace.pridat_nakazenych(self.nakazenych)
            self.populace.update()

    def stop(self):
        self.master.destroy()

    def pauza(self):
        self.populace.zastavit_pohyb()
        self.start_zmacknuto = False

    def reset(self):
        self.nakazenych = 1
        self.populace.nastav_pocet_zdravych(self.slider0Var.get())
        self.start_zmacknuto = False
        self.canvas.delete("all")
        self.populace.zastavit_pohyb()
        self.populace.list_zdravych.clear()
        self.populace.list_nakazenych.clear()


class Populace:
    def __init__(self, app):
        self.app = app
        self.list_zdravych = []
        self.list_nakazenych = []

    def nastav_pocet_zdravych(self, hodnota):
        self.app.zdravych = int(hodnota)
        self.app.celkem = self.app.zdravych + self.app.nakazenych
        print("Velikost populace zvolena:", self.app.zdravych)

    def pridej_zdraveho(self, posX, posY, rychlostX, rychlostY):
        self.list_zdravych.append([posX, posY, rychlostX, rychlostY])

    def pridej_nakazeneho(self, posX, posY, rychlostX, rychlostY):
        self.list_nakazenych.append([posX, posY, rychlostX, rychlostY])

    def nakazeni(self, index):
        print(f"Objekt {index} se nakazil")
        self.app.nakazenych += 1
        self.app.zdravych -= 1
        print("Nakaženo:", self.app.nakazenych)
        pos = self.list_zdravych[index]
        self.pridej_nakazeneho(*pos)
        del self.list_zdravych[index]

    def srazka(self, i, j, lst):
        lst[i][2] *= -1
        lst[i][0] += 4 * lst[i][2]
        lst[i][3] *= -1
        lst[i][1] += 4 * lst[i][3]
        lst[j][2] *= -1
        lst[j][0] += 4 * lst[j][2]
        lst[j][3] *= -1
        lst[j][1] += 4 * lst[j][3]

    def otoceni_smeru(self, subjekt):
        if subjekt[0] < 10 or subjekt[0] > 590:
            subjekt[2] *= -1
            subjekt[0] += 5 if subjekt[0] < 10 else -5
        if subjekt[1] < 10 or subjekt[1] > 590:
            subjekt[3] *= -1
            subjekt[1] += 5 if subjekt[1] < 10 else -5

    def pridat_zdravych(self, pocet):
        for _ in range(pocet):
            vx, vy = randint(1, 3), randint(1, 3)
            x, y = randint(0, 350), randint(0, 350)
            self.pridej_zdraveho(x, y, vx, vy)

    def pridat_nakazenych(self, pocet):
        for _ in range(pocet):
            vx, vy = randint(1, 3), randint(1, 3)
            x, y = randint(0, 350), randint(0, 350)
            self.pridej_nakazeneho(x, y, vx, vy)

    def pohyb(self, objekt):
        objekt[0] += objekt[2]
        objekt[1] += objekt[3]

    def zastavit_pohyb(self):
        for zdravy in self.list_zdravych:
            zdravy[2], zdravy[3] = 0, 0
        for nemocny in self.list_nakazenych:
            nemocny[2], nemocny[3] = 0, 0

    def update(self):
        self.app.canvas.delete("all")
        self._kontrola_srazek(self.list_zdravych)
        self._kontrola_srazek(self.list_nakazenych)
        self._kontrola_srazek_nakazeni()

        for zdravy in self.list_zdravych:
            self.pohyb(zdravy)
            self.app.canvas.create_oval(zdravy[0] - self.app.r, zdravy[1] - self.app.r, zdravy[0] + self.app.r,
                                        zdravy[1] + self.app.r, fill="red")
            self.otoceni_smeru(zdravy)

        for nemocny in self.list_nakazenych:
            self.pohyb(nemocny)
            self.app.canvas.create_oval(nemocny[0] - self.app.r, nemocny[1] - self.app.r, nemocny[0] + self.app.r,
                                        nemocny[1] + self.app.r, fill="blue")
            self.otoceni_smeru(nemocny)

        self.app.canvas.after(self.app.rychlost_vykreslovani, self.update)

    def _kontrola_srazek(self, lst):
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                distance = ((lst[i][0] - lst[j][0]) ** 2 + (lst[i][1] - lst[j][1]) ** 2) ** 0.5
                if distance < 20:
                    self.srazka(i, j, lst)

    def _kontrola_srazek_nakazeni(self):
        for i in range(len(self.list_zdravych)):
            for j in range(len(self.list_nakazenych)):
                try:
                    distance = ((self.list_zdravych[i][0] - self.list_nakazenych[j][0]) ** 2 + (
                                self.list_zdravych[i][1] - self.list_nakazenych[j][1]) ** 2) ** 0.5
                except:
                    break
                if distance < 20:
                    self.srazka(i, j, self.list_zdravych)
                    if randint(0, 100) < self.app.pravdepodovnost_nakazeni:
                        self.nakazeni(i)
                        break


if __name__ == "__main__":
    root = tk.Tk()
    app = VirusSimulationApp(root)
    root.mainloop()
