# Final Assignment ICS3U1 - Powersmash Scroller Game
# Azeem, Shayaan

# Press ESC to quit game when it is in menu
# Press ESC to go from controls/leaderboard to menu
# Press ESC when game is over to quit the game

# The functionality to return to the menu while the game loop is running doesn't work due to the implementation, and I can't seem to figure it out. Other than that, I did restore and re-implement it in a more modular way. However, some functionalities are still redundant due to time constraints.

import os
from pygame import *
import pygame.draw
import math
import random

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (20, 20)

# Function to update the leaderboard with a new score
def update_leaderboard(score):
    leaderboard = []
    # Read the leaderboard file
    with open("leaderboard.txt", "r") as file:
        leaderboard = file.readlines()

    # Check if the score is already in the leaderboard
    if str(score) + "\n" not in leaderboard:
        # Add the new score to the leaderboard list
        leaderboard.append(str(score) + "\n")
        # Write the updated leaderboard back to the file
        with open("leaderboard.txt", "w") as file:
            file.writelines(leaderboard)

# Function to draw the game
def drawGame(screen):
    # Set the size of the game window
    size = width, height = 635, 680

    # Define colors
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Define fonts
    menuFont = font.SysFont("Arial", 60)
    score_font = font.SysFont("Arial", 30)

    # Initialize the game variables
    running = True
    myClock = time.Clock()
    score = 0

    # Set the background color of the screen to blue
    screen.fill(BLUE)

    # Load the track
    bg = image.load("F1TRACK.png").convert()

    # Set the initial scroll position and scroll speed
    scroll = [0, 0]
    scroll_speed = 5
    speed_cap = 18

    # Calculate the number of tiles needed to cover the screen height
    tiles = math.ceil(height / bg.get_height()) + 1

    # Load the car
    redbull = image.load("redbull.png")
    redbull = transform.scale(redbull, (96, 224))

    # Load the battery and bin
    battery = image.load("battery.png")
    bin = image.load("bin.png")

    # Coordinates for battery and bin spawn
    coordinates = [(80, -95), (280, -95), (480, -95)]

    # Randomly spawn battery and bin
    available_coordinates = [i for i in range(3)]
    battery_index = random.choice(available_coordinates)
    battery_x, battery_y = coordinates[battery_index]
    available_coordinates.remove(battery_index)
    bin_index = random.choice(available_coordinates)
    bin_x, bin_y = coordinates[bin_index]

    while battery_x == bin_x:  # Ensure battery and bin never have the same x value
        bin_index = random.choice(available_coordinates)
        bin_x, bin_y = coordinates[bin_index]

    # initial position of car
    redbull_x = 250
    redbull_y = 320

    # Game states
    GAME_RUNNING = 0
    GAME_OVER = 1
    game_state = GAME_RUNNING

    # Game Loop
    x_position = 2
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
            elif e.type == KEYDOWN:
                if game_state == GAME_RUNNING:
                    if e.key == K_LEFT:
                        if x_position > 1:
                            x_position -= 1
                    elif e.key == K_RIGHT:
                        if x_position < 3:
                            x_position += 1
                elif game_state == GAME_OVER:
                    if e.key == K_SPACE:
                        game_state = GAME_RUNNING
                        score = 0
                        scroll_speed = 5
                        x_position = 2
                        available_coordinates = [i for i in range(3)]
                        battery_index = random.choice(available_coordinates)
                        battery_x, battery_y = coordinates[battery_index]
                        available_coordinates.remove(battery_index)
                        bin_index = random.choice(available_coordinates)
                        bin_x, bin_y = coordinates[bin_index]

                        while bin_x == battery_x:
                            bin_index = random.choice(available_coordinates)
                            bin_x, bin_y = coordinates[bin_index]

                        available_coordinates.remove(bin_index)

        # Handle the escape key outside the event loop
        if game_state == GAME_OVER:
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                game_state = STATE_MENU
                running = False

        # Update the scroll position
        scroll[1] += scroll_speed

        # Reset the scroll position when it reaches the bottom
        if scroll[1] >= bg.get_height():
            scroll[1] = 0

        # Draw the background tiles
        i = 0
        while i < tiles:
            screen.blit(bg, (0, -bg.get_height() * i + scroll[1]))
            i += 1

        # Draw the Red Bull
        if x_position == 1:
            redbull_x = 70
        elif x_position == 2:
            redbull_x = 250
        else:
            redbull_x = 440

        screen.blit(redbull, (redbull_x, redbull_y))

        # Draw the battery
        battery_y += scroll_speed
        screen.blit(battery, (battery_x, battery_y))

        # Check if the battery has moved off the screen, if so, respawn it
        if battery_y > 680:
            battery_index = random.randint(0, 2)
            battery_x, battery_y = coordinates[battery_index]
            available_coordinates = [i for i in range(3) if i != battery_index]

        # Draw the bin
        bin_y += scroll_speed
        screen.blit(bin, (bin_x, bin_y))

        if redbull.get_rect(topleft=(redbull_x, redbull_y)).colliderect(
                battery.get_rect(topleft=(battery_x, battery_y))):
            score += 10
            battery_index = random.randint(0, 2)
            battery_x, battery_y = coordinates[battery_index]
            available_coordinates = [i for i in range(3) if i != battery_index]
            if score % 20 == 0:
                scroll_speed += (speed_cap - scroll_speed) / 5

        # Check if the bin has moved off the screen, if so, respawn it
        if bin_y > 680:
            bin_index = random.choice(available_coordinates)
            bin_x, bin_y = coordinates[bin_index]
            available_coordinates = [i for i in range(3) if i != bin_index]

        score_text = score_font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(score_text, (270, 10))

        bin_rect = bin.get_rect(topleft=(bin_x, bin_y))
        if redbull.get_rect(topleft=(redbull_x, redbull_y)).colliderect(bin_rect):
            game_state = GAME_OVER

        if game_state == GAME_OVER:
            # Pause the game
            scroll_speed = 0
            update_leaderboard(score)
            # Display game over message and final score
            game_over_text = menuFont.render("Game Over", True, RED)
            final_score_text = score_font.render("Final Score: " + str(score), True, RED)
            restart_text = score_font.render("Press SPACE BAR to try again", True, RED)

            screen.blit(game_over_text, (180, 250))
            screen.blit(final_score_text, (220, 320))
            screen.blit(restart_text, (120, 400))

        score_text = score_font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(score_text, (270, 10))
        display.flip()
        myClock.tick(60)

# Define game states
STATE_MENU = 0
STATE_LEADERBOARD = 1
STATE_CONTROL = 2
STATE_GAME = 3

# Function to draw the menu screen
def drawMenu(screen, button, mx, my, state):
    blockWidth = width // 3
    blockHeight = height // 7
    rectList = [
        Rect(blockWidth, blockHeight, blockWidth, blockHeight),  # Play Game
        Rect(blockWidth, 3 * blockHeight, blockWidth, blockHeight),  # Leaderboard
        Rect(blockWidth, 5 * blockHeight, blockWidth, blockHeight),  # Control
    ]
    stateList = [STATE_GAME, STATE_LEADERBOARD, STATE_CONTROL]  # Updated state list
    titleList = ["Play Game", "Leaderboard", "Controls"]
    draw.rect(screen, RED, (0, 0, width, height))

    for i in range(len(rectList)):
        rect = rectList[i]  # get the current Rect
        draw.rect(screen, WHITE, rect)  # draw the Rect
        text = menuFont.render(titleList[i], 1, RED)  # make the font
        textWidth, textHeight = menuFont.size(titleList[i])  # get the font size
        useW = (blockWidth - textWidth) // 2  # use for centering
        useH = (blockHeight - textHeight) // 2
        # getting a centered Rectangle
        textRect = Rect(rect[0] + useW, rect[1] + useH, textWidth, textHeight)
        screen.blit(text, textRect)  # draw to screen

        if rect.collidepoint(mx, my):
            draw.rect(screen, BLACK, rect, 2)
            if button == 1:
                state = stateList[i]  # Update the state when a button is clicked
    return state

# Function to draw the leaderboard screen
def drawLeaderboard(screen, button, mx, my, state):
    leaderboard = []
    # Read the leaderboard file
    with open("leaderboard.txt", "r") as file:
        leaderboard = file.readlines()

    # Set up fonts
    font = pygame.font.SysFont("Arial", 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = STATE_MENU
                    return state

        screen.fill((255, 255, 255))

        # Display leaderboard
        leaderboard_y = 50
        for i, score_text in enumerate(sorted(leaderboard, key=lambda x: int(x), reverse=True)):
            position = "P{}".format(i + 1)
            score_text = "{}: {}".format(position, score_text.strip())
            leaderboard_text = font.render(score_text, True, (0, 0, 0))
            screen.blit(leaderboard_text, (50, leaderboard_y + i * 30))

        pygame.display.update()

        if button == 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return STATE_MENU
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return STATE_MENU

# Function to draw the controls screen
def drawControl(screen, button, mx, my, state):
    controls = pygame.image.load("controls.png")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return STATE_MENU
                if event.key == pygame.K_SPACE:
                    running = False

        screen.blit(controls, (0, 0))
        pygame.display.update()

    return state

# Game setup
size = width, height = 635, 680
screen = display.set_mode(size)
menuFont = font.SysFont("Futura", 30)
running = True
myClock = time.Clock()
state = STATE_MENU
mx = my = 0

# Game Loop
while running:
    button = 0
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == MOUSEBUTTONDOWN:
            mx, my = e.pos
            button = e.button
        elif e.type == MOUSEMOTION:
            mx, my = e.pos
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                if state != STATE_MENU:
                    state = STATE_MENU
                else:
                    running = False

    if state == STATE_MENU:
        state = drawMenu(screen, button, mx, my, state)
        if state == STATE_GAME:
            drawGame(screen)
    elif state == STATE_LEADERBOARD:
        state = drawLeaderboard(screen, button, mx, my, state)
    elif state == STATE_CONTROL:
        state = drawControl(screen, button, mx, my, state)
    else:
        running = False

    display.flip()
    myClock.tick(60)

quit()
