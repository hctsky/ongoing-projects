import pygame
import random
import math
from vector2d import Vector2D
from vehicle import Vehicle
from vehicle import TargetCircle
from steering import Behaviour
from steering import LineSegment



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



c_red = (255, 0, 0)
c_green = (0, 255, 0)
c_blue = (0, 0, 255)
c_yellow = (255, 255, 0)
c_gray = (100, 100, 100)
c_darkblue = (0, 0, 150)
c_darkgreen = (0, 150, 0)
c_lightblue = (100, 100, 250)
c_pink = (200, 100, 100)
c_white = (255, 255, 255)

fps = 1/100





def WrapAround(vehicle):
    if vehicle.position.x < 0:
        vehicle.position.x = SCREEN_WIDTH - 10
    if vehicle.position.x > SCREEN_WIDTH:
        vehicle.position.x = 10
    if vehicle.position.y < 0:
        vehicle.position.y = SCREEN_HEIGHT - 10
    if vehicle.position.y > SCREEN_HEIGHT:
        vehicle.position.y = 10






def main():

    b_creating_line = False
    start_of_line = Vector2D(0,0)
    end_of_line = Vector2D(0,0)

    line_segment_list = []

    debug = True
    def show_UI(x,y):
        words = font.render(str(mode_text), True, (255, 255, 255))
        screen.blit(words, (x, y) )

        words = font2.render("wander_radius: " + str(one_guy.steer.wander_radius), True, (255, 255, 255))
        screen.blit(words, (x, y + 20) )
        words = font2.render("wander_distance: " + str(one_guy.steer.wander_distance), True, (255, 255, 255))
        screen.blit(words, (x + 300, y + 20) )
        words = font2.render("wander_jitter: " + str(one_guy.steer.wander_jitter), True, (255, 255, 255))
        screen.blit(words, (x + 600, y + 20) )

    time = 0
    def draw_gameobjects():
        pygame.draw.circle(screen, c_red, (target.position.x, target.position.y), target.scale)
        pygame.draw.circle(screen, c_lightblue, (one_guy.position.x, one_guy.position.y), one_guy.bounding_radius)
        pygame.draw.polygon(screen, c_blue,points=[(one_guy.front_pt.x, one_guy.front_pt.y), (one_guy.port_pt.x, one_guy.port_pt.y), (one_guy.starboard_pt.x, one_guy.starboard_pt.y)])

        # debug draw lines

        #start_x = target.position.x
        #start_y = target.position.y
        #end_x = one_guy.position.x
        #end_y = one_guy.position.y

        #pygame.draw.line(screen, c_yellow, (start_x, start_y), (end_x, end_y), 3)

        #start_x = one_guy.position.x
        #start_y = one_guy.position.y
        #end_x = one_guy.position.x + one_guy.steer.wander_target.x * one_guy.steer.wander_distance
        #end_y = one_guy.position.y + one_guy.steer.wander_target.y * one_guy.steer.wander_distance

        #pygame.draw.line(screen, c_green, (start_x, start_y), (end_x, end_y), 3)
        #pygame.draw.circle(screen, c_yellow, (end_x, end_y), 3)

        if (len(one_guy.steer.feeler_list) > 0):
            for f in one_guy.steer.feeler_list:
                p_x = one_guy.position.x + f.x
                p_y = one_guy.position.y + f.y
                pygame.draw.line(screen, c_pink, (one_guy.position.x, one_guy.position.y), (p_x, p_y), 3)








        if b_creating_line:
            m_x, m_y = pygame.mouse.get_pos()
            pygame.draw.line(screen, c_green, (start_of_line.x, start_of_line.y), (m_x, m_y), 3)


        for line in line_segment_list:
            pygame.draw.line(screen, c_white, (line.start_point.x, line.start_point.y), (line.end_point.x, line.end_point.y), 3)
            pygame.draw.line(screen, c_green, (line.start_point.x, line.start_point.y), (line.start_point.x + line.normal.x * 10, line.start_point.y + line.normal.y * 10), 3)




        pygame.draw.circle(screen, c_yellow, (one_guy.reference_pt.x, one_guy.reference_pt.y), 3, width = 1)




        if debug:
            start_x = one_guy.position.x
            start_y = one_guy.position.y
            end_x = one_guy.position.x + one_guy.m_heading.x * one_guy.steer.wander_distance
            end_y = one_guy.position.y + one_guy.m_heading.y * one_guy.steer.wander_distance

            pygame.draw.line(screen, c_green, (start_x, start_y), (end_x, end_y), 3)
            pygame.draw.circle(screen, c_yellow, (end_x, end_y), one_guy.steer.wander_radius, width = 1)

            p_x = one_guy.position.x + one_guy.steer.wander_target.x
            p_y = one_guy.position.y + one_guy.steer.wander_target.y

            pygame.draw.circle(screen, c_darkgreen, (p_x, p_y), 5)
            pygame.draw.line(screen, c_red, (start_x, start_y), (p_x, p_y), 3)

            start_x = p_x
            start_y = p_y
            end_x = p_x + one_guy.steer.change.x
            end_y = p_y + one_guy.steer.change.y

        #pygame.draw.line(screen, c_pink, (start_x, start_y), (end_x, end_y), 3)



    target = TargetCircle(-1, 0, 0)

    # init for pygame'
    pygame.init()
    # create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # title and icon
    pygame.display.set_caption("AI C3 using Pygame")
    # prep font
    font = pygame.font.Font('freesansbold.ttf', 20)
    font2 = pygame.font.Font('freesansbold.ttf', 11)

    mode_text_start = "Current Behaviour: "
    mode_text = mode_text_start + "Arrive"

    gameobject_id = 0
    one_guy = Vehicle(gameobject_id, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    one_guy.target = target.position

    # game loop
    running = True
    while running:

        one_guy.target = target.position
        #one_guy.target = target.position
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if event.button == 1: # left click
                    target.position.x, target.position.y = pygame.mouse.get_pos()
                    one_guy.target = target.position
                elif event.button == 3: # right click
                    if b_creating_line == False:
                        b_creating_line = True
                        start_of_line.x, start_of_line.y = pygame.mouse.get_pos()
                    else:
                        b_creating_line = False
                        end_of_line.x, end_of_line.y = pygame.mouse.get_pos()

                        line_segment = LineSegment(len(line_segment_list), start_of_line.x, start_of_line.y, end_of_line.x, end_of_line.y);
                        line_segment_list.append(line_segment)



            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    if one_guy.steer.behaviour == Behaviour.SEEK:
                        one_guy.steer.behaviour = Behaviour.FLEE
                        mode_text = mode_text_start + "Flee"
                    elif one_guy.steer.behaviour == Behaviour.FLEE:
                        one_guy.steer.behaviour = Behaviour.ARRIVE
                        mode_text = mode_text_start + "Arrive"
                    elif one_guy.steer.behaviour == Behaviour.ARRIVE:
                        one_guy.steer.behaviour = Behaviour.WANDER
                        mode_text = mode_text_start + "Wander"
                    elif one_guy.steer.behaviour == Behaviour.WANDER:
                        one_guy.steer.behaviour = Behaviour.SEEK
                        mode_text = mode_text_start + "Seek"
                if keys[pygame.K_F2]:
                    debug = not debug
                if keys[pygame.K_p]:
                    line_segment_list.clear()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                one_guy.steer.wander_radius += 1
            if keys[pygame.K_z]:
                one_guy.steer.wander_radius -= 1
                one_guy.steer.wander_radius = max(1, one_guy.steer.wander_radius)
            if keys[pygame.K_s]:
                one_guy.steer.wander_distance += 1
            if keys[pygame.K_x]:
                one_guy.steer.wander_distance -= 1
                one_guy.steer.wander_distance = max(1, one_guy.steer.wander_distance)
            if keys[pygame.K_d]:
                one_guy.steer.wander_jitter += 0.1
            if keys[pygame.K_c]:
                one_guy.steer.wander_jitter -= 0.1
                one_guy.steer.wander_jitter = max(0.1, one_guy.steer.wander_jitter)            # yep, instant fix
            #one_guy.m_velocity = Vector2D(0,0)
            #if mouse_presses[0]:
            #    mouse_x, mouse_y = pygame.mouse.get_pos()
            #    one_guy.m_heading = (Vector2D(mouse_x, mouse_y) - one_guy.position).normalize()

        time += 0.003
        one_guy.Update(fps, line_segment_list)
        target.Update(time)
        # drawing
        # RGB, red green blue

        WrapAround(one_guy)

        screen.fill( ( 0, 0, 0) )

        draw_gameobjects()
        show_UI(20,500)
        pygame.display.update()






if __name__ == '__main__':
    main()
