# Tetris Game developed in Python
# Le Baron 2019
# ------------------------------------

# --------- Import Section ------------

import pygame
import random
import csv
from datetime import datetime

# --------- End of Section ------------

# --------- Initialization ------------
# Define the tetrominoes to be used and their corresponding positions once rotated
Shapes = {
    "T": {
          1: [[0, 1, 0],
              [1, 1, 1]],
          2: [[1, 0],
              [1, 1],
              [1, 0]],
          3: [[1, 1, 1],
              [0, 1, 0]],
          4: [[0, 1],
              [1, 1],
              [0, 1]]
           },
    "O": {
          1: [[1, 1],
              [1, 1]],
          2: [[1, 1],
              [1, 1]],
          3: [[1, 1],
              [1, 1]],
          4: [[1, 1],
              [1, 1]]
           },
    "J": {
          1: [[0, 1],
              [0, 1],
              [1, 1]],
          2: [[1, 0, 0],
              [1, 1, 1]],
          3: [[1, 1],
              [1, 0],
              [1, 0]],
          4: [[1, 1, 1],
              [0, 0, 1]]
           },
    "L": {
          1: [[1, 0],
              [1, 0],
              [1, 1]],
          2: [[1, 1, 1],
              [1, 0, 0]],
          3: [[1, 1],
              [0, 1],
              [0, 1]],
          4: [[0, 0, 1],
              [1, 1, 1]]
           },
    "S": {
          1: [[1, 0],
              [1, 1],
              [0, 1]],
          2: [[0, 1, 1],
              [1, 1, 0]],
          3: [[1, 0],
              [1, 1],
              [0, 1]],
          4: [[0, 1, 1],
              [1, 1, 0]]
           },
    "5": {
          1: [[0, 1],
              [1, 1],
              [1, 0]],
          2: [[1, 1, 0],
              [0, 1, 1]],
          3: [[0, 1],
              [1, 1],
              [1, 0]],
          4: [[1, 1, 0],
              [0, 1, 1]]
           },
    "I": {
          1: [[1],
              [1],
              [1],
              [1]],
          2: [[1, 1, 1, 1]],
          3: [[1],
              [1],
              [1],
              [1]],
          4: [[1, 1, 1, 1]]
           }
}
# Dictionary of colors to be used on the game
Colors = {
    "Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Red": (255, 0, 0),
    "Blue": (0, 0, 255),
    "Lime": (0, 255, 0),
    "Green": (0, 128, 0),
    "Yellow": (255, 255, 0),
    "Purple": (128, 0, 128),
    "Pink": (255, 20, 147),
    "Gray": (125, 125, 125)
}
# List of colors to be used for tetrominoes
choice_color = [key for key in list(Colors)[2:-1]]
# height and width of the screen
wn_height, wn_width = 400, 300
# Game variables
lt, rt, tp, bt, wt = 100, 200, 100, 350, 2  # lt:left  - rt:right  - tp:top - bt:bottom - wt:width - Game borders
piece_size = 10  # Block size of each tetromino
exit_game = False
pause_game = False
game_board = []  # to hold each cell of the screen
full_line = [1 for i in range((rt - lt) // 10)]
empty_line = [0 for i in range((rt - lt) // 10)]
score = 0  # to hold the score of the game
Highscores = {}

# --------- End of Section ------------

# --------- Class Section -------------
# Create a shape class
class shape(object):
    def __init__(self, form, x_cor, y_cor, z_width, color):  # initialization method setting up all attributes
        self.form = form
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.z_width = z_width
        self.color = color

    def move_shape(self, axis, distance):  # method to move the shape based on the axis and distance provided
        if axis == "x":
            self.x_cor += distance

        if axis == "y":
            self.y_cor += distance

    def draw_shape(self):  # method to draw the shape on the screen surface
        temp_x = self.x_cor
        temp_y = self.y_cor
        for i, row in enumerate(self.form):
            for j, col in enumerate(row):
                if self.form[i][j] == 0:
                    # draw empty rectangle piece of the shape with the -1 parameter meaning no border
                    pygame.draw.rect(game_window, Colors["Black"], [temp_x, temp_y, self.z_width, self.z_width], -1)
                else:
                    pygame.draw.rect(game_window, self.color, [temp_x, temp_y, self.z_width, self.z_width])
                temp_x += self.z_width
            temp_y += self.z_width
            temp_x = self.x_cor


# --------- End of Section ------------

# -------- Functions Section ----------

def write_high_score():
    if score > int(high_scores["1"]["score"]):  # only save highest score and position 1 is the highest recorded score
        now = datetime.now()
        formatedDay = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
        with open("scores.csv", "w") as my_file:
            csv_writer = csv.writer(my_file)
            line = ["1", str(score), Player_name, formatedDay]
            csv_writer.writerow(line)

            for i, data in high_scores.items():
                csv_writer.writerow([int(i) + 1, data["score"], data["name"], data["date"]])


def rotate_shape(shape, x):  # Function to rotate the shape and checking the x position for it not to go outside borders
    global Shapes
    for i, default_shape_dict in Shapes.items():
        for j, default_shape in default_shape_dict.items():
            if shape == default_shape:
                if x + len(Shapes[i][j] * piece_size) <= rt:  # would shape stay within outside borders ?
                    return Shapes[i][(j % 4) + 1]  # pick the next shape position of the same form
                else:
                    return shape  # do not rotate if shape is going outside the borders


def remove_full_line():  # check for a line that is totally filled and clear it, update score at the same time
    global game_board
    global score
    bonus = 0
    temp = list(map(list, zip(*game_board)))  # Transpose the board matrix
    for index, each_row in enumerate(temp):
        if each_row == full_line:
            temp.pop(index)   # remove line
            temp.append(empty_line)  # replace the line with a empty one
            score += 10 + (bonus * 10)   # update score giving a bonus for multiple lines cleared
            bonus += 1
    game_board = list(map(list, zip(*temp)))  # restore the board position


def game_over():  # check if the top line has been reached to end the game
    global game_board
    temp = list(map(list, zip(*game_board)))
    if 1 in temp[len(temp) - 1]:  # if a shape has reached a cell on the top level
        write_high_score()
        return True
    else:
        return False


# Check for any collision between the shape and any filled position on the board
def is_collision(shape, pos_x, pos_y, wd_z):
    global game_board
    for i in range(len(shape[0])):
        for j in range(len(shape) - 1, -1, -1):
            if shape[j][i] == 1:
                if 1 == game_board[(pos_x - lt + (i * wd_z)) // wd_z][(bt - pos_y - (j * wd_z) - wd_z) // wd_z]:
                    return True
    return False


# if a shape has touched the bottom line on any existing position on the board, update the board with its position
def draw_shape_on_board(shape, pos_x, pos_y, wd_z):
    global game_board
    for i, rows in enumerate(shape):
        for j, cols in enumerate(rows):
            if shape[i][j] == 1:  # Only draw positions that are not empty
                if pos_y < bt - (len(shape) * wd_z):
                    game_board[(pos_x - lt + (wd_z * j)) // wd_z][(bt - pos_y - (wd_z * i)) // wd_z] = 1
                else:
                    game_board[(pos_x - lt + (wd_z * j)) // wd_z][(bt - pos_y - (wd_z * i) - wd_z) // wd_z] = 1


def draw_game_grid():  # draw game borders and grid
    for i in range(1, (rt - lt) // 10):
        pygame.draw.line(game_window, Colors["Gray"], (lt + (i * piece_size), tp), (lt + (i * piece_size), bt))
    for i in range(1, (bt - tp) // 10):
        pygame.draw.line(game_window, Colors["Gray"], (lt, tp + (i * piece_size)), (rt, tp + (i * piece_size)))
    pygame.draw.line(game_window, Colors["White"], (lt, tp), (lt, bt), wt)
    pygame.draw.line(game_window, Colors["White"], (rt, tp), (rt, bt), wt)
    pygame.draw.line(game_window, Colors["White"], (lt, tp), (rt, tp), wt)
    pygame.draw.line(game_window, Colors["White"], (lt, bt), (rt, bt), wt)


def write_text(msg, text_size, pos_x, pos_y, color):  # Function to ease the display of text on screen surface
    font = pygame.font.SysFont("monospace", text_size, bold=True)
    to_display = font.render(msg, 1, color)
    game_window.blit(to_display, (pos_x, pos_y))


def draw_game_board():  # draw board data on screen surface
    for i, rows in enumerate(game_board):
        for j, cols in enumerate(rows):
            if game_board[i][j] == 1:
                my_color = Colors["White"]
            else:
                my_color = Colors["Black"]
            pygame.draw.rect(game_window, my_color, [lt + (i * piece_size), bt - (j * piece_size) - piece_size, piece_size, piece_size])


def init_game():  # initial value of the game, useful for game relaunch after game over
    global game_board
    global score
    global high_scores
    game_board = [[0 for j in range((bt - tp) // 10)] for i in range((rt - lt) // 10)]
    score = 0
    # Open the high score file for reading
    with open("scores.csv", "r") as my_file:
        reader = csv.reader(my_file)
        high_scores = {}
        for row in reader:
            high_scores[row[0]] = {"score": row[1], "name": row[2], "date": row[3]}


# --------- End of Section ------------

# ---------- Main Section -------------
# get player name, useful for storing high scores
Player_name = input("Please enter your name and press enter:") or "Player"
# Initialize shape object
m_shape = shape(Shapes[random.choice(["T", "J", "S", "L", "5", "O", "I"])][random.randint(1, 4)],
                random.randint((lt + piece_size) // piece_size, (rt - (4 * piece_size)) // piece_size) * piece_size,
                tp,
                piece_size,
                Colors[random.choice(choice_color)])
# Initialize game screen and caption
pygame.init()
pygame.key.set_repeat(150,30)
game_window = pygame.display.set_mode((wn_width, wn_height))
pygame.display.set_caption("Tetris - Mutanga")
game_window.fill(Colors["Black"])
pygame.display.flip()
init_game()  # initialize game

while not exit_game:  # while game still on
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # when close window button is pressed
            exit_game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and m_shape.x_cor > lt and not pause_game and not game_over():
                m_shape.move_shape("x", piece_size * -1)
            if event.key == pygame.K_RIGHT and m_shape.x_cor < (rt - (piece_size * len(m_shape.form[0]))) \
                    and not pause_game and not game_over():
                m_shape.move_shape("x", piece_size)
            if event.key == pygame.K_UP and not pause_game and not game_over():
                m_shape.form = rotate_shape(m_shape.form, m_shape.x_cor)
            if event.key == pygame.K_DOWN and not pause_game and not game_over():
                m_shape.move_shape("y", 1)
            if event.key == pygame.K_ESCAPE and game_over():  # use escape key to restart game after game over
                init_game()
            if event.key == pygame.K_SPACE and not game_over():  # use space key to pause the game
                pause_game = not pause_game

    if not pause_game and not game_over():  # if game not paused and not over drop the shape
        if m_shape.y_cor < (bt - (piece_size * len(m_shape.form))):  # if shape has not reached the bottom border
            m_shape.move_shape("y", 1)  # drop shape by 1px
            if is_collision(m_shape.form, m_shape.x_cor, m_shape.y_cor, m_shape.z_width):
                # if there was a collision then draw shape on board and generate new one
                draw_shape_on_board(m_shape.form, m_shape.x_cor, m_shape.y_cor, m_shape.z_width)
                m_shape.y_cor = tp
                m_shape.x_cor = random.randint((lt + piece_size) // piece_size, (rt - (4 * piece_size)) // piece_size) * piece_size
                m_shape.form = Shapes[random.choice(["T", "J", "S", "L", "5", "O", "I"])][random.randint(1, 4)]
                m_shape.color = Colors[random.choice(choice_color)]
        else:  # if shape has reach bottom then draw shape on board and generate new one
            draw_shape_on_board(m_shape.form, m_shape.x_cor, m_shape.y_cor, m_shape.z_width)
            m_shape.y_cor = tp
            m_shape.x_cor = random.randint((lt + piece_size) // piece_size, (rt - (4 * piece_size)) // piece_size) * piece_size
            m_shape.form = Shapes[random.choice(["T", "J", "S", "L", "5", "O", "I"])][random.randint(1, 4)]
            m_shape.color = Colors[random.choice(choice_color)]

    remove_full_line()  # check and remove fully filled line
    game_window.fill(Colors["Black"])  # fill the screen with black background as starting point
    draw_game_board()  # draw board with current status
    m_shape.draw_shape()  # draw moving shape
    draw_game_grid()   # draw game boarders and grid

    write_text("Welcome " + Player_name, 12, 10, 10, Colors["White"])  # write player name on top
    write_text("Your score:" + str(score), 12, 10, 25, Colors["White"])  # write current score
    write_text("High Score:" + str(high_scores["1"]["score"]) + " by " + high_scores["1"]["name"],
               12, 10, 40, Colors["White"])    # from the file take the current highest score and write on screen
    if pause_game and not game_over():
        write_text("PAUSE", 50, 75, 200, Colors["Red"])  # if game paused display it on screen surface
    if game_over():
        write_text("Game Over", 50, 15, 200, Colors["Red"])  # if game over display it on screen surface

    pygame.display.update()  # screen refresh
    pygame.time.delay(20)  # speed of refresh delayed by 20ms

# if game exited then quit application
pygame.quit()
quit()
# --------- End of Section ------------
