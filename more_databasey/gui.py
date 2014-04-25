import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from demo import Site

"""
code initally taken from:
http://matplotlib.org/examples/widgets/slider_demo.html

TODO
- add 'do 10 steps' button (unless can slide back and forth in time)
- add something displaying quantitative difference between truth and graph
- BUG - hitting 'step' after restart seems to restart also...
- setting nodes to something other than valinit, then stepping...makes reset
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

spop   = Slider(axpop,   'Population',  1,  500, valinit=100, valfmt='%1.0f')
sprob  = Slider(axprob,  'Probability', 0., 1.,  valinit=0.3)
snodes = Slider(axnodes, 'Nodes',       1,  100, valinit=5,  valfmt='%1.0f')

shonest = Slider(axhonest, 'Honesty',       0., 1., valinit=.7)
smisb   = Slider(axmisb,   'Misbelief',     0., 1., valinit=.2)
spart   = Slider(axpart,   'Participation', 0., 1., valinit=.4)



# SOMETHING WEIRD WITH INIT STILL...?


#pop = 20
#size = 5
#connect_prob = 0.2
#s = Site(pop, size, connect_prob)
s = Site(int(round(spop.val)), int(round(snodes.val)), sprob.val, 
         shonest.val, smisb.val, spart.val)    
for _ in range(1): s.tick()
s.test_draw(ax1, ax2, ax3)

axrestart = plt.axes([0.65, 0.015, 0.1, 0.035])
brestart = Button(axrestart, 'Restart', color=axcolor, hovercolor='0.975')
def restart(event):
    global s
    s = Site(int(round(spop.val)), int(round(snodes.val)), sprob.val,
             shonest.val, smisb.val, spart.val)    
    for _ in range(10): s.tick()
    ax1.cla()
    ax2.cla()
    ax3.cla()
    s.test_draw(ax1, ax2, ax3)
    fig.canvas.draw_idle()
    #spop.reset()
brestart.on_clicked(restart)

axstep = plt.axes([0.53, 0.015, 0.1, 0.035])
bstep = Button(axstep, 'Step 10', color=axcolor, hovercolor='0.975')
def step(event):
    global s
    #for _ in range(50): s.tick()
    for _ in range(10): s.tick()
    ax1.cla()
    ax2.cla()
    ax3.cla()
    s.test_draw(ax1, ax2, ax3)
    fig.canvas.draw_idle()
bstep.on_clicked(step)

plt.show()
