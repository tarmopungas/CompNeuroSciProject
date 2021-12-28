import psychopy.visual.rect
from psychopy import visual, event, core
from psychopy.hardware import keyboard

# D  L  R  U
frequencies = [1, 2, 6, 10]

win = visual.Window([1000, 700], color='black', units='pix', fullscr=False, )

triangle1 = psychopy.visual.Polygon(win=win,
                                    edges=3,
                                    radius=100,
                                    fillColor=[1, -1, -1], pos=(0, 180))

light1 = psychopy.visual.Circle(win=win,
                                    edges=32,
                                    radius=20,
                                    fillColor=[1, 1, 1], pos=(100, 210))
triangle2 = psychopy.visual.Polygon(win=win,
                                    edges=3,
                                    radius=100,
                                    ori=90,
                                    fillColor=[1, -1, -1], pos=(300, 0))
light2 = psychopy.visual.Circle(win=win,
                                    edges=32,
                                    radius=20,
                                    fillColor=[1, 1, 1], pos=(450, 0))
triangle3 = psychopy.visual.Polygon(win=win,
                                    edges=3,
                                    radius=100,
                                    ori=-90,
                                    fillColor=[1, -1, -1], pos=(-300, 0))
light3 = psychopy.visual.Circle(win=win,
                                    edges=32,
                                    radius=20,
                                    fillColor=[1, 1, 1], pos=(-450, 0))
triangle4 = psychopy.visual.Polygon(win=win,
                                    edges=3,
                                    radius=100,
                                    ori=180,
                                    fillColor=[1, -1, -1], pos=(0, -180))
light4 = psychopy.visual.Circle(win=win,
                                    edges=32,
                                    radius=20,
                                    fillColor=[1, 1, 1], pos=(100, -210))



rectangle1 = psychopy.visual.Polygon(win=win,
                                     ori=45,
                                    edges=4,
                                    radius=40,
                                    fillColor='green', pos=(0, 180))
rectangle2 = psychopy.visual.Polygon(win=win,
                                     ori=45,
                                    edges=4,
                                    radius=40,
                                    fillColor='green', pos=(300, 0))
rectangle3 = psychopy.visual.Polygon(win=win,
                                     ori=45,
                                    edges=4,
                                    radius=40,
                                    fillColor='green', pos=(-300, 0))
rectangle4 = psychopy.visual.Polygon(win=win,
                                     ori=45,
                                    edges=4,
                                    radius=40,
                                    fillColor='green', pos=(0, -180))
frq = [60 / f for f in frequencies]
tri = [triangle4, triangle3, triangle2, triangle1]
rects = [rectangle1,rectangle2,rectangle3,rectangle4]
rects.reverse()
current_frame = 0
while True:
    light1.draw()
    light2.draw()
    light3.draw()
    light4.draw()

    for key in event.getKeys():
        print(key)
        if key in ['escape', 'q']:
            core.quit()
        if key == 'up':
            light1.color = 'yellow'

        if key == 'down':
            light4.color = 'yellow'

        if key == 'left':
            light3.color = 'yellow'
        if key == 'right':
            light2.color = 'yellow'

    for i in range(4):
        if current_frame % (2 * frq[i]) < frq[i]:
            tri[i].draw()
            rects[i].draw()
    win.flip()
    current_frame += 1







