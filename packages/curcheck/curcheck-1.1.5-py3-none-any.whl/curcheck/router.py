"""
    Модуль роутеров-сборников команд, вызывающих нужные события-декораторы.

    Каждый роутер-это отдельный сайт. Регулирует кол-во страниц и тд в каждом
    отдельном сайте для наиболее эффективного парсинга.
"""

import asyncio
import json

from typing import List, Awaitable
from aiohttp import ClientSession

from pyppeteer import launch
from pyppeteer.browser import Browser

from .events import EventPage, EventPaginator, EventLongpoll


class SiteRouter:
    def __init__(
        self, domain: str, is_spa: bool = False, is_login=False, login_wait=60,
    ) -> None:
        self.domain = domain
        self.is_spa = is_spa
        self.is_login = is_login
        self.login_wait = login_wait # Сколько надо ждать чтобы залогиниться

        self.browser: Browser = None

        self.pages: List[EventPage] = []
        self.paginators: List[EventPaginator] = []
        self.longpolls: List[EventLongpoll] = []

    def paginate_page(
        self, 
        url: str, 
        pages_links_xpath: str, 
        count_in_approach: int = 10,
        auxiliary_function: Awaitable|None = None, 
        paginate_urls: list|None = None
    ) -> EventPaginator:
        paginator = EventPaginator(
            domain=self.domain, 
            url=url,
            pages_links_xpath=pages_links_xpath, 
            count_in_approach=count_in_approach,
            is_browser=self.is_spa,
            auxiliary_function=auxiliary_function,
            paginate_urls=paginate_urls,
        )
        self.paginators.append(paginator)

        return paginator

    def page(self, url: str) -> EventPage:
        page = EventPage(
            domain=self.domain, 
            url=url,
            is_browser=self.is_spa,
        )
        self.pages.append(page)

        return page

    def longpoll(
        self, url: str, timeout: int = 60, count: int|None = None
    ) -> EventLongpoll:
        longpoll = EventLongpoll(
            domain=self.domain,
            url=url,
            timeout=timeout,
            count=count,
            is_browser=self.is_spa,
        )
        self.longpolls.append(longpoll)

        return longpoll
    
    def _set_cookies_in_pages(self, cookie):
        for page in self.pages:
            page.cookies = cookie
        
        for paginator in self.paginators:
            paginator.cookies = cookie
        
        for longpoll in self.longpolls:
            longpoll.cookies = cookie

    async def executor(self, browser: Browser|None = None) -> None:
        if self.is_spa:
            if self.is_login:
                try:
                    with open(f"{self.domain.split('/')[-1]}.json") as f:
                        self._set_cookies_in_pages(json.load(f))
                except FileNotFoundError:
                    browser = await launch(headless=False)
                    page = await browser.newPage()
                    page.setDefaultNavigationTimeout(0)
                    await page.goto(self.domain)
                    await page.evaluate(
                        f"() => alert('Привет, это окно для логина. "
                        f"Обязательно нажми ок и залогинься в течении {self.login_wait} секунд.')"
                    )
                    await asyncio.sleep(self.login_wait)

                    with open(f"{self.domain.split('/')[-1]}.json", 'w+') as f:
                        json.dump(await page.cookies(), f)
                        self._set_cookies_in_pages(await page.cookies())

            if not browser:
                browser = await launch(headless=True)

            await asyncio.gather(
                *[page.task(browser) for page in self.pages]
            )

            await asyncio.gather(
                *[paginator.task(browser) for paginator in self.paginators]
            )

            await asyncio.gather(
                *[longpoll.task(browser) for longpoll in self.longpolls]
            )
        else:
            async with ClientSession() as session:
                await asyncio.gather(
                    *[page.task(session) for page in self.pages]
                )

                await asyncio.gather(
                    *[paginator.task(session) for paginator in self.paginators]
                )

                await asyncio.gather(
                    *[longpoll.task(session) for longpoll in self.longpolls]
                )
