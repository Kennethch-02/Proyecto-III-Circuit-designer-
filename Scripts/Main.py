import sys
import random
from datetime import datetime
import pygame
import os
from Clases import *

##Variables globales
cursor1 = cursor()

#/____________________________________________________________________________________________________________________
#/_________________________________________VENTANA INDICACIONES_______________________________________________________
def Indicaciones():
    # Variables de la ventana
    global cursor1
    pygame.init()
    pantalla = pygame.display.set_mode([800, 600])
    pygame.display.set_caption('Inicio')
    salir = False
    blanco = (255, 255, 255)
    negro = (0, 0, 0)
    rojo = (200, 0, 0)
    colorfondo = blanco
    fuente = pygame.font.SysFont("Javanese text", 45)
    texto = fuente.render("Indicaciones", True, negro)  # Texto de bienvenida
    Archive = open("Indicaciones.txt", "r")
    text_ = Archive.read()
    text_ = text_.split("\n")

    # Variables del Boton
    boton_a2 = pygame.image.load("./boton_atras.gif")
    boton_a3 = pygame.image.load("./boton_atras.gif")
    boton_atras = boton(boton_a3, boton_a2, 590, 400)  # cambia la posicion del boton

    # Ciclo de la ventana
    while salir != True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor1.colliderect(boton_atras.rect):
                    return Main()
            if event.type == pygame.QUIT:
                salir = True
                sys.exit()
        # actualizaciones e impresiones del trabajo
        pantalla.fill(colorfondo)
        pantalla.blit(texto, (270, 50))  # Texto de bienvenida
        cursor1.update(pantalla)
        boton_atras.update(pantalla, cursor1)
        x = 10
        y = 150
        for line in text_:
            font = pygame.font.Font("times.ttf", 18)
            txt = font.render(line, True, (0, 0, 0))
            pantalla.blit(txt,(x,y))
            y+=20
        pygame.display.update()
    pygame.quit()
    #Indicaciones()


# /____________________________________________________________________________________________________________________
# /_________________________________________VENTANA SIMULADOR__________________________________________________________
def Simulador():
    global cursor1
    pygame.init()
    WIDTH = 1000
    HEIGHT = 800
    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('My Game')
    Circuit = Circuito(pantalla)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 255)

    boton_a2 = pygame.image.load("./boton_atras.jpg")
    IMG_B_Up = pygame.image.load("./arrow_up.png")
    IMG_B_up = pygame.image.load("./arrow_u.png")
    IMG_Save = pygame.image.load("./boton_save.jpg")
    IMG_Load= pygame.image.load("./boton_load.jpg")
    IMG_F_P = pygame.image.load("./F_P.PNG")
    IMG_R = pygame.image.load("./R.PNG")
    IMG_Cable = pygame.image.load("./C_Cable.png")
    IMG_Cable_A = pygame.image.load("./C_Cable_A.png")
    boton_atras = boton(boton_a2, boton_a2, WIDTH-200,HEIGHT-50)  # cambia la posicion del boton
    botton_save = boton(IMG_Save, IMG_Save, 25, HEIGHT-50)
    botton_load = boton(IMG_Load, IMG_Load, 170, 115)
    text_load = text_box(10, 100, 150, 30, "Archive")
    is_running = True
    is_down = False
    draw_line_h = False
    draw_line_v = False
    coord_line = (0,0)
    menu = Bar_Menu(0,0)
    pantalla.fill(GREEN)
    B_F_P = Dynamic_Button(IMG_F_P, IMG_F_P, 25, 25, 60,60, "B_F_P")
    B_Res = Dynamic_Button(IMG_R, IMG_R, 25, 25, 60, 60, "B_Res")
    B_Cable = Dynamic_Button(IMG_Cable, IMG_Cable_A, 25, 25, 60, 60, "B_Cable")
    menu.add_button(B_F_P)
    menu.add_button(B_Res)
    menu.add_button(B_Cable)
    coord_line = 0
    while is_running:
        pantalla.fill(WHITE)
        cursor1.update(pantalla)
        Circuit.Lines.update()
        menu.update(pantalla, cursor1)
        Circuit.Elements.update(pantalla, cursor1)
        boton_atras.update(pantalla, cursor1)
        botton_save.update(pantalla, cursor1)
        botton_load.update(pantalla, cursor1)
        text_load.update(pantalla, cursor1, False, (20, 100))
        pygame.display.update()
        for event in pygame.event.get():
            menu.event(event, cursor1)
            text_load.text_update(event)
            for s in Circuit.Elements:
                if cursor1.active_cable != True:
                    s.move_sprite(event, cursor1)
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for s in menu.Botones:
                    if cursor1.colliderect(s.rect):
                        if s.get_type() == "B_F_P":
                            batery = Batery(0, IMG_F_P,random.randint(0,800) , random.randint(100,600), 100, 100, "batery")
                            Circuit.Elements.add(batery)
                            cursor1.normal_cursor()
                        if s.get_type() == "B_Res":
                            resistence = Resistance(1, 1, IMG_R, random.randint(50,700), random.randint(100,500), 100, 100, "resistance")
                            Circuit.Elements.add(resistence)
                            cursor1.normal_cursor()
                        if s.get_type() == "B_Cable":
                            if cursor1.active_cable:
                                cursor1.normal_cursor()
                            else:
                                cursor1.cable_cursor(pantalla)
                is_down = True
                if cursor1.active_cable:
                    coord_line = pygame.mouse.get_pos()
                    lines = Line_(pantalla, BLACK, coord_line[0], coord_line[1], 1,1)
                    Circuit.Lines.add(lines)
                if cursor1.colliderect(boton_atras.rect):
                    cursor1.normal_cursor()
                    return Main()
                if cursor1.colliderect(botton_save.rect):
                    cursor1.normal_cursor()
                    Circuit.Save_Circuit()
                if cursor1.colliderect(botton_load.rect):
                    Circuit.Load_Circuit(text_load.get_text())
            if event.type == pygame.MOUSEBUTTONUP:
                is_down = False
                if cursor1.active_cable:
                    draw_line_h = False
                    draw_line_v = False
                    coord_line = 0
            if coord_line!=0 and draw_line_v != True and draw_line_h != True:
                actual_coord = pygame.mouse.get_pos()
                if((actual_coord[0]-coord_line[0]) > 10):
                    draw_line_h = True
                if ((actual_coord[0] - coord_line[0]) < -10):
                    draw_line_h = True
                if ((actual_coord[1] - coord_line[1]) > 10):
                    draw_line_v = True
                if ((actual_coord[1] - coord_line[1]) < -10):
                    draw_line_v = True
        #if is_down:

        if draw_line_h:
            coord = pygame.mouse.get_pos()
            if((coord[0]-coord_line[0])<0):
                lines.line.set_x((coord[0]))
                lines.line.set_width(-1*(coord[0] - coord_line[0]))
            else:
                lines.line.set_width(coord[0]-coord_line[0])
        if draw_line_v:
            coord_v = pygame.mouse.get_pos()
            if((coord_v[1]-coord_line[1])<0):
                lines.line.set_y((coord_v[1]))
                lines.line.set_height(-1*(coord_v[1] - coord_line[1]))
            else:
                lines.line.set_height(coord_v[1]-coord_line[1])
    pygame.quit()
    #Simulador()

def Main():
    global cursor1
    #Variables Ventana
    pygame.init()
    pantalla = pygame.display.set_mode([800,600])
    pygame.display.set_caption('Inicio')
    salir = False
    blanco = (255,255,255)
    negro = (0,0,0)
    rojo = (200,0,0)
    colorfondo = blanco
    fuente = pygame.font.SysFont("Javanese text",55)
    texto = fuente.render("Circuit Designer", True, negro)#Texto de bienvenida
    #variables para el boton
    boton_ind1 = pygame.image.load ("./boton_ind1.gif")
    boton_ind2 = pygame.image.load("./boton_ind1.gif")
    boton_sim1 = pygame.image.load("./boton_sim1.gif")
    boton_sim2 = pygame.image.load("./boton_sim1.gif")
    boton1 = boton(boton_ind1,boton_ind2)
    boton2 = boton(boton_sim1, boton_sim2,300,120)


    while salir != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir = True
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor1.colliderect(boton1.rect):
                    return Indicaciones()
                elif cursor1.colliderect(boton2.rect):
                    return  Simulador()

        #actualizaciones e impresiones del trabajo
        pantalla.fill(colorfondo)
        pantalla.blit(texto, (220,70))
        cursor1.update(pantalla)
        boton1.update(pantalla, cursor1)
        boton2.update(pantalla, cursor1)
        pygame.display.update()
    pygame.quit()

#t = Thread(target=Main)
#t.start()
Main()