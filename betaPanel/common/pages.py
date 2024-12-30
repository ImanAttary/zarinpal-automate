import json
import random
import string
import time
import pyperclip
from abc import ABC
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import conftest
from .elements import (
    Element,
    Clickable,
    Button,
    UploadButton,
    PlainInput,
    SecretInput,
    Box,
    Checkbox,
    Error,
    Info,
    Image,
    Text,
    Table,
    DropDown
)

# Variable :
BETA_URL_ZARINPAL = 'https://next.zarinpal.com/beta/'
ACCOUNT_NUMBER = "09548036993"
IDENTIFIER = "automtion_account"


def generate_random_string(lengh):
    # Choose from all lowercase, uppercase letters, and digits
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(lengh))


def generate_editrandom_string(lengh):
    # Choose from all lowercase, uppercase letters, and digits
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(lengh))



class Container(ABC):
    def __init__(self, identifying_element: Element):
        """Create a Page/Modal with some identifying_element.

        Presence and visibility of the identifying_element on a screen
        should identify the presence of this page unambiguously.
        """
        self.identifying_element = identifying_element

    def wait(self):
        self.identifying_element.wait()


class Page(Container):
    """Parent of all visible pages. Each page has a unique URL."""

    def __init__(self, url_path: str, identifying_element: Element):
        self.url = BETA_URL_ZARINPAL + url_path
        super().__init__(identifying_element)


class Modal(Container):
    """Parent of all modals. A modal might be opened on several pages."""

    pass


class Menu(Container):
    """Parent of all menus. A menu has at least one visible element which
    can be used to open/close the menu and make other contained elements
    visible/invisible consequently.
    """

    def __init__(self, clickable_switch: Clickable, identifying_element: Element):
        """Initialize a menu instance

        :param clickable_switch: A clickable element which opens/closes menu
        :param identifying_element: The main element which indicates that menu is open
        """
        self.clickable_switch = clickable_switch
        super().__init__(identifying_element)

    def wait_for_menu(self):
        """Wait for the menu itself to be visible independent of its state

        The menu might be open or closed. This method returns as soon as
        the menu switch is visible, hence, it can be opened/closed.
        If you want to wait for the open menu, either use the
        :py:meth:`wait()` or the :py:meth:`open_menu()` method.
        """
        self.clickable_switch.wait()

    def open_menu(self):
        self.clickable_switch.click()
        self.identifying_element.wait()

    def close_menu(self):
        self.clickable_switch.click()
        self.identifying_element.wait("invisible")


class zarinpallogin(Page):
    def __init__(self, driver):
        self.login_input = PlainInput(
            driver, "//input[@name='username']"
        )
        self.submit_btn = Button(
            driver, "//button[@class='btn primary']"
        )
        self.otp_input = PlainInput(
            driver, "//*[@id='digit-1']"
        )
        super().__init__("", self.login_input)

    def login(self):
        self.login_input.is_displayed()
        self.login_input.click_enter_string(ACCOUNT_NUMBER)
        self.submit_btn.wait()
        self.submit_btn.click()
        otp_code = conftest.zarinpal_otp_generator(IDENTIFIER)
        self.otp_input.is_displayed()
        self.otp_input.enter_string(otp_code)


class welcomeModal(Modal):
    def __init__(self, driver):
        self.welcome_modal = Box(
            driver, '//*[@id="modal-container"]'
        )
        self.welcome_btn = Button(
            driver, '//*[@id="modal-container"]//button//div[span[text()="متوجه شدم"]]'
        )
        self.changelog_modal = Box(
            driver, '//*[@id="modal-container"]'
        )

        self.changelog_btn = Button(
            driver, '//*[@id="modal-container"]//button//div[span[text()="متوجه شدم"]]'
        )
        self.onboardmodal = Button(
            driver, '//*[@id="modal-container"]//button//div[span[text()="الان نه"]]'
        )
        self.userlabel = Text(
            driver, '//*[@id="user-label"]'
        )
        self.userLabel_close = Button(
            driver, '//*[@id="user-label"]/following-sibling::button[@aria-label="Close Tour"]'
        )
        super().__init__(self.welcome_modal)

    def closeModal(self):
        try:
            self.welcome_modal.wait_presense()
            self.welcome_btn.click()
        except (TimeoutException, NoSuchElementException):
            # If modal is not found or not visible, continue without interaction
            print("Welcome modal not present, continuing...")
            return

    def closeChangeLogModal(self):
        try:
            self.changelog_modal.wait_presense()
            self.changelog_btn.click()
        except (TimeoutException, NoSuchElementException):
            # If modal is not found or not visible, continue without interaction
            print("changelog modal not present, continuing...")
            return
    def closeOnboardModal(self):
        try:
            self.changelog_modal.wait_presense()
            self.onboardmodal.click()
            self.userlabel.wait_presense()
            self.userLabel_close.click()

        except (TimeoutException, NoSuchElementException):
            # If modal is not found or not visible, continue without interaction
            print("changelog modal not present, continuing...")
            return

class zarinpalDashboard(Page):
    def __init__(self, driver):
        
        self.sidbar = Element(
            driver, '//*[@id="sidebar"]'
        )
        self.dashboard_btn = Button(
            driver, '//*[@id="sidebar"]//button//div[span[text()="پیشخوان"]]'
        )
        self.observe_all_transaction = Button(
            driver, '//*[@id = "__nuxt"]//div[span[text()="تراکنش‌های اخیر"]]/following-sibling::button//div[span[text()="مشاهده همه"]]'
        )
        self.observe_all_reconciliation = Text(
            driver, '//*[@id = "__nuxt"]//div[span[text()="تسویه‌حساب‌ها"]]/following-sibling::button'
        )
        self.personal_link = Button(
            driver, '//*[@id="__nuxt"]//div[contains(@class, "w-fit flex gap-xs")]//span'
        )
        self.personal_linkModal = Button(
            driver, '//*[@id="modal-container"]'
        )
        self.personal_linkText = Text(
            driver, '//*[@id="modal-container"]//span[@class="clip-board__main--link"]'
        )
        self.copy_button = Button(
            driver, '//*[@id="modal-container"]//i[contains(@class, "icon-Copy")]'
        )
        self.closemodal_button = Button(
            driver, '//*[@id="modal-container"]//i[contains(@class, "icon-Close")]'  
        )
        self.redirect_button = Button(
            driver, '//*[@id="modal-container"]//i[contains(@class, "icon-ArrowTopRight")]'
        )
        self.payment_name = Text(
            driver, '///*[@id="imanattary"]//div[text()="نام پرداخت کننده (اجباری)"]'
        )
        self.payment_name_mobile = Text(
            driver, '//*[@id="imanattary"]//div[text()="شماره موبایل پرداخت کننده (اجباری)"]'
        )

        super().__init__('automation_zarin.com/dashboard', self.payment_name)

    def personalLink(self, driver):
        time.sleep(3) # for demo
        self.personal_link.wait_presense()
        self.personal_link.click()
        self.personal_linkModal.wait_presense()
        self.personal_linkText.find()
        link_text = self.personal_linkText.get_text()
        self.copy_button.wait_presense()
        time.sleep(2)
        self.copy_button.click()
        copied_text = pyperclip.paste()
        print(link_text)
        print(copied_text)
        assert link_text == copied_text, 'The link is not same each other'
        
        main_window = driver.current_window_handle
        self.redirect_button.wait_to_become_clickable()
        self.redirect_button.click()
        driver.implicitly_wait(10)
        new_window = driver.window_handles[-1]
        time.sleep(2)
        driver.switch_to.window(new_window)
        try:
       
            assert self.payment_name.is_clickable()
            assert self.payment_name_mobile.is_clickable()

        except TimeoutException:
            # Handle the case when the element is not found within 20 seconds
            print("Element with ZP.id not found within the given time.")

        except AssertionError as e:
            # Handle the case when the assertion fails
            print(f"Assertion failed: {e}")

        except Exception as e:
            # Handle any other exceptions
            print(f"An error occurred: {e}")
        time.sleep(3)

        driver.switch_to.window(main_window)
        self.closemodal_button.click()
    def allTransactionCheck(self, driver):
        self.observe_all_transaction.wait_presense()
        self.observe_all_transaction.click()        
        time.sleep(3)
        expected_url = "https://next.zarinpal.com/beta/panel/automation_zarin.com/session"
        current_url = driver.current_url
        assert current_url == expected_url, f"Expected URL to be {expected_url} but got {current_url}"
        self.dashboard_btn.click()

        
    def allreconciliationCheck(self,driver):
        self.sidbar.find()
        self.dashboard_btn.wait_presense()
        self.dashboard_btn.click()
        self.observe_all_transaction.wait_presense()
        self.observe_all_reconciliation.click()
        time.sleep(3) #for demo


        expected_url = "https://next.zarinpal.com/beta/panel/automation_zarin.com/reconciliation"
        current_url = driver.current_url
        assert current_url == expected_url, f"Expected URL to be {expected_url} but got {current_url}"
        self.dashboard_btn.click()



class zarinpalProduct(Page):
    def __init__(self, driver):
     
        self.sidbar = Element(
            driver, '//*[@id="sidebar"]'
        )
        self.product_btn = Button(
            driver, '//*[@id="sidebar"]//button//div[span[text()="محصولات"]]'
        )
        self.status_pr = Button(
            driver, '//div[@class="root__row--default"][1]//p'
        )
        self.main_card = Box(
            driver, '//div[@class="card"]'
        )
        self.create_btn = Button(
            driver, '//button//span[text()="ایجاد محصول"]'
        )
        self.saveEdit = Button(
            driver, '//button//span[text()="ذخیره"]'
        )
        self.firstItem_dot = Box(
            driver, '//div[@class="root__row--default"][1]//i[contains(@class, "icon-DotsMenu")]'
        )
        self.firstItem_copy = Button(
            driver, '//div[@class="root__row--default"][1]//div[contains(@class, "card")]//span[text()="کپی لینک پرداخت"]'
        )
        self.firstItem_Id = Text(
            driver, '//div[@class="root__row--default"][1]//span[contains(@class, "text-text-soft")]'
        )
        self.firstItem_grid = Box(
            driver, '//div[@class="root__row--default"][1]//div[@class="root__row__rows"][1]'
        )
        self.penedit_firstItem = Image(
            driver, '//div[@class="root__row--default"][1]//div[@class="anime"]//i[contains(@class, "icon-PenEdit")]'
        )
        self.prmodal = Box(
            driver, '//div[@class="root__row--default"][1]//div[contains(@class, "card")]'
        )
        self.sharePr_firstItem = Button(
            driver, '//div[@class="root__row--default"][1]//div[contains(@class, "card")]//span[text()="اشتراک‌گذاری"]'
        )
        self.transactionPr = Button(
            driver, '//div[@class="root__row--default"][1]//div[contains(@class, "card")]//span[text()="تراکنش‌ها"]'
        )
        self.activationPr_firstItem = Button(
            driver, '//div[@class="root__row--default"][1]//div[contains(@class, "card")]//span[text()="غیرفعال کردن لینک پرداخت"]'
        )
        self.deactivationPr_firstItem = Button(
            driver, '//div[@class="root__row--default"][1]//div[contains(@class, "card")]//span[text()="فعال کردن لینک پرداخت"]'
        )
        self.firstItem_grid_name = Text(
            driver, '//div[@class="root__row--default"][1]//span[contains(@class, "truncate")]'
        )
        self.get_firstPr_name = Text(
            driver, '//*[@id="app"]//div[contains(@class, "product-card-title")]'
        )
        self.title_input = PlainInput(
            driver, '//*[@id="title"]'
        )
        self.amout_input = PlainInput(
            driver, '//*[@id="amount"]'
        )
        self.description_input = PlainInput(
            driver, '//*[@id="description"]'
        )
        self.final_create_btn = Button(
            driver, '//button//span[text()="ایجاد محصول"]'
        )
        self.payform_name = PlainInput(
            driver, '//*[@id="app"]//form//div[contains(@class, "input-group") and .//div[contains(text(), "نام و نام‌خانوادگی")]]//input[contains(@class, "text-input")]'
        )
        self.payform_mob = PlainInput(
            driver, '//*[@id="app"]//form//div[contains(@class, "input-group") and .//div[contains(text(), "شماره موبایل")]]//input[contains(@class, "text-input")]'
        )
        self.payform_email = PlainInput(
            driver, '//*[@id="app"]//form//div[contains(@class, "input-group") and .//div[contains(text(), "آدرس ایمیل")]]//input[contains(@class, "text-input")]'
        )
        self.payform_desc = PlainInput(
            driver, '//*[@id="app"]//form//div[contains(@class, "input-group") and .//div[contains(text(), "توضیحات سفارش")]]//textarea[contains(@class, "text-input")]'
        )
        self.payform_sub = Button(
            driver, '//*[@id="app"]//button[contains(., "پرداخت")]'
        )
        self.payform_placholderatt = Text(
            driver, '//*[@id="app"]//div[contains(@class, "product-card-price")]'
        )
        self.cancel_paypage = Button(
            driver, '//*[@id="Cancel"]'
        )
        self.cancelModal_paypage = Box(
            driver, '/html/body/div[2]/div/div[3]'
        )
        self.cancelpayBtn_paypage = Button(
            driver, '/html/body/content/div/div/section[2]/div/div[3]/div[2]/button'
        )
        self.cancelmassege_modal = Box(
            driver, '//div[contains(@class, "receipt-card-body")]'
        )
        self.receiptMerchantName = Text(
            driver, '//div[contains(@class, "terminal-name")]'
        )
        self.receiptMessage = Text(
            driver, '//div[@class="error-description"]/div'
        )
        self.emptyTransactionPr = Text(
            driver, '//div[@class="root__title"]'
        )
        self.trueTransactionPr = Button(
            driver, '//div[@class="root__row--default"][1]//p[text()="پرداخت موفق"]'
        )
        self.desTransactionPr = Text(
            driver, '//i[@class="icon-ArrowTopLeft"]'
        )
        super().__init__('automation_zarin.com/product', self.product_btn)

    def tapPr(self, driver):
        current_url = driver.current_url
        target_url = "https://next.zarinpal.com/beta/panel/automation_zarin.com/product?page=1&pageSize=15"

        
        if current_url == target_url:
            return
        else:
            self.product_btn.click()

    def createPr(self):
        self.product_btn.click()
        self.create_btn.wait_to_become_clickable()
        time.sleep(5)
        self.create_btn.click()
        self.title_input.wait_presense()
        time.sleep(2)
        random_string = generate_random_string(10)
        self.title_input.click_enter_string(random_string)
        time.sleep(2)
        self.amout_input.wait_presense()
        self.amout_input.click_enter_string('10000')
        time.sleep(2)
        self.description_input.wait_presense()
        self.description_input.click_enter_string(random_string)
        time.sleep(2)
        self.final_create_btn.wait_to_become_clickable()
        time.sleep(2)

        self.final_create_btn.click()
        self.firstItem_grid.wait_presense()
        name = self.firstItem_grid_name.get_text()
        assert name == random_string , 'name is not same with echother'
        time.sleep(5) #time sleep for demo

    def updatePr(self, driver):
        self.firstItem_grid.wait_presense()
        element_to_hover = self.firstItem_dot.find()
        actions = ActionChains(driver)
        # Perform the hover action
        actions.move_to_element(element_to_hover).perform()
        self.penedit_firstItem.wait_presense()
        time.sleep(2)

        self.penedit_firstItem.click()
        time.sleep(3) #for Demo
        editrandom_string = generate_editrandom_string(10)
        time.sleep(2)

        self.title_input.clear_input(10)
        time.sleep(2)

        self.title_input.click_enter_string(editrandom_string)
        time.sleep(2)

        self.description_input.clear_input(10)
        time.sleep(2)

        self.description_input.click_enter_string(editrandom_string)
        time.sleep(2)

        self.saveEdit.wait_to_become_clickable()
        self.saveEdit.click()
        self.firstItem_grid.wait_presense()

        name = self.firstItem_grid_name.get_text()
        assert name == editrandom_string , 'name is not same with echother'

    def paylinkPr(self,driver):
        self.product_btn.click()
        time.sleep(2)

        self.firstItem_grid.wait_presense()
        time.sleep(2)

        main_window = driver.current_window_handle
        name = self.firstItem_grid_name.get_text()
        time.sleep(2)

        element_to_hover = self.firstItem_dot.find()
        actions = ActionChains(driver)
        # Perform the hover action
        actions.move_to_element(element_to_hover).click().perform()
        self.firstItem_copy.click()
        time.sleep(2)

        prLink = pyperclip.paste()
        driver.execute_script("window.open('');")
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)
        driver.get(prLink)
        time.sleep(2)
        prName = self.get_firstPr_name.get_text()
        assert name == prName , 'prName is not same with first product name'
        amount = self.payform_placholderatt.get_text()
        time.sleep(2)
        print(amount)
        assert amount == '10,000 ریال'
        time.sleep(2)
        self.payform_name.click_enter_string('ایمان عطاری')
        self.payform_mob.click_enter_string('09016797633')
        time.sleep(2)

        self.payform_email.click_enter_string('imanattary@gmail.com')
        time.sleep(2)

        self.payform_desc.click_enter_string('تست اتومیشن برای پرداخت محصول')
        time.sleep(2)

        self.payform_sub.click()
        time.sleep(5) # For Demo
        # self.cancel_paypage.click()
        # time.sleep(2)

        self.cancelpayBtn_paypage.wait_to_become_clickable()
        time.sleep(2)

        self.cancelpayBtn_paypage.click()
        time.sleep(2) # For Demo
        self.cancelmassege_modal.is_present()
        receiptMerchantName = self.receiptMerchantName.get_text()
        time.sleep(2)

        print(receiptMerchantName)
        assert receiptMerchantName == 'اتومیشن زرین پال', 'merchant name is not equal with value'
        receiptMessage = self.receiptMessage.get_text()
        time.sleep(2)

        assert receiptMessage == 'در صورتی که مبلغ از حساب شما کسر شده باشد، حداکثر ظرف مدت ۷۲ ساعت به حساب شما برگشت داده می‌شود. در صورت وجود هرگونه مشکل می‌توانید با شماره ۰۲۱۴۱۲۳۹ تماس حاصل فرمایید.' , 'merchant message is not equal with value'
        driver.switch_to.window(main_window)

    # def shareFunc(self, driver):
    #     driver.refresh()
    #     self.firstItem_grid.wait()
    #     element_to_hover = self.firstItem_dot.find()
    #     actions = ActionChains(driver)
    #     # Perform the hover action
    #     actions.move_to_element(element_to_hover).click().perform()
    #     self.sharePr_firstItem.click()
    
    def activationPr(self, driver):
        self.firstItem_grid.wait()
        element_to_hover = self.firstItem_dot.find()
        actions = ActionChains(driver)
        # Perform the hover action
        actions.move_to_element(element_to_hover).click().perform()
        self.activationPr_firstItem.click()
        time.sleep(2)

    def deActivationPr(self, driver):
        self.firstItem_grid.wait()
        element_to_hover = self.firstItem_dot.find()
        actions = ActionChains(driver)
        # Perform the hover action
        actions.move_to_element(element_to_hover).click().perform()
        self.deactivationPr_firstItem.click()
        time.sleep(2)


    def checkAcStatus(self):
        self.firstItem_grid.wait()
        st = self.status_pr.get_text()
        assert st == 'فعال' , 'the status text is not Active'

    def checkDeStatus(self):
        self.firstItem_grid.wait()
        st = self.status_pr.get_text()
        assert st == 'غیرفعال' , 'the status text is not Deactive'

    def transActionPr(self, driver):
        self.firstItem_grid.wait()
        prId = self.firstItem_Id.get_text().split('#')[1]
        print(prId)
        element_to_hover = self.firstItem_dot.find()
        actions = ActionChains(driver)
        # Perform the hover action
        actions.move_to_element(element_to_hover).click().perform()
        self.transactionPr.click()
        try:
            # Check if empty transaction message exists
            self.emptyTransactionPr.find()  # Attempt to find the empty transaction element
            assert_url = f'https://next.zarinpal.com/beta/panel/automation_zarin.com/session?relation_id={prId}&status=ACTIVE'
            assert driver.current_url == assert_url, 'The current URL is not the same as your expected URL'
            
            emptyText = self.emptyTransactionPr.get_text()  # Get the text of the empty transaction element
            assert emptyText == 'نتیجه‌ای یافت نشد', 'The text message is not correct with the expected result'
            
        except:
            # If no empty transaction message is found, proceed with the transaction process
            self.trueTransactionPr.wait_presense()  # Wait for the presence of a valid transaction
            self.trueTransactionPr.click()          # Click on the transaction
            self.desTransactionPr.wait_presense()   # Wait for the presence of the description
            self.desTransactionPr.click()           # Click on the description
            
            # Assert that the URL matches the expected product URL
            assert_url = f'https://next.zarinpal.com/beta/panel/automation_zarin.com/product?productId={prId}'
            assert driver.current_url == assert_url, 'The current URL is not the same as the expected product URL'
                        

# class productShareModal(Modal):
#     def __init__(self, driver):
#         self.shareModal = Element(
#            driver,  '//*[@id="modal-container"]'
#         )
#         self.shareLink = Text(
#            driver,  '//*[@id="modal-container"]//span[@class="clip-board__main--link"]'
#         )
#         self.copyLink = Button(
#            driver,  '//*[@id="modal-container"]//i[@class="icon-Copy opacity-100"]'
#         )
#         self.closeModal_btn = Button(
#             driver, '//*[@id="modal-container"]//i[@class="icon-Close opacity-100"]'
#         )
#         super().__init__(self.shareModal)

#     def checkShareLink(self):
#         self.shareModal.wait()
#         sharelink = self.shareLink.get_text()
#         print(sharelink)
#         self.copyLink.click()
#         copiedLink = pyperclip.paste()
#         assert sharelink == copiedLink , 'share link is not correct'
#         self.closeModal_btn.click()
        

class productAcivationLinkModal(Modal):
    def __init__(self, driver):
        self.deactiveModal = Element(
           driver,  '//*[@id="modal-container"]'
        )
        self.successChanges = Button(
           driver,  '//*[@id="modal-container"]//span[text()="تایید"]'
        )
        self.cancelChanges = Button(
           driver,  '//*[@id="modal-container"]//span[text()="انصراف"]'
        )
        self.closeModal_btn = Button(
            driver, '//*[@id="modal-container"]//i[contains(@class, "icon-Close")]'
        )
        super().__init__(self.deactiveModal)

    def checkActivationLink(self):
        self.deactiveModal.wait()
        self.successChanges.click()
    

    
class zarinpalTerminalModal(Modal):
    def __init__(self, driver):
        self.terminal_icoc = Box(
            driver, '//*[@id="sidebar"]//div[@class="terminal-section"]'
        )
        self.terminal_section = Box(
            driver, '//*[@id="sidebar"]//div[@class="tippy-content"]'

        )
        self.terminal_content = Box(
            driver, '//*[@id="sidebar"]//div[contains(@class, "overflow-auto")]'
        )
        self.terminals = Box(
            driver, '//*[@id="sidebar"]//div[contains(@class, "overflow-auto")]/div'
        )
        self.zarinlink = Text(
            driver, '//*[@id="sidebar"]//div[text()="زرین پال اتومیشن"]'
        )
        self.fiboteamname = Text(
            driver, '//div[contains(@class, "heading-title")]'
        )
        super().__init__(self.terminal_icoc)

    def getTerminalList(self):
        self.terminal_icoc.click()
        assert self.terminals.is_present() , 'terminals list '

    def scrollAndSelectTerminal(self, driver):
        element = self.zarinlink.find()
        if not element:
            raise Exception("Element not found for scrolling into view.")
        
        # Scroll into view and highlight the element
        driver.execute_script(
            """
            arguments[0].style.border='5px solid green';
            """, 
            element
        )
        time.sleep(3)
        self.zarinlink.click()
        time.sleep(3)
        name = self.fiboteamname.get_text().split('پیشخوان ')[1]
        assert name == 'زرین پال اتومیشن' , print(name)
        assert driver.current_url == 'https://next.zarinpal.com/beta/panel/zarinp.al%2Fautomation_zarinpal/dashboard'

class zarinpalCouponPage(Page):
    def __init__(self, driver):
        self.sidbar = Element(
            driver, '//*[@id="sidebar"]'
        )
        self.coupon_btn = Button(
            driver, '//*[@id="sidebar"]//button//div[span[text()="کد‌های تخفیف"]]'
        )
        self.create_btn = Button(
            driver, '//*[@id="__nuxt"]//span[text()="ایجاد کد تخفیف"]'
            
        )
        self.update_btn = Button(
            driver, '//*[@id="__nuxt"]//span[text()="ذخیره"]'
        )
        self.random_btn = Button(
            driver, '//*[@id="__nuxt"]//span[text()="تولید کد تصادفی"]'
        )
        self.id = PlainInput(
            driver, '//*[@id="code"]'
        )
        self.discount_percent = PlainInput(
            driver, '//*[@id="discount_percent"]'
        )
        self.first_tb_row = Box(
            driver, '//*[@id="__nuxt"]//div[@class="root__row--default"][1]'
        ) 
        self.first_tb_item = Box(
            driver, '//div[contains(@class, "root__row--default")][1]//div[contains(@class, "text-text") and contains(@class, "b2")]'
        )
        self.firstItem_dot = Box(
            driver, '//div[@class="root__row--default"][1]//i[contains(@class, "icon-DotsMenu")]'
        )
        self.penedit_firstItem = Image(
            driver, '//div[@class="root__row--default"][1]//div[@class="anime"]//i[contains(@class, "icon-PenEdit")]'
        )
        self.firstItem_copy = Button(
            driver, '//div[@class="root__row--default"][1]//div[@class="anime"]//i[contains(@class, "icon-Copy")]'
        )
        self.first_tb_percent = Box(
            driver, "//div[@class='root__row--default'][1]//div[contains(@class, 'text-text') and contains(@class, 'b3')]//span[1]"
        )
        self.activationCoupon_firstItem = Button(
            driver, '//div[@class="root__row--default"][1]//div[contains(@class, "card")]//span[text()="غیرفعال کردن"]'
        )
        self.deactivationCoupon_firstItem = Button(
            driver, '//div[@class="root__row--default"][1]//div[contains(@class, "card")]//span[text()="فعال کردن"]'
        )
        self.status_coupon = Button(
            driver, '//*[@id="__nuxt"]//div[@class="root__row--default"][1]//p'
        )
        super().__init__('automation_zarin.com/coupon', self.coupon_btn)


    def entercouponPage(self,driver):
        self.sidbar.wait()
        current_url = driver.current_url
        target_url = "https://next.zarinpal.com/beta/panel/automation_zarin.com/coupon"

        
        if current_url == target_url:
            return
        else:
            self.coupon_btn.click()

    def createCoupon(self):
        try:
            self.first_tb_row.wait_presense()
            perv_name = self.first_tb_item.get_text()
            self.create_btn.wait_to_become_clickable()
            self.create_btn.click()
            time.sleep(2)
            self.random_btn.click()
            self.discount_percent.wait_presense()
            self.discount_percent.click()
            self.discount_percent.enter_string('12')
            time.sleep(2)
            self.create_btn.click()
            time.sleep(2)
            self.first_tb_row.wait()
            new_name = self.first_tb_item.get_text()
            assert new_name!= perv_name , 'The Coupon name is not new'
        except (TimeoutException, NoSuchElementException):
            # If modal is not found or not visible, continue without interaction
            print("There isn't any created coupon")
            time.sleep(2)
            self.create_btn.wait_to_become_clickable()
            self.create_btn.click()
            time.sleep(2)
            self.random_btn.click()
            self.discount_percent.wait_presense()
            self.discount_percent.click()
            self.discount_percent.enter_string('12')
            time.sleep(2)
            self.create_btn.click()
            time.sleep(2)
            self.first_tb_row.wait_presense()
            new_name = self.first_tb_item.get_text()
            assert new_name == str
            
    def updateCoupon(self, driver):
        self.first_tb_row.wait_presense()
        perv_percent = self.first_tb_percent.get_text().split('درصد')[-2]
        element_to_hover = self.firstItem_dot.find()
        actions = ActionChains(driver)
        # Perform the hover action
        actions.move_to_element(element_to_hover).perform()
        time.sleep(2)
        self.penedit_firstItem.wait_presense()
        self.penedit_firstItem.click()
        time.sleep(5)
        self.discount_percent.click()
        self.discount_percent.clear_input(2)
        self.discount_percent.enter_string('10')
        time.sleep(2)
        self.update_btn.click()
        self.first_tb_item.wait_presense()
        new_percent = self.first_tb_percent.get_text().split('درصد')[-2]
        assert new_percent != perv_percent , 'The coupon is not updated'

    def checkCopylink(self, driver):
        self.first_tb_row.wait_presense()
        time.sleep(5)
        perv_name = self.first_tb_item.get_text()
        element_to_hover = self.firstItem_dot.find()
        actions = ActionChains(driver)
        actions.move_to_element(element_to_hover).perform()
        time.sleep(5)
        self.firstItem_copy.click()
        time.sleep(1)
        copied_text = pyperclip.paste()
        print(copied_text)
        print(perv_name)
        assert perv_name == copied_text , 'The copied coupon Link is not same with main coupon link'

    
    def activationCoupon(self, driver):
        self.first_tb_item.wait()
        element_to_hover = self.firstItem_dot.find()
        actions = ActionChains(driver)
        # Perform the hover action
        actions.move_to_element(element_to_hover).click().perform()
        self.activationCoupon_firstItem.click()

    def deActivationCoupon(self, driver):
        self.first_tb_item.wait()
        element_to_hover = self.firstItem_dot.find()
        actions = ActionChains(driver)
        # Perform the hover action
        actions.move_to_element(element_to_hover).click().perform()
        self.deactivationCoupon_firstItem.click()

    def checkAcStatus(self):
        self.first_tb_item.wait_presense()
        st = self.status_coupon.get_text()
        time.sleep(2)
        assert st == 'فعال' , 'the status text is not Active'

    def checkDeStatus(self):
        self.first_tb_item.wait_presense()
        st = self.status_coupon.get_text()
        time.sleep(2)
        assert st == 'غیرفعال' , 'the status text is not Deactive'
        
class couponActivationkModal(Modal):
    def __init__(self, driver):
        self.modal = Element(
           driver,  '//*[@id="modal-container"]'
        )
        self.successChanges = Button(
           driver,  '//*[@id="modal-container"]//span[text()="ذخیره"]'
        )
        self.cancelChanges = Button(
           driver,  '//*[@id="modal-container"]//span[text()="انصراف"]'
        )
        self.closeModal_btn = Button(
            driver, '//*[@id="modal-container"]//i[contains(@class, "icon-Close")]'
        )
        self.deactSuccess = Button(
            driver, '//*[@id="modal-container"]//span[text()="بله، غیرفعال شود"]'
        )
        super().__init__(self.modal)

    def tapactiv(self):
        self.modal.wait()
        self.successChanges.click()

    def tapdeactive(self):
        self.modal.wait()
        self.deactSuccess.click()

class reconciliationPage(Page):
    def __init__(self, driver):
        self.sidbar = Element(
            driver, '//*[@id="sidebar"]'
        )
        self.reconciliation_btn = Button(
            driver, '//*[@id="sidebar"]//button//div[span[text()="تسویه‌حساب‌"]]'
        )
        self.recon_list = Box(
            driver, '//div[@class="root__row--default"]'
        )
        self.recon_list_item = Text(
            driver, '//div[@class="root__row--default"][1]//div[@class="cursor-pointer root__row__rows"]//span[contains(@class, "truncate")]'
        )
        self.check_recon_item = Text(
            driver, '//div[text()="شناسه‌ ارجاع بانکی"]/following-sibling::div'
        )
        self.empty_recon_list = Text(
            driver, '//*[@id="__nuxt"]//div[@class="root__description"]'
        )
        self.add_not = Button(
            driver, '*//button//i[contains(@class, "icon-Plus")]'
        )
        self.edit_not = Button(
            driver, '*//button//i[contains(@class, "icon-PenEdit")]'
        )
        self.delete_note = Button(
            driver, '//i[contains(@class, "icon-Trash")]'
        )
        self.textarea = PlainInput(
            driver, '//textarea[@id="note"]'
        )
        self.saved_note = Text(
            driver, '//div[@class="time-line__main--title"]'
        )
        self.save_note_button = Button(
            driver, '//span[text()="ذخیره"]'
        )
        super().__init__("automation_zarin.com/reconciliation",self.reconciliation_btn)

    def enterreconciliationPage(self,driver):
        self.sidbar.wait()
        current_url = driver.current_url
        target_url = "https://next.zarinpal.com/beta/panel/automation_zarin.com/reconciliation"

        
        if current_url == target_url:
            return
        else:
            self.reconciliation_btn.click()
            assert driver.current_url == target_url , 'The url is not correct'


    def checkReconItem(self):
        if self.recon_list_item.is_present():
           main = self.recon_list_item.get_text()
           self.recon_list_item.click()
           check = self.check_recon_item.get_text()
           assert main == check , 'The name is not same'
        else:
            self.empty_recon_list.is_displayed()
            empty_text = self.empty_recon_list.get_text()
            assert empty_text == 'هیچ تسویه‌حسابی در این درگاه صورت نگرفته است'
            return False            
    
    def note(self):
        entered_text = 'Automation Test'
        deleted_text = len(entered_text)
        edited_text = 'Edit Automation Test'
        if self.add_not.is_present():
            self.add_not.click()
            self.textarea.click_enter_string(entered_text)
            self.save_note_button.click()
            self.edit_not.wait_presense()
            time.sleep(3)
            print(self.saved_note.get_text())
            print(entered_text)
            
            assert self.saved_note.get_text() == entered_text , 'incorrect add'
        else:
            self.edit_not.is_present()
            self.edit_not.click()
            self.textarea.clear_input(deleted_text)
            self.textarea.enter_string(edited_text)
            self.save_note_button.click()
            self.edit_not.wait_presense()
            time.sleep(2)
            print(self.saved_note.get_text())
            print(edited_text)

            assert self.saved_note.get_text() == edited_text , 'incorrect edit'

    def deleteNote(self, driver):
        entered_text = 'Automation Test'

        if self.edit_not.is_present():
            self.edit_not.click()
            time.sleep(3)
            self.delete_note.click()
            time.sleep(3)
            driver.refresh()
            assert self.add_not.is_present()
        elif self.add_not.is_present():
            self.add_not.click()
            time.sleep(3)
            self.textarea.click_enter_string(entered_text)
            time.sleep(3)
            self.save_note_button.click()
            self.edit_not.wait_presense()
            self.edit_not.click()
            time.sleep(3)
            self.delete_note.click()
            time.sleep(2)
            driver.refresh()

            assert self.add_not.is_present()
        else:
            print('your persmision is not enough for adding note')
        


            

class transactionPage(Page):
    def __init__(self, driver):
        self.sidbar = Element(
            driver, '//*[@id="sidebar"]'
        )
        self.transaction_btn = Button(
            driver, '//*[@id="sidebar"]//button//div[span[text()="تراکنش‌ها"]]'
        )
        self.trans_list = Box(
            driver, '//div[@class="root__row--default"]'
        )
        self.trans_list_item = Text(
            driver, '//div[@class="root__row--default"][1]//div[contains(@class, "cursor-pointer")][2]'
        )
        self.check_trans_item = Text(
            driver, '//div[text()="شناسه پرداخت"]/following-sibling::div'
        )
        self.empty_trans_list = Text(
            driver, '//div[@class="root__description"]'
        )
        self.add_not = Button(
            driver, '*//button//i[contains(@class, "icon-Plus")]'
        )
        self.edit_not = Button(
            driver, '*//button//i[contains(@class, "icon-PenEdit")]'
        )
        self.delete_note = Button(
            driver, '//i[contains(@class, "icon-Trash")]'
        )
        self.textarea = PlainInput(
            driver, '//textarea[@id="note"]'
        )
        self.saved_note = Text(
            driver, '//div[contains(@class, "time-line")]//div[@class="time-line__main--title"]'
        )
        self.save_note_button = Button(
            driver, '//span[text()="ذخیره"]'
        )
        super().__init__("automation_zarin.com/session",self.transaction_btn)

    def entertransactionPage(self,driver):
        self.sidbar.wait()
        current_url = driver.current_url
        target_url = "https://next.zarinpal.com/beta/panel/automation_zarin.com/session"

        
        if current_url == target_url:
            return
        else:
            self.transaction_btn.click()
            assert driver.current_url == target_url , 'The url is not correct'

    def checkTransItem(self):
        
        if self.trans_list_item.is_present():
           main = self.trans_list_item.get_text()
           self.trans_list_item.click()
           check = self.check_trans_item.get_text()

           assert main == check , 'The name is not same'
        else:
            self.empty_trans_list.is_displayed()
            empty_text = self.empty_trans_list.get_text()
            assert empty_text == 'تاکنون تراکنشی در این درگاه انجام نشده‌ است'
            return False
    
    def note(self,driver):
        entered_text = 'Automation Test'
        deleted_text = len(entered_text)
        edited_text = 'Edit Automation Test'
        if self.add_not.is_present():
            self.add_not.click()
            self.textarea.click_enter_string(entered_text)
            self.save_note_button.click()
            driver.refresh()

            self.edit_not.wait_presense()
            time.sleep(3)
            print(self.saved_note.get_text())
            print(entered_text)
            
            assert self.saved_note.get_text() == entered_text , 'incorrect add'
        else:
            self.edit_not.is_present()
            self.edit_not.click()
            self.textarea.clear_input(50)
            self.textarea.enter_string(edited_text)
            self.save_note_button.click()
            driver.refresh()

            self.edit_not.wait_presense()
            time.sleep(2)
            print(self.saved_note.get_text())
            print(edited_text)

            assert self.saved_note.get_text() == edited_text , 'incorrect edit'

    def deleteNote(self, driver):
        entered_text = 'Automation Test'

        if self.edit_not.is_present():
            self.edit_not.click()
            time.sleep(3)
            self.delete_note.click()
            time.sleep(3)
            driver.refresh()
            assert self.add_not.is_present()
        elif self.add_not.is_present():
            self.add_not.click()
            time.sleep(3)
            self.textarea.click_enter_string(entered_text)
            time.sleep(3)
            self.save_note_button.click()
            self.edit_not.wait_presense()
            self.edit_not.click()
            time.sleep(3)
            self.delete_note.click()
            time.sleep(2)
            driver.refresh()

            assert self.add_not.is_present()
        else:
            print('your persmision is not enough for adding note')