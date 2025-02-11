import numpy as np
import matplotlib.pyplot as plt

class Wire:
    I: np.float32
    x: np.float32
    y: np.float32

    def __init__(self, I, x, y):
        self.I = I
        self.x = x
        self.y = y

class Stream:
    def __init__(self, ax, arr=set(), N=50):
        self.ax = ax

        self.x, self.y = np.meshgrid(np.linspace(-2, 2, N), np.linspace(-2, 2, N))
        self.B_x = None
        self.B_y = None

        self.arr = set()
        for w in arr:
            self.add_wire(w.I, w.x, w.y)
        
    
    def add_wire(self, I, x, y):
        self.arr.add(Wire(I=I, x=x, y=y))

        r = np.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        if self.B_x is None:
            self.B_x = -I * (self.y - y) / r ** 3
            self.B_y = I * (self.x - x) / r ** 3
        else:
            self.B_x += -I * (self.y - y) / r ** 3
            self.B_y += I * (self.x - x) / r ** 3
    
    def delete_wire(self, I, x, y):
        for_del = []
        for w in self.arr:
            if np.sqrt((x - w.x) ** 2 + (x - w.y) ** 2) < I:
                for_del.append(w)
        for d in for_del:
            self.arr.remove(d)
            r = np.sqrt((self.x - d.x) ** 2 + (self.y - d.y) ** 2)
            self.B_x -= -d.I * (self.y - d.y) / r ** 3
            self.B_y -= +d.I * (self.x - d.x) / r ** 3
    
    def paint(self):
        if self.B_x is not None:
            self.ax.contour(self.x, self.y, self.B_x)#, color='green', linewidth=1, density=1, arrowstyle='->', integration_direction='forward')
        
        #for x in range():
            #plt.plot(r[0], r[1], color=(sigm(r[2]), 0.1, 0.8 * (1 - sigm(r[2]))))
        
        for w in self.arr:
            circle = plt.Circle((w.x, w.y), 0.1 * w.I, color='red' if w.I > 0 else 'blue')
            self.ax.add_artist(circle)
        
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-2, 2)
