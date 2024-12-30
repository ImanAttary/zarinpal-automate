from typing import Optional, Union
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from .utils import wait_for_element, find_all_elements


class Element:
    def __init__(self, driver, xpath):
        self.driver = driver
        self.xpath = xpath

    def wait(self, wait_method="visible", text=None):
        wait_for_element(self.driver, self.xpath,
                         wait_method=wait_method, text=text)
        
    def wait_presense(self, wait_method="presence", text=None):
        wait_for_element(self.driver, self.xpath,
                         wait_method=wait_method, text=text)

    def find(self):
        return self.driver.find_element("xpath", self.xpath)

    def is_present(self):
        return len(find_all_elements(self.driver, self.xpath)) > 0

    def is_displayed(self):
        return self.find().is_displayed()
    

class Clickable(Element):
    def click(self):
        self.find().click()

    def wait_to_become_clickable(self):
        self.wait("click")

    def is_clickable(self):
        return "disable-btn" not in self.find().get_attribute("class")


class Checkbox(Clickable):
    def toggle(self):
        self.click()


class Image(Clickable):
    pass


class Text(Clickable):
    """Any element which can render a text"""

    def get_text(self) -> str:
        return self.find().text

    def get_id(self) -> str:
        return self.find().get_attribute("id")
    def get_plac(self) -> str:
        return self.find().get_attribute("placeholder")


class TextInput(Text):
    def __init__(self, driver, xpath):
        super().__init__(driver, xpath)

    def enter_string(self, input_str: str) -> None:
        self.find().send_keys(input_str)

    def select_file(self) -> None:
        self.find().send_keys()

    def click_enter_string(self, input_str: str) -> None:
        self.find().click()
        # CLASS INSTANCE of STR WAS PASSING, FIXED
        self.enter_string(input_str)

    def clear_input(self, length: Optional[Union[int]]) -> None:
        if length:
            for i in range(length):
                self.find().send_keys(Keys.BACKSPACE)
        else:
            self.find().clear()

    def direct_press_key(self) -> None:
        self.find().send_keys(Keys.ENTER)

    def press_key(self, key):
        if key == "enter":
            self.find().send_keys(Keys.ENTER)
        elif key == "down":
            self.find().send_keys(Keys.ARROW_DOWN)
        elif key == "up":
            self.find().send_keys(Keys.ARROW_UP)


class Button(Text):
    pass


class PlainInput(TextInput):
    pass


class UploadButton(TextInput):
    pass


class SecretInput(TextInput):
    pass


class Box(Text):
    pass


class Error(Text):
    pass


class Info(Text):
    pass


class Table(Text):
    def get_rows(self):
        table = self.find()
        table_body = table.find_element(By.TAG_NAME, "tbody")
        return table_body.find_elements(By.TAG_NAME, "tr")

    def get_data_cell(self, row):
        cells = row.find_elements(By.TAG_NAME, "td")
        return cells


class DropDown(Text):
    def select_option(self, visible_text):
        drop_down = self.find()
        options = Select(drop_down)
        return options.select_by_visible_text(visible_text)
