from typing import Optional
import matplotlib.backend_bases
import matplotlib.pyplot as plt
import matplotlib.text
import numpy as np
from time import time

from simulator import Wire, Stream

marker: Optional[matplotlib.text.Text] = None

def press(event: matplotlib.backend_bases.MouseEvent) -> None:
    axes = event.inaxes
    global last_press

    last_press = time()

def release(event: matplotlib.backend_bases.MouseEvent) -> None:
    axes = event.inaxes

    # Если кликнули вне какого-либо графика, то не будем ничего делать
    if axes is None:
        return
    
    global last_press
    if last_press is None:
        return

    global s
    I = time() - last_press
    if event.key is not None:
        if " " in event.key:
            s.add_wire(-I, event.xdata, event.ydata)
    else:
        s.add_wire(I, event.xdata, event.ydata)
    ax.cla()
    s.paint()
    
    #global marker, last
    #if marker is not None:
        #marker.remove()
    #marker = axes.text(event.xdata, event.ydata, f'({event.xdata:.3f}; {event.ydata:.3f})')

    # Обновим график
    axes.figure.canvas.draw()

if __name__ == '__main__':
    global s, last_press
    last_press = None
    fig, ax = plt.subplots(figsize=(8, 8), dpi=254 / 2)
    s = Stream(ax)
    s.paint()

    # Подписка на событие
    fig.canvas.mpl_connect('button_press_event', press)
    fig.canvas.mpl_connect('button_release_event', release)

    plt.show()