from tkinter import *
from tkinter.ttk import Progressbar
import tkinter.messagebox
import tkinter.ttk
import random
from fractions import Fraction
import socket
import static_funcs
import ast
import time
import datetime
import re
import threading
import base64
from urllib.request import urlopen
import ftplib
# need to import as Image or there is a clash with tkinter seen as i imported * from tkinter.
import PIL.Image as Image
import os
from tkinter.filedialog import askopenfilename
import json
import math


# set width and height of desired window, aslo position window in middle of screen.
def set_window(w, h, window):
    # get the required x coordinate where the window can be w pixels wide and be placed in the centre of the
    # user's screen
    x = int((root.winfo_screenwidth() / 2) - (w / 2))
    # get the required y coordinate where the window can be h pixels high and be placed in the centre of the
    # user's screen
    y = int((root.winfo_screenheight() / 2) - (h / 2))
    window.geometry(str(w) + "x" + str(h) + "+" + str(x) + "+" + str(y))

# Do not let more than a limit of characters be in a spesific entry widget
def limit_size(entry, limit):
    value = entry.get()
    if len(value) > limit:
        entry.set(value[:limit])

#handles the client's connection to the database
def db(func, *args):
    s = socket.socket()
    port = 1200
    try:
        s.connect((host, port))
    except ConnectionRefusedError:
        tkinter.messagebox.showerror("Server Error", "Cannot connect to database,\n"
                                                     " check connection and try again.")
        return
    msgr = static_funcs.bytetostr(s.recv(1024))
    print(msgr)
    msgs = bytes("Test", "utf8")
    s.send(msgs)
    msgr = static_funcs.bytetostr(s.recv(1024))
    if msgr == "y":
        print("Access granted")
        if func == "query":
            text = '["select", "' + args[0] + '", "' + args[1] + '"]'
        elif func == "login":
            text = str(['login', args[0], args[1]])
        elif func == "register":
            text = str(['register', args[0], args[1], args[2], args[3], args[4], args[5]])
        elif func == "save_work_results":
            text = str(['save_work_results', args[0], args[1], args[2], args[3], args[4], args[5], args[6]])
        elif func == "save_duel_results":
            text = str(['save_duel_results', args[0], args[1], args[2], args[3], args[4], args[5], args[6]])
        elif func == "update_elo":
            text = str(['update_elo', args[0], args[1]])
        elif func == "leaderboard":
            text = "['leaderboard']"
        msgs = bytes(text, "utf8")
        s.send(msgs)
        msgr = static_funcs.bytetostr(s.recv(4092))
        if args[1] == "all2":
            msgr = static_funcs.remove_slash(msgr)
            if msgr is None:
                return None
        s.close()
        return ast.literal_eval(msgr)
    else:
        print("Access denied")


class SplashScreen(Toplevel):
    def __init__(self, master):
        super(SplashScreen, self).__init__(master)
        set_window(500, 225, self)
        self.master = master
        self.master.withdraw()
        # get rid of window borders
        self.wm_overrideredirect(True)
        self.sc_image = PhotoImage(file="img\\sc2.png")
        self.sc_img = Label(self)
        self.sc_img.config(image=self.sc_image)
        self.sc_img.image = self.sc_image
        self.progress = Progressbar(self, orient=HORIZONTAL, length=500, mode='determinate')
        self.setup_info_text = StringVar()
        self.setup_info_text.set("Loading GUI(1)")
        self.setup_info = Label(self, textvariable=self.setup_info_text)
        self.sc_img.grid()
        self.progress.grid(row=1, sticky="W")
        self.setup_info.grid(row=1)
        # start red
        self.colour = "#ff1500"
        self.sc_img.wait_visibility()
        self.increase = True

    def colour_pulse(self):
        if self.increase:
            # increase green RGB value (turn more orange)
            green = str(hex(int(self.colour[3:5], 16) + 0x3))
            self.colour = self.colour[:3] + green[2:] + self.colour[5:]
            if int(self.colour[3:5], 16) >= 0x9a:
                self.increase = False
        else:
            # decrease green RGB value (turn more red)
            green = str(hex(int(self.colour[3:5], 16) - 0x3))
            self.colour = self.colour[:3] + green[2:] + self.colour[5:]
            if int(self.colour[3:5], 16) <= 0x50:
                self.increase = True
        self.sc_img.config(bg=self.colour)
        self.sc_img.after(100, self.colour_pulse)
        if self.progress["value"] == 100:
            self.destroy()

    def set_progress(self, value, text):
        self.progress["value"] = value
        self.setup_info_text.set(text)
        self.master.update_idletasks()

    def set_progress_done(self):
        self.progress["value"] = 100
        self.setup_info_text.set("done")
        self.master.update_idletasks()
        self.master.deiconify()


class FractionQuestionFrame(Frame):
    def __init__(self, master, number, func, mode):
        super(FractionQuestionFrame, self).__init__(master)
        self.mode = mode
        self.marked = False
        self.function_var = StringVar()
        self.x1, self.y1, self.x2, self.y2, self.a1, self.a2 = StringVar(), StringVar(), StringVar(),\
                                                               StringVar(), StringVar(), StringVar()
        self.a1_temp, self.a2_temp = [], []
        self.function = func
        function_display = Label(self, text=self.function)
        div1 = Label(self, text="―")
        div2 = Label(self, text="―")
        div3 = Label(self, text="―")
        self.div4 = Label(self, text="―")
        self.q_number = StringVar()
        q = Label(self, text=(str(number) + ")"))
        x1_display = Entry(self, textvariable=self.x1, state="disabled", width=4, relief=FLAT, justify=CENTER)
        y1_display = Entry(self, textvariable=self.y1, state="disabled", width=4, relief=FLAT, justify=CENTER)
        x2_display = Entry(self, textvariable=self.x2, state="disabled", width=4, relief=FLAT, justify=CENTER)
        y2_display = Entry(self, textvariable=self.y2, state="disabled", width=4, relief=FLAT, justify=CENTER)
        self.e1_display = Entry(self, width=4, justify=CENTER)
        self.e2_display = Entry(self, width=4, justify=CENTER)
        self.a1_display = Entry(self, textvariable=self.a1, state="disabled", width=4, relief=RIDGE, justify=CENTER)
        self.a2_display = Entry(self, textvariable=self.a2, state="disabled", width=4, relief=RIDGE, justify=CENTER)
        equals = Label(self, text="=")
        self.tick = PhotoImage(file="img\\tick2.png")
        self.cross = PhotoImage(file="img\\cross2.png")
        self.check = Label(self)
        q.grid(row=0, column=0)
        x1_display.grid(row=1, column=1)
        div1.grid(row=2, column=1)
        x2_display.grid(row=3, column=1)
        function_display.grid(row=2, column=2)
        y1_display.grid(row=1, column=3)
        div2.grid(row=2, column=3)
        y2_display.grid(row=3, column=3)
        equals.grid(row=2, column=4)
        self.e1_display.grid(row=1, column=5)
        div3.grid(row=2, column=5)
        self.e2_display.grid(row=3, column=5)
        self.check.grid(row=2, column=6)
        if self.mode == "worksheet":
            self.set_values()
            self.get_correct()

    def set_values(self):
        rand = random.randrange(1, 20)
        if rand <= 10:
            self.x1.set(str(random.randrange(1, 6)))
            self.x2.set(str(random.randrange(1, 6)))
            self.y1.set(str(random.randrange(1, 6)))
            self.y2.set(str(random.randrange(1, 6)))
        elif 10 < rand < 16:
            self.x1.set(str(random.randrange(1, 11)))
            self.x2.set(str(random.randrange(1, 11)))
            self.y1.set(str(random.randrange(1, 11)))
            self.y2.set(str(random.randrange(1, 11)))
        else:
            self.x1.set(str(random.randrange(1, 21)))
            self.x2.set(str(random.randrange(1, 21)))
            self.y1.set(str(random.randrange(1, 21)))
            self.y2.set(str(random.randrange(1, 21)))

    def get_correct(self):
        if self.function == "+":
            decimal_answer = (int(self.x1.get()) / int(self.x2.get())) + (int(self.y1.get()) / int(self.y2.get()))
        elif self.function == "-":
            decimal_answer = (int(self.x1.get()) / int(self.x2.get())) - (int(self.y1.get()) / int(self.y2.get()))
        elif self.function == "*":
            decimal_answer = (int(self.x1.get()) / int(self.x2.get())) * (int(self.y1.get()) / int(self.y2.get()))
        else:
            decimal_answer = (int(self.x1.get()) / int(self.x2.get())) / (int(self.y1.get()) / int(self.y2.get()))
        answer = str(Fraction(decimal_answer).limit_denominator())
        if "/" in answer:
            count = 0
            for i in answer:
                if i != "/":
                    self.a1_temp.append(i)
                    count += 1
                else:
                    for o in answer[count + 1:]:
                        self.a2_temp.append(o)
                    break
            self.a1_temp = "".join(self.a1_temp)
            self.a2_temp = "".join(self.a2_temp)
        else:
            self.a1_temp = str(int(answer))
            self.a2_temp = "1"

    def mark(self):
        if self.a1_temp == self.e1_display.get() and self.a2_temp == self.e2_display.get():
            self.check.config(image=self.tick)
            self.check.image = self.tick
            self.marked = True
        else:
            if self.mode == "worksheet":
                self.show_answers()

    def show_answers(self):
        self.check.config(image=self.cross)
        self.check.image = self.cross
        self.a1.set(self.a1_temp)
        self.a2.set(self.a2_temp)
        self.a1_display.grid(row=1, column=7)
        self.div4.grid(row=2, column=7)
        self.a2_display.grid(row=3, column=7)


class QuadraticsQuestionFrameFactorise(Frame):
    def __init__(self, master, number, mode):
        super(QuadraticsQuestionFrameFactorise, self).__init__(master)
        self.mode = mode
        self.marked = False
        self.q = Label(self, text=(str(number) + ")"))
        self.valid_pair = (0, 0)
        self.question_text = StringVar()
        self.correct_text = StringVar()
        self.question_label = Label(self, textvariable=self.question_text)
        self.a, self.b, self.c = 0, 0, 0,
        self.a1, self.a2, self.a3, self.a4 = 0, 0, 0, 0
        self.tick = PhotoImage(file="img\\tick2.png")
        self.cross = PhotoImage(file="img\\cross2.png")
        self.check = Label(self)
        self.answer_label1 = Label(self, text="(")
        self.coefficient1 = Entry(self, width=2)
        self.answer_label2 = Label(self, text="x + ")
        self.coefficient2 = Entry(self, width=2)
        self.answer_label3 = Label(self, text=")(")
        self.coefficient3 = Entry(self, width=2)
        self.answer_label4 = Label(self, text="x + ")
        self.coefficient4 = Entry(self, width=2)
        self.answer_label5 = Label(self, text=")")
        self.correct_label = Label(self, textvariable=self.correct_text)
        self.q.grid(row=0, column=0)
        self.question_label.grid(row=1, column=0)
        self.answer_label1.grid(row=1, column=1)
        self.coefficient1.grid(row=1, column=2)
        self.answer_label2.grid(row=1, column=3)
        self.coefficient2.grid(row=1, column=4)
        self.answer_label3.grid(row=1, column=5)
        self.coefficient3.grid(row=1, column=6)
        self.answer_label4.grid(row=1, column=7)
        self.coefficient4.grid(row=1, column=8)
        self.answer_label5.grid(row=1, column=9)
        self.check.grid(row=2, column=0)
        # if mode == duels don't bother to run self.set_values() and self.get)correct() because they get overidden in
        # DuelFrame inheritance
        if self.mode == "worksheet":
            self.set_values()
            self.get_correct()

    def set_values(self):
        simple_numbers = False
        while True:
            # Generate random numbers for values.
            self.a = random.randint(1, 4)
            self.b = random.randint(1, 10)
            self.c = random.randint(1, 20)
            # If the square root of the discrimanent of the generated numbers is an integer and a*c has a pair of
            # factors where the sum of the pair = b, then the quadratic can be factorised simply and these numbers
            # can be used.
            try:
                if math.sqrt((self.b ** 2) - (4 * self.a * self.c)) % 1 == 0:
                    ac = self.a * self.c
                    ac_factors = static_funcs.get_factors(ac)
                    for pair in ac_factors:
                        if pair[0] + pair[1] == self.b:
                            self.valid_pair = pair
                            simple_numbers = True
                            break
                    if simple_numbers:
                        break
            except:
                pass
        self.question_text.set(str(self.a) + "x^2 + " + str(self.b) + "x + " + str(self.c) + " =")


    def get_correct(self):
        # calculate the answers
        factor = static_funcs.hcf(self.a, self.a, self.valid_pair[0])
        # store the factor of a and one value from the valid pair and the simplified expression
        # eg. where 8 is a and 6 is the value of one of the valid pairs (8(x^2) + 6x)
        # = 2x(4x + 3) where 2 is the factor, 4 is the new value of a and 3 is the new value of one of the valid pairs
        p1 = [factor, int(self.a / factor), int(self.valid_pair[0] / factor)]
        factor = static_funcs.hcf(self.c, self.c, self.valid_pair[1])
        # eg (16x + 12) = 4(4x + 3)
        self.a1, self.a2, self.a3, self.a4 = p1[0], factor, p1[1], p1[2]
        # eg (2x + 4) (4x + 3)
        self.correct_text.set("("+str(self.a1)+"x + "+str(self.a2)+")("+str(self.a3)+"x + "+str(self.a4)+")")

    def mark(self):
        if str(self.a1) == self.coefficient1.get() and str(self.a2) == self.coefficient2.get() and str(self.a3) ==\
                self.coefficient3.get() and str(self.a3) == self.coefficient3.get():
            self.check.config(image=self.tick)
            self.check.image = self.tick
            self.marked = True
        elif str(self.a3) == self.coefficient1.get() and str(self.a4) == self.coefficient2.get() and str(self.a1) ==\
                self.coefficient3.get() and str(self.a2) == self.coefficient4.get():
            self.check.config(image=self.tick)
            self.check.image = self.tick
            self.marked = True
        else:
            if self.mode == "worksheet":
                self.show_answers()

    def show_answers(self):
        self.check.config(image=self.cross)
        self.check.image = self.cross
        self.correct_label.grid(row=2, column=1, columnspan=6, sticky="W")


class QuadraticsQuestionFrameExpand(Frame):
    def __init__(self, master, number, mode):
        super(QuadraticsQuestionFrameExpand, self).__init__(master)
        self.mode = mode
        self.marked = False
        self.q = Label(self, text=(str(number) + ")"))
        self.question_text = StringVar()
        self.correct_text = StringVar()
        self.question_label = Label(self, textvariable=self.question_text)
        self.q1, self.q2, self.q3, self.q4 = 0, 0, 0, 0
        self.a, self.b, self.c = 0, 0, 0
        self.tick = PhotoImage(file="img\\tick2.png")
        self.cross = PhotoImage(file="img\\cross2.png")
        self.check = Label(self)
        self.answer_label1 = Label(self, text="(")
        self.coefficient1 = Entry(self, width=2)
        self.answer_label2 = Label(self, text="x^2 + ")
        self.coefficient2 = Entry(self, width=2)
        self.answer_label3 = Label(self, text="x +")
        self.coefficient3 = Entry(self, width=2)
        self.answer_label4 = Label(self, text=")")
        self.correct_label = Label(self, textvariable=self.correct_text)
        self.q.grid(row=0, column=0)
        self.question_label.grid(row=1, column=0)
        self.answer_label1.grid(row=1, column=1)
        self.coefficient1.grid(row=1, column=2)
        self.answer_label2.grid(row=1, column=3)
        self.coefficient2.grid(row=1, column=4)
        self.answer_label3.grid(row=1, column=5)
        self.coefficient3.grid(row=1, column=6)
        self.answer_label4.grid(row=1, column=7)
        self.check.grid(row=2, column=0)
        if self.mode == "worksheet":
            self.set_values()
            self.get_correct()

    def set_values(self):
        self.q1 = random.randint(1, 4)
        self.q2 = random.randint(1, 10)
        self.q3 = random.randint(1, 4)
        self.q4 = random.randint(1, 10)
        self.question_text.set("("+str(self.q1)+"x +"+str(self.q2)+")("+str(self.q3)+"x + "+str(self.q4)+") = ")

    def get_correct(self):
        #calculate the answers
        self.a = self.q1 * self.q3
        self.b = (self.q1 * self.q4) + (self.q2 * self.q3)
        self.c = self.q2 * self.q4
        #simplify the answers
        highest_common_factor = static_funcs.hcf(self.a, self.b, self.c)
        self.a = int(self.a / highest_common_factor)
        self.b = int(self.b / highest_common_factor)
        self.c = int(self.c / highest_common_factor)
        self.correct_text.set(str(self.a) + "x^2 + " + str(self.b) + "x + " + str(self.c))

    def mark(self):
        if str(self.a) == self.coefficient1.get() and str(self.b) == self.coefficient2.get() and str(self.c) ==\
                self.coefficient3.get():
            self.check.config(image=self.tick)
            self.check.image = self.tick
            self.marked = True
        else:
            if self.mode == "worksheet":
                self.show_answers()

    def show_answers(self):
        self.check.config(image=self.cross)
        self.check.image = self.cross
        self.correct_label.grid(row=2, column=1, columnspan=6, sticky="W")


class QuadraticsDuelFrameFactorise(QuadraticsQuestionFrameFactorise):
    def __init__(self, master, number, data):
        super(QuadraticsDuelFrameFactorise, self).__init__(master, number, "duel")
        self.data = data
        self.set_values()
        self.get_correct()

    # set questions generated by server
    def set_values(self):
        print(self.data)
        self.a = self.data[0]
        self.b = self.data[1]
        self.c = self.data[2]
        self.valid_pair = self.data[3]
        self.question_text.set(str(self.a) + "x^2 + " + str(self.b) + "x + " + str(self.c) + " =")


class QuadraticsDuelFrameExpand(QuadraticsQuestionFrameExpand):
    def __init__(self, master, number, data):
        super(QuadraticsDuelFrameExpand, self).__init__(master, number, "duel")
        self.data = data
        self.set_values()
        self.get_correct()

    # set questions generated by server
    def set_values(self):
        print(self.data)
        self.q1 = self.data[0]
        self.q2 = self.data[1]
        self.q3 = self.data[2]
        self.q4 = self.data[3]
        self.question_text.set(
            "(" + str(self.q1) + "x +" + str(self.q2) + ")(" + str(self.q3) + "x + " + str(self.q4) + ") = ")


class FractionDuelFrame(FractionQuestionFrame):
    def __init__(self, master, number, func, data):
        super(FractionDuelFrame, self).__init__(master, number, func, "duel")
        self.data = data
        self.set_values()
        self.get_correct()

    #set questions generated by server
    def set_values(self):
        print(self.data)
        self.x1.set(self.data[0])
        self.x2.set(self.data[1])
        self.y1.set(self.data[2])
        self.y2.set(self.data[3])


class SheetOptions(Toplevel):
    def __init__(self, master):
        super(SheetOptions, self).__init__(master)
        self.title("Sheet Options")
        self.iconbitmap("img\\favicon2.ico")
        self.main_frame = Frame(self)
        self.question_no = StringVar()
        self.question_no.set("1")
        self.question_no.trace('w', lambda *args: limit_size(self.question_no, 2))
        self.question_no_label = Label(self.main_frame, text="Number of questions:")
        self.question_no_entry = Entry(self.main_frame, width=3, textvariable=self.question_no)
        self.question_no_menu = OptionMenu(self.main_frame, self.question_no, "1", "5", "10", "20")


class QuadraticsSheetOptions(SheetOptions):
    def __init__(self, master, user_id, mode):
        super(QuadraticsSheetOptions, self).__init__(master)
        self.user_id = user_id
        self.mode = mode
        set_window(150, 175, self)
        types_label = Label(self.main_frame, text="Functions:")
        fact_var, exp_var = IntVar(), IntVar()
        fact_check = Checkbutton(self.main_frame, text="Factorising", variable=fact_var)
        exp_check = Checkbutton(self.main_frame, text="Expanding", variable=exp_var)
        fact_check.select()
        generate_button = Button(self.main_frame, text="Generate", command=lambda: self.generate(self.question_no.get(),
                                                                                        fact_var.get(), exp_var.get()))
        self.question_no_label.grid(row=0, column=0, pady=2)
        if self.mode == "worksheet":
            self.question_no_entry.grid(row=1, column=0, pady=2)
        else:
            self.question_no_menu.grid(row=1, column=0, pady=2)
        types_label.grid(row=2, column=0, pady=2, sticky="W")
        fact_check.grid(row=3, column=0, sticky="W")
        exp_check.grid(row=4, column=0, sticky="W")
        generate_button.grid(row=5, column=0)
        self.main_frame.grid(padx=5)
        self.question_no_entry.focus_force()

    def generate(self, question_no, op1, op2):
        self.destroy()
        if self.mode == "worksheet":
            QuadraticsWorksheet(root, question_no, op1, op2, mode="worksheet", user_id=self.user_id)
        else:
            DuelSearch(root, uid=self.user_id, topic="quadratics", qn=question_no, funcs=[op1, op2])


class FractionsSheetOptions(SheetOptions):
    def __init__(self, master, user_id, mode):
        super(FractionsSheetOptions, self).__init__(master)
        self.user_id = user_id
        self.mode = mode
        set_window(150, 220, self)
        functions_label = Label(self.main_frame, text="Functions:")
        add_var, sub_var, mult_var, div_var = IntVar(), IntVar(), IntVar(), IntVar()
        add_check = Checkbutton(self.main_frame, text="Addition", variable=add_var)
        sub_check = Checkbutton(self.main_frame, text="Subtraction", variable=sub_var)
        mult_check = Checkbutton(self.main_frame, text="Multiplication", variable=mult_var)
        div_check = Checkbutton(self.main_frame, text="Division", variable=div_var)
        add_check.select()
        generate_button = Button(self.main_frame, text="Generate", command=lambda: self.generate(self.question_no.get(),
                                                        add_var.get(), sub_var.get(), mult_var.get(), div_var.get()))
        self.question_no_label.grid(row=0, column=0, pady=2)
        if self.mode == "worksheet":
            self.question_no_entry.grid(row=1, column=0, pady=2)
        else:
            self.question_no_menu.grid(row=1, column=0, pady=2)
        functions_label.grid(row=2, column=0, pady=2, sticky="W")
        add_check.grid(row=3, column=0, sticky="W")
        sub_check.grid(row=4, column=0, sticky="W")
        mult_check.grid(row=5, column=0, sticky="W")
        div_check.grid(row=6, column=0, sticky="W")
        generate_button.grid(row=7, column=0)
        self.main_frame.grid(padx=5)
        self.question_no_entry.focus_force()

    def generate(self, question_no, op1, op2, op3, op4):
        self.destroy()
        if self.mode == "worksheet":
            FractionsWorksheet(root, question_no, op1, op2, op3, op4, mode="worksheet", user_id=self.user_id)
        else:
            DuelSearch(root, uid=self.user_id, topic="fractions", qn=question_no, funcs=[op1, op2, op3, op4])


class Worksheet(Toplevel):
    def __init__(self, master):
        super(Worksheet, self).__init__(master)
        self.withdraw()
        self.start_time = time.time()
        self.title("Worksheet")
        self.iconbitmap("img\\favicon2.ico")

    def mark(self, user_id, questions, window, menu_item, topic, type):
        if tkinter.messagebox.askyesno("Submit Marks", "Are you sure you want to submit your marks?\n"
                                                       "These marks will be saved to your profile and"
                                                       " will be unchangeable"):
            finish_time = time.time()
            window.focus_force()
            correct = 0
            for question in questions:
                question.mark()
                if question.marked:
                    correct += 1
            percentage = (correct / len(questions)) * 100
            if percentage >= 80:
                grade = PhotoImage(file="img\\A.png")
            elif percentage >= 70:
                grade = PhotoImage(file="img\\B.png")
            elif percentage >= 60:
                grade = PhotoImage(file="img\\C.png")
            else:
                grade = PhotoImage(file="img\\D.png")
            percentage_text = StringVar()
            percentage_text.set(str(round(percentage, 2)) + "%")
            time_taken = round(finish_time - self.start_time, 2)
            time_taken_text = StringVar()
            minutes, seconds = static_funcs.time_format(int(time_taken))
            time_format = "Time taken: {}:{}".format(minutes, seconds)
            time_taken_text.set(time_format)
            result_window = Toplevel()
            set_window(210, 150, result_window)
            result_frame = Frame(result_window)
            result_window.title("Results")
            correct_final = StringVar()
            correct_final.set(str(correct))
            no_questions = StringVar()
            no_questions.set(str(len(questions)))
            grade_display = Label(result_frame)
            grade_display.config(image=grade)
            grade_display.image = grade
            time_display = Label(result_frame, textvariable=time_taken_text)
            a1_display = Entry(result_frame, textvariable=correct_final, state="disabled", width=4, relief=RIDGE,
                               justify=CENTER)
            a2_display = Entry(result_frame, textvariable=no_questions, state="disabled", width=4, relief=RIDGE,
                               justify=CENTER)
            div = Label(result_frame, text="―")
            equals_label = Label(result_frame, text="=")
            percentage_display = Label(result_frame, textvariable=percentage_text)
            grade_display.grid(row=0, column=0, columnspan=3, pady=5)
            a1_display.grid(row=1, column=0)
            div.grid(row=2, column=0)
            a2_display.grid(row=3, column=0)
            equals_label.grid(row=2, column=1)
            percentage_display.grid(row=2, column=2)
            time_display.grid(row=4, column=0, columnspan=3)
            result_window.grid_rowconfigure(2, weight=1)
            result_window.grid_columnconfigure(0, weight=1)
            result_window.grid_columnconfigure(2, weight=1)
            result_frame.grid(row=1, column=1)
            menu_item.entryconfig(1, state="disabled")
            type2 = []
            if topic == "fractions":
                for i in type:
                    if i == 0:
                        type2.append("Addition")
                    elif i == 1:
                        type2.append("Subtraction")
                    elif i == 2:
                        type2.append("Multiplication")
                    else:
                        type2.append("Division")
            elif topic == "quadratics":
                for i in type:
                    if i == 0:
                        type2.append("Factorising")
                    else:
                        type2.append("Expanding")

            db("save_work_results", user_id, time_taken, correct, len(questions), topic, type2,
               str(datetime.datetime.now()))

    def change_page(self, dest_page, frames):
        frames[self.curr_frame].grid_remove()
        if dest_page == "next":
            if self.curr_frame + 1 < len(frames):
                self.curr_frame += 1
            else:
                self.curr_frame = 0
        elif dest_page == "previous":
            if self.curr_frame - 1 >= 0:
                self.curr_frame -= 1
            else:
                self.curr_frame = len(frames) - 1
        frames[self.curr_frame].grid()


class QuadraticsWorksheet(Worksheet):
    def __init__(self, master, question_no, op1, op2, **kwargs):
        super(QuadraticsWorksheet, self).__init__(master)
        set_window(750, 550, self)
        function_number = 0
        self.questions = []
        functions = []
        self.frames = []
        for i in [op1, op2]:
            if i != 0:
                functions.append(function_number)
            function_number += 1
        question = 0
        f = 0
        for i in range((int(question_no) // 24) + 1):
            self.frames.append(Frame(self))
        if kwargs["mode"] == "worksheet":
            self.user_id = kwargs["user_id"]
            for func in functions:
                # make an even number of each type of question
                for i in range(1, int(int(question_no) / len(functions) + 1)):
                    question += 1
                    if func == 0:
                        self.questions.append(QuadraticsQuestionFrameFactorise(self.frames[f], question, "worksheet"))
                    elif func == 1:
                        self.questions.append(QuadraticsQuestionFrameExpand(self.frames[f], question, "worksheet"))
                    # if there are 24 questions on this frame, then start adding to a new frame
                    if question % 24 == 0:
                        f += 1
            if question != int(question_no):
                for i in range(int(question_no) - question):
                    question += 1
                    if functions[-1] == 0:
                            self.questions.append(QuadraticsQuestionFrameFactorise(self.frames[f], question,
                                                                                   "worksheet"))
                    elif functions[-1] == 1:
                            self.questions.append(QuadraticsQuestionFrameExpand(self.frames[f], question, "worksheet"))
                    if question % 24 == 0:
                        f += 1
        else:
            print(kwargs["data"])
            for func in functions:
                for i in range(1, int(int(question_no) / len(functions) + 1)):
                    question += 1
                    if func == 0:
                        self.questions.append(QuadraticsDuelFrameFactorise(self.frames[0], question, kwargs["data"][0]))
                    elif func == 1:
                        self.questions.append(QuadraticsDuelFrameExpand(self.frames[0], question, kwargs["data"][0]))
                    del kwargs["data"][0]
            if question != int(question_no):
                for i in range(int(question_no) - question):
                    question += 1
                    if functions[-1] == 0:
                            self.questions.append(QuadraticsDuelFrameFactorise(self.frames[0], question,
                                                                               kwargs["data"][0]))
                    elif functions[-1] == 1:
                            self.questions.append(QuadraticsDuelFrameExpand(self.frames[0], question,
                                                                            kwargs["data"][0]))
        question = 1
        #row
        r = 0
        #column
        c = 0
        # grid every question generated
        for question_frame in self.questions:
            question_frame.grid(row=r, column=c)
            # can not have more than 3 columns
            if (question % 3) == 0:
                r += 1
                c = 0
            else:
                c += 1
            question += 1
        # grid the first page
        self.frames[0].grid()
        self.curr_frame = 0
        self.file_menu = Menu(Menu(self))
        self.config(menu=self.file_menu)
        self.file_menu.add_command(label="Mark", command=lambda: self.mark(self.user_id, self.questions, self,
                                                                           self.file_menu, "quadratics", functions))
        self.file_menu.add_command(label="Next page", command=lambda: self.change_page("next", self.frames))
        self.file_menu.add_command(label="Previous page", command=lambda: self.change_page("previous", self.frames))
        self.deiconify()
        self.focus()


class QuadraticsDuel(QuadraticsWorksheet):
    def __init__(self, master, opponent, question_no, op1, op2, game_data):
        super(QuadraticsDuel, self).__init__(master, question_no, op1, op2, mode="Duel", data=game_data)
        self.title("Duel")
        self.empty_menu = Menu(self)
        self.config(menu=self.empty_menu)
        self.question_no = question_no
        self.correct = 0
        self.time = time.time()
        self.my_progress_text = StringVar()
        self.opponent_progress_text = StringVar()
        self.my_progress_text.set("0")
        self.opponent_progress_text.set("0")
        self.state = "running"
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Destroy>", lambda e: self.set_state("finished"))
        self.my_progressbar = Progressbar(self, orient=HORIZONTAL, length=500, mode='determinate')
        self.opponent_progressbar = Progressbar(self, orient=HORIZONTAL, length=500, mode='determinate')
        self.my_current_progress_label = Label(self, textvariable=self.my_progress_text)
        self.opponent_current_progress_label = Label(self, textvariable=self.opponent_progress_text)
        self.my_progress_label = Label(self, text="My Progress:")
        self.opponent_progress_label = Label(self, text="Opponent's Progress:")
        self.my_progress_label.grid(row=1)
        self.my_progressbar.grid(row=2)
        self.my_current_progress_label.grid(row=2)
        self.opponent_progress_label.grid(row=3)
        self.opponent_current_progress_label.grid(row=4)
        self.opponent_progressbar.grid(row=4)
        self.deiconify()
        self.focus()

    def set_state(self, state):
        self.time = time.time() - self.time
        self.state = state

    def check_answers(self):
        print("f")
        correct = 0
        for i in self.questions:
            i.mark()
            if i.marked:
                correct += 1
        self.correct = correct
        if self.state == "finished":
            for i in self.questions:
                i.mark()
                if not i.marked:
                    i.show_answers()
            return
        self.after(500, self.check_answers)


class FractionsWorksheet(Worksheet):
    def __init__(self, master, question_no, op1, op2, op3, op4, **kwargs):
        super(FractionsWorksheet, self).__init__(master)
        set_window(750, 500, self)
        function_number = 0
        self.questions = []
        functions = []
        self.frames = []
        for i in [op1, op2, op3, op4]:
            if i != 0:
                functions.append(function_number)
            function_number += 1
        question = 0
        f = 0
        for i in range((int(question_no) // 24) + 1):
            self.frames.append(Frame(self))
        if kwargs["mode"] == "worksheet":
            self.user_id = kwargs["user_id"]
            for func in functions:
                for i in range(1, int(int(question_no) / len(functions) + 1)):
                    question += 1
                    if func == 0:
                        self.questions.append(FractionQuestionFrame(self.frames[f], question, "+", "worksheet"))
                    elif func == 1:
                        self.questions.append(FractionQuestionFrame(self.frames[f], question, "-", "worksheet"))
                    elif func == 2:
                        self.questions.append(FractionQuestionFrame(self.frames[f], question, "*", "worksheet"))
                    else:
                        self.questions.append(FractionQuestionFrame(self.frames[f], question, "/", "worksheet"))
                    if question % 24 == 0:
                        f += 1
            if question != int(question_no):
                for i in range(int(question_no) - question):
                    question += 1
                    if functions[-1] == 0:
                            self.questions.append(FractionQuestionFrame(self.frames[f], question, "+", "worksheet"))
                    elif functions[-1] == 1:
                            self.questions.append(FractionQuestionFrame(self.frames[f], question, "-", "worksheet"))
                    elif functions[-1] == 2:
                        self.questions.append(FractionQuestionFrame(self.frames[f], question, "*", "worksheet"))
                    else:
                        self.questions.append(FractionQuestionFrame(self.frames[f], question, "/", "worksheet"))
                    # cannont have more than 24 questions per frame, so start adding questions to new frame
                    if question % 24 == 0:
                        f += 1
        else:
            for func in functions:
                for i in range(1, int(int(question_no) / len(functions) + 1)):
                    question += 1
                    if func == 0:
                        self.questions.append(FractionDuelFrame(self.frames[0], question, "+", kwargs["data"][0]))
                    elif func == 1:
                        self.questions.append(FractionDuelFrame(self.frames[0], question, "-", kwargs["data"][0]))
                    elif func == 2:
                        self.questions.append(FractionDuelFrame(self.frames[0], question, "*", kwargs["data"][0]))
                    else:
                        self.questions.append(FractionDuelFrame(self.frames[0], question, "/", kwargs["data"][0]))
                    del kwargs["data"][0]
            if question != int(question_no):
                for i in range(int(question_no) - question):
                    question += 1
                    if functions[-1] == 0:
                            self.questions.append(FractionDuelFrame(self.frames[0], question, "+", kwargs["data"][0]))
                    elif functions[-1] == 1:
                            self.questions.append(FractionDuelFrame(self.frames[0], question, "-", kwargs["data"][0]))
                    elif functions[-1] == 2:
                        self.questions.append(FractionDuelFrame(self.frames[0], question, "*", kwargs["data"][0]))
                    else:
                        self.questions.append(FractionDuelFrame(self.frames[0], question, "/", kwargs["data"][0]))
        question = 1
        #row
        r = 0
        #column
        c = 0
        # grid every question generated
        for question_frame in self.questions:
            question_frame.grid(row=r, column=c)
            # can not have more than 4 columns
            if (question % 4) == 0:
                r += 1
                c = 0
            else:
                c += 1
            question += 1
        # grid the first page
        self.frames[0].grid()
        self.curr_frame = 0
        self.file_menu = Menu(Menu(self))
        self.config(menu=self.file_menu)
        self.file_menu.add_command(label="Mark", command=lambda: self.mark(self.user_id, self.questions, self,
                                                                           self.file_menu, "fractions", functions))
        self.file_menu.add_command(label="Next page", command=lambda: self.change_page("next", self.frames))
        self.file_menu.add_command(label="Previous page", command=lambda: self.change_page("previous", self.frames))
        self.deiconify()
        self.focus()


class FractionsDuel(FractionsWorksheet):
    def __init__(self, master, opponent, question_no, op1, op2, op3, op4, game_data):
        super(FractionsDuel, self).__init__(master, question_no, op1, op2, op3, op4, mode="Duel", data=game_data)
        self.title("Duel")
        self.empty_menu = Menu(self)
        self.config(menu=self.empty_menu)
        self.question_no = question_no
        self.correct = 0
        self.time = time.time()
        self.my_progress_text = StringVar()
        self.opponent_progress_text = StringVar()
        self.my_progress_text.set("0")
        self.opponent_progress_text.set("0")
        self.state = "running"
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Destroy>", lambda e: self.set_state("finished"))
        self.my_progressbar = Progressbar(self, orient=HORIZONTAL, length=500, mode='determinate')
        self.opponent_progressbar = Progressbar(self, orient=HORIZONTAL, length=500, mode='determinate')
        self.my_current_progress_label = Label(self, textvariable=self.my_progress_text)
        self.opponent_current_progress_label = Label(self, textvariable=self.opponent_progress_text)
        self.my_progress_label = Label(self, text="My Progress:")
        self.opponent_progress_label = Label(self, text="Opponent's Progress:")
        self.my_progress_label.grid(row=1)
        self.my_progressbar.grid(row=2)
        self.my_current_progress_label.grid(row=2)
        self.opponent_progress_label.grid(row=3)
        self.opponent_current_progress_label.grid(row=4)
        self.opponent_progressbar.grid(row=4)
        self.deiconify()
        self.focus()

    def set_state(self, state):
        self.time = time.time() - self.time
        self.state = state

    def check_answers(self):
        print("f")
        correct = 0
        for i in self.questions:
            i.mark()
            if i.marked:
                correct += 1
        self.correct = correct
        if self.state == "finished":
            for i in self.questions:
                i.mark()
                if not i.marked:
                    i.show_answers()
            return
        self.after(500, self.check_answers)


class DuelSearch(Toplevel):
    def __init__(self, master, **kwargs):
        super(DuelSearch, self).__init__(master)
        self.withdraw()
        self.uid, self.topic, self.qn, self.funcs = str(kwargs["uid"]), kwargs["topic"], kwargs["qn"], kwargs["funcs"]
        self.title("Duel Search")
        self.iconbitmap("img\\favicon2.ico")
        set_window(300, 200, self)
        self.main_frame = Frame(self)
        self.time = 0
        self.elo = db("query", "SELECT elo FROM user WHERE user_id='"+self.uid+"'", "one")[0]
        self.search_text = StringVar()
        self.profile_pic_img = static_funcs.set_profile_pic(self.uid)
        self.profile_pic = Label(self.main_frame, image=self.profile_pic_img)
        self.elo_label = Label(self.main_frame, text=("Elo: " + str(self.elo)))
        self.search_label = Label(self.main_frame, textvariable=self.search_text)
        self.profile_pic.grid(row=0, column=0)
        self.elo_label.grid(row=1, column=0)
        self.search_label.grid(row=2, column=0)
        self.main_frame.grid(padx=80)
        self.deiconify()
        self.s = socket.socket()
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Destroy>", lambda e: self.safe_connection_shutdown())
        connect_thread = threading.Thread(target=self.connect, args=())
        update_time_thread = threading.Thread(target=self.update_time(), args=())
        connect_thread.start()
        update_time_thread.start()

    def update_time(self):
        self.time += 1
        minutes, seconds = static_funcs.time_format(self.time)
        self.search_text.set("Time taken: {}:{}".format(minutes, seconds))
        self.after(1000, self.update_time)

    def safe_connection_shutdown(self, **kwargs):
        kwargs.setdefault("error", False)
        if kwargs["error"]:
            tkinter.messagebox.showerror("Server Error", "Cannot connect to game servers,\n"
                                                         " check connection and try again.")
        self.destroy()
        self.s.close()

    def status_update(self, duel, opponent):
        socket.setdefaulttimeout(3)
        while True:
            if duel.state == "finished":
                break
            correct = duel.correct
            print(correct)
            self.s.send(bytes(str(correct), "utf8"))
            try:
                msgr = static_funcs.bytetostr(self.s.recv(1024))
            except:
                if correct == self.qn:
                    duel.set_state("finished")
                    GameOver(root, "win", self.elo, opponent, duel.time, self.uid, self.topic, self.qn, self.funcs)
                else:
                    self.safe_connection_shutdown(error=True)
                break
            print("asdf"+self.qn)
            print(msgr)
            if correct != 0:
                duel.my_progressbar["value"] = (correct / int(self.qn)) * 100
                duel.my_progress_text.set(str(correct))
            if msgr != "end" and int(msgr) > 0:
                duel.opponent_progressbar["value"] = (int(msgr) / int(self.qn)) * 100
                duel.opponent_progress_text.set(msgr)
            if msgr == self.qn:
                duel.set_state("finished")
                GameOver(root, "lose", self.elo, opponent, duel.time, self.uid, self.topic, self.qn, self.funcs)
                break
            elif str(correct) == self.qn:
                duel.set_state("finished")
                GameOver(root, "win", self.elo, opponent, duel.time, self.uid, self.topic, self.qn, self.funcs)
                break
        socket.setdefaulttimeout(None)
        self.safe_connection_shutdown()

    def connect(self):
        port = 1201
        try:
            self.s.connect((host, port))
        except ConnectionRefusedError:
            self.safe_connection_shutdown(error=True)
            return
        msgr = static_funcs.bytetostr(self.s.recv(1024))
        print(msgr)
        msgs = bytes("Test", "utf8")
        self.s.send(msgs)
        msgr = static_funcs.bytetostr(self.s.recv(1024))
        if msgr == "y":
            text = str([self.uid, self.topic, self.qn, self.funcs])
            msgs = bytes(text, "utf8")
            self.s.send(msgs)
            print("h")
            while True:
                msgr = static_funcs.bytetostr(self.s.recv(1024))
                if msgr == "check":
                    msgs = bytes("check", "utf8")
                    self.s.send(msgs)
                    print("ko")
                else:
                    try:
                        msgr = ast.literal_eval(msgr)
                    except (ValueError, SyntaxError):
                        self.safe_connection_shutdown(error=True)
                        return
                    opponent = msgr[0]
                    game_data = msgr[1]
                    self.withdraw()
                    print(opponent, game_data)
                    if self.topic == "fractions":
                        duel = FractionsDuel(root, opponent, self.qn, self.funcs[0], self.funcs[1], self.funcs[2],
                                             self.funcs[3], game_data)
                    elif self.topic == "quadratics":
                        duel = QuadraticsDuel(root, opponent, self.qn, self.funcs[0], self.funcs[1], game_data)
                    time.sleep(2)
                    threading._start_new_thread(duel.check_answers, ())
                    threading._start_new_thread(self.status_update, (duel, opponent))
                    break
        else:
            print("Access Denied")
            self.safe_connection_shutdown(error=True)
            return


class GameOver(Toplevel):
    def __init__(self, master, win_state, elo, opponent, time, uid, topic, qn, funcs):
        super(GameOver, self).__init__(master)
        self.title("Duel Results")
        self.iconbitmap("img\\favicon2.ico")
        set_window(225, 225, self)
        self.opponent_info_frame = Frame(self)
        self.win_text = StringVar()
        self.your_elo_text = StringVar()
        self.opponent_info = db("query", "SELECT username, elo FROM user WHERE user_id='"+opponent+"'", "one")
        win_chance = 1 / (1 + (10 ** ((int(self.opponent_info[1]) - int(elo)) / 400)))
        if win_state == "win":
            self.win_text.set("Victory against:")
            new_elo = int(int(elo) + round(32 * (1 - win_chance)))
            elo_change = new_elo - int(elo)
            self.your_elo_text.set("Your Elo:\n"+str(elo)+" + "+str(elo_change)+" = "+str(new_elo))
            funcs2 = []
            print(funcs)
            if topic == "fractions":
                if funcs[0] == 1:
                    funcs2.append("Addition")
                if funcs[1] == 1:
                    funcs2.append("Subtraction")
                if funcs[2] == 1:
                    funcs2.append("Multiplication")
                if funcs[3] == 1:
                    funcs2.append("Division")
            elif topic == "quadratics":
                if funcs[0] == 1:
                    funcs2.append("Factorising")
                if funcs[1] == 1:
                    funcs2.append("Expanding")

            username1 = db("query", "SELECT username FROM user WHERE user_id='"+uid+"'", "one")[0]
            username2 = db("query", "SELECT username FROM user WHERE user_id='"+opponent+"'", "one")[0]
            db("save_duel_results", username1, username2, int(time), qn, topic, funcs2, str(datetime.datetime.now()))

        else:
            self.win_text.set("Defeat against:")
            new_elo = int(int(elo) + round(32 * -win_chance))
            elo_change = int(elo) - new_elo
            self.your_elo_text.set("Your Elo:\n"+str(elo)+" - "+str(elo_change)+" = "+str(new_elo))
        db("update_elo", uid, str(new_elo))

        self.win_label = Label(self, textvariable=self.win_text, font=(None, 10))
        self.profile_pic_img = static_funcs.set_profile_pic(opponent)
        self.profile_pic = Label(self, image=self.profile_pic_img)
        self.opponent_label = Label(self, text=str(self.opponent_info[0])+", Elo: "+self.opponent_info[1])
        self.opponent_username_label = Label(self.opponent_info_frame, text=self.opponent_info[0], font=(None, 15))
        self.opponent_info_label = Label(self.opponent_info_frame, text="Elo: "+self.opponent_info[1])
        self.your_elo_Label = Label(self, textvariable=self.your_elo_text)
        minutes, seconds = static_funcs.time_format(int(time))
        self.time_taken_label = Label(self, text="Time taken: {}:{}".format(minutes, seconds))

        self.opponent_username_label.grid(row=0, column=0)
        self.opponent_info_label.grid(row=1, column=0)
        self.win_label.grid(row=0, column=0, columnspan=2)
        self.profile_pic.grid(row=1, column=0)
        self.opponent_info_frame.grid(row=1, column=1)
        self.your_elo_Label.grid(row=2, column=0, columnspan=2)
        self.time_taken_label.grid(row=3, column=0, columnspan=2)


# Code between these comments is not written by me. src:
# https://www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter (start comment)
class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left', background='cyan', relief='solid', borderwidth=1,
                      font=("times", "8", "normal"))
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()
# Code between these comments is not written by me. src:
# https://www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter (end comment)


class Register(Toplevel):
    def __init__(self, master):
        super(Register, self).__init__(master)
        self.title("Register")
        self.iconbitmap("img\\favicon2.ico")
        set_window(160, 330, self)
        self.main_frame = Frame(self)
        self.validation = StringVar()
        self.validation.set("Hover over text to see\nfield requirements")
        self.username_label, self. username_entry = Label(self.main_frame, text="username:"), Entry(self.main_frame)
        self.firstname_label, self.firstname_entry = Label(self.main_frame, text="First name:"), Entry(self.main_frame, width=10)
        self.secondname_label, self.secondname_entry = Label(self.main_frame, text="Second name:"), Entry(self.main_frame, width=10)
        self.email_label, self.email_entry = Label(self.main_frame, text="Email:"), Entry(self.main_frame)
        self.password_label, self.password_entry = Label(self.main_frame, text="Password:"), Entry(self.main_frame, show="*")
        self.re_enter_label, self.re_enter_entry = Label(self.main_frame, text="Re-enter password:"), Entry(self.main_frame, show="*")
        self.school_label, self.school_entry = Label(self.main_frame, text="School code:"), Entry(self.main_frame, width=10)
        self.postcode_label, self.postcode_entry = Label(self.main_frame, text="Postcode:"), Entry(self.main_frame, width=10)
        self.register_button = Button(self.main_frame, text="Register", command=lambda: self.register())
        self.validation_label = Label(self.main_frame, textvariable=self.validation)
        self.username_label.grid(columnspan=2)
        self.username_entry.grid(row=1, columnspan=2, padx=20)
        self.firstname_label.grid(row=2)
        self.secondname_label.grid(row=2, column=1)
        self.firstname_entry.grid(row=3)
        self.secondname_entry.grid(row=3, column=1)
        self.email_label.grid(row=4, columnspan=2)
        self.email_entry.grid(row=5, columnspan=2)
        self.password_label.grid(row=6, columnspan=2)
        self.password_entry.grid(row=7, columnspan=2)
        self.re_enter_label.grid(row=8, columnspan=2)
        self.re_enter_entry.grid(row=9, columnspan=2)
        self.school_label.grid(row=10)
        self.postcode_label.grid(row=10, column=1)
        self.school_entry.grid(row=11)
        self.postcode_entry.grid(row=11, column=1)
        self.register_button.grid(row=12, columnspan=2, pady=5)
        self.validation_label.grid(row=13, columnspan=2)
        self.main_frame.grid()
        username_ttp = CreateToolTip(self.username_label, "-Have 3-16 characters")
        firstname_ttp = CreateToolTip(self.firstname_label, "-Only letters\n-Have 1-16 characters")
        secondname_ttp = CreateToolTip(self.secondname_label, "-Only letters\n-Have 1-16 characters")
        email_ttp = CreateToolTip(self.email_label, "-In the form 'example@email.com'")
        password_ttp = CreateToolTip(self.password_label, "-At least 8 characters\n-At least one number\n-At least one special character")
        school_ttp = CreateToolTip(self.school_label, "-Unique school code given by teacher")
        self.register_enter = self.bind("<Return>", (lambda e: self.register()))
        self.username_entry.focus_force()

    def register(self):
        error_list = []
        if not (2 < len(self.username_entry.get()) < 17):
            error_list.append("Username")
        if not(0 < len(self.firstname_entry.get()) < 17) or not self.firstname_entry.get().isalpha():
            error_list.append("Firstname")
        if not(0 < len(self.secondname_entry.get()) < 17) or not self.secondname_entry.get().isalpha():
            error_list.append("Secondname")
        email_re = re.compile("([a-z]|[A-Z]|[0-9])+@([a-z]|[0-9])+\.([a-z]|.)+")
        m = email_re.match(self.email_entry.get())
        if m == None or len(self.email_entry.get()) - (m.end() - m.start()) != 0:
            error_list.append("Email")
        if len(self.password_entry.get()) > 7:
            numeric_valid = True
            special_valid = True
            for i in self.password_entry.get():
                if i in "1234567890":
                    numeric_valid = False
                elif i in " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~":
                    special_valid = False
            if numeric_valid and special_valid:
                error_list.append("Password")
        else:
            error_list.append("Password")
        if not(self.password_entry.get() == self.re_enter_entry.get()):
            error_list.append("Re-enter Password")
        print("e" + str(error_list))
        if not json.load(urlopen("http://api.postcodes.io/postcodes/%20"+self.postcode_entry.get()+"/validate"))["result"]:
            error_list.append("postcode")
        if len(error_list) == 0:
            name = static_funcs.name_format(self.firstname_entry.get(), self.secondname_entry.get())
            error_list = db("register", self.username_entry.get(), name, self.password_entry.get(),
                            self.email_entry.get(), self.school_entry.get(), self.postcode_entry.get())
            if len(error_list) == 0:
                tkinter.messagebox.showinfo("Registration", "Registration complete.")
                self.destroy()
            else:
                valid = "Invalid entry:\n"
                for i in error_list:
                    valid += " " + i + "\n"
                self.validation.set(valid)
        else:
            valid = "Invalid entry:"
            for i in error_list:
                valid += " " + i + "\n"
            self.validation.set(valid)


class Profile(Toplevel):
    def __init__(self, master, user_data, edit_permission, colour):
        super(Profile, self).__init__(master)
        self.colour = colour
        self.withdraw()
        self.title("Profile")
        self.iconbitmap("img\\favicon2.ico")
        set_window(700, 500, self)
        self.config(bg=colour)
        self.user_data = user_data
        self.worksheet_data = db("query", "SELECT topic, type, correct, no_questions, time, date, result_id FROM work_results WHERE user_id='"+str(self.user_data[0])+"'", "all2")
        self.duel_data = db("query", "SELECT topic, type, user_id1, user_id2, time, date, result_id FROM duel_results WHERE user_id1='"+str(self.user_data[1])+"' OR user_id2='"+str(self.user_data[1])+"'", "all2")
        self.info_frame = Frame(self, bg=colour)
        self.button_frame = Frame(self)
        self.profile_pic_frame = Frame(self.info_frame, bg=colour)
        self.profile_pic_img = static_funcs.set_profile_pic(user_data[0])
        self.profile_pic = Label(self.profile_pic_frame, image=self.profile_pic_img, bg=colour)
        self.edit_img = PhotoImage(file="img\\edit1.png")
        self.edit = Label(self.profile_pic_frame, image=self.edit_img, bg=colour)
        self.username_label = Label(self.info_frame, text=user_data[1], font=(None, 15), bg=colour)
        self.info_label = Label(self.info_frame, text=user_data[3]+" from "+str(db("query", "SELECT name FROM school WHERE code='"+user_data[5]+"'", "one")[0])+"\nElo: "+str(db("query", "SELECT elo FROM user WHERE user_id='"+str(user_data[0])+"'", "one")[0]), bg=colour)
        self.history_label = Label(self, text="History:", bg=colour)
        self.worksheets_button = Button(self.button_frame, text="Worksheets", command=lambda: self.change_table_from_to(self.tree2, self.tree1))
        self.duels_button = Button(self.button_frame, text="Duels", command=lambda: self.change_table_from_to(self.tree1, self.tree2))
        self.tree1 = tkinter.ttk.Treeview(self)
        self.set_tree_worksheets()
        self.set_data(self.tree1, 5, "worksheet")
        self.tree2 = tkinter.ttk.Treeview(self)
        self.set_tree_duels()
        self.set_data(self.tree2, 5, "duel")

        self.profile_pic.grid()
        self.profile_pic_frame.grid(row=0, column=0, rowspan=2)
        self.username_label.grid(row=0, column=1)
        self.info_label.grid(row=1, column=1)
        self.worksheets_button.grid(row=0, column=0, sticky="W")
        self.duels_button.grid(row=0, column=1, sticky="E")
        self.info_frame.grid(row=0, column=1)
        self.history_label.grid(row=1, column=1)
        self.button_frame.grid(row=2, column=1)
        self.tree1.grid(row=3, column=0, columnspan=3)
        if edit_permission:
            self.profile_pic_frame.bind("<Enter>", lambda e: self.edit.place(x="48", y="48"))
            self.profile_pic_frame.bind("<Leave>", lambda e: self.edit.place_forget())
            self.profile_pic.bind("<Button-1>", lambda e: self.upload_profile_pic(user_data[0]))
            self.edit.bind("<Button-1>", lambda e: self.upload_profile_pic(user_data[0]))
        self.deiconify()
        
    def upload_profile_pic(self, user_id):
        try:
            session = ftplib.FTP("spackwell.hol.es", "u377515927.billymaths", "0rC?@q/nqmji7x@PxS")
            image = Image.open(askopenfilename(filetypes=(("Image files", "*.png;*.jpg;*.gif"), ("All files", "*.*"))))
            resized_image = image.resize((128, 128), Image.ANTIALIAS)
            resized_image.save("img\\temp.png")
            rb_image = open("img\\temp.png", "rb")
            session.storbinary("STOR profile_pics/" + str(user_id) + ".png", rb_image)
            image.close()
            rb_image.close()
            session.quit()
            os.remove("img\\temp.png")
            if tkinter.messagebox.askyesno("File upload",
                                           "File was successfully uploaded.\n Would you like to reload your profile?"):
                self.destroy()
                Profile(root, self.user_data, True, self.colour)
            else:
                self.focus_force()

        except AttributeError:
            tkinter.messagebox.showerror("File Error", "File not selected.")
        except OSError:
            tkinter.messagebox.showerror("File Error", "Invalid file type.")

    def set_tree_worksheets(self):
        self.tree1["columns"] = ("type", "score", "time", "date")
        self.tree1.heading("#0", text="Topic", anchor="w", command=lambda: self.set_data(self.tree1, 0, "worksheet"))
        self.tree1.column("#0", anchor="w", width=150)
        self.tree1.heading("type", text="Type", command=lambda: self.set_data(self.tree1, 1, "worksheet"))
        self.tree1.column("type", anchor="w", width=250)
        self.tree1.heading("score", text="Score", command=lambda: self.set_data(self.tree1, 3, "worksheet"))
        self.tree1.column("score", anchor="w", width=75)
        self.tree1.heading("time", text="Time", command=lambda: self.set_data(self.tree1, 4, "worksheet"))
        self.tree1.column("time", anchor="w", width=75)
        self.tree1.heading("date", text="Date", command=lambda: self.set_data(self.tree1, 5, "worksheet"))
        self.tree1.column("date", anchor="w", width=150)


    def set_tree_duels(self):
        self.tree2["columns"] = ("type", "winner", "loser", "date")
        self.tree2.heading("#0", text="Topic", anchor="w", command=lambda: self.set_data(self.tree2, 0, "duel"))
        self.tree2.column("#0", anchor="w", width=150)
        self.tree2.heading("type", text="Type", command=lambda: self.set_data(self.tree2, 1, "duel"))
        self.tree2.column("type", anchor="w", width=250)
        self.tree2.heading("winner", text="Winner", command=lambda: self.set_data(self.tree2, 2, "duel"))
        self.tree2.column("winner", anchor="w", width=75)
        self.tree2.heading("loser", text="Loser", command=lambda: self.set_data(self.tree2, 3, "duel"))
        self.tree2.column("loser", anchor="w", width=75)
        self.tree2.heading("date", text="Date", command=lambda: self.set_data(self.tree2, 5, "duel"))
        self.tree2.column("date", anchor="w", width=150)

    def set_data(self, tree, orderby, mode):
        tree.delete(*tree.get_children())
        if tree == self.tree1:
            if self.worksheet_data is not None:
                self.worksheet_data = static_funcs.sort_table_data(self.worksheet_data, orderby, mode)
                print(self.worksheet_data)
                for i in self.worksheet_data:
                    print(i)
                    tree.insert('', 'end', text=i[0], values=(i[1], (str(i[2]) + "/" + str(i[3])), i[4], i[5]))
        elif tree == self.tree2:
            if self.duel_data is not None:
                self.duel_data = static_funcs.sort_table_data(self.duel_data, orderby, mode)
                print(self.duel_data)
                for i in self.duel_data:
                    print(i)
                    tree.insert('', 'end', text=i[0], values=(i[1], str(i[2]), str(i[3]), i[5]))


    def change_table_from_to(self, table1, table2):
        table1.grid_remove()
        table2.grid(row=3, column=0, columnspan=3)


class ProfileSearch(Toplevel):
    def __init__(self, master, colour):
        super(ProfileSearch, self).__init__(master)
        self.title("Profile Search")
        self.iconbitmap("img\\favicon2.ico")
        set_window(150, 50, self)
        self.colour = colour
        self.profile_label = Label(self, text="Profile:")
        self.profile_entry = Entry(self)
        self.search_button = Button(self, text="Search", command=lambda: self.search(self.profile_entry.get()))
        self.profile_label.grid(row=0, column=0)
        self.profile_entry.grid(row=0, column=1)
        self.search_button.grid(row=2, column=0, columnspan=2)
        self.profile_entry.focus_force()
        self.search_bind = self.bind("<Return>", lambda e: self.search(self.profile_entry.get()))

    def search(self, username):
        user_data = db("query", "SELECT user_id, username, admin_lvl, name, email, school FROM user WHERE username='" + username + "'", "one")
        if user_data is None:
            tkinter.messagebox.showerror("Entry Error", "Username does not exist.")
            self.profile_entry.focus_force()
        else:
            self.destroy()
            Profile(root, user_data, False, self.colour)


class Leaderboard(Toplevel):
    def __init__(self, master):
        super(Leaderboard, self).__init__(master)
        self.withdraw()
        self.title("Leaderboard")
        self.iconbitmap("img\\favicon2.ico")
        set_window(300, 225, self)
        self.leaderboard_data = db("leaderboard", "", "")
        self.tree = tkinter.ttk.Treeview(self)
        self.tree["columns"] = ("username", "won", "win %")
        self.tree.heading("#0", text="Elo", anchor="w")
        self.tree.column("#0", anchor="w", width=75)
        self.tree.heading("username", text="Username")
        self.tree.column("username", anchor="w", width=75)
        self.tree.heading("won", text="Won")
        self.tree.column("won", anchor="w", width=75)
        self.tree.heading("win %", text="Win %")
        self.tree.column("win %", anchor="w", width=75)
        for i in self.leaderboard_data:
            if i[2] == 0:
                self.tree.insert('', 'end', text=str(i[0]), values=(i[1], str(i[2]), "0"))
            elif i[3] == 0:
                self.tree.insert('', 'end', text=str(i[0]), values=(i[1], str(i[2]), "100"))
            else:
                self.tree.insert('', 'end', text=str(i[0]), values=(i[1], str(i[2]), str(round((i[2] / (i[2] + (i[3])))*100))))
        self.tree.grid(row=0, column=0)
        self.deiconify()
class MathsGui(Frame):
    def __init__(self, master):
        super(MathsGui, self).__init__(master)
        self.master = master
        self.settings = self.load_config()
        self.user_data = []
        self.validation = StringVar()
        self.master.grid_columnconfigure(0, weight=1)
        self.config(width=500, height=300)
        master.config(bg=self.settings[1])
        self.main_menu_frame = Frame(self, bg=self.settings[1])
        self.worksheets_frame = Frame(self, bg=self.settings[1])
        self.duels_frame = Frame(self, bg=self.settings[1])
        self.profile_frame = Frame(self, bg=self.settings[1])
        self.login_frame = Frame(self, bg=self.settings[1])
        if self.settings[0] == "1":
            self.splash_screen = SplashScreen(root)
            pulse_thread = threading.Thread(target=self.splash_screen.colour_pulse, args=())
            setup_thread = threading.Thread(target=self.setup, args=())
            pulse_thread.start()
            setup_thread.start()
        else:
            self.create_menu_widgets()
            self.create_worksheets_widgets()
            self.create_duels_widgets()
            self.create_profile_widgets()
            self.create_login_widgets()
            self.grid()
            self.gotofrom(self.login_frame, "None")



    def setup(self):
        self.create_menu_widgets()
        self.splash_screen.set_progress(20, "Loading GUI(2)")
        self.create_worksheets_widgets()
        self.create_duels_widgets()
        self.splash_screen.set_progress(40, "Loading GUI(3)")
        self.create_profile_widgets()
        self.splash_screen.set_progress(60, "Loading GUI(4)")
        self.create_login_widgets()
        self.splash_screen.set_progress(80, "finalizing setup")
        self.splash_screen.after(10000, self.splash_screen.set_progress_done)
        self.grid()
        self.gotofrom(self.login_frame, "None")

    def load_config(self):
        if not os.path.isfile("config.txt"):
            config_file = open("config.txt", "w")
            config_file.write("splash_screen_enable = 0\ncolur_scheme = #26f23e\n")
            config_file.close()
        config_file = open("config.txt", "r")
        config, temp = [], ""
        for line in config_file:
            count = 1
            for i in line:
                count += 1
                if i == "=":
                    break
            config.append(line[count:-1])
        if len(config) != 2:
            config[0] = ["1"]
        try:
            self.config(bg=config[1])
        except:
            config[1] = "#26f23e"
            self.config(bg=config[1])
        config_file.close()
        return config

    def create_login_widgets(self):
        self.validation.set("Username=Steve\n Password=Test")
        user_label = Label(self.login_frame, text="Username:", bg=self.settings[1])
        pass_label = Label(self.login_frame, text="Password:", bg=self.settings[1])
        validation_label = Label(self.login_frame, textvariable=self.validation, bg=self.settings[1])
        user_entry = Entry(self.login_frame)
        pass_entry = Entry(self.login_frame, show="*")
        register_button = Button(self.login_frame, text="Register", command=lambda: Register(root))
        login_button = Button(self.login_frame, text="Login", command=lambda: self.login(user_entry.get(), pass_entry.get()))
        user_label.grid(row=0, column=0)
        user_entry.grid(row=1, column=0)
        pass_label.grid(row=3, column=0)
        pass_entry.grid(row=4, column=0)
        login_button.grid(row=5, column=0, pady=10, sticky="W")
        register_button.grid(row=5, column=0, pady=10, sticky="E")
        validation_label.grid(row=6, column=0)
        user_entry.focus_force()
        self.login_enter = root.bind("<Return>", (lambda e: (self.login(user_entry.get(), pass_entry.get()))))

    def create_menu_widgets(self):
        #set_window(500, 300)
        header_label = Label(self.main_menu_frame, text="Main Menu", bg=self.settings[1])
        profile_button = Button(self.main_menu_frame, text="Profile", command=lambda: self.gotofrom(self.profile_frame,
                                                                                                    self.main_menu_frame))
        worksheets_button = Button(self.main_menu_frame, text="Worksheets",
                                   command=lambda: self.gotofrom(self.worksheets_frame,
                                                                 self.main_menu_frame))
        duels_button = Button(self.main_menu_frame, text="Duels",
                              command=lambda: self.gotofrom(self.duels_frame,
                                                            self.main_menu_frame))
        header_label.grid(row=0, column=0)
        profile_button.grid(row=1, column=0, pady=5)
        duels_button.grid(row=2, column=0, pady=5)
        worksheets_button.grid(row=3, column=0, pady=5)

    # ungrid current frame and grid the desired frame, also change window size if necessary
    def gotofrom(self, dest_frame, curr_frame):
        if curr_frame != "None":
            curr_frame.grid_remove()
        if dest_frame == self.login_frame:
            set_window(250, 200, root)
            dest_frame.grid(pady=10)
        elif dest_frame == self.main_menu_frame:
            set_window(500, 300, root)
            dest_frame.grid(padx=50, pady=12, sticky="NEW")
        else:
            dest_frame.grid(padx=50, pady=12)

    def create_worksheets_widgets(self):
        header_label = Label(self.worksheets_frame, text="Worksheets", bg=self.settings[1])
        back_button = Button(self.worksheets_frame, text="Back to menu", command=lambda: self.gotofrom(self.main_menu_frame,
                                                                                                       self.worksheets_frame, ))
        work1_button = Button(self.worksheets_frame, text="Fractions", command=lambda: FractionsSheetOptions(root, self.user_data[0], "worksheet"))
        work2_button = Button(self.worksheets_frame, text="Quadratics", command=lambda: QuadraticsSheetOptions(root, self.user_data[0], "worksheet"))

        header_label.grid(row=0, column=0)
        back_button.grid(row=1, column=0, pady=4)
        work1_button.grid(row=2, column=0, pady=4)
        work2_button.grid(row=3, column=0, pady=4)

    def create_profile_widgets(self):
        header_label = Label(self.profile_frame, text="Profile", bg=self.settings[1])
        back_button = Button(self.profile_frame, text="Back to menu", command=lambda: self.gotofrom(self.main_menu_frame,
                                                                                                    self.profile_frame, ))
        my_profile_button = Button(self.profile_frame, text="My Profile", command=lambda: Profile(root, self.user_data, True, self.settings[1]))
        profile_search_button = Button(self.profile_frame, text="Profile Search", command=lambda: ProfileSearch(root, self.settings[1]))
        header_label.grid(row=0, column=0)
        back_button.grid(row=1, column=0, pady=4)
        my_profile_button.grid(row=2, column=0, pady=4)
        profile_search_button.grid(row=3, column=0, pady=4)

    def create_duels_widgets(self):
        header_label = Label(self.duels_frame, text="Duels", bg=self.settings[1])
        back_button = Button(self.duels_frame, text="Back to menu", command=lambda: self.gotofrom(self.main_menu_frame,
                                                                                                  self.duels_frame, ))
        work1_button = Button(self.duels_frame, text="Fractions", command=lambda: FractionsSheetOptions(root, self.user_data[0], "duel"))
        work2_button = Button(self.duels_frame, text="Quadratics", command=lambda: QuadraticsSheetOptions(root, self.user_data[0], "duel"))
        leaderboard_button = Button(self.duels_frame, text="Leaderboard", command=lambda: Leaderboard(root))

        header_label.grid(row=0, column=0)
        back_button.grid(row=1, column=0, pady=4)
        work1_button.grid(row=2, column=0, pady=4)
        work2_button.grid(row=3, column=0, pady=4)
        leaderboard_button.grid(row=4, column=0, pady=4)

    def login(self, user, passw):
        valid = db("login", user, passw)
        if valid[0] == "none":
            self.validation.set("Invalid Username.")
        elif valid[0] == "user":
            self.validation.set("Invalid Password.")
        else:
            self.user_data = valid[1]
            root.unbind("<Return>", self.login_enter)
            self.gotofrom(self.main_menu_frame, self.login_frame)

host = socket.gethostname()
root = Tk()
root.title("BillyMaths")
root.iconbitmap("img\\favicon2.ico")
MathsGui(root)
root.mainloop()
#add new config stuff to testing and validation
