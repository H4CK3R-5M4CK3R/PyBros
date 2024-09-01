import asyncio
from functools import wraps
from bs4 import BeautifulSoup
from requests_html import HTML
from bs4.element import Tag
from selenium.webdriver.common.by import By
from arsenic.constants import SelectorType
from arsenic import session
from arsenic.session import Element as AElement
from selenium.webdriver.common.action_chains import ActionChains as Element
import re

def __as__(sync_func, async_func):
    @wraps(sync_func)
    def wrapper(*args, **kwargs):
        if asyncio.get_event_loop().is_running():
            return async_func(*args, **kwargs)
        else:
            return sync_func(*args, **kwargs)
    return wrapper

class Scrapper:

    def __init__(self, html_string: str = None, browser: session=None):
        self.html = html_string
        self.browser = browser
        self.html_soup = BeautifulSoup(html_string, 'lxml')
        self.html_requests = HTML(html=html_string)
        self._attach_methods_to_elements(self.html_soup)

    def _attach_methods_to_elements(self, soup):
        for element in self.html_soup.find_all(True):
            element.save_photo = lambda filename, el=element: self.take_screenshot(el, filename)
            element.rHTML = lambda el=element: self.get_html(el)
            element.ImagesLink = lambda include_others, only_include, el=element: self.get_images(el, include_others, only_include)
            element.click = lambda el=element: self.click(el)
            element.GetElement = lambda el=element: self.DElement(el)

    async def _take_screenshot_async(self, element, filename: str, write=True) -> str:
        if not isinstance(filename, str):
            raise ValueError("filename must be a string")
        if not isinstance(element, Tag):
            raise ValueError("element must be a BeautifulSoup Tag")

        if self.browser:
            xpath = self._get_xpath(element)
            el = await self.browser.get_element(xpath, SelectorType.xpath)
            file = await el.get_screenshot()
            if write:
                with open(filename, "wb") as op:
                    op.write(file.getvalue())
                return filename
            else:
                return file
        else:
            raise ValueError("Browser instance is not defined")

    def _take_screenshot_sync(self, element, filename: str) -> str:
        if not isinstance(filename, str):
            raise ValueError("filename must be a string")
        if not isinstance(element, Tag):
            raise ValueError("element must be a BeautifulSoup Tag")

        if self.browser:
            xpath = self._get_xpath(element)
            el = self.browser.find_element(By.XPATH, xpath)
            el.screenshot(filename)
            return f"Screenshot saved as {filename} (sync)"
        else:
            raise ValueError("Browser instance is not defined")

    def _get_xpath(self, element):
        if not isinstance(element, Tag):
            raise ValueError("element must be a BeautifulSoup Tag")

        components = []
        while element is not None and element.name != '[document]':
            siblings = element.find_previous_siblings(element.name)
            index = len(siblings) + 1  # XPath is 1-indexed
            components.append(f'{element.name}[{index}]')
            element = element.parent
        components.reverse()
        xpath = f"/{'/'.join(components)}"
        return xpath

    def __getattr__(self, name):
        if hasattr(self.html_soup, name):
            attr = getattr(self.html_soup, name, None)
            if attr:
                if callable(attr):
                    return attr
                return attr

        if hasattr(self.html_requests, name):
            attr = getattr(self.html_requests, name, None)
            if attr:
                if callable(attr):
                    return attr
                return attr

        raise AttributeError(f"'Scrapper' object has no attribute '{name}'")

    def _geht(self, element):
        return HTML(html=str(element))
    
    def _get_images(self, el, include_others: bool = False, only_include: list = None) -> list:
            pag = HTML(html=str(el))
            if only_include:
                st = "\.("
                for extension in only_include:
                    st = f"{st}|{extension}"
                st = f"{st})$"
                es = re.escape(st)
                image_pattern = re.compile(es, re.IGNORECASE)
            elif include_others == False:
                image_pattern = re.compile(r'\.(jpg|jpeg|png|webp|)$', re.IGNORECASE)
            else:
                image_pattern = re.compile(r'\.(jpg|jpeg|png|gif|bmp|webp|svg)$', re.IGNORECASE)
            out = []
            for url in pag.absolute_links:
                if bool(image_pattern.search(url)):
                    out.append(url)
            return out

    def _click(self, el) -> bool:
        """Click on the given element

        Returns:
            bool: Return True if clicked success else false
        """
        if self.browser:
            xpath = self._get_xpath(el)
            el = self.browser.find_element(xpath, SelectorType.xpath)
        try:
            el.click()
            return True
        except:
            return False

    async def _aclick(self, el) -> bool:
        """Click on the given element

        Returns:
            bool: True if clicked else false
        """
        if self.browser:
            xpath = self._get_xpath(el)
            el = await self.browser.get_element(xpath, SelectorType.xpath)
        try:
            await el.click()
            return True
        except:
            return False

    def _gele(self, el: Element) -> Element:
        """Return the element webDriver element
        """
        if self.browser:
            xpath = self._get_xpath(el)
            el = self.browser.find_element(xpath, SelectorType.xpath)
        return el

    async def _agele(self, el: AElement) -> AElement:
        """Return the element webDriver element
        """
        if self.browser:
            xpath = self._get_xpath(el)
            el = await self.browser.get_element(xpath, SelectorType.xpath)
        return el

    get_images = _get_images
    get_html = _geht
    take_screenshot = __as__(_take_screenshot_sync, _take_screenshot_async)
    click = __as__(_click, _aclick)
    DElement = __as__(_gele, _agele)
