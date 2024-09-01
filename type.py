from typing import List, Optional
from requests_html import HTML
from arsenic.session import Element
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

class ScrapperMixin:
    def get_images(self, include_others: bool = False, only_include: Optional[List[str]] = None) -> List[str]:
        """Get the total number of images.

        Args:
            include_others (bool, optional): Whether to include additional non-important photos. Defaults to False.
            only_include (list, optional): List of file extensions to include, without the dot. Defaults to None.

        Returns:
            List[str]: List of image links.
        """
        pass

    def rHTML(self) -> HTML:
        """Get the HTML of the current element.

        Returns:
            HTML: HTML instance.
        """
        pass

    def save_photo(self, filename: str) -> str:
        """Save the photo of the current element to the specified directory.

        Args:
            filename (str): The name of the file to save the photo as.

        Returns:
            str: Path to the saved photo.
        """
        pass

    def click(self) -> bool:
        """Click on the element.

        Returns:
            bool: True if click was successful, False otherwise.
        """
        pass

    def GetElement(self) -> ActionChains:
        """Get the webdriver element for additional actions.

        Returns:
            ActionChains: The ActionChains instance.
        """
        pass

class ScrapperMixAsy:
    def __init__(self) -> None:
        pass

    async def get_images(self, include_others: bool = False, only_include: Optional[List[str]] = None) -> List[str]:
        """Get the total number of images asynchronously.

        Args:
            include_others (bool, optional): Whether to include additional non-important photos. Defaults to False.
            only_include (list, optional): List of file extensions to include, without the dot. Defaults to None.

        Returns:
            List[str]: List of image links.
        """
        pass

    def rHTML(self) -> HTML:
        """Get the HTML of the current element.

        Returns:
            HTML: HTML instance.
        """
        pass

    async def save_photo(self, filename: str) -> str:
        """Save the photo of the current element asynchronously to the specified directory.

        Args:
            filename (str): The name of the file to save the photo as.

        Returns:
            str: Path to the saved photo.
        """
        pass

    async def click(self) -> bool:
        """Click on the element asynchronously.

        Returns:
            bool: True if click was successful, False otherwise.
        """
        pass

    async def GetElement(self) -> Element:
        """Get the arsenic element for additional actions.

        Returns:
            Element: The arsenic Element instance.
        """
        pass

class Scrapper_(ScrapperMixin, BeautifulSoup):
    def __init__(self, markup: str, features: Optional[str] = None) -> None:
        super().__init__(markup, features)

class AScrapper_(ScrapperMixAsy, BeautifulSoup):
    def __init__(self, markup: str, features: Optional[str] = None) -> None:
        super().__init__(markup, features)
