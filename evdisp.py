"""event display for WSentinel.
Shows the mp4 file 1 frame at a time with WSentinel's CSV data superposed.
"""

import numpy as np
import matplotlib.pyplot as plt
import imageio
import sys

wscsvrow = np.dtype({'names':['ts','n','I','x','y','azi','alt'],
                     'formats':['S19','i4']+['f8']*5})

class evdisp:
    def __init__(self, fn):
        """fn is any filename of the event in
        path/cYYYYmmdd_HHMMSS_fff.xxx format"""
        self.iframe = 0
        self.f, self.ax = plt.subplots()
        self.f.canvas.mpl_connect('key_press_event',
                                  lambda event: self.press(event))
        self.timer = self.f.canvas.new_timer(interval=33)
        self.timer.add_callback(self.nextframe_loop)
        if fn:
            self.open(fn)
        
    def open(self, fn):
        """fn is any filename of the event in
        path/cYYYYmmdd_HHMMSS_fff.xxx format"""
        ts = fn[-23:-4]
        path = fn[:-25]
        csv = '%s/c%s.csv'%(path,ts)
        mp4 = '%s/m%s.mp4'%(path,ts)
        self.data = np.array(list(tuple(l.split(',')) for l in open(csv)),
                             dtype=wscsvrow)
        self.vid = imageio.get_reader(mp4)
        self.plotcentroid = False
        self.f.show()
        self.runvideo()
        
    def showframe(self):
        i = self.iframe
        cdat = self.data[i]
        fdat = self.vid.get_data(i)
        plt.figure(self.f.number)
        plt.cla()
        plt.imshow(fdat)
        if self.plotcentroid:
            plt.plot(cdat['x'], cdat['y'], 'o', markerfacecolor='none')
        plt.title('%3d %19s %3d %4d %5.1f %5.1f %6.2f %6.2f'%
                  ( (self.iframe,cdat[0].decode(),) + tuple(cdat)[1:] ))
        self.f.canvas.draw_idle()

    def press(self, event):
        if event.key == 'k':
            self.stopvideo()
            self.iframe += 1
            if self.iframe >= len(self.data):
                self.iframe = len(self.data)-1
            else:
                self.showframe()
        elif event.key == 'j':
            self.stopvideo()
            self.iframe -= 1
            if self.iframe < 0:
                self.iframe = 0
            else:
                self.showframe()
        elif event.key == 'v':
            self.plotcentroid = False
            self.runvideo()
        elif event.key == 'x':
            self.stopvideo()
        elif event.key == 'c':
            self.plotcentroid = not self.plotcentroid
            self.showframe()
        else:
            print('unknown key pressed ', event.key)
            sys.stdout.flush()

    def runvideo(self):
        self.timer.start()

    def stopvideo(self):
        self.timer.stop()

    def nextframe_loop(self):
        self.iframe += 1
        if self.iframe >= len(self.data):
            self.iframe = 0
        self.showframe()
            
