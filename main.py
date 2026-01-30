import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
LANG_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")

# ------------------------ COMMANDS ------------------------ #

to_learn = {}
card = {}

try:
    data = pandas.read_csv("data/french_words_to_learn.csv")
except FileNotFoundError:
    og_data = pandas.read_csv("data/french_words.csv")
    to_learn = og_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")



def next_card():
    global card, flip_timer
    window.after_cancel(flip_timer)
    card = random.choice(to_learn)
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_text, text=card["French"], fill="black")
    flip_timer = window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_text, text=card["English"], fill="white")

def remove_card():
    to_learn.remove(card)
    # print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/french_words_to_learn.csv", index=False)
    next_card()



# ------------------------ UI ------------------------ #

window = Tk()
window.title("My Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

# Images
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
check = PhotoImage(file="images/right.png")
cross = PhotoImage(file="images/wrong.png")

# Canvas
canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, font=LANG_FONT)
card_text = canvas.create_text(400, 263, font=WORD_FONT)
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
right_btn = Button(image=check, highlightthickness=0, command=remove_card)
right_btn.grid(column=0, row=1)

wrong_btn = Button(image=cross, highlightthickness=0, command=next_card)
wrong_btn.grid(column=1, row=1)

next_card()

window.mainloop()
