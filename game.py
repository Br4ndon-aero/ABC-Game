import os
import time
import random
import keyboard
import ctypes   # ⭐ Needed for pure window centering


# ⭐ PURE PYTHON WINDOW CENTERING (works in .py AND .exe)
def center_window(width=1000, height=700):
    user32 = ctypes.windll.user32
    screen_w = user32.GetSystemMetrics(0)
    screen_h = user32.GetSystemMetrics(1)

    x = int((screen_w - width) / 2)
    y = int((screen_h - height) / 2)

    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.MoveWindow(hwnd, x, y, width, height, True)


# Call the centering function immediately
center_window()


# Game settings
LANES = 3
WIDTH = 60
SPACING = 1

# Player settings
player_lane = 1
player_icon = "😎"

# Object settings
obstacle_icon = "🚗"
coin_icon = "💰"

obstacles = []
coins = []

# Score
score = 0
coins_collected = 0


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# ⭐ START MENU
def start_menu():
    clear_screen()
    print("+" + "-" * WIDTH + "+")
    print("|" + "ABC GAME".center(WIDTH) + "|")
    print("|" + " ".center(WIDTH) + "|")
    print("|" + "Press ENTER to start".center(WIDTH) + "|")
    print("|" + " ".center(WIDTH) + "|")
    print("+" + "-" * WIDTH + "+")

    while True:
        if keyboard.is_pressed("enter"):
            time.sleep(0.2)
            break
        time.sleep(0.05)


# ⭐ DIFFICULTY MENU
def difficulty_menu():
    clear_screen()
    print("+" + "-" * WIDTH + "+")
    print("|" + "SELECT DIFFICULTY".center(WIDTH) + "|")
    print("|" + " ".center(WIDTH) + "|")
    print("|" + "1 = EASY".center(WIDTH) + "|")
    print("|" + "2 = NORMAL".center(WIDTH) + "|")
    print("|" + "3 = HARD".center(WIDTH) + "|")
    print("|" + " ".center(WIDTH) + "|")
    print("+" + "-" * WIDTH + "+")

    while True:
        if keyboard.is_pressed("1"):
            time.sleep(0.2)
            return "easy"
        if keyboard.is_pressed("2"):
            time.sleep(0.2)
            return "normal"
        if keyboard.is_pressed("3"):
            time.sleep(0.2)
            return "hard"
        time.sleep(0.05)


# ⭐ RESTART MENU
def restart_menu():
    print()
    print("Press R to restart")
    print("Press Q to quit")

    while True:
        if keyboard.is_pressed("r"):
            time.sleep(0.2)
            return "restart"
        if keyboard.is_pressed("q"):
            exit()
        time.sleep(0.05)


# ⭐ MAIN GAME LOOP
def game_loop():
    global player_lane, score, coins_collected, obstacles, coins

    player_lane = 1
    score = 0
    coins_collected = 0
    obstacles = []
    coins = []

    difficulty = difficulty_menu()

    if difficulty == "easy":
        spawn_rate = 0.08
        move_every = 4
        speed = 0.05
    elif difficulty == "normal":
        spawn_rate = 0.14
        move_every = 3
        speed = 0.05
    elif difficulty == "hard":
        spawn_rate = 0.22
        move_every = 2
        speed = 0.04

    frame = 0

    while True:
        clear_screen()
        print("+" + "-" * WIDTH + "+")

        frame += 1

        # ⭐ Smooth movement
        if frame % move_every == 0:
            for o in obstacles:
                o[1] -= 1
            for c in coins:
                c[1] -= 1

            obstacles[:] = [o for o in obstacles if o[1] >= -1]
            coins[:] = [c for c in coins if c[1] >= -1]

        # ⭐ Ghost‑proof collision
        for o_lane, o_x in obstacles:
            if o_lane == player_lane and o_x <= 0:
                print("💥 GAME OVER 💥")
                print(f"Final Score: {score}")
                print(f"Coins Collected: {coins_collected}")
                if restart_menu() == "restart":
                    return

        # ⭐ Coin pickup
        for c in coins[:]:
            if c[0] == player_lane and c[1] <= 0:
                coins_collected += 1
                score += 10
                coins.remove(c)

        # ⭐ Spawning
        if random.random() < spawn_rate:
            obstacles.append([random.randint(0, LANES - 1), WIDTH - 1])

        if random.random() < spawn_rate * 0.6:
            coins.append([random.randint(0, LANES - 1), WIDTH - 1])

        # ⭐ Drawing
        for lane in range(LANES):
            row = [" "] * WIDTH

            if lane == player_lane:
                row[0] = player_icon

            for o_lane, o_x in obstacles:
                if o_lane == lane and 0 <= o_x < WIDTH:
                    row[o_x] = obstacle_icon

            for c_lane, c_x in coins:
                if c_lane == lane and 0 <= c_x < WIDTH:
                    row[c_x] = coin_icon

            print("|" + "".join(row) + "|")
            for _ in range(SPACING):
                print("|" + " " * WIDTH + "|")

        print("+" + "-" * WIDTH + "+")
        print(f"Score: {score}   Coins: {coins_collected}")
        print("Controls: A = left, C = middle, B = right")

        # ⭐ Player input
        if keyboard.is_pressed("a") and player_lane > 0:
            player_lane -= 1
        elif keyboard.is_pressed("c"):
            player_lane = 1
        elif keyboard.is_pressed("b") and player_lane < LANES - 1:
            player_lane += 1

        score += 1
        time.sleep(speed)


# ⭐ GAME FLOW
while True:
    start_menu()
    game_loop()
