import tkinter as tk
from tkinter import ttk

from PIL.Image import Resampling
from PIL import Image, ImageTk
from collections import namedtuple

rgb = namedtuple('rgb', ['r', 'g', 'b'])


def round_rectangle(canvas, x1, y1, width, height, radius=25, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              width - radius, y1,
              width - radius, y1,
              width, y1,
              width, y1 + radius,
              width, y1 + radius,
              width, height - radius,
              width, height - radius,
              width, height,
              width - radius, height,
              width - radius, height,
              x1 + radius, height,
              x1 + radius, height,
              x1, height,
              x1, height - radius,
              x1, height - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)


def createGradient(canvas, position_x, position_y, width, height, startRGB: rgb, endRGB: rgb, direction="h",
                   definition=1):
    global newRect

    def rgb2hex(r, g, b):
        r = int(r)
        g = int(g)
        b = int(b)
        return "#%s%s%s" % tuple([hex(c)[2:].rjust(2, "0") for c in (r, g, b)])

    amount = lambda start, end, w: float(end - start) / (w * definition)
    newRect = lambda x1, y1, x2, y2, rgb: canvas.create_rectangle(x1, y1, x2, y2, fill=rgb2hex(rgb.r, rgb.g, rgb.b),
                                                                  outline=rgb2hex(rgb.r, rgb.g, rgb.b))
    if direction == "h":
        rAmount = amount(startRGB.r, endRGB.r, width)
        gAmount = amount(startRGB.g, endRGB.g, width)
        bAmount = amount(startRGB.b, endRGB.b, width)
        for x in range(width * definition):
            thisRGB = rgb._make([startRGB.r + x * rAmount, startRGB.g + x * gAmount, startRGB.b + x * bAmount])
            newRect(position_x + (x * (1 / definition)), position_y, position_x + (x * (1 / definition)),
                    position_y + height, thisRGB)
    elif direction == "v":
        rAmount = amount(startRGB.r, endRGB.r, height)
        gAmount = amount(startRGB.g, endRGB.g, height)
        bAmount = amount(startRGB.b, endRGB.b, height)
        for y in range(height * definition):
            thisRGB = rgb._make([startRGB.r + y * rAmount, startRGB.g + y * gAmount, startRGB.b + y * bAmount])
            newRect(position_x, position_y + (y * (1 / definition)), position_x + width,
                    position_y + (y * (1 / definition)), thisRGB)
    else:
        raise ValueError("Direction only accept 'h' and 'v'")


def path2tkImg(path, size, formats: tuple = None):
    img = Image.open(path, formats=formats)
    img = img.resize(size, Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)
    return img


class winView():
    def __init__(self, win, rwidth, rheight, mainView: bool):
        self.win = win
        self.rwidth = rwidth
        self.rheight = rheight
        self.withToolbar = mainView

    def addFloat(self, widget):
        tempX = 0
        tempY = 0

        def start_drag(event):
            global tempX, tempY
            tempX = event.x
            tempY = event.y

        def do_move(event):
            global tempX, tempY
            moveX = event.x - tempX
            moveY = event.y - tempY
            x = self.win.winfo_x() + moveX
            y = self.win.winfo_y() + moveY
            self.win.geometry(f"+{x}+{y}")

        def stop_move(event):
            global tempX, tempY
            tempX = None
            tempY = None

        widget.bind("<ButtonPress-1>", start_drag)
        widget.bind("<ButtonRelease-1>", stop_move)
        widget.bind("<B1-Motion>", do_move)

    def outlined(self, canvas, item, color):
        bbox = canvas.bbox(item)
        rect_item = canvas.create_rectangle(bbox, outline=color, fill="")
        canvas.tag_raise(item, rect_item)

    def goIconify(self, event):
        # win.update_idletasks()
        self.win.overrideredirect(False)
        self.win.iconify()

    def newView(self, title, icons):
        frame = tk.Canvas(self.win, height=self.rheight - 1.5, width=self.rwidth - 1, relief='raised',
                          highlightthickness=1)
        frame.config(highlightbackground="#031cc4", highlightcolor="#031cc4")
        frame.place(x=0.5, y=-1)
        self.addFloat(frame)

        # Highlight - Dark
        createGradient(frame, position_x=0, position_y=0, width=self.rwidth + 3, height=5, startRGB=rgb(55, 138, 254),
                       endRGB=rgb(0, 87, 230), direction="v", definition=1)
        # mid-dark upper
        createGradient(frame, position_x=0, position_y=5, width=self.rwidth + 3, height=18, startRGB=rgb(0, 87, 230),
                       endRGB=rgb(0, 87, 230), direction="v", definition=1)
        # mid-dark lower
        createGradient(frame, position_x=0, position_y=23, width=self.rwidth + 3, height=12, startRGB=rgb(0, 87, 230),
                       endRGB=rgb(3, 107, 255), direction="v", definition=1)
        # Body
        createGradient(frame, position_x=0, position_y=35, width=self.rwidth + 3, height=self.rwidth - 30,
                       endRGB=rgb(3, 50, 196),
                       startRGB=rgb(3, 103, 255), direction="v", definition=1)

        frame.create_text((34, 23), text=title, font="MSGothic 17 bold", fill="#fff", anchor="w")
        frame.create_image(18, 20, image=icons["icon"])

        closeBtn = frame.create_image(self.rwidth - 20, 20, image=icons["close"])
        frame.tag_bind(closeBtn, "<ButtonPress-1>", lambda event: self.win.loop.stop())#self.win.quit())

        minimizeBtn = frame.create_image(self.rwidth - 50, 20, image=icons["small"])
        frame.tag_bind(minimizeBtn, "<ButtonPress-1>", self.goIconify)
        frame.bind("<Map>", lambda event: self.win.overrideredirect(True))

        view = tk.Canvas(self.win, height=self.rheight - 42, width=self.rwidth - 10.5, bg="#ebe9d8",
                         highlightthickness=1.5)
        view.config(highlightbackground="#023cc7", highlightcolor="#023cc7")
        view.place(x=4, y=35)

        if self.withToolbar:
            wrapperHeight = self.rheight - 67
            ttk.Separator(view, orient='horizontal').place(x=2, y=27, width=self.rwidth - 10.5, height=0)
            # ToolBars
            topToolBar = tk.Canvas(view, background="#ebe9d7", highlightthickness=0, width=self.rwidth - 12, height=23)
            topToolBar.place(x=3, y=3)
            bottomToolBar = tk.Canvas(view, background="#ebe9d7", highlightthickness=0, width=self.rwidth - 12, height=19.5)
            bottomToolBar.place(x=3, y=wrapperHeight + 7)
            ttk.Separator(view, orient='horizontal').place(x=2, y=wrapperHeight + 7, width=self.rwidth - 10.5, height=0)

            # Main Wrapper
            wrapper = ttk.Frame(view, width=self.rwidth - 10.5, height=wrapperHeight)
            wrapper.place(x=3, y=28)
            wrapper['padding'] = (5, 5)

            return wrapper, topToolBar, bottomToolBar
        else:
            # Main Wrapper
            wrapper = ttk.Frame(view, width=self.rwidth - 10.5, height=self.rheight - 42)
            wrapper.place(x=3, y=28)
            wrapper['padding'] = (5, 5)
            return wrapper


class imgAssets():
    def __init__(self):
        self.icon = path2tkImg("resources/100.ico", (21, 21))
        self.closeBtn = path2tkImg("resources/close.png", (27, 27))
        self.minimizeBtn = path2tkImg("resources/small.png", (27, 27))
        self.send = path2tkImg("resources/921.ico", (21, 21))
        self.cancel = path2tkImg("resources/849.ico", (25, 25))
        self.run = path2tkImg("resources/875.ico", (19, 19))
        self.info = path2tkImg("resources/978.ico", (25, 25))
        self.portrait = path2tkImg("resources/bot.png", (33, 33))
        self.user = path2tkImg("resources/959.ico", (28, 28))
        self.drawer = path2tkImg("resources/drawer.png", (18, 23))
