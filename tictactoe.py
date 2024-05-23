import tkinter as tk
from tkinter import messagebox
import random
import os
import winsound
import time

class TicTacToeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self.geometry("300x380")
        self.configure(bg="#8B4513")  # Wood-themed background color
        self.current_player = "X"
        self.player1 = ""
        self.player2 = ""
        self.buttons = []
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.win_animations = []

        self.load_sounds()
        self.create_widgets()

    def load_sounds(self):
        self.click_sound = "click_sound.wav"

    def create_widgets(self):
        # Name input frame
        self.name_input_frame = tk.Frame(self, bg="#8B4513")  # Wood-themed background color
        self.name_input_frame.pack()

        tk.Label(self.name_input_frame, text="Player 1 (X): ", bg="#8B4513", fg="#FFFFFF").grid(row=0, column=0)
        self.player1_entry = tk.Entry(self.name_input_frame)
        self.player1_entry.grid(row=0, column=1)

        tk.Label(self.name_input_frame, text="Player 2 (O): ", bg="#8B4513", fg="#FFFFFF").grid(row=1, column=0)
        self.player2_entry = tk.Entry(self.name_input_frame)
        self.player2_entry.grid(row=1, column=1)

        self.play_with_computer = tk.BooleanVar()
        self.play_with_computer.set(False)
        tk.Checkbutton(self.name_input_frame, text="Play with Computer", variable=self.play_with_computer, bg="#8B4513", fg="#FFFFFF").grid(row=2, columnspan=2)

        self.start_button = tk.Button(self.name_input_frame, text="Start Game", command=self.start_game, bg="#DEB887")  # Burlywood button color
        self.start_button.grid(row=3, columnspan=2)

        # Game frame
        self.game_frame = tk.Frame(self, bg="#8B4513")  # Wood-themed background color
        self.game_frame.pack()

        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.game_frame, width=10, height=3, command=lambda i=i, j=j: self.play(i, j), bg="#DEB887")  # Burlywood button color
                button.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def start_game(self):
        self.player1 = self.player1_entry.get() if self.player1_entry.get() else "Player 1"
        self.player2 = self.player2_entry.get() if self.player2_entry.get() else "Player 2"
        if self.play_with_computer.get():
            self.player2 = "Computer"
        self.name_input_frame.destroy()
        self.update_title()

    def update_title(self):
        if self.current_player == "X":
            self.title(f"Tic Tac Toe - {self.player1}'s Turn")
        else:
            self.title(f"Tic Tac Toe - {self.player2}'s Turn")

    def play(self, i, j):
        if not self.board[i][j]:
            self.board[i][j] = self.current_player
            self.buttons[i][j].config(text=self.current_player, state="disabled", fg="#FFFFFF")  # White font color
            winsound.PlaySound(self.click_sound, winsound.SND_ASYNC)
            if self.check_winner():
                self.play_win_animation()
            elif self.is_board_full():
                self.reset_game()
            else:
                self.switch_player()

            if self.current_player == "O" and self.player2 == "Computer":
                self.after(1000, self.computer_play)

    def computer_play(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if not self.board[i][j]]
        if empty_cells:
            cell = random.choice(empty_cells)
            self.play(cell[0], cell[1])

    def switch_player(self):
        self.current_player = "X" if self.current_player == "O" else "O"
        self.update_title()

    def get_current_player(self):
        return self.player1 if self.current_player == "X" else self.player2

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False

    def is_board_full(self):
        return all(self.board[i][j] for i in range(3) for j in range(3))

    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal")
        self.update_title()

    def play_win_animation(self):
        winner = self.get_current_player()
        self.win_animations = []

        # Display winner
        winner_label = tk.Label(self.game_frame, text=f"{winner} wins!", bg="#8B4513", fg="#FFFFFF")  # Wood-themed background and white font color
        winner_label.grid(row=3, columnspan=3)
        self.win_animations.append(winner_label)

        # Show party animation
        party_text = tk.Label(self.game_frame, text="🎉🥳🎊", bg="#8B4513", fg="#FFFFFF", font=("Arial", 24))  # Wood-themed background and white font color
        party_text.grid(row=4, columnspan=3)
        self.win_animations.append(party_text)

        # Next game button
        next_game_button = tk.Button(self.game_frame, text="Next Game", command=self.reset_win_animation, bg="#DEB887")  # Burlywood button color
        next_game_button.grid(row=5, columnspan=3)
        self.win_animations.append(next_game_button)

        # Play party sounds
        winsound.PlaySound("party_sound.wav", winsound.SND_ASYNC)

    def reset_win_animation(self):
        for widget in self.win_animations:
            widget.destroy()
        self.reset_game()
        self.update_title()

if __name__ == "__main__":
    app = TicTacToeGame()
    app.mainloop()
