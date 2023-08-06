"""
    GUI for parsers

    <-- in develop -->
"""

import tkinter as tk

from abc import ABC, abstractmethod
from typing import List

from .router import SiteRouter


class AbstractGUIParser(ABC):

    @abstractmethod
    async def update_data(self):
        pass
    
    @abstractmethod
    async def executor(self):
        pass


class GUIParserTk(AbstractGUIParser):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Парсер")
        self.root.geometry("300x300")

    async def update_data(
        self,
        mpa_routers: List[SiteRouter],
        spa_routers: List[SiteRouter],
    ):
        self.mpa_routers = mpa_routers
        self.spa_routers = spa_routers

    async def executor(self):
        self.root.mainloop()
