"""Sample Extracting data from on Linux using chrome"""
import os
from pdfextractor.lspdfextractor import Extractor

def run():
    e = Extractor(Extractor.CHROME, os.getcwd() + "/drivers/linux/chromedriver.exe", True)
    e.open()
    e.load_file(os.getcwd() + "/gst.pdf")
    e.extract_data()
    e.close()