import pygame
from Sprites import *
import pygame_gui
import os
from Planner import *


EDITOR_WIDTH = 900
EDITOR_HEIGHT = 900

DRAWING_WIDTH = 900
DRAWING_HEIGHT = 800


def initiate_ui():

    PLANNER_DIR = os.path.realpath(os.path.dirname(__file__))
    manager = pygame_gui.UIManager((900, 900), os.path.join(
        PLANNER_DIR, "assets", "themes", "editor-theme.json"))

    global panel
    panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect(0, 0, 900, 100),
        starting_layer_height=0,
        manager=manager)

    global title
    title = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(10, 18, -1, -1),
        text="Path Editor",
        manager=manager,
        container=panel)

    global clear_button
    clear_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(325, 18, 100, 50),
        text="CLEAR",
        manager=manager,
        container=panel,
        object_id="CLEAR_BUTTON")

    global pos_x_text
    pos_x_text = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(440, 18, -1, -1),
        text="X: ",
        manager=manager,
        container=panel)

    global pos_x_entry
    pos_x_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(485, 18, 75, 50),
        manager=manager,
        container=panel,
        object_id="#POS_X_TEXT_ENTRY")

    pos_x_entry.set_allowed_characters('numbers')
    pos_x_entry.set_text_length_limit(3)

    global pos_y_text
    pos_y_text = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(570, 18, -1, -1),
        text="Y: ",
        manager=manager,
        container=panel)

    global pos_y_entry
    pos_y_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(620, 18, 75, 50),
        manager=manager,
        container=panel,
        object_id="#POS_Y_TEXT_ENTRY")

    global angle_text
    angle_text = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(705, 18, -1, -1),
        text="D: ",
        manager=manager,
        container=panel)

    global angle_entry
    angle_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(750, 18, 100, 50),
        manager=manager,
        container=panel,
        object_id="#POS_Y_TEXT_ENTRY")

    pos_y_entry.set_allowed_characters('numbers')
    pos_y_entry.set_text_length_limit(3)

    return manager


def initiate_screen():
    pygame.init()
    flags = pygame.RESIZABLE | pygame.SCALED 
    display = pygame.display.Info()
    screen = pygame.display.set_mode((EDITOR_WIDTH, EDITOR_HEIGHT), flags)
    screen.fill("0xA4A4A4")
    pygame.display.set_caption("Path Editor")


    manager = initiate_ui()

    return screen, manager


def add_point(pos):

    Y = 1
    X = 0

    global last_mouse_pos, start_pos

    if (100 < pos[Y] < 900 and 0 < pos[X] < 900 and pygame.mouse.get_pos() != last_mouse_pos):

        points.append(Point(pos[X], pos[Y] - 100))
        last_mouse_pos = pos

        if (len(points) == 1): return

        last_point_angle = points[-2].heading.angle
        points[-1].heading.update_angle(last_point_angle)
        

def draw_points(screen, points):

    global start_pos, end_pos

    screen.fill("0xA4A4A4")
    for index, point in enumerate(points):

        point.draw(screen)
        if (index > 0):
            pos = point.get_abs_pos()
            last_pos = (points[index - 1].get_abs_pos())

            pygame.draw.line(screen, (0, 0, 0), last_pos, pos, 3)

    if selected_point:
        pygame.draw.circle(screen, (255, 0, 0),
                           selected_point.get_abs_pos(), 3)
        
        selected_point.heading.draw(screen)

    for point in special_points:
        point.draw(screen)
        point.heading.draw(screen)

    if start_pos: pygame.draw.circle(screen, (0, 255, 0), (start_pos[0], start_pos[1] + 100) , 3)
    if end_pos: pygame.draw.circle(screen, (255, 0, 0), (end_pos[0], end_pos[1] + 100), 3)


def update_point(change):

    # While the user is holding the left mouse button and the mouse is in the edit zone continue updating the point.
    while (pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[1] > 100):
        
        mouse_pos = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 100 # Get the mouse position relative to the edit zone.

        if change == "POINT":
            selected_point.update(mouse_pos[0], mouse_pos[1])

        if change == "HEADING":
            selected_point.heading.update(selected_point.pos, mouse_pos) 

        process_events()
        update_ui()
        draw_points(screen, points)
        manager.draw_ui(screen)

        pygame.display.update()
        manager.update(60)
        clock.tick(240)


def modify_point(selected_point: Point):

    global manager

    mouse_pos = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 100 # Get the mouse position relative to the edit zone.
    if selected_point.rect.collidepoint(mouse_pos):
        update_point("POINT")

    elif selected_point.heading.rect.collidepoint(mouse_pos):
        init_angle = selected_point.heading.angle # Used to later check if the user had changed the angle.
        update_point("HEADING")

        if (init_angle != selected_point.heading.angle):
            point_index = points.index(selected_point)
            for index, point in enumerate(points[point_index + 1:]):
                if (int(point.heading.angle) == int(init_angle)):
                    point.heading.update_angle(selected_point.heading.angle) 

                else: break

            special_points.append(selected_point)
            

def update_ui():

    global selected_point
    if (selected_point): # if a point is selected
        pos_x_entry.show() # show the text entry boxes
        pos_y_entry.show()
        pos_x_text.show()
        pos_y_text.show()
        angle_entry.show()
        angle_text.show()

        if (pygame.mouse.get_pos()[1] > 100):
            pos_x_entry.set_text(str(selected_point.pos[0])) # Update the text entries with the selected point's position.
            pos_y_entry.set_text(str(800 - selected_point.pos[1]))
            angle_entry.set_text(str(int(selected_point.heading.angle)))
        
        else:
            init_angle = selected_point.heading.angle # Used to later check if the user had changed the angle.

            pos_x = int(pos_x_entry.get_text() if pos_x_entry.get_text() != "" else 0)
            pos_y = DRAWING_HEIGHT - int(pos_y_entry.get_text() if pos_y_entry.get_text() != "" else 0)
            angle = int(angle_entry.get_text() if angle_entry.get_text().replace("-", "") != "" else 0)

            selected_point.update(pos_x if pos_x < 900 else 900, 
                                  pos_y if pos_y < 800 else 800)

            selected_point.heading.update_angle(angle)

            if (init_angle != selected_point.heading.angle):
                point_index = points.index(selected_point)
                for index, point in enumerate(points[point_index + 1:]):
                    if (int(point.heading.angle) == int(init_angle)):
                        point.heading.update_angle(selected_point.heading.angle) 

                    else: break

                special_points.append(selected_point)

    else:
        pos_x_entry.hide()
        pos_y_entry.hide()
        pos_x_text.hide()
        pos_y_text.hide()
        angle_entry.hide()
        angle_text.hide()


def process_events():

    global selected_point, points, manager, mode, special_points, start_pos, end_pos, start_pos, end_pos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                mode = "cursor" if mode == "edit" else "edit"
                print("[INFO] MODE CHANGED TO: " + mode)
                selected_point = None

            if event.key == pygame.K_s:
                print("[INFO] SAVING PATH")
                generate_path(convert_points(points, start_pos))
                

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == clear_button:
                print("[INFO] POINTS CLEARED")
                selected_point = None
                points = []
                special_points = []
                start_pos = None
                end_pos = None

        manager.process_events(event)

    if (len(points) > 0):
        if start_pos != points[0].pos: # If the start position has changed, update the start position.
            start_pos = points[0].pos

        if end_pos != points[-1].pos and len(points) > 1:
            end_pos = points[-1].pos


def main():

    global points, last_mouse_pos, selected_point, manager, clock, screen, mode, special_points, start_pos, end_pos

    screen, manager = initiate_screen()
    last_mouse_pos = (0, 0), (1, 1)
    clock = pygame.time.Clock()
    running = True
    points = []
    mode = "edit"
    selected_point = None
    special_points = []
    start_pos = (0, 0)
    end_pos = (0, 0)

    while running:

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_ESCAPE]:
            running = False

        if pygame.mouse.get_pressed()[0] and mode == "edit":
            add_point(pygame.mouse.get_pos())

        elif pygame.mouse.get_pressed()[0] and mode == "cursor":
            for point in points:
                mouse_pos = (pygame.mouse.get_pos()[0], 
                            pygame.mouse.get_pos()[1] - 100)

                if point.rect.collidepoint(mouse_pos) and not point == selected_point:
                    selected_point = point
                    print("[INFO] Selected point: ", point.pos)
                    break

            if selected_point:
                modify_point(selected_point)

        
        process_events()

        update_ui()
        draw_points(screen, points)
        manager.draw_ui(screen)
        pygame.display.update()
        manager.update(60)
        clock.tick(240)

    pygame.quit()


if __name__ == "__main__":
    main()
