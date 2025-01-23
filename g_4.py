import tkinter as tk
import random

# Konfigurasi dasar game
GAME_WIDTH = 500
GAME_HEIGHT = 400
CAR_SIZE = 30
COIN_SIZE = 20
BLOCK_SIZE = 50

# Warna objek
CAR_COLOR = "blue"
COIN_COLOR = "green"
BLOCK_COLOR = "red"
BACKGROUND_COLOR = "white"

class CarGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Game")

        # Skor dan target kemenangan
        self.score = 0
        self.target_score = 50  # Pemain menang jika mencapai skor ini
        self.game_over = False

        # Timer
        self.time_left = 40

        # Frame utama
        self.canvas = tk.Canvas(root, width=GAME_WIDTH, height=GAME_HEIGHT, bg=BACKGROUND_COLOR)
        self.canvas.pack(side=tk.LEFT)

        # Sidebar untuk skor dan waktu
        self.sidebar = tk.Frame(root)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.score_label = tk.Label(self.sidebar, text=f"Score: {self.score}")
        self.score_label.pack()

        self.timer_label = tk.Label(self.sidebar, text=f"Time: {self.time_left}s")
        self.timer_label.pack()

        # Mobil biru (pemain)
        self.car = self.canvas.create_rectangle(
            GAME_WIDTH // 2 - CAR_SIZE // 2,
            GAME_HEIGHT - CAR_SIZE - 10,
            GAME_WIDTH // 2 + CAR_SIZE // 2,
            GAME_HEIGHT - 10,
            fill=CAR_COLOR
        )

        # Koin hijau
        self.coin = self.create_coin()

        # Tembok merah
        self.blocks = []
        self.create_block()

        # Bind kontrol mobil
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        # Tombol main lagi
        self.restart_button = tk.Button(self.sidebar, text="Main Lagi", command=self.restart_game)
        self.restart_button.pack()
        self.restart_button.config(state=tk.DISABLED)

        # Timer game
        self.update_timer()
        self.move_blocks()
        self.move_coin()

    def create_coin(self):
        x = random.randint(0, GAME_WIDTH - COIN_SIZE)
        y = random.randint(0, GAME_HEIGHT // 2)
        return self.canvas.create_oval(x, y, x + COIN_SIZE, y + COIN_SIZE, fill=COIN_COLOR)

    def create_block(self):
        for _ in range(3):
            x = random.randint(0, GAME_WIDTH - BLOCK_SIZE)
            y = random.randint(0, GAME_HEIGHT // 2)
            block = self.canvas.create_rectangle(x, y, x + BLOCK_SIZE, y + BLOCK_SIZE, fill=BLOCK_COLOR)
            self.blocks.append(block)

    def move_left(self, event):
        if not self.game_over and self.canvas.coords(self.car)[0] > 0:
            self.canvas.move(self.car, -20, 0)

    def move_right(self, event):
        if not self.game_over and self.canvas.coords(self.car)[2] < GAME_WIDTH:
            self.canvas.move(self.car, 20, 0)

    def move_blocks(self):
        if not self.game_over:
            for block in self.blocks:
                self.canvas.move(block, 0, 5)
                if self.canvas.coords(block)[1] > GAME_HEIGHT:
                    x = random.randint(0, GAME_WIDTH - BLOCK_SIZE)
                    self.canvas.coords(block, x, 0, x + BLOCK_SIZE, BLOCK_SIZE)

                # Deteksi tabrakan dengan mobil
                if self.check_collision(self.car, block):
                    self.end_game("Game Over! You hit a block.")

            # Lanjutkan animasi blok
            self.root.after(50, self.move_blocks)

    def move_coin(self):
        if not self.game_over:
            self.canvas.move(self.coin, 0, 3)
            if self.canvas.coords(self.coin)[1] > GAME_HEIGHT:
                self.canvas.delete(self.coin)
                self.coin = self.create_coin()

            # Deteksi tabrakan dengan mobil
            if self.check_collision(self.car, self.coin):
                self.score += 10
                self.score_label.config(text=f"Score: {self.score}")
                self.canvas.delete(self.coin)
                self.coin = self.create_coin()

                # Cek kemenangan
                if self.score >= self.target_score:
                    self.end_game("You Win!")

            # Lanjutkan animasi koin
            self.root.after(50, self.move_coin)

    def update_timer(self):
        if not self.game_over:
            if self.time_left > 0:
                self.time_left -= 1
                self.timer_label.config(text=f"Time: {self.time_left}s")
                self.root.after(1000, self.update_timer)
            else:
                self.end_game("Game Over! Time's up.")

    def check_collision(self, obj1, obj2):
        x1, y1, x2, y2 = self.canvas.coords(obj1)
        a1, b1, a2, b2 = self.canvas.coords(obj2)
        return not (x2 < a1 or x1 > a2 or y2 < b1 or y1 > b2)

    def end_game(self, message):
        self.game_over = True
        self.canvas.create_text(
            GAME_WIDTH // 2, GAME_HEIGHT // 2,
            text=message, font=("Arial", 24), fill="black"
        )
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")
        self.restart_button.config(state=tk.NORMAL)

    def restart_game(self):
        self.game_over = False
        self.score = 0
        self.time_left = 30
        self.score_label.config(text=f"Score: {self.score}")
        self.timer_label.config(text=f"Time: {self.time_left}s")
        self.canvas.delete("all")
        self.car = self.canvas.create_rectangle(
            GAME_WIDTH // 2 - CAR_SIZE // 2,
            GAME_HEIGHT - CAR_SIZE - 10,
            GAME_WIDTH // 2 + CAR_SIZE // 2,
            GAME_HEIGHT - 10,
            fill=CAR_COLOR
        )
        self.coin = self.create_coin()
        self.blocks = []
        self.create_block()
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.restart_button.config(state=tk.DISABLED)
        self.update_timer()
        self.move_blocks()
        self.move_coin()

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    game = CarGame(root)
    root.mainloop()
