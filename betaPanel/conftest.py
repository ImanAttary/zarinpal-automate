import json
import time
import pyotp
import os
import pytest
import pickle
from enum import Enum
from pathlib import Path
from selenium import webdriver
from common import pages
from common.elements import (
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
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent
TESTS_DIR = BASE_DIR / 'betaPanel'
with open(TESTS_DIR / "config.json") as config:
    ALL_CONFIG = json.load(config)

resolution = ALL_CONFIG["resolution"]
sleep_pace = int(ALL_CONFIG["sleep_pace"])
close_browser_after_test = bool(ALL_CONFIG["close_browser_after_test"])
web_driver_uri = ALL_CONFIG["uri"]


uri = 'https://next.zarinpal.com/beta/'
URI = 'https://next.zarinpal.com/beta/panel/automation_zarin.com/dashboard'


directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(directory, "cookies.pkl")


@pytest.fixture(scope="session")
def web_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=old')  # اجرای بدون رابط کاربری
    options.add_argument('--no-sandbox')   # حذف محدودیت‌های sandbox
    options.add_argument('--disable-dev-shm-usage')  # استفاده از TMP برای اشتراک حافظه
    options.add_argument('--disable-gpu')  # غیرفعال کردن GPU
    options.add_argument('--disable-extensions')  # غیرفعال کردن افزونه‌ها
    options.add_argument('--disable-logging')
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome(options=options,service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    driver.implicitly_wait(15)

    # Check if cookies exist and load them
    file_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "cookies.pkl")

    if os.path.exists(file_path):
        driver.get(URI)  # Navigate to the base URI first
        cookies = pickle.load(open(file_path, "rb"))
        for cookie in cookies:
            # cookie['domain'] = 'next.zarinpal.com'

            driver.add_cookie(cookie)
        driver.refresh()  # Reload the page with the cookies applied
        driver.get(URI)  # Navigate to the base URI first
    else:
        driver.get(uri)  # If no cookies, start from the base URI

    yield driver
    driver.quit()



@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logstart(nodeid, location):
    print(f"\nStarting test: {nodeid}")

    
# generate oto for login
class OTP:
    class OtpGenerator(Enum):
        hoseinimandar = "LZZ7WRDA4GKB3UMC"  # 09128890816
        imanattary = "I3KLBSCAKPTTQENC"  # 09128036993
        imanattary_irancell = "TDVXOAJQK2TX3HMZ",  # 09016797633
        testac = "B64VEMWQVWWPNHDL",
        automtion_account = "K4F2SKEQ5LW3DSTJ" #09548036993


    @staticmethod
    def get_otp(identifier):
        return OTP.OtpGenerator[identifier].value


def zarinpal_otp_generator(identifier):
    assert identifier, "Identifier must be provided"
    otp_secret = OTP.get_otp(identifier)
    otp = pyotp.TOTP(otp_secret)
    return otp.now()



@pytest.fixture(scope="function")
def zarinpallogin_page(web_driver):
    return pages.zarinpallogin(web_driver)


@pytest.fixture(scope='function')
def welcome_modal(web_driver):
    return pages.welcomeModal(web_driver)


@pytest.fixture(scope='function')
def dashboard_page(web_driver):
    return pages.zarinpalDashboard(web_driver)

# @pytest.fixture(scope='function')
# def productShare_modal(web_driver):
#     return pages.productShareModal(web_driver)

@pytest.fixture(scope='function')
def productActivation_modal(web_driver):
    return pages.productAcivationLinkModal(web_driver)

@pytest.fixture(scope='function')
def couponActivation_modal(web_driver):
    return pages.couponActivationkModal(web_driver)


@pytest.fixture(scope='function')
def product_page(web_driver):
    return pages.zarinpalProduct(web_driver)

@pytest.fixture(scope='function')
def terminals_modal(web_driver):
    return pages.zarinpalTerminalModal(web_driver)


@pytest.fixture(scope='function')
def coupon_page(web_driver):
    return pages.zarinpalCouponPage(web_driver)

@pytest.fixture(scope='function')
def reconciliation_page(web_driver):
    return pages.reconciliationPage(web_driver)


@pytest.fixture(scope='function')
def transaction_page(web_driver):
    return pages.transactionPage(web_driver)


@pytest.fixture(scope="function")
def web_driver_in_zarinpallogin_page(zarinpallogin_page, web_driver, welcome_modal):

    zarinpallogin_page.login()

    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()

    with open(file_path, "wb") as file:
        pickle.dump(web_driver.get_cookies(), file)



    yield web_driver, zarinpallogin_page, welcome_modal


@pytest.fixture(scope='function')
def web_driver_in_personalLinkDashboard_page(dashboard_page, web_driver, welcome_modal):
    
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()


    dashboard_page.personalLink(web_driver)

    yield web_driver, dashboard_page


@pytest.fixture(scope='function')
def web_driver_in_transcActionDashboard_page(dashboard_page, web_driver, welcome_modal):
        
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()

    dashboard_page.allTransactionCheck(web_driver)

    yield web_driver, dashboard_page

@pytest.fixture(scope='function')
def web_driver_in_reconsalationDashboard_page(welcome_modal, dashboard_page, web_driver):
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()

    dashboard_page.allreconciliationCheck(web_driver)

    yield web_driver, dashboard_page

@pytest.fixture(scope='function')
def web_driver_in_createproduct_page(welcome_modal, product_page, web_driver):

    
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()


    
    product_page.createPr()

    yield web_driver, product_page

@pytest.fixture(scope='function')
def web_driver_in_updateproduct_page(welcome_modal, product_page, web_driver):
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()

    product_page.tapPr(web_driver)



    product_page.updatePr(web_driver)
 
    yield web_driver, product_page, 

@pytest.fixture(scope='function')
def web_driver_in_payoutproduct_page(welcome_modal, product_page, web_driver):
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()


    product_page.paylinkPr(web_driver)

    yield web_driver, product_page

# @pytest.fixture(scope='function')
# def web_driver_in_shareLinkproduct_page(welcome_modal, product_page, web_driver, productShare_modal):
#     welcome_modal.closeModal()
#     welcome_modal.closeChangeLogModal()
#     welcome_modal.closeOnboardModal()

#     product_page.tapPr(web_driver)


#     product_page.shareFunc(web_driver)
#     productShare_modal.checkShareLink()

#     yield web_driver, product_page , productShare_modal


@pytest.fixture(scope='function')
def web_driver_in_activationProduct_page(welcome_modal, product_page, web_driver, productActivation_modal):
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()

    product_page.tapPr(web_driver)
    product_page.checkAcStatus()
    product_page.activationPr(web_driver)
    productActivation_modal.checkActivationLink()
    time.sleep(3)
    web_driver.refresh()
    product_page.checkDeStatus()


    yield web_driver, product_page , productActivation_modal


@pytest.fixture(scope='function')
def web_driver_in_deAtivationProduct_page(welcome_modal, product_page, web_driver, productActivation_modal):

    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()

    product_page.tapPr(web_driver)

    product_page.checkDeStatus()
    product_page.deActivationPr(web_driver)
    productActivation_modal.checkActivationLink()
    time.sleep(3)
    web_driver.refresh()
    product_page.checkAcStatus()

    yield web_driver, product_page , productActivation_modal

@pytest.fixture(scope='function')
def web_driver_in_transactionProduct_page(web_driver, welcome_modal, product_page):
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()

    product_page.tapPr(web_driver)

    product_page.transActionPr(web_driver)

    yield web_driver, product_page 

@pytest.fixture(scope='function')
def web_driver_in_terminals_modal(web_driver, welcome_modal, terminals_modal):
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()

    terminals_modal.getTerminalList()
    terminals_modal.scrollAndSelectTerminal(web_driver)

    yield web_driver, terminals_modal , welcome_modal


@pytest.fixture(scope='function')
def web_driver_in_create_coupon_page(web_driver, welcome_modal, coupon_page):
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()

    coupon_page.entercouponPage(web_driver)
    coupon_page.createCoupon()


    yield web_driver, welcome_modal , coupon_page

@pytest.fixture(scope='function')
def web_driver_in_edit_coupon_page(web_driver, welcome_modal, coupon_page):
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()

    coupon_page.entercouponPage(web_driver)
    coupon_page.updateCoupon(web_driver)


    yield web_driver, welcome_modal , coupon_page


@pytest.fixture(scope='function')
def web_driver_in_activationCoupon_page(welcome_modal, coupon_page, web_driver, couponActivation_modal):
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()

    coupon_page.entercouponPage(web_driver)

    coupon_page.checkAcStatus()
    coupon_page.activationCoupon(web_driver)
    couponActivation_modal.tapdeactive()
    web_driver.refresh()
    coupon_page.checkDeStatus()


    yield web_driver, coupon_page , couponActivation_modal


@pytest.fixture(scope='function')
def web_driver_in_deAtivationCoupon_page(welcome_modal, coupon_page, web_driver, couponActivation_modal):
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()

    coupon_page.entercouponPage(web_driver)
    coupon_page.checkDeStatus()
    coupon_page.deActivationCoupon(web_driver)
    couponActivation_modal.tapactiv()
    web_driver.refresh()
    coupon_page.checkAcStatus()


    yield web_driver, coupon_page , couponActivation_modal


@pytest.fixture(scope='function')
def web_driver_in_reconciliation_page(welcome_modal, web_driver, reconciliation_page):
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()


    reconciliation_page.enterreconciliationPage(web_driver)
    if not reconciliation_page.checkReconItem():
        yield None  # بازگشت مقدار خالی برای ادامه نیافتن فرآیند
        return

    reconciliation_page.note()

    reconciliation_page.deleteNote(web_driver)


    yield web_driver, reconciliation_page


@pytest.fixture(scope='function')
def web_driver_in_transaction_page(welcome_modal, web_driver, transaction_page):
    welcome_modal.closeModal()
    welcome_modal.closeChangeLogModal()
    welcome_modal.closeOnboardModal()

    transaction_page.entertransactionPage(web_driver)
    if not transaction_page.checkTransItem():
        yield None  # بازگشت مقدار خالی برای ادامه نیافتن فرآیند
        return
        
    transaction_page.note(web_driver)
    transaction_page.deleteNote(web_driver)


    yield web_driver, transaction_page
