import logging

logger = Logger.getLogger()

def extract_txt(file_path):
    text = textract.process(file_path, method='tesseract')
    logger.info(text)