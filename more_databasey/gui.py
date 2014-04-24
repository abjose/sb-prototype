import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from demo import Site

"""
code initally taken from:
http://matplotlib.org/examples/widgets/slider_demo.html

TODO
- get to display all three graphs
- add sliders for number nodes, connect prob, population
- add sliders for honesty, participation, misbelief
- add 'reset' button
- add 'do 10 steps' button (unless can slide back and forth in time)
"""

fig, ax = plt.subplots()
ax.set_axis_off()
#ax.axes.get_xaxis().set_ticks([])
#ax.axes.get_yaxis().set_ticks([])
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)
plt.subplots_adjust(left=0.15, bottom=0.26)

axcolor = 'lightgoldenrodyellow'
axpop    = plt.axes([0.15, 0.06, 0.65, 0.02], axisbg=axcolor)
axprob   = plt.axes([0.15, 0.09, 0.65, 0.02], axisbg=axcolor)
axnodes  = plt.axes([0.15, 0.12, 0.65, 0.02], axisbg=axcolor)

axhonest = plt.axes([0.15, 0.16, 0.65, 0.02], axisbg=axcolor)
axpart   = plt.axes([0.15, 0.19, 0.65, 0.02], axisbg=axcolor)
axmisb   = plt.axes([0.15, 0.22, 0.65, 0.02], axisbg=axcolor)

spop   = Slider(axpop,   'Population',   1,  500,   valinit=20, valfmt='%1.0f')
sprob  = Slider(axprob,  'Probability',  0., 1.,    valinit=0.6)
snodes = Slider(axnodes, 'Nodes',        1,  100,   valinit=5,  valfmt='%1.0f')

shonest = Slider(axhonest, 'Honesty',       0., 1., valinit=.75)
spart   = Slider(axpart,   'Participation', 0., 1., valinit=.75)
smisb   = Slider(axmisb,   'Misbelief',     0., 1., valinit=.75)


pop = 20
size = 5
connect_prob = 0.2
s = Site(pop, size, connect_prob)
for _ in range(100): s.tick()
#s.show_difference()

s.test_draw(ax1, ax2, ax3)

def update(val):
    #amp = samp.val
    #freq = sfreq.val
    #print int(round(freq))
    #l.set_ydata(amp*np.sin(2*np.pi*freq*t))
    #s = amp*np.sin(2*np.pi*freq*t)
    #plt.plot(t,s, lw=2, color='red')
    #l.plot(t,s, lw=2, color='red')
    #fig.draw()
    ax1.cla()
    ax2.cla()
    ax3.cla()
    s.test_draw(ax1, ax2, ax3)
    fig.canvas.draw_idle()
#sfreq.on_changed(update)
#samp.on_changed(update)

resetax = plt.axes([0.65, 0.015, 0.1, 0.035])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
def reset(event):
    sfreq.reset()
    samp.reset()
button.on_clicked(reset)

#rax = plt.axes([0.025, 0.5, 0.15, 0.15], axisbg=axcolor)
#radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)
#def colorfunc(label):
#    l.set_color(label)
#    fig.canvas.draw_idle()
#radio.on_clicked(colorfunc)

plt.show()
