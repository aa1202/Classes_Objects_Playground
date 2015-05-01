# ### IMPROVEMENTS AND BUGS THAT NEEDS TO BE FIXED ####
# - Use sprites instead of circle
# - Fix the score (make it so it doesn't count three times, rather just once)

import logging
import random
import webbrowser
import pygame
import pymysql
from database import connect_to_database

# Modify the logging output. If it's logging.WARNING only logging.warning("someError") will be displayed.
# If it's logging.INFO as default, every logging.info("someText") will be displayed.
logging.getLogger().setLevel(logging.WARNING)
pygame.init()
pygame.mixer.init()

# Defines X (display_width) and Y (display_height) axis for gameDisplay
display_width = 800
display_height = 600
game_display = pygame.display.set_mode([display_width, display_height])
pygame.display.set_caption('Flappy Bird')
background = pygame.image.load("Sprites\\bg.jpg").convert()
game_display.blit(background, [0, 0])

# Defines some essentials colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
light_red = (255, 0, 0)
green = (0, 155, 0)
light_green = (0, 255, 0)
blue = (0, 0, 255)
pink = (255, 200, 200)
yellow = (200, 200, 0)
light_yellow = (255, 255, 0)

# Sets some default game variables
first_pipe_location = 800
second_pipe_location = 400
final_score = 0
circle_width = 20
pipe_speed = 5
# If you change gravity and force here, remember to change it at line 341
gravity = 4
force = 5
mixer_playing = False
modified_game_variables = False
score_requirement = 3
color = None
valid_connection, cur = connect_to_database()

# Sets FPS and defines a color list (for the pipes)
FPS = 60
clock = pygame.time.Clock()
colorList = [red, green, yellow, white, black, blue]

# introMusic = pygame.mixer.Sound("introMusic.wav")
# Defines some essentials fonts, which is used later on in the program when displaying text
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)


def text_objects(text, color, size):
    global textsurface
    if size == "small":
        textsurface = smallfont.render(text, True, color)
    elif size == "medium":
        textsurface = medfont.render(text, True, color)
    elif size == "large":
        textsurface = largefont.render(text, True, color)
    return textsurface, textsurface.get_rect()


def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size="small"):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = ((buttonx + (buttonwidth / 2)), buttony + (buttonheight / 2))
    game_display.blit(text_surf, text_rect)


def message_to_screen_center(msg, color, y_displace=0, size="small"):
    # Renders centered text to the screen
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (display_width / 2), (display_height / 2) + y_displace
    game_display.blit(text_surf, text_rect)


def message_to_screen_costumpos(msg, xpos, ypos, color, fontsize=25):
    # Renders a customizable position textblock to the screen
    font = pygame.font.SysFont("calibri", fontsize)
    text = font.render(msg, 1, color)
    game_display.blit(text, (xpos, ypos))

def load_top_highscore():
    # Loads the current highscore holder's name as well as score, for renderInGameText to display
    if valid_connection:
        global cur
        cur.execute("SELECT * FROM highscores ORDER BY score DESC LIMIT 1")
        for row in cur.fetchall():
            global globalHighscoreName, globalHighscoreScore
            globalHighscoreName = row[1]
            globalHighscoreScore = row[2]
    else:
        pass


def render_info_to_screen(score):
    # Renders the ingame text, which includes current score, highest global highscore, gravity and force
    if valid_connection:
        # Displays the highscore
        text = smallfont.render("Highscore: " + str(globalHighscoreScore), True, black)
        game_display.blit(text, [0, 30])
        # Displays the current highscore holder's name
        text = smallfont.render("(" + str(globalHighscoreName) + ")", True, black)
        game_display.blit(text, [180, 30])
    if not valid_connection:
        message_to_screen_costumpos("No connection", 0, 30, black)
    # Score
    text = smallfont.render("Score: " + str(score), True, black)
    game_display.blit(text, [0, 0])
    # Gravity
    text = smallfont.render("Gravity: " + str(gravity), True, black)
    game_display.blit(text, [650, 0])
    # Force
    text = smallfont.render("Force: " + str(force), True, black)
    game_display.blit(text, [650, 30])


def obstacle_properties(recttype):
    # Generates different rectangular properties for the two pipes displayed at once
    global pipe_height, pipe_width, color, topPipe_height, pipe_height_2, toppipe_height_2
    pipe_width = 40
    color = red
    if recttype == 1:
        pipe_positions = random.choice(
            [(100, -400), (150, -350), (200, -300), (250, -250), (300, -200), (350, -150),
             (400, -100)])
        topPipe_height = pipe_positions[0]
        pipe_height = pipe_positions[1]
    elif recttype == 2:
        pipe_positions_2 = random.choice(
            [(100, -400), (150, -350), (200, -300), (250, -250), (300, -200), (350, -150),
             (400, -100)])
        toppipe_height_2 = pipe_positions_2[0]
        pipe_height_2 = pipe_positions_2[1]


def render_obstacle_1():
    # Draws one set of pipes to the screen
    # Top Rectangle
    pygame.draw.rect(game_display, color, [first_pipe_location, 0, pipe_width, topPipe_height])
    # Bottom Rectangle
    pygame.draw.rect(game_display, color, [first_pipe_location, display_height, pipe_width, pipe_height])


def render_obstacle_2():
    # Draws a second set of pipes to the screen
    # Top Rectangle
    pygame.draw.rect(game_display, color, [second_pipe_location, 0, pipe_width, toppipe_height_2])
    # Bottom Rectangle
    pygame.draw.rect(game_display, color, [second_pipe_location, display_height, pipe_width, pipe_height_2])


def move_player(x, y):
    # Function for controlling the players movement
    pygame.draw.circle(game_display, black, [x, y], circle_width)
    # Draw eyes
    pygame.draw.circle(game_display, white, [x - int(circle_width / 2), y - 10], 5)
    pygame.draw.circle(game_display, white, [x + int(circle_width / 2), y - 10], 5)
    pygame.draw.circle(game_display, red, [x - int(circle_width / 2), y - 10], 2)
    pygame.draw.circle(game_display, red, [x + int(circle_width / 2), y - 10], 2)
    # Mouth
    # pygame.draw.rect(game_display, blue, [x-10,y,20,5])


def write_score_to_database(score, name):
    # Writes score and name to the MySQL database.
    # This function is called whenever the user crashes and the outputScore is >= 3
    connect_to_database()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO highscores (username, score) VALUES ('" + str(name) + "'," + str(score) + ")")
    print("Successfully wrote the new highscore of", score, "to MySQL database")


def button(text, x, y, width, height, inactivecolor, activecolor, action=None):
    # Function "borrowed" from this tutorial
    # (https://www.youtube.com/watch?v=D69T-pfI6LY&list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq&index=46)
    cursor_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    global gravity, force, second_pipe_location, first_pipe_location
    if x + width > cursor_pos[0] > x and y + height > cursor_pos[1] > y:
        pygame.draw.rect(game_display, activecolor, (x, y, width, height))
        if click[0] == 1 and action is not None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "controls":
                controls_screen()
            if action == "play":
                first_pipe_location = 800
                second_pipe_location = 400
                main_screen()
            # If the user presses "Mute music" the mixerPlaying variable is set to False.
            # This means that the "Resume music"button will appear.
            # The music is also set on pause, and can be resumed.
            if action == "muteMusic":
                logging.info("LOG: Stopped music")
                global mixer_playing
                mixer_playing = False
                pygame.mixer.pause()
            # IF the user presses "Resume music" the mixerPlaying variable is set to True.
            # This means that the "Mute music"
            # button will appear. It seemed like earlier the sound just looped over and over, so watch out for that
            if action == "resumeMusic":
                mixer_playing = True
                # introMusic.play()
                logging.info("LOG: Resumed music")
            if action == "globalhighscores":
                highscore_screen()
                logging.info("LOG: Displayed global highscores")
            if action == "mainmenu":
                intro_screen()
            if action == "restart":
                main_screen()
            if action == "incrementGravity":
                gravity += 1
            if action == "decreaseGravity":
                gravity -= 1
            if action == "incrementforce":
                force += 1
            if action == "decreaseforce":
                force -= 1
            if action == "resetvariables":
                gravity = 5
                force = 5
            if action == "visitwebpage":
                webbrowser.open_new("http://www.amundsen.co")
    else:
        pygame.draw.rect(game_display, inactivecolor, (x, y, width, height))
    text_to_button(text, black, x, y, width, height)


def pause_screen():
    # A pause function, which freezes the game. Will be activated when the user press P
    paused = True
    message_to_screen_center("Paused", black, -100, size="large")
    message_to_screen_center("Press C to continue or Q to quit", black, 25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(5)


def highscore_screen():
    # introMusic.play(5)
    # Separate screen which shows the top 10 highscores from the database
    connect_to_database()
    controls_screen = True
    while controls_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            game_display.fill(white)
            if valid_connection:
                text_y_pos = 90
                # global highscoreName
                cur.execute("SELECT * FROM highscores ORDER BY score DESC LIMIT 10")
                for row in cur.fetchall():
                    global globalHighscore
                    globalHighscore = [row[0], row[1], row[2]]

                    # Loops trough determined how many rows there are
                    message_to_screen_costumpos("ID: " + str(globalHighscore[0]), 10, text_y_pos, red)
                    message_to_screen_costumpos("Username: " + str(globalHighscore[1]), 150, text_y_pos, red)
                    message_to_screen_costumpos("Score: " + str(globalHighscore[2]), 520, text_y_pos, red)
                    text_y_pos += 41

                    # Renders the headline as well as the black borders on the screen
                    message_to_screen_center("GLOBAL HIGHSCORES", green, -265, "medium")
                    # ID separator line
                    pygame.draw.rect(game_display, black, [135, 75, 5, 410])
                    # Headline separator line
                    pygame.draw.rect(game_display, black, [0, 75, 800, 5])
                    # Username and score separator line
                    pygame.draw.rect(game_display, black, [500, 75, 5, 410])
                    # Bottom line
                    pygame.draw.rect(game_display, black, [0, 485, 800, 5])
            if not valid_connection:
                message_to_screen_center("Can't connect to MySQL database", red, -100)
                message_to_screen_center("Make sure you have a valid internet connection", red, -65)

            button("Play", 0, 550, 266, 50, green, light_green, action="play")
            button("Main menu", 266, 550, 266, 50, yellow, light_yellow, action="mainmenu")
            button("Quit", 532, 550, 270, 50, red, light_red, action="quit")
            pygame.display.update()
            clock.tick(30)


def controls_screen():
    # Separate screen which allows the user to customize gameplay variables
    controls_screen = True
    while controls_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

            game_display.fill(white)
            message_to_screen_center("COSTUM GAMEPLAY", green, -265, "medium")

            global gravity
            message_to_screen_costumpos("Gravity", 20, 80, red, 100)
            message_to_screen_costumpos(str(gravity), 330, 80, red, 100)
            button("Increment", 450, 75, display_width - 450, 51, white, red, action="incrementGravity")
            button("Decrease", 450, 126, display_width - 450, 51, white, red, action="decreaseGravity")

            global force
            message_to_screen_costumpos("Force", 20, 190, red, 100)
            message_to_screen_costumpos(str(force), 330, 190, red, 100)
            button("Increase", 450, 177, display_width - 450, 51, white, red, action="incrementforce")
            button("Decrease", 450, 228, display_width - 450, 51, white, red, action="decreaseforce")

            button("Reset", 455, 279, display_width - 450, 51, white, red, action="resetvariables")

            if force < 1:
                force = 1
            if force > 99:
                force = 99
            if gravity < 1:
                gravity = 1
            if gravity > 99:
                gravity = 99

            if force != 5 or gravity != 3:
                message_to_screen_center("Changing the variables will not save the highscore to the database!", green,
                                         80)
                global modified_game_variables
                modified_game_variables = True

            # Headline separator
            pygame.draw.rect(game_display, black, [0, 75, 800, 5])
            # Gravity and force separator line (vertical)
            pygame.draw.rect(game_display, black, [320, 75, 5, 205])
            # Gravity and force separator line (horizontal)
            pygame.draw.rect(game_display, black, [0, 177, display_width, 5])
            pygame.draw.rect(game_display, black, [0, 279, display_width, 5])
            # pygame.draw.rect(gameDisplay, black, [0, 381, display_width, 5])
            # Number separator line
            pygame.draw.rect(game_display, black, [450, 75, 5, 205])
            # Bottom line
            # pygame.draw.rect(gameDisplay, black, [0,485,800,5])

            button("Play", 0, 550, 266, 50, green, light_green, action="play")
            button("Main menu", 266, 550, 266, 50, yellow, light_yellow, action="mainmenu")
            button("Quit", 532, 550, 270, 50, red, light_red, action="quit")

            pygame.display.update()
            clock.tick(30)


def intro_screen():
    intro = True
    # introMusic.play(5)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            game_display.fill(white)
            message_to_screen_center("Welcome to Flappy Bird", green, -100, "medium")
            message_to_screen_center("Your mission is to not hit the pipes while flapping", black, -30)
            message_to_screen_center("If you cross between the pipes you'll score", black, 10)
            message_to_screen_center("But if you hit the pipes you'll die", black, 50)

            button("Play", 0, 550, 266, 50, green, light_green, action="play")
            button("Controls", 266, 550, 266, 50, yellow, light_yellow, action="controls")
            button("Quit", 532, 550, 270, 50, red, light_red, action="quit")
            button("Global highscores", 0, 0, 220, 50, red, light_red, action="globalhighscores")
            button("Visit my webpage", 0, 50, 220, 50, green, light_green, action="visitwebpage")

            # If the mixer IS NOT playing a "Resume music" button is being displayed
            if not mixer_playing:
                button("Resume music", display_height - 150, 0, 200, 50, red, light_red, action="resumeMusic")
            # If the mixer IS PLAYING a "Mute music button is being displayed
            if mixer_playing:
                button("Mute music", display_width - 150, 0, 150, 50, green, light_green, action="muteMusic")

            pygame.display.update()
            clock.tick(30)


def main_screen():
    global final_score, outputScore, first_pipe_location, toppipe_height_2
    global pipe_height_2, second_pipe_location, globalHighscoreScore

    first_pipe_location = 800
    second_pipe_location = 400

    direction = "right"
    x_playerpos = 30
    y_playerpos = int(display_height / 2)

    game_exit = False
    game_over = False

    obstacle_properties(1)
    render_obstacle_1()

    # This block makes sure that the first rect does not render, so the player has some time to prepare
    toppipe_height_2 = 0
    pipe_height_2 = 0
    render_obstacle_2()
    not_crossed = True

    # Loads the current highscore from the database, and feeds it to the renderInGameText function
    load_top_highscore()
    logging.info("LOG: Rect Generated")

    while not game_exit:
        if game_over:
            if valid_connection:
                if not modified_game_variables and outputScore >= score_requirement:
                    global highscoreName
                    highscoreName = g.enterbox("Please enter your name for highscores purposes")
                    write_score_to_database(outputScore, highscoreName)
                elif modified_game_variables:
                    print("Modified game variables")
            else:
                print("Can't connect to the database, and therefore your score will not be logged!")

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    pygame.quit()
                    quit()

            message_to_screen_center("Game over!", black, 0, "large")
            pygame.draw.rect(game_display, black, [0, 545, 800, 5])
            button("Restart", 0, 550, 266, 50, green, light_green, action="restart")
            button("Main menu", 266, 550, 266, 50, yellow, light_yellow, action="mainmenu")
            button("Quit", 532, 550, 270, 50, red, light_red, action="quit")
            pygame.display.update()

            final_score = 0
            outputScore = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_UP:
                    direction = "up"
                if event.key == pygame.K_SPACE:
                    direction = "up"
                if event.key == pygame.K_p:
                    pause_screen()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    direction = "down"
                if event.key == pygame.K_SPACE:
                    direction = "down"

        if direction == "up":
            y_playerpos -= force
        if direction == "down":
            y_playerpos += gravity

        first_pipe_location -= pipe_speed
        second_pipe_location -= pipe_speed

        # Redraws the rect based on lead_x, lead_x_2 and y changes
        game_display.blit(background, [0, 0])
        render_obstacle_1()
        render_obstacle_2()
        move_player(x_playerpos, y_playerpos)

        # Displays the highscore (and name) and current score
        outputScore = int(final_score / 3)
        render_info_to_screen(outputScore)

        # Hitdetection for pipes
        if first_pipe_location >= display_width or first_pipe_location < 0:
            # Generates new attributes for the first set of pipes, and then renders it with obstacle_properties(1)
            obstacle_properties(1)
            render_obstacle_1()
            first_pipe_location = display_width
        if second_pipe_location >= display_width or second_pipe_location < 0:
            # Generates new attributes for the second set of pipes, and then renders it with obstacle_properties(2)
            obstacle_properties(2)
            render_obstacle_2()
            second_pipe_location = display_width

        # Hit-detection for circle (Currently rectangular collision)
        # Ground collision
        if y_playerpos + circle_width >= display_height or y_playerpos - circle_width <= 0:
            game_over = True
        # TOP COLLIDE
        if x_playerpos + circle_width > first_pipe_location and y_playerpos - circle_width <= topPipe_height or x_playerpos + circle_width > second_pipe_location and y_playerpos - circle_width <= toppipe_height_2:
            game_over = True
        # BOT COLLIDE
        if x_playerpos + circle_width > first_pipe_location and y_playerpos + circle_width >= display_height + pipe_height or x_playerpos + circle_width > second_pipe_location and y_playerpos + circle_width >= display_height + pipe_height_2:
            game_over = True
        # Score incrementation
        if x_playerpos + circle_width > first_pipe_location > x_playerpos or x_playerpos + circle_width > second_pipe_location > x_playerpos:
            if not_crossed:
                pass
            else:
                final_score += 1
            not_crossed = False

        # Checks if pipes exceeds over screen borders (should't really happen in theory)
        if pipe_height > display_height or pipe_width > display_width or topPipe_height > display_height:
            logging.error("Rect crossed screen borders - fix it")

        clock.tick(FPS)
        pygame.display.update()


intro_screen()
