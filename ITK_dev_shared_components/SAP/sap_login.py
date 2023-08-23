"""This module provides a single function to open SAP GUI using the KMD Portal website."""

import os
import pathlib
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def login(user:str, password:str):
    """Open KMD Portal in Edge, login and start SAP GUI.

    Args:
        user: KMD Portal username.
        password: KMD Portal password.
    """
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get('https://portal.kmd.dk/irj/portal')
    driver.maximize_window()

    #Login
    user_field = driver.find_element(By.ID, 'logonuidfield')
    pass_field = driver.find_element(By.ID, 'logonpassfield')
    login_button = driver.find_element(By.ID, 'buttonLogon')

    user_field.clear()
    user_field.send_keys(user)

    pass_field.clear()
    pass_field.send_keys(password)

    login_button.click()

    #Opus
    mine_genveje = driver.find_element(By.CSS_SELECTOR, "div[title='Mine Genveje']")
    mine_genveje.click()

    #Wait for download and launch file
    _wait_for_download()

    driver.quit()

    #TODO: Wait for if SAP has opened

def _wait_for_download():
    """Private function that checks if the SAP .erp file has been downloaded.

    Raises:
        TimeoutError: If the file hasn't been downloaded within 5 seconds.
    """
    downloads_folder = str(pathlib.Path.home() / "Downloads")
    for _ in range(10):
        for file in os.listdir(downloads_folder):
            if file.endswith(".sap"):
                path = os.path.join(downloads_folder, file)
                os.startfile(path)
                return
            
        time.sleep(0.5)
    raise TimeoutError(f".SAP file not found in {downloads_folder}")

if __name__=="__main__":
    user, password = os.environ['Opus Login'].split(';')
    login(user, password)


