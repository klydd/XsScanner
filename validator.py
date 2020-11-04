from time import sleep

from selenium import webdriver
from selenium.common.exceptions import (NoAlertPresentException,
                                        NoSuchElementException)

firefox_path = "/usr/bin/firefox-esr"


def validator(url, seed, payload, payload_type):
    validator_type = payload_type
    with webdriver.Firefox(firefox_binary=firefox_path) as driver:
        driver.get(url)

        # Skip or validate alerts
        while True:
            try:
                alert = driver.switch_to.alert
                if seed in alert.text and validator_type == "initial":
                    return True
                alert.accept()
                sleep(0.05)
            except NoAlertPresentException:
                break

        # Shouldn't work
        if validator_type == "initial":
            return False

        elif validator_type == "linker":
            try:
                elem = driver.find_element_by_link_text(seed)
            except NoSuchElementException:
                return False

            elem.click()

            try:
                alert = driver.switch_to.alert
            except NoAlertPresentException:
                return False

            if seed in alert.text:
                return True
            return False

        else:
            print("Unknown validator type: " + validator_type)
            return False
