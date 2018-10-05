"""
PDF Data Extraction Using Selenium and Python.
Author: Ayush Agarwal (thisisayush), Letstream
"""
# Standard Libraries
import os
import time

# Selenium Classes
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# For headless working
from pyvirtualdisplay import Display

class Extractor(object):

    CHROME = "chrome"
    FIREFOX = "firefox"

    class InvalidBrowserError(Exception):
        pass
    
    class _page_is_loaded(object):
        def __init__(self, page):
            self.page = page
        
        def __call__(self, driver):
            if self.page.get_attribute('data-loaded') == None:
                return False
            return self.page

    def __init__(self, browser, executable_path=None, headless=True):
        self.browser = browser
        self.executable_path = executable_path

        self.headless = headless
        self.display = None
        self.driver = None
    
    def open(self):
        self.open_driver()

    def open_driver(self):
        """Start Virtual Display and Browser Instance"""
        if self.headless:
            self.start_virtual_display()
        
        if self.browser == self.CHROME:
            self.driver = webdriver.Chrome(self.executable_path)
        elif self.browser == self.FIREFOX:
            self.driver = webdriver.Firefox(self.executable_path)
        else:
            raise self.InvalidBrowserError(self.browser)

    def load_file(self, path):
        """Load File in browser using file:// Protocol"""
        self.load_url("file://%s" % path)

    def load_url(self, url):
        """Load URL in browser"""
        self.driver.get(url)
    
    def extract_data(self):
        """Extract Data using Firefox/Chrome"""
        if self.browser == self.CHROME:
            return self.extract_data_chrome()
        elif self.browser == self.FIREFOX:
            return self.extract_data_firefox()
        else:
            raise self.InvalidBrowserError(self.browser)
    
    def driver_wait(self, secs):
        """Explicity Wait for Few Seconds"""
        time.sleep(secs)

    def extract_data_firefox(self):
        """Extract Data using Firefox"""
        try:
            # Wait for initial page to load
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "page")))

            # Select all Pages
            pages = self.driver.find_elements_by_class_name('page')
            
            # Iterate through all pages, extracting data on the go
            for page in pages:
                # Check for data-loaded attribute in page
                while page.get_attribute('data-loaded') != "true":
                    try:
                        # Explicity Scroll page to load the page
                        ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
                        # Wait while page is loaded
                        WebDriverWait(self.driver, 10).until(self._page_is_loaded(page))
                        # Explicity Scroll page to load the next page
                        ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
                    except TimeoutException:
                        # Just in case, page is struck in between
                        ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
                
                # Wait while the content is loaded
                while len(page.text) == 0:
                    self.driver_wait(0.5)
                
                # Write current page content to file
                self.write_to_file(page.text, True)
        
        except TimeoutError:
            print("Timeout Occured: %s" % e)

    def extract_data_chrome(self):
        """Extract PDF using Chrome"""
        try:
            # Wait for PDF plugin to load the PDF
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "plugin")))

            # Explicity wait for PDF to load completely
            self.driver_wait(10)

            # Select the plugin element
            plugin = self.driver.find_element_by_id("plugin")    
            
            # Select all text
            ActionChains(self.driver).click(on_element=plugin).perform()
            ActionChains(self.driver).key_down(Keys.CONTROL).key_down('A').key_up('A').key_up(Keys.CONTROL).perform()

            # Explicity Wait 10 seconds incase of large file
            self.driver_wait(10)

            # Copy the text to clipboard
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
            
            # Explicity Wait 5 seconds incase of large file
            self.driver_wait(5)
            
            # Load the Text Extraction URL
            self.load_file(os.getcwd() + "/html/paste.html")

            # Wait for page to load and id:main to appear
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "main")))

            # Select the id:main textarea
            c = self.driver.find_element_by_id("main")
            
            # Focus and Paste the text to Main
            ActionChains(self.driver).click(c).perform()
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys_to_element(c, 'v').key_up(Keys.CONTROL).perform()

            # Explicity Wait 5 seconds incase of large file
            self.driver_wait(5)
            
            # Locate and click the Submit btn to make text extractable
            p = self.driver.find_element_by_id("submit")
            ActionChains(self.driver).click(on_element=p).perform()

            # Explicity Wait 5 seconds incase of large file
            self.driver_wait(5)
            
            # Write data to file
            self.write_to_file(c.text)
        
        except TimeoutError as e:
            print("Timeout Occured: %s" % e)
    
    def write_to_file(self, text, append=False):
        """Write content to file, append mode supported"""

        with open("data.txt", "a" if append else "w") as f:
            f.write(text)

    def start_virtual_display(self):
        """Starts PyVirtualDisplay Instance"""
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
    
    def close_driver(self):
        """Close Driver and Headless Virtual Display"""
        self.driver.close()

        if self.headless:
            self.display.stop()
    
    def close(self):
        self.close_driver()

    def __del__(self):
        self.close()