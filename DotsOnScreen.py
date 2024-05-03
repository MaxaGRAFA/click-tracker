import tkinter as tk
import pandas as pd

class DrawDots():
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data
        self.root = self.set_root()
        self.canvas = self.set_canvas()

    def set_root(self) -> tk.Tk:
        root = tk.Tk()

        root.wait_visibility(root)
        root.wm_attributes("-fullscreen", 1)
        root.wm_attributes("-transparentcolor", root['bg'])

        return root
    
    def set_canvas(self) -> tk.Canvas:
        frame = tk.Frame(self.root)
        frame.pack()

        canvas = tk.Canvas(frame, width=self.root.winfo_width(), height=self.root.winfo_height())
        canvas.pack()

        return canvas
    
    def draw_one_dot(self, pos: tuple, color: str) -> None: 
        self.canvas.create_oval(pos[0]-2, pos[1]-2, pos[0]+2, pos[1]+2, fill=color, width=0)

    def draw_dots(self) -> None:
        for row in self.data.itertuples():
            self.draw_one_dot((row.x, row.y), row.color)

        self.root.mainloop()
