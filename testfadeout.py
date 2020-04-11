from tkinter import *

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        b = Button(self, text="Click to fade away", command=self.quit)
        b.pack()
        self.parent = parent

    def quit(self):
        self.fade_away()

    def fade_away(self):
        alpha = self.parent.attributes("-alpha")
        if alpha > 0:
            alpha -= .0051
            self.parent.attributes("-alpha", alpha)
            self.after(25, self.fade_away)
        else:
            self.parent.destroy()

if __name__ == "__main__":
    root = Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()