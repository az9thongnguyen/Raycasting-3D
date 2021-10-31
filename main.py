import tkinter as tk
from Raycasting import *


def main():
    top = tk.Tk()
    demo = Raycasting(top)
    demo.run()


if __name__ == "__main__":
    # press w,s to move
    # press a,d to rotate
    main()
