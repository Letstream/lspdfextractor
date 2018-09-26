# PDF Data Extraction using Python and Selenium

**Author:** Ayush Agarwal (@thisisayush), Letstream
**License:** GNU General Public License V3

## Features

Extracting data from PDF by loading the PDF in browser and then extracting data.

- Support Headless Mode, for servers and systemd services.
- Supports Extraction using Firefox/Chrome.
- Writes all the text extracted in a ```data.txt``` file in CWD.

## Requirements

- For running in Headless Mode, install any one of the backends from https://pyvirtualdisplay.readthedocs.io/en/latest/
- Geckodriver (for firefox) and Chromedriver (for Chrome)
- Tested on xvfb backend ```sudo apt install xvfb``` and chrome/firefox on Ubuntu Server 18.04
- Tested on Non-Headless Mode in Windows 10 Chrome/Firefox.

## How to use

Import the ```Extractor``` class and initialise it with following parameters
- browser: Required, must be on of `Extractor.CHROME` or `Extractor.FIREFOX`
- executable_path: Required, must be complete absolute path to the corrosponding webdriver (chromedriver or geckodriver) executable
- headless: Default (True), whether to run in a PyVirtualDisplay or Normal Mode.


&copy; Letstream | All Rights Reserved.