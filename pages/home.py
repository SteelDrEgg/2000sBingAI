import asyncio
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class chatDisplay():
    def __init__(self, page):
        self.page = page
        # Creating wrapper
        self.chatsWrap = ttk.Frame(page.view)
        self.chatsWrap.config(border=2, relief="sunken")

        # Setting geometry
        self.responseDisplayWidth = page.app.rwidth - 265
        self.responseDisplayHeight = page.app.rheight - 225
        # Creating Canvas
        self.responseDisplay = tk.Canvas(self.chatsWrap, background="#ffffff", highlightthickness=0,
                                         width=self.responseDisplayWidth,
                                         height=self.responseDisplayHeight)

        self.responseDisplay.grid(column=0, row=0)
        # Creating scrollbar
        self.responseScroller = ttk.Scrollbar(self.chatsWrap, orient="vertical", command=self.responseDisplay.yview)
        self.responseScroller.grid(row=0, column=1, sticky="ns")
        # Update scrollbar
        self.responseDisplay.configure(scrollregion=self.responseDisplay.bbox("all"))
        self.dialogLineHeight = 5

    def better_new_line(self, text):
        textLen = len(text)
        allowedLen = int(self.responseDisplayWidth / 7) - 3
        if textLen > allowedLen:
            words = text.split(" ")
            newText = ""
            curLineLen = 0
            for word in words:
                if len(word) + 1 + curLineLen < allowedLen:
                    newText = newText + word + " "
                    curLineLen += len(word) + 1
                else:
                    newText = newText + "\n" + word + " "
                    curLineLen = len(word) + 1
            return newText

        else:
            return text

    def show(self):
        self.chatsWrap.grid(column=0, row=0, padx=5, pady=9, columnspan=2, sticky="we")

    def hide(self):
        self.chatsWrap.grid_forget()

    def add_resp(self, text):
        text = self.better_new_line(text)
        self.responseDisplay.create_image(10, 18 + self.dialogLineHeight, anchor="w", image=self.page.assets.portrait)
        self.responseDisplay.create_text(50, 10 + self.dialogLineHeight, anchor="nw", text=text, fill="black")
        self.dialogLineHeight += 18 + (len(text.split("\n")) * 15)
        self.responseDisplay.configure(scrollregion=self.responseDisplay.bbox("all"))

    def new_resp(self):
        self.responseDisplay.create_image(10, 18 + self.dialogLineHeight, anchor="w", image=self.page.assets.portrait)
        textID = self.responseDisplay.create_text(50, 10 + self.dialogLineHeight, anchor="nw", text="", fill="black")
        self.responseDisplay.configure(scrollregion=self.responseDisplay.bbox("all"))
        self.lastRespHeight = 0
        self.dialogLineHeight += 18
        return textID

    def append_resp(self, textID, text):
        text = self.better_new_line(text)
        self.dialogLineHeight += (len(text.split("\n")) * 15) - self.lastRespHeight
        self.lastRespHeight = len(text.split("\n")) * 15
        self.responseDisplay.itemconfigure(textID, text=text)
        self.responseDisplay.configure(scrollregion=self.responseDisplay.bbox("all"))

    def add_requ(self, text):
        text = self.better_new_line(text)
        self.responseDisplay.create_image(self.responseDisplayWidth - 5, 18 + self.dialogLineHeight, anchor="e",
                                          image=self.page.assets.info)
        self.responseDisplay.create_text(self.responseDisplayWidth - 40, 10 + self.dialogLineHeight, anchor="ne",
                                         text=text, fill="black")
        self.dialogLineHeight += 18 + (len(text.split("\n")) * 15)
        self.responseDisplay.configure(scrollregion=self.responseDisplay.bbox("all"))


class home():
    def __init__(self, app, view, assets):
        self.view = view
        self.assets = assets
        self.app = app
        self.draw()

    def draw_chats(self):
        self.mainDisplay = chatDisplay(page=self)
        self.mainDisplay.show()

    def draw_bottomToolbar(self):
        # self.app.mainBottomBar.configure(background="red")
        # ttk.Label(self.app.mainBottomBar, text="test", background="red").place(x=0, y=0)
        # ttk.Style().configure("bottom.TProgressbar", thickness=2)
        self.pb = ttk.Progressbar(self.app.mainBottomBar, orient="horizontal", length=100, mode="indeterminate")
        self.pb.place(x=0, y=0)
        self.statusDisplay = self.app.mainBottomBar.create_text(110, 4, text="Waiting", fill="#323232",
                                                                font=('Lucida Console', 13),
                                                                anchor="nw")

    def draw_topToolBar(self):
        self.app.mainTopBar.create_text(10, 3, text="About", fill="#323232", font=('Lucida Console', 13), anchor="nw")
        self.app.mainTopBar.create_line(60, 0, 60, 30, fill="#97a0a5", width=1)
        self.app.mainTopBar.bind("<ButtonPress-1>", lambda event: tk.messagebox.showinfo("showinfo",
                                                                                         "disclaimer: Just a Tkinter Practice") if event.x < 60 else None)

    def updateBottomBar(self, progressing: bool, status):
        if progressing:
            self.pb.start(interval=50)
        else:
            self.pb.stop()
        self.app.mainBottomBar.itemconfigure(self.statusDisplay, text=status)

    def draw_preference(self):
        # Preference
        preferences = ttk.LabelFrame(self.view, text='Preference', border=2)
        preferences["relief"] = "sunken"  # flat, groove, raised, ridge, solid, or sunken
        preferences.grid(column=2, row=0, padx=7, pady=0, sticky="news", rowspan=3)
        ttk.Label(preferences, width=self.app.rwidth - 779).grid(column=0, row=0)

        self.draw_bottomToolbar()
        self.draw_topToolBar()

        self.start = ttk.Button(preferences, text="go")
        # self.start.grid(column=0, row=2)

        self.app.chatStyle = "Creative"
        # Menu
        menuTitle = tk.Canvas(preferences, background="#fff", width=0, height=25, highlightthickness=1,
                              highlightbackground="#97a0a5")
        menuTitle.grid(column=0, row=0, sticky="we", padx=20, pady=5)
        menuTitle.create_image(133, 2, anchor='nw', image=self.assets.drawer)
        curStyle = menuTitle.create_text(5, 6, text=self.app.chatStyle, fill="#323232", font=('Lucida Console', 13),
                                         anchor="nw")
        menuTitle.update()

        def draw_options():
            def toggle_selection(event):
                if menuSelection.place_info():
                    menuSelection.place_forget()
                else:
                    menuSelection.place(x=20, y=31)

            def update_style(event):
                if event.y < 25:
                    self.app.chatStyle = "Creative"
                elif event.y < 50:
                    self.app.chatStyle = "Balanced"
                else:
                    self.app.chatStyle = "Precise"
                menuTitle.itemconfig(curStyle, text=self.app.chatStyle)
                toggle_selection(None)

            menuSelection = tk.Canvas(preferences, width=menuTitle.winfo_width() - 2, height=75, background='#fff',
                                      highlightthickness=1,
                                      highlightbackground="#96a0a5")
            menuTitle.bind("<ButtonPress-1>", toggle_selection)
            # Creative
            menuSelection.create_text(5, 5, text="Creative", fill="#323232", font=('Lucida Console', 13), anchor="nw")
            menuSelection.create_line(0, 25, menuTitle.winfo_width() - 2, 25, fill="#97a0a5")
            # Balanced
            menuSelection.create_text(5, 30, text="Balanced", fill="#323232", font=('Lucida Console', 13), anchor="nw")
            menuSelection.create_line(0, 50, menuTitle.winfo_width() - 2, 50, fill="#97a0a5")
            # Precise
            menuSelection.create_text(5, 55, text="Precise", fill="#323232", font=('Lucida Console', 13), anchor="nw")
            # Bind
            menuSelection.bind("<ButtonPress-1>", update_style)

        conversations = ttk.Treeview(preferences, selectmode="browse", columns=("Conversations",), show="headings",
                                     height=preferences.winfo_height() - 380)
        conversations.heading("#1", text="Conversations")
        conversations.column("#1", width=menuTitle.winfo_width() + 6, stretch="no")
        conversations.grid(column=0, row=3, padx=15, pady=5, sticky="ns")
        conversations.insert("", "end", text="hi")
        draw_options()

    def draw(self):
        # Draw Chat
        self.draw_chats()

        # Prompts
        self.promptInput = tk.Text(self.view, bg="#ffffff", fg="black", highlightthickness=2, height=7, width=65)
        self.promptInput.config(highlightbackground="#7c7a70", highlightcolor="#c3d5fc", insertbackground='black',
                                border=0,
                                relief="ridge")
        self.promptInput.grid(row=1, column=0, padx=5, sticky="w")

        chatTools = ttk.Frame(self.view)
        chatTools.grid(row=1, column=1, pady=1, sticky="nw")

        # Shortcuts
        # def submit():
        #     chats.delete("1.0", "end-1c")
        #     chats.insert("end-1c", self.promptInput.get("1.0", 'end-1c'))
        self.submit = ttk.Button(chatTools, text='Click', image=self.assets.send)
        self.submit.grid(row=0, column=0, sticky="w", ipadx=4, ipady=4, padx=5)
        cancel = ttk.Button(chatTools, text='Click', image=self.assets.cancel,
                            command=lambda: self.promptInput.delete("1.0", "end-1c"))
        cancel.grid(row=0, column=1, sticky="w", ipadx=2, ipady=2, padx=5)

        ttk.Style().configure('home.TButton', font=('Lucida Console', 11))
        newTopic = ttk.Button(chatTools, text="New Topic", compound=tk.RIGHT, image=self.assets.run, width=8,
                              style="home.TButton")
        newTopic.grid(row=1, column=0, columnspan=2, pady=8, ipady=5, ipadx=2)

        self.draw_preference()
