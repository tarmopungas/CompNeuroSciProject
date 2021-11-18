import psychopy.visual.rect
from psychopy import visual, event, core

# D  L  R  U
frequencies = [8, 12, 8, 15]

win = visual.Window([1000, 700], color='black', units='pix', fullscr=False, )

triangle1 = psychopy.visual.Polygon(win=win,
                                    edges=3,
                                    radius=100,
                                    fillColor=[1, -1, -1], pos=(0, 180))
triangle2 = psychopy.visual.Polygon(win=win,
                                    edges=3,
                                    radius=100,
                                    ori=90,
                                    fillColor=[1, -1, -1], pos=(300, 0))
triangle3 = psychopy.visual.Polygon(win=win,
                                    edges=3,
                                    radius=100,
                                    ori=-90,

                                    fillColor=[1, -1, -1], pos=(-300, 0))
triangle4 = psychopy.visual.Polygon(win=win,
                                    edges=3,
                                    radius=100,
                                    ori=180,
                                    fillColor=[1, -1, -1], pos=(0, -180))
frq = [60 / f for f in frequencies]
tri = [triangle4, triangle3, triangle2, triangle1]
current_frame = 0
while True:
    for i in range(4):
        if current_frame % (2 * frq[i]) < frq[i]:
            tri[i].draw()
    win.flip()
    current_frame += 1
    for key in event.getKeys():
        if key in ['escape', 'q']:
            core.quit()
