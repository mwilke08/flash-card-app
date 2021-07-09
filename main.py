from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
french_word_display = True
to_learn = {}


# ------------ Flips the card after 3 seconds ------------------
def flip_card():
    global french_word_display

    if french_word_display:
        my_canvas.itemconfig(canvas_image, image=card_back_img)
        english_word = current_card["English"]
        my_canvas.itemconfig(card_title, text="English", fill="white")
        my_canvas.itemconfig(card_word, text=f"{english_word}", fill="white")
        french_word_display = False
    else:
        my_canvas.itemconfig(canvas_image, image=card_front_img)
        french_word = current_card["French"]
        my_canvas.itemconfig(card_title, text="French", fill="black")
        my_canvas.itemconfig(card_word, text=f"{french_word}", fill="black")
        french_word_display = True

    window.after(3000, flip_card)


# window set up
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)


# ------------ Get Data from CSV -----------------------------
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ------------ Generate new word from button click -------------

def generate_new_word():
    global current_card, flip_timer
    current_card = choice(to_learn)
    french_word = current_card["French"]
    my_canvas.itemconfig(card_title, text="French", fill="black")
    my_canvas.itemconfig(card_word, text=f"{french_word}", fill="black")
    my_canvas.itemconfig(canvas_image, image=card_front_img)


# ------------ Don't Know button was clicked ------------------
def dont_know():
    generate_new_word()


# ------------ Know button was clicked ------------------------
def know():
    global current_card
    print(len(to_learn))
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)

    generate_new_word()


# ------------ UI Set Up ---------------------------------------

# create images for the canvas
card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")

# canvas set up
my_canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas_image = my_canvas.create_image(400, 263, image=card_front_img)
card_title = my_canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = my_canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
my_canvas.grid(row=0, column=0, columnspan=2)

# button set up
dont_know_btn_img = PhotoImage(file="images/wrong.png")
know_btn_img = PhotoImage(file="images/right.png")
dont_know_btn = Button(image=dont_know_btn_img, highlightthickness=0, command=dont_know)
know_btn = Button(image=know_btn_img, highlightthickness=0, command=know)
dont_know_btn.grid(row=1, column=0)
know_btn.grid(row=1, column=1)

generate_new_word()

window.mainloop()
