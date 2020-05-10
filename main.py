import pygame, random, sys
from pygame.locals import *

fps = 15
win_wt = 640
win_ht = 480
cell_sz = 20
assert win_wt%cell_sz == 0, "qwerty"
assert win_ht%cell_sz == 0, "qwerty"

cell_wt = int(win_wt/cell_sz)
cell_ht = int(win_ht/cell_sz)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
darkgreen = (0, 155, 0)
darkgrey = (40, 40, 40)
bgcolor = (30, 30, 30)

up = "up"
down = "down"
right = "right"
left = "left"

head = 0

def main():
    global fps_clock, display_surf, basic_font

    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((win_wt, win_ht))
    basic_font = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption("WORMY")
    pygame.display.set_icon(pygame.image.load("data/icon.png"))

    show_start_screen()
    
    while True:
        run_game()
        show_game_over_screen()

def run_game():
    eat = pygame.mixer.Sound("data/eat.wav")
    start_x = random.randint(5, cell_wt - 6)
    start_y = random.randint(5, cell_ht - 6)
    worm_cords = [{"x": start_x,     "y": start_y},
                  {"x": start_x - 1, "y": start_y},
                  {"x": start_x - 2, "y": start_y}]
    direction = right

    apple = get_random_location()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != right:
                    direction = left
                elif (event.key == K_RIGHT or event.key == K_d) and direction != left:
                    direction = right
                elif (event.key == K_UP or event.key == K_w) and direction != down:
                    direction = up
                elif (event.key == K_DOWN or event.key == K_s) and direction != up:
                    direction = down
                elif (event.key == K_ESCAPE):
                    terminate()

        if (worm_cords[head]["x"] == -1) or (worm_cords[head]["x"] == cell_wt) or (worm_cords[head]["y"] == -1) or (worm_cords[head]["y"] == cell_ht):
           return

        for worm_body in worm_cords[1:]:
            if (worm_body["x"] == worm_cords[head]["x"]) and (worm_body["y"] == worm_cords[head]["y"]):
                return

        if (worm_cords[head]["x"] == apple["x"]) and (worm_cords[head]["y"] == apple["y"]):
            eat.play()
            apple = get_random_location()

        else:
            del worm_cords[-1]

        if direction == up:
            new_head = {"x": worm_cords[head]["x"], "y": worm_cords[head]["y"] - 1}
        elif direction == down:
            new_head = {"x": worm_cords[head]["x"], "y": worm_cords[head]["y"] + 1}
        elif direction == left:
            new_head = {"x": worm_cords[head]["x"] - 1, "y": worm_cords[head]["y"]}
        elif direction == right:
            new_head = {"x": worm_cords[head]["x"] + 1, "y": worm_cords[head]["y"]}
        worm_cords.insert(0, new_head)

        display_surf.fill(bgcolor)
        draw_grid()
        draw_worm(worm_cords)
        draw_apple(apple)
        draw_score(len(worm_cords) - 3)
        pygame.display.update()
        fps_clock.tick(fps)

def draw_press_msg():
    #item = basic_font.render("press any key to start", True, (200, 200, 200))
    item = basic_font.render("press 1 for easy, 2 for medium and 3 if you want a challenge", True, (200, 200, 200))
    item_rect = item.get_rect()
    item_rect.topleft = (win_wt - 580, win_ht - 20)
    display_surf.blit(item, item_rect)

def check_for_key_press():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return key_up_events[0].key

def show_start_screen():
    global fps
    title_font = pygame.font.Font("freesansbold.ttf", 100)
    title_surf_1 = title_font.render("WORMY", True, darkgreen, black)

    degrees_1 = 0
    degrees_2 = 0

    while True:
        display_surf.fill(bgcolor)
        rotated_surf_1 = pygame.transform.rotate(title_surf_1, degrees_1)
        rotated_rect_1 = rotated_surf_1.get_rect()
        rotated_rect_1.center = (int(win_wt / 2), int(win_ht / 2))
        display_surf.blit(rotated_surf_1, rotated_rect_1)

        draw_press_msg()

        if check_for_key_press():
            pygame.event.get()
            return

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_1:
                    fps = 10
                    return
                if event.key == pygame.K_2:
                    fps = 20
                    return
                if event.key == pygame.K_3:
                    fps = 25
                    return

        pygame.display.update()
        fps_clock.tick(fps)
        degrees_1 += 3

def terminate():
    pygame.quit()
    sys.exit()

def get_random_location():
    return {"x": random.randint(0, cell_wt - 1), "y": random.randint(0, cell_ht - 1)}

def show_game_over_screen():
    display_surf.fill(bgcolor)
    draw_grid()
    game_over_font = pygame.font.Font('freesansbold.ttf', 150)
    game_surf = game_over_font.render("GAME", True, white)
    over_surf = game_over_font.render("OVER", True, white)
    game_rect = game_surf.get_rect()
    over_rect = over_surf.get_rect()
    game_rect.midtop = (int(win_wt/2), 100)
    over_rect.midtop = (int(win_wt/2), int(game_rect.height + 10 + 80))

    display_surf.blit(game_surf, game_rect)
    display_surf.blit(over_surf, over_rect)
    item = basic_font.render("press any key to start again", True, (200, 200, 200))
    item_rect = item.get_rect()
    item_rect.topleft = (win_wt - 420, win_ht - 40)
    display_surf.blit(item, item_rect)
    pygame.display.update()

    pygame.time.wait(500)
    check_for_key_press()

    while True:
        if check_for_key_press():
            pygame.event.get()
            return

def draw_score(score):
    score_surf = basic_font.render("Score: %s" % (score), True, white)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (win_wt - 120, 10)
    display_surf.blit(score_surf, score_rect)

def draw_worm(worm_cords):
    snake = pygame.image.load("data/snake.png")
    for coord in worm_cords:
        x = coord["x"] * cell_sz
        y = coord["y"] * cell_sz
        display_surf.blit(snake, (x, y))
        """
        worm_seg_rect = pygame.Rect(x, y, cell_sz, cell_sz)
        pygame.draw.rect(display_surf, darkgreen, worm_seg_rect)
        worm_inner = pygame.Rect(x + 4, y + 4, cell_sz - 8, cell_sz - 8)
        pygame.draw.rect(display_surf, green, worm_inner)
        """

def draw_apple(coord):
    x = coord["x"] * cell_sz
    y = coord["y"] * cell_sz
    apple = pygame.image.load("data/apple.png")
    display_surf.blit(apple, (x, y))

def draw_grid():
    for x in range(0, win_wt, cell_sz):
        pygame.draw.line(display_surf, darkgrey, (x, 0), (x, win_ht))
    for y in range(0, win_ht, cell_sz):
        pygame.draw.line(display_surf, darkgrey, (0, y), (win_wt, y))


if __name__ =="__main__":
    main()


"""
    open portals
    make bricks
    add super points
    add 50 different levels
    hell why not make it skyrim
    """