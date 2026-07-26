import pygame as pg

ww, wh = 1000, 800

running = True
window = pg.display.set_mode((ww,wh))
buffer = []
for i in range(ww):
    buffer.append([])
    for j in range(wh):
        buffer[-1].append((0,0,0))
    
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    mp = pg.mouse.get_pos()
    try:
        buffer[mp[0]][mp[1]] = (255,255,255)
    except Exception as whatevertf:
        print("NOO DONT DO THAT")
    
    window.fill((0,0,0))
    for i in range(ww):
        for j in range(wh):
            pg.draw.circle(window, buffer[i][j], (i,j), 0.5)

    pg.display.flip()