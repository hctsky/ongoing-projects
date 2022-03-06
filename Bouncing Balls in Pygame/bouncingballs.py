import pygame
import random
import math
from ball import Ball
from ball import LineSegment
from vector2d import Vector2D

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


BALL_SPEED = 5

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

clock = pygame.time.Clock()
target_fps = 16 #16ms




def main():

    draw_aiming_line = False
    list_of_balls = []
    list_of_lines = []

    selected_ball = None
    selected_line = None

    ref_closest_pt = Vector2D(0,0)


    def DoCirclesOverlap(b1, b2):
        dist_between_balls = (b1.position - b2.position).lengthsqrd()
        r1 = b1.radius
        r2 = b2.radius
        if dist_between_balls <= (r1+r2)*(r1+r2):
            return True
        return False

    def IsPointInCircle(bx, by, br, px, py):
        return math.fabs( (bx - px) * (bx - px) + (by - py) * (by - py) < (br * br) )


    def Add_Line(sx, sy, ex, ey, radius):
        l = LineSegment(sx, sy, ex, ey, radius)
        list_of_lines.append(l)

    def Add_Ball(x, y, radius):
        b = Ball(x,y, radius)
        #b.velocity.x = random.randrange(-1, 1)
        #b.velocity.y = random.randrange(-1, 1)
        list_of_balls.append(b)

    def draw_gameobjects():
        for b in list_of_balls:
            if selected_ball != None and b == selected_ball:
                pygame.draw.circle(screen, c_blue, (b.position.x, b.position.y), b.radius, width = 0)
            else:
                pygame.draw.circle(screen, c_white, (b.position.x, b.position.y), b.radius, width = 0)
            #if (abs(b.velocity) > 0.001):
            #    pygame.draw.line(screen, c_white, (b.position.x, b.position.y), (b.position.x + (b.velocity.x / abs(b.velocity)) * b.radius , b.position.y + (b.velocity.y / abs(b.velocity)) * b.radius), 3)


        for l in list_of_lines:
            pygame.draw.circle(screen, c_gray, (l.start_pt.x, l.start_pt.y), l.radius + 1)

            pygame.draw.circle(screen, c_gray, (l.end_pt.x, l.end_pt.y), l.radius + 1)
            normal = Vector2D(l.end_pt.x - l.start_pt.x, l.end_pt.y - l.start_pt.y).perpendicular().normalize()

            p1 = l.start_pt + normal * l.radius
            p2 = l.end_pt + normal * l.radius

            p3 = l.start_pt - normal * l.radius
            p4 = l.end_pt - normal * l.radius

            pygame.draw.line(screen, c_gray, (p1.x, p1.y), (p2.x, p2.y), 2)
            pygame.draw.line(screen, c_gray, (p3.x, p3.y), (p4.x, p4.y), 2)

        for c in colliding_pairs:
            pygame.draw.line(screen, c_red, (c[0].position.x, c[0].position.y), (c[1].position.x, c[1].position.y), 3)

        if selected_ball and draw_aiming_line:
            pygame.draw.line(screen, c_blue, (selected_ball.position.x, selected_ball.position.y), (pygame.mouse.get_pos()), 3)



        #if ref_closest_pt:
        #    pygame.draw.circle(screen, c_red, (ref_closest_pt.x, ref_closest_pt.y), 3, width = 3)

    def show_UI(x,y):
        #text = "Bouncing balls in pygame test"
        #words = font.render(str(text), True, (255, 255, 255))
        #screen.blit(words, (x, y))

        words = font2.render("FPS: " + str(round(clock.get_fps(), 2)), True, (255, 255, 255))
        screen.blit(words, (20, 20) )


    def OnCreate():
        ball_radius = 15
        line_radius = 5
        for i in range(30):
            Add_Ball(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), ball_radius)

        Add_Line(10, 10, 1270, 10, line_radius)
        #Add_Line(10, 710, 1270, 710, line_radius)
        #Add_Line(10, 10, 10, 710, line_radius)
        #Add_Line(1270, 10, 1270, 710, line_radius)


    def OnUserUpdate(time_elapsed):

        simulation_updates = 1
        sim_elapsed_time = time_elapsed / simulation_updates

        max_simulation_steps = 1

        # do positions update
        for i in range(simulation_updates):
            for b in list_of_balls:
                b.sim_time_remaining = sim_elapsed_time

            for step in range(max_simulation_steps):
                for b in list_of_balls:

                    if b.sim_time_remaining > 0.0:

                        b.o_position = b.position

                        b.acceleration = b.velocity * -0.8
                        b.acceleration.y += 80

                        b.velocity += b.acceleration * b.sim_time_remaining
                        b.position += b.velocity * b.sim_time_remaining

                        if b.position.x < 0:
                            b.position.x = SCREEN_WIDTH
                        if b.position.x >  SCREEN_WIDTH:
                            b.position.x = 0

                        if b.position.y < 0:
                            b.position.y = SCREEN_HEIGHT
                        if b.position.y > SCREEN_HEIGHT:
                            b.position.y = 0

                        if abs(b.velocity) < 0.01:
                            b.velocity = Vector2D(0,0)


                #static collisions check
                for b in list_of_balls:
                    # against edges static check
                    for l in list_of_lines:
                        line1 = l.end_pt - l.start_pt
                        line2 = b.position - l.start_pt

                        edge_length = line1.lengthsqrd()

                        t = float (max(0, min(edge_length, float(line1.dot(line2)))) / edge_length)

                        closest_pt = l.start_pt + line1 * t

                        dist = b.position.distance_to(closest_pt)

                        if dist <= b.radius + l.radius:
                            #print("collided")
                            fakeball = Ball(closest_pt.x, closest_pt.y, l.radius)
                            fakeball.mass = b.mass
                            fakeball.velocity = Vector2D(-b.velocity.x, -b.velocity.y)

                            colliding_pairs.append((b, fakeball))

                            overlap = dist - b.radius - fakeball.radius
                            b.position -= (b.position - fakeball.position).normalize() * overlap

                    for target in list_of_balls:
                        if b.id != target.id:
                            if DoCirclesOverlap(b, target):
                                colliding_pairs.append((b, target))
                                dist_between_balls = b.position.distance_to(target.position)
                                overlap = (dist_between_balls - b.radius - target.radius) * 0.5

                                b.position -= (b.position - target.position).normalize() * overlap
                                target.position += (b.position - target.position).normalize() * overlap

                    intended_speed = abs(b.velocity)
                    intended_distance = intended_speed * b.sim_time_remaining
                    actual_distance = b.position.distance_to(b.o_position)
                    if intended_speed != 0:
                        actual_time = actual_distance / intended_speed
                    else:
                        actual_time = 0#b.sim_time_remaining

                    #b.sim_time_remaining = b.sim_time_remaining - actual_time
                    b.sim_time_remaining = b.sim_time_remaining - actual_time

                # work out dynamic collisions check
                for c in colliding_pairs:
                    b1 = c[0]
                    b2 = c[1]
                    dist = b1.position.distance_to(b2.position)
                    normal = (b2.position - b1.position).normalize()
                    tangent = normal.perpendicular()

                    #dot product tangent
                    dp_tan1 = b1.velocity.dot(tangent)
                    dp_tan2 = b2.velocity.dot(tangent)
                    dp_norm1 = b1.velocity.dot(normal)
                    dp_norm2 = b2.velocity.dot(normal)

                    m1 = (dp_norm1 * (b1.mass - b2.mass) + 2 * b2.mass * dp_norm2) / (b1.mass + b2.mass)
                    m2 = (dp_norm2 * (b2.mass - b1.mass) + 2 * b1.mass * dp_norm1) / (b1.mass + b2.mass)
                    b1.velocity.x = tangent.x * dp_tan1 + normal.x * m1
                    b1.velocity.y = tangent.y * dp_tan1 + normal.y * m1

                    b2.velocity.x = tangent.x * dp_tan2 + normal.x * m2
                    b2.velocity.y = tangent.y * dp_tan2 + normal.y * m2

                colliding_pairs.clear()


    # init for pygame'
    pygame.init()

    # create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # title and icon
    pygame.display.set_caption("Balls, Pygame version")
    # prep font
    font = pygame.font.Font('freesansbold.ttf', 20)
    font2 = pygame.font.Font('freesansbold.ttf', 11)

    OnCreate()

    # game loop
    running = True
    game_time = 0
    elapsed_time = 0
    last_update_time = pygame.time.get_ticks()
    while running:
        game_time = pygame.time.get_ticks()
        elapsed_time = game_time - last_update_time

        if elapsed_time < target_fps:
            continue;

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if event.button == 1 or event.button == 3 : # left click or right click
                    m_x, m_y = pygame.mouse.get_pos()
                    selected_ball = None
                    for b in list_of_balls:
                        if IsPointInCircle(b.position.x, b.position.y, b.radius, m_x, m_y):
                            selected_ball = b
                            break

                    selected_line = None
                    selected_linestart = False
                    for l in list_of_lines:
                        if IsPointInCircle(l.start_pt.x, l.start_pt.y, l.radius, m_x, m_y):
                            selected_line = b
                            selected_linestart = True
                            break
                        elif IsPointInCircle(l.end_pt.x, l.end_pt.y, l.radius, m_x, m_y):
                            selected_line = b
                            selected_linestart = False
                            break
            mouse_presses = pygame.mouse.get_pressed()
            m_x, m_y = pygame.mouse.get_pos()
            if mouse_presses[0] == True:
                if selected_ball != None:
                    b.position.x = m_x
                    b.position.y = m_y
                elif selected_line != None:
                    if selected_linestart:
                        l.start_pt.x = m_x
                        l.start_pt.y = m_y
                    else:
                        l.end_pt.x = m_x
                        l.end_pt.y = m_y

            if mouse_presses[2] == True:
                if selected_ball != None:
                    draw_aiming_line = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    if selected_ball != None:
                        m_x, m_y = pygame.mouse.get_pos()
                        selected_ball.velocity = (selected_ball.position - Vector2D(m_x, m_y)) * BALL_SPEED
                        #print("ball vel: "  + str(selected_ball.velocity))
                selected_ball = None
                selected_line = None




        colliding_pairs = []
        OnUserUpdate(1/target_fps)


        screen.fill( ( 0, 0, 0) )

        #OnUpdate()

        draw_gameobjects()
        show_UI(20,500)
        pygame.display.update()
        clock.tick()
        colliding_pairs.clear()
        last_update_time = game_time
        #

if __name__ == '__main__':
    main()
