from PyBros.utils import __as__, Scrapper
from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from arsenic import get_session, browsers, services
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from functools import wraps
from typing import Callable, Union, Coroutine, Any
from PyBros.type import Scrapper_, AScrapper_

class Browser:

    def __init__(self, browser_type='chrome', hidden=True):
        self.browser_type = browser_type
        self.hidden = hidden
        self.url = None
        self.driver = None
        self.session = None

    def _setup_sync_browser(self):
        if self.browser_type.lower() == 'chrome':
            options = ChromeOptions()
            if self.hidden:
                options.add_argument('--headless')
            options.add_experimental_option("prefs", {
                "download.default_directory": "/dev/null",
                "download.prompt_for_download": False,
                "safebrowsing.enabled": True,
            })
            options.add_argument('--window-size=1920,1200')
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        elif self.browser_type.lower() == 'firefox':
            options = FirefoxOptions()
            if self.hidden:
                options.add_argument('--headless')
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.dir", "/dev/null")
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            options.set_preference("pdfjs.disabled", True)
            options.add_argument('--window-size=1920,1200')
            self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

        elif self.browser_type.lower() == 'huggingface':
            options = ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1200')
            options.add_experimental_option("prefs", {
                "download.default_directory": "/dev/null",
                "download.prompt_for_download": False,
                "safebrowsing.enabled": True,
            })
            self.driver = webdriver.Chrome(options=options)
        else:
            raise ValueError('Unsupported browser. Only "chrome" and "firefox" are supported.')

        return self.driver

    async def _setup_async_browser(self):
        if self.browser_type == 'chrome':
            service = services.Chromedriver(binary=ChromeDriverManager().install())
            browser = browsers.Chrome(
                **{
                    'goog:chromeOptions': {
                        'args': [
                            '--headless' if self.hidden else '',
                            '--window-size=1920,1200'
                        ],
                        'prefs': {
                            'download.default_directory': '/dev/null',
                            'download.prompt_for_download': False,
                            'safebrowsing.enabled': True,
                        }
                    }
                }
            )
        elif self.browser_type == 'firefox':
            service = services.Geckodriver(binary=GeckoDriverManager().install())
            browser = browsers.Firefox(
                **{
                    'moz:firefoxOptions': {
                        'args': [
                            '--headless' if self.hidden else '',
                            '--window-size=1920,1200'
                        ],
                        'prefs': {
                            'browser.download.folderList': 2,  # Custom location
                            'browser.download.dir': '/dev/null',  # Redirect downloads to a non-existent directory
                            'browser.helperApps.neverAsk.saveToDisk': 'application/octet-stream',
                            'pdfjs.disabled': True,  # Disable PDF viewer
                        }
                    }
                }
            )
        elif self.browser_type == 'huggingface':
            service = services.Chromedriver(binary=ChromeDriverManager().install())
            browser = browsers.Chrome(
                **{
                    'goog:chromeOptions': {
                        'args': [
                            '--headless' if self.hidden else '',
                            '--window-size=1920,1200'
                        ],
                        'prefs': {
                            'download.default_directory': '/dev/null',
                            'download.prompt_for_download': False,
                            'safebrowsing.enabled': True,
                        }
                    }
                }
            )
        else:
            raise ValueError('Unsupported browser. Only "chrome" and "firefox" are supported.')

        self.session = await get_session(service, browser).__aenter__()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            try:
                await self.session.close()
                return True
            except Exception:
                return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            try:
                self.driver.quit()
                return True
            except Exception:
                return False

    def __g(self, url: str, cookies: dict={}, domain: str = None):
        self.url = url
        if len(cookies) > 0:
            self.driver.get(url)
        for key, paire in cookies:
            if domain:
                self.driver.add_cookie(
                    {
                        'name' : key,
                        'value' : paire,
                        "domain" : domain
                    }
                )
            else:
                self.driver.add_cookie(
                    {
                        'name' : key,
                        'value' : paire
                    }
                )
        self.driver.get(url)
        scrp = Scrapper(self.get_html(), self.driver, current_url=url)
        return scrp
    
    async def __ag(self, url: str, cookies: dict={}, domain: str = None):
        self.url = url
        if len(cookies)  > 0:
            await self.session.get(url)
        for key, paire in cookies.items():
            if domain:
                await self.session.add_cookie(
                    name=key,
                    value=paire,
                    domain=domain
                )
            else:
                await self.session.add_cookie(name=key, value=paire)
        await self.session.get(url)
        scrp = Scrapper(await self.get_html(), self.session, current_url=url)
        return scrp

    def _gel(self):
        scrp = Scrapper(self.get_html(), self.driver, current_url=self.url)
        return scrp

    async def _agel(self):
        scrp = Scrapper(await self.get_html(), self.session, current_url=self.url)
        return scrp

    def __c(self):
        self.driver.close()

    async def __ac(self):
        await self.session.close()

    def __gh(self):
        return self.driver.page_source

    async def __agh(self):
        return await self.session.get_page_source()

    def __ejs(self, js: str) -> any:
        if js == None:
            doc = "<a href='https://google.com'>"
            html = HTML(html=doc)
            val = html.render(script=js, reload=reload)
            return val
        else:
            doc = self.get_html()
            html = HTML(html=doc)
            val = html.render()
            return val

    async def __aejs(self, js: str) -> any:
        if js == None:
            doc = "<a href='https://google.com'>"
            html = HTML(html=doc)
            val = await html.arender(script=js, reload=reload)
            return val
        else:
            doc = await self.get_html()
            html = HTML(html=doc)
            val = await html.arender()
            return val

    def __ejop(self, js: str, wait: float = 0.2) -> any:
        val = self.driver.execute_script(js)
        return val
    
    async def __aejop(self, js: str, wait: float = 0.2) -> any:
        val = await self.session.execute_script(js)
        return val

    async def _async_request_interceptor(self, data):
        request_url = data['request']['url']
        self.link_history.append(request_url)
        print(f"Added to the history : {request_url}")

    def _scro(self, percentage: float):
        total_height = self.execute_js_on_page("return document.body.scrollHeight")
        per = percentage / 100
        scroll_position = total_height * per
        self.execute_js_on_page(f"window.scrollTo(0, {scroll_position});")
        return True

    async def _ascro(self, percentage: float):
        total_height = await self.execute_js_on_page("return document.body.scrollHeight")
        per = percentage / 100
        scroll_position = total_height * per
        await self.execute_js_on_page(f"window.scrollTo(0, {scroll_position});")
        return True

    get_element = __as__(_gel, _agel)

    setup_browser = __as__(_setup_sync_browser, _setup_async_browser)
    """
    this is a simple classic examples
    """

    get: Union[Callable[[str, dict, str], Scrapper_], Callable[[str, dict, str], Coroutine[None, None, AScrapper_]]] = __as__(__g, __ag)
    """
    Make a get request and retrieves the Scrapper instance for the given URL.

    Args:
        url (str): The URL to make a request.
        cookies: (dict): Pass the cookies here
        domain: (str): Pass the string domain here

    Returns:
        Scrapper: The Scrapper instance with page content.
    """

    close = __as__(__c, __ac)
    """
    Close the browser
    """

    get_html: Union[Callable[[None], Any], Callable[[str], Coroutine[None, None, str]]] = __as__(__gh, __agh)
    """
    Return the HTML instance from the requests-html.HTML
    """

    execute_js: Union[Callable[[str], Any], Callable[[str], Coroutine[None, None, Any]]] = __as__(__ejs, __aejs)
    """
    Execute javascript if you have custom javascript then you can use this
    """

    execute_js_on_page: Union[Callable[[str, float], Any], Callable[[str], Coroutine[None, None, Any]]] = __as__(__ejop, __aejop)
    """
    Execute custom javascript on a page

    Args:
        js (str): Pass the custom javascript here
        wait (float): Pass the wait time here before js to executed

    Return:
        Any: Return the output
    """

    scroll_down = __as__(_scro, _ascro)
    """
    This function helps to scroll to the specific place pass the percentage as float

    Args:
        percentage (float): Percentage in float
    """
