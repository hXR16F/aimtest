#!/usr/bin/python

# Programmed by hXR16F
# hXR16F.ar@gmail.com, https://github.com/hXR16F

import time
import pygame
from random import randint


def main(first):
    global acc
    global avgct

    circle_rect[0], circle_rect[1] = randint(0, width - circle_size), randint(0, height - circle_size)

    clicks, misses = 0, 0
    finished = False

    if first:
        text_first_click_info = font.render("Click first circle to start.", True, (255, 255, 255))
        text_accuracy = font.render("Accuracy: " + "-", True, (255, 255, 255))
        text_avg_click_time = font.render("Average click time: " + "-", True, (255, 255, 255))
    else:
        text_first_click_info = font.render("Click circle to start again.", True, (255, 255, 255))
        text_accuracy = font.render("Accuracy: " + str(acc) + "%", True, (255, 255, 255))
        text_avg_click_time = font.render("Average click time: " + str(avgct) + " ms", True, (255, 255, 255))

    first_click = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not finished:
                    mouse = mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= circle_rect[0] and mouse_x <= circle_rect[0] + circle_rect[2] and mouse_y >= circle_rect[1] and mouse_y <= circle_rect[1] + circle_rect[3]:
                        if first_click:
                            first_click = False
                            started = time.time_ns()
                            
                        circle_click.stop()
                        circle_click.play()
                        clicks += 1
                        circle_rect[0], circle_rect[1] = randint(0, width - circle_size), randint(0, height - circle_size)
                    else:
                        misses += 1

                if clicks >= 30:
                    finished = True
                    accuracy = 100 - round((misses / 30) * 100, 2)
                    avg_click_time = round(((time.time_ns() - started) / 30) / 1000000)
                    text_accuracy = font.render("Accuracy: " + str(accuracy) + "%", True, (255, 255, 255))
                    text_avg_click_time = font.render("Average click time: " + str(avg_click_time) + " ms", True, (255, 255, 255))
                    acc = accuracy
                    avgct = avg_click_time
                    return

        text_clicks = font.render("Clicks: " + str(clicks) + " / 30", True, (255, 255, 255))

        screen.fill(bg_color)
        screen.blit(circle, circle_rect)
        if first_click:
            screen.blit(text_first_click_info, (width / 2 - text_first_click_info.get_width() / 2, height / 1.6))

        screen.blit(text_accuracy, (40, height - 80 - text_accuracy.get_height()))
        screen.blit(text_avg_click_time, (40, height - 40 - text_avg_click_time.get_height()))
        screen.blit(text_clicks, (40, 40))

        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    fps = 100
    clock = pygame.time.Clock()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    bg_color = 40, 40, 40

    pygame.init()
    pygame.font.init()
    # pygame.mixer.init()

    font = pygame.font.Font("assets/Jura-Light.ttf", 36) # https://fonts.google.com/specimen/Jura
    circle_click = pygame.mixer.Sound("assets/click.wav") # https://www.zapsplat.com/music/single-click-screen-press-on-smart-phone-1
    circle = pygame.image.load("assets/circle.png") # https://www.pngwing.com/en/free-png-zuamu

    pygame.display.set_caption("aimtest")
    pygame.display.set_icon(circle)

    circle_size = 80
    circle = pygame.transform.scale(circle, (circle_size, circle_size))
    circle_rect = circle.get_rect()

    main(first=True)
    while True:
        main(first=False)
