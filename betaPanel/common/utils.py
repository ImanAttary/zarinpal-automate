from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_by_type(driver, locator_type):
    locator_type = locator_type.lower()
    if locator_type == "id":
        return By.ID
    elif locator_type == "name":
        return By.NAME
    elif locator_type == "xpath":
        return By.XPATH
    elif locator_type == "css":
        return By.CSS_SELECTOR
    elif locator_type in ("classname", "class_name"):
        return By.CLASS_NAME
    elif locator_type in ("linktext", "link_text"):
        return By.LINK_TEXT
    else:
        print(
            "getByType error: Locator type "
            + locator_type
            + " is not correct/supported"
        )
        return False


def wait_for_element(
        driver, locator, locator_type="xpath", wait_method="visible", timeout=10, text=None
):
    try:
        by_type = get_by_type(driver, locator_type)
        wait = WebDriverWait(driver, timeout)
        if wait_method == "click":
            wait.until(EC.element_to_be_clickable((by_type, locator)))

        elif wait_method == "visible":
            wait.until(EC.visibility_of_element_located((by_type, locator)))

        elif wait_method == "invisible":
            wait.until(EC.invisibility_of_element_located((by_type, locator)))

        elif wait_method == "presence":
            wait.until(EC.presence_of_element_located((by_type, locator)))
            
        elif wait_method == "text":
            wait.until(EC.text_to_be_present_in_element(
                (by_type, locator), text))

        elif wait_method == "js_var":
            wait.until(
                lambda driver: driver.execute_script(
                    f"return {locator}") == text
            )

    except Exception as e:
        raise e


def get_js_var(driver, js_var_name: str) -> str:
    return driver.execute_script(f"return {js_var_name}")


def find_all_elements(driver, locator, locator_type="xpath"):
    by_type = get_by_type(driver, locator_type)
    return driver.find_elements(by_type, locator)
