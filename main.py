import asyncio
import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedTk

from util import winView, imgAssets
from pages.home import home
from bingbot import chat, chaos2text


class app(ThemedTk):
    win: ThemedTk
    rwidth: int
    rehight: int
    images: imgAssets
    pages: dict = {}

    def __init__(self, loop, interval=1 / 120):
        super().__init__()
        self.loop = loop
        # self.protocol("WM_DELETE_WINDOW", self.close)
        self.tasks = []
        # self.tasks.append(loop.create_task(self.rotator(1 / 60, 2)))
        self.tasks.append(loop.create_task(self.updater(interval)))

        self.overrideredirect(True)
        self.configure(background="systemTransparent", themebg="#ebe9d8", theme="winxpblue")
        self.rwidth = 800
        self.rheight = 500
        self.geometry(f"{self.rwidth}x{self.rheight}")
        self.attributes('-transparent', 'false', '-notify', 'true')

        ttk.Label(self, text="hi").pack()

        self.images = imgAssets()
        self.mainView, self.mainTopBar, self.mainBottomBar = winView(self, self.rwidth, self.rheight, True).newView(
            "Chat Assistant",
            {"icon": self.images.icon,
             "close": self.images.closeBtn,
             "small": self.images.minimizeBtn})

        # self.tasks.append(loop.create_task(self.drawer()))
        self.drawer()
        self.bindings()
        # self.tasks.append(loop.creat`e_task(self.pb()))
        self.thisConversation = chat()
        self.tasks.append(loop.create_task(self.thisConversation.newBot()))

    def drawer(self):
        self.pages["home"] = home(self, self.mainView, self.images)

    def bindings(self):
        self.pages["home"].start.configure(command=lambda: self.tasks.append(loop.create_task(self.pb())))
        self.pages["home"].submit.configure(command=lambda: self.tasks.append(loop.create_task(self.sendPrompt())))

    async def sendPrompt(self):
        # self.pages["home"].updateBottomBar(progressing=True, status="Generating")
        prompt = self.pages["home"].promptInput.get("1.0", 'end-1c')
        self.pages["home"].promptInput.delete("1.0", "end-1c")
        self.pages["home"].mainDisplay.add_requ(prompt)
        resp = self.thisConversation.ask_stream(prompt)
        respView = self.pages["home"].mainDisplay.new_resp()
        async for quotes in resp:
            organized = chaos2text(quotes)
            self.pages["home"].mainDisplay.append_resp(respView, organized)
        # self.pages["home"].updateBottomBar(progressing=False, status="Finished")

    async def pb(self):
        # self.pages["home"].start.configure(command=)
        # async def t():
        for i in range(100):
            await asyncio.sleep(0.1)
            self.pages["home"].pb['value'] += 1

    async def updater(self, interval):
        while True:
            self.update()
            await asyncio.sleep(interval)


# images = imgAssets()
# viewCreator = winView(win, rwidth, rheight, True)
# view, topBar, bottomBar = viewCreator.newView("Chat Assistant",
#                                               {"icon": images.icon, "close": images.closeBtn,
#                                                "small": images.minimizeBtn})
# home = home(view, images)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
app = app(loop)
loop.run_forever()
loop.close()
# loop=asyncio.get_event_loop()
# loop.run_until_complete(app.run())
