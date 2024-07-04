import tkinter as tk
import poker_func
from PIL import Image, ImageTk
import timeit


# Zwraca listę siły rąk przekazanych graczy
def compare_7_card_hands(hands_7_cards):
    hands_and_scores = []
    for hand in hands_7_cards:
        hands_and_scores.append((hand, poker_func.check_hand_7_cards(hand)))

    return hands_and_scores


def calculate(hands, table_cards):

    available_cards = poker_func.generate_av_cards(hands, table_cards)

    start = timeit.default_timer()
    win_tie_counts, amount_of_tables = poker_func.win_probability(
        hands, table_cards, available_cards, 50000
    )
    print(timeit.default_timer() - start)
    strings = []

    for i, win_tie in enumerate(win_tie_counts):
        strings.append(
            f"{hands[i][0]} {hands[i][1]}\n Win: {win_tie[0] / amount_of_tables * 100:.2f} %\nTie: {win_tie[1] / amount_of_tables * 100:.2f} %"
        )
        print(f"{hands[i]},", end=" ")
        print(f"Win: {win_tie[0] / amount_of_tables * 100:.2f} %,", end=" ")
        print(f"Tie: {win_tie[1] / amount_of_tables * 100:.2f} %")

    return strings


def calculate_unknown(hero_hand, table_cards):

    available_cards = poker_func.generate_av_cards([hero_hand], table_cards)

    start = timeit.default_timer()
    results = poker_func.win_probability_against_unknown_cards(
        hero_hand,
        table_cards,
        available_cards,
        num_of_cards_to_generate=1225,
        num_of_tables=100,
        choice="automatic",
    )
    print(timeit.default_timer() - start)

    # noinspection PyListCreation
    strings = []

    strings.append(
        f"{hero_hand[0]} {hero_hand[1]}\n Win: {results[0] / results[3] * 100:.2f} %\nTie: {results[2] / results[3] * 100:.2f} %"
    )
    print(f"{hero_hand},", end=" ")
    print(f"Win: {results[0] / results[3] * 100:.2f} %,", end=" ")
    print(f"Tie: {results[2] / results[3] * 100:.2f} %")

    strings.append(
        f"? ?\n Win: {results[1] / results[3] * 100:.2f} %\nTie: {results[2] / results[3] * 100:.2f} %"
    )
    print(f"? ?,", end=" ")
    print(f"Win: {results[1] / results[3] * 100:.2f} %,", end=" ")
    print(f"Tie: {results[2] / results[3] * 100:.2f} %")

    return strings


def get_hand_input():
    hands = []

    labels[0].place_forget()
    labels[1].place_forget()
    labels[2].place_forget()
    labels[3].place_forget()
    labels[4].place_forget()
    labels[5].place_forget()
    table_label.place_forget()

    unknown = 0
    for i, text_box1 in enumerate(text_boxes):
        inputted = text_box1.get(1.0, "end-1c")
        if len(inputted) != 5:
            if inputted == "? ?" or inputted == "? ? ":
                unknown = 1
                show[i] = 1
            else:
                show[i] = 0
            continue
        hands.append(poker_func.parse_cards(inputted))
        show[i] = 1

    table_string = table_box.get(1.0, "end-1c")

    table_cards = poker_func.parse_cards(table_string)

    table_string_to_show = ""
    for card in table_cards:
        table_string_to_show += f"{card} "
    table_label.configure(text=table_string_to_show)
    table_label.place(relx=0.5, rely=0.6, anchor="center")

    num_of_hands = len(hands)
    if num_of_hands:
        print(f"{num_of_hands=}")
        print(f"{unknown=}")
        if unknown and num_of_hands == 1:
            received_strings = calculate_unknown(hands[0], table_cards)
        else:
            received_strings = calculate(hands, table_cards)
        k = 0
        for i, label in enumerate(labels):
            if show[i]:
                label.configure(text=received_strings[k])
                k += 1
                match i:
                    case 0:
                        labels[0].place(
                            relx=x_row_2 + x_diff,
                            rely=y_row_1 + y_diff,
                            anchor="center",
                        )
                    case 1:
                        labels[1].place(
                            relx=x_row_3 + x_diff,
                            rely=y_row_2 + y_diff,
                            anchor="center",
                        )
                    case 2:
                        labels[2].place(
                            relx=x_row_3 + x_diff,
                            rely=y_row_3 + y_diff,
                            anchor="center",
                        )
                    case 3:
                        labels[3].place(
                            relx=x_row_2 + x_diff,
                            rely=y_row_4 + y_diff,
                            anchor="center",
                        )
                    case 4:
                        labels[4].place(
                            relx=x_row_1 + x_diff,
                            rely=y_row_3 + y_diff,
                            anchor="center",
                        )
                    case 5:
                        labels[5].place(
                            relx=x_row_1 + x_diff,
                            rely=y_row_2 + y_diff,
                            anchor="center",
                        )

    table_string = ""


# Top level window
frame = tk.Tk()
frame.title("Poker probabilities")

width = 900
height = 500

frame.geometry(f"{width}x{height}")


# Load an image in the script
img = Image.open("images/table.png")

# Resize the Image using resize method
resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
background = ImageTk.PhotoImage(resized_img)

background_label = tk.Label(frame, image=background, pady=500)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# TextBox Creation

text_boxes = []
table_box = tk.Text(frame, height=1, width=14)
table_box.place(relx=0.5, rely=0.5, anchor="center")
table_box.configure(font=("Helvetica", 32))
table_label = tk.Label(
    frame, text="", bg="#f0f0f0", bd=5, fg="black", font=("Helvetica", 15)
)


for _ in range(6):
    text_boxes.append(
        tk.Text(frame, height=1, width=6),
    )

for text_box in text_boxes:
    text_box.configure(font=("Helvetica", 32))

x_row_1 = 0.22
x_row_2 = 0.5
x_row_3 = 0.78

y_row_1 = 0.2
y_row_2 = 0.28
y_row_3 = 0.6
y_row_4 = 0.7

text_boxes[0].place(relx=x_row_2, rely=y_row_1, anchor="center")
text_boxes[1].place(relx=x_row_3, rely=y_row_2, anchor="center")
text_boxes[2].place(relx=x_row_3, rely=y_row_3, anchor="center")
text_boxes[3].place(relx=x_row_2, rely=y_row_4, anchor="center")
text_boxes[4].place(relx=x_row_1, rely=y_row_3, anchor="center")
text_boxes[5].place(relx=x_row_1, rely=y_row_2, anchor="center")

labels = []
for _ in range(6):
    labels.append(
        tk.Label(frame, text="", bg="#f0f0f0", bd=5, fg="black", font=("Helvetica", 15))
    )

x_diff = 0
y_diff = 0.14


show = [0 for _ in range(len(text_boxes))]

# Button Creation
calculate_btn = tk.Button(
    frame, text="Calculate", command=get_hand_input, font=("Helvetica", 20)
)
calculate_btn.place(relx=0.75, rely=0.93, anchor="center")


frame.mainloop()
