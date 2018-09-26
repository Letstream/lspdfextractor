"""Sample Extracting data from on Windows using Firefox"""
import os
from pdfextractor.lspdfextractor import Extractor

def run():
    e = Extractor(Extractor.FIREFOX, os.getcwd() + "/drivers/linux/geckodriver.exe", False)
    e.open()
    e.load_file(os.getcwd() + "/gst.pdf")
    e.extract_data()
    e.close()