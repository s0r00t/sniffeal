"""
This is a virtual implementation of the BHOREAL MIDI controller.
It depends on : wxPython, Mido, python-rtmidi (therefore, (lib)rtmidi)
v0.1
by s0r00t
LICENSE : CC-BY-SA
"""
import wx
import mido
from Queue import Queue
from threading import Thread

def hue2rgb(hue):
    """
    This is a reimplementation in Python of the hue2rgb function
    used in the Bhoreal firmware to get colors
    source : https://github.com/bhoreal/bhoreal/blob/master/firmware/bhoreal_slim_midi/Bhoreal.cpp#L745
    """
    #TODO: are those the same results than on the real controller?
    hue = hue << 3
    
    if hue < 341:
        hue = (hue*3)/4
        r = 255 - hue
        g = hue
        b = 1
    elif hue < 682:
        hue = ((hue-341)*3)/4
        r = 1
        g = 255 - hue
        b = hue
    else:
        hue = ((hue-683)*3)/4
        r = hue
        g = 1
        b = 255 - hue
    return (r,g,b)

def midiProcess(parent):
    while True:
        msg = parent.queue.get()
        wx.CallAfter(parent.buttons[msg.note].SetBackgroundColour, hue2rgb(msg.velocity))


class mainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.SetBackgroundColour('black')
        self.Show(True)
        self.sizer = wx.GridSizer(rows=8, cols=8, hgap=10, vgap=10)
        self.SetSizer(self.sizer)
        self.buttons = []
        for i in range(0,64):
            self.buttons.append(wx.Panel(self, id=i, style=wx.NO_BORDER))
            self.buttons[i].SetBackgroundColour((35,35,35))
            self.buttons[i].Bind(wx.EVT_LEFT_UP, self.onButtonDrop)
            self.buttons[i].Bind(wx.EVT_LEFT_DOWN, self.onButtonClick)
            self.sizer.Add(self.buttons[i],1,wx.EXPAND)
        
        self.queue = Queue()
        thread = Thread(target=midiProcess, args=(self,))
        thread.setDaemon(True)
        thread.start()

        mido.set_backend('mido.backends.rtmidi')
        self.port = mido.open_ioport("Arduino Leonardo",virtual=True,callback=self.onInput)

    def onButtonClick(self, event):
        self.port.send(mido.Message('note_on', note=event.Id, velocity=64))

    def onButtonDrop(self, event):
        #TODO: fix the double message sent when double clicking (is that normal behavior on the controller?)
        self.port.send(mido.Message('note_on', note=event.Id, velocity=0))

    def onInput(self, message):
        print "IN:", message
        self.queue.put(message)

if __name__ == "__main__":
    app = wx.App(False)
    window = mainWindow(None, "Bhoreal MIDI Emulator")
    app.MainLoop()
