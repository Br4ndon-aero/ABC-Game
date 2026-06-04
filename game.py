import os
import time
import random
import keyboard  # make sure: pip install keyboard

# Game settings
LANES = 3
WIDTH = 30

# Player settings
player_lane = 1  # start in the middle lane
player_icon = "😎"

# Object settings
object_icon = "🚗"
coin_icon = "💰"

objects = []  # list of [lane, x]
coins = []    # list of [lane, x]

# Score
score = 0
coins_collected = 0

# Speed
speed = 0.1

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
    clear_screen()

    # Move objects and coins
    for obj in objects:
        obj[1] -= 1
    for coin in coins:
        coin[1] -= 1

    # Remove off-screen objects and coins
    objects = [obj for obj in objects if obj[1] >= 0]
    coins = [coin for coin in coins if coin[1] >= 0]

    # Check for collisions with objects
    for obj in objects:
        if obj[0] == player_lane and obj[1] == 0:
            print("Game Over! Final Score:", score)
            print("Coins collected:", coins_collected)
            exit()

    # Check for collisions with coins (safe removal)
    for coin in coins[:]:
        if coin[0] == player_lane and coin[1] == 0:
            coins_collected += 1
            score += 10
            coins.remove(coin)

    # Spawn new objects and coins randomly
    if random.random() < 0.3:  # 30% chance to spawn an object
        lane = random.randint(0, LANES - 1)
        objects.append([lane, WIDTH - 1])

    if random.random() < 0.2:  # 20% chance to spawn a coin
        lane = random.randint(0, LANES - 1)
        coins.append([lane, WIDTH - 1])

    # Draw the game state
    for lane in range(LANES):
        line = ""
        for x in range(WIDTH):
            if lane == player_lane and x == 0:
                line += player_icon
            elif any(obj[0] == lane and obj[1] == x for obj in objects):
                line += object_icon
            elif any(coin[0] == lane and coin[1] == x for coin in coins):
                line += coin_icon
            else:
                line += " "
        print(line)

    print(f"Score: {score} | Coins: {coins_collected}")
    print("Controls: A = left, C = middle, B = right")

    # Handle player input (A/C/B instead of arrows)
    if keyboard.is_pressed('a') and player_lane > 0:
        player_lane -= 1
    elif keyboard.is_pressed('c'):
        player_lane = 1
    elif keyboard.is_pressed('b') and player_lane < LANES - 1:
        player_lane += 1

    time.sleep(speed)
