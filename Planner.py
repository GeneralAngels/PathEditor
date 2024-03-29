
import numpy as np
import math
import Path_Editor as path_editor


def generate_path(points: list) -> list:
    """A function to generate vectors from a list of coordinates."""

    X = 0
    Y = 1
    ANGLE = 2
    SPEED = 2
    
    WIDTH = 23
    HEIGHT = 23

    # [time, x', y', omega, x, y, angle]

    path = []
    t0 = 0

    for index, point in enumerate(points[:-1]):
        
        curr_point = point
        next_point = points[index + 1]

        d = math.sqrt(((next_point[X] * WIDTH) - (curr_point[X] * WIDTH)) ** 2 + 
                      ((next_point[Y] * HEIGHT) - (curr_point[Y] * HEIGHT)) ** 2)

        dT = d / SPEED
        
        x = curr_point[X] * WIDTH
        y = curr_point[Y] * HEIGHT
        angle = curr_point[ANGLE]

        iterations = int(dT / 0.01)
        for t in range(iterations + 1):

            t = t0 + t * 0.01
            Va = (next_point[ANGLE] - curr_point[ANGLE]) / dT
            
            Vx = ((next_point[X] * WIDTH - curr_point[X] * WIDTH) / dT) 
            Vy = ((next_point[Y] * HEIGHT - curr_point[Y] * HEIGHT) / dT) 

            path.append([t, Vx, Vy, Va, x, y, angle])

            x += Vx * 0.01
            y += Vy * 0.01
            angle += Va * 0.01


        t0 += int(dT / 0.01) * 0.01
    
    with open ("Paths/Path.txt", "w") as file:
        s_path = str(path)
        s_path = s_path.replace("[", "")
        s_path = s_path.replace("],", "\n").replace(" ", "").replace("]", "")
        file.write(s_path)




def convert_points(points, start_pos=(0,0)):
 
    path = []
    start_pos = (start_pos[0], path_editor.DRAWING_HEIGHT - start_pos[1])

    for point in points:
        converted_pos = (point.pos[0], path_editor.DRAWING_HEIGHT - point.pos[1])
        point_pos = ((start_pos[0] -  converted_pos[0]) / 900, (start_pos[1] - converted_pos[1]) / 800)
        path.append([point_pos[0], point_pos[1], point.heading.angle])

    return path