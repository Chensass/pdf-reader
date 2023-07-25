import glob
import os
import pdfplumber
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class TextualWord:
    x0: float
    x1: float
    text: str
PagesToWords = Dict[int, List[TextualWord]]


def get_pdfs_paths_list():
    root = os.path.dirname(os.path.abspath(__file__))
    return glob.glob(os.path.join(root, 'pdfs', '*.pdf'))


def get_loaded_pdfs_list():
    pdfs_list = get_pdfs_paths_list()
    return [pdfplumber.open(pdf) for pdf in pdfs_list]


def pdf_to_dict(pdfplumber_pdf: pdfplumber.PDF) -> PagesToWords:
    text_word_by_page = []
    for page_number in range(len(pdfplumber_pdf.pages)):
        page_words = pdfplumber_pdf.pages[page_number].extract_words()
        single_sentence_info = []
        for word_info in page_words:
            single_sentence_info.append(TextualWord(x0=word_info['x0'],x1=word_info['x1'], text=word_info['text']))
        text_word_by_page.append(single_sentence_info)
    return dict(list(enumerate(text_word_by_page)))


@dataclass
class Chart():
    name: str
    dob: str
    has_valid_ekg: bool = False


def get_chart_info():
    name = None
    dob = None
    has_valid_ekg=True
    pdfs_list = get_loaded_pdfs_list()
    for pdf in pdfs_list:
        for page_number in range(len(pdf.pages)):
            page_words = pdf.pages[page_number].extract_text_lines()
            for line in page_words:
                text = line['text']
                if 'Name:' in text:
                    name = text[text.rfind('Name:')+6:]
                if 'DOB:' in text:
                    dob = text[text.rfind('DOB:')+5:]
                if 'EKG' in text and 'No' in text:
                    has_valid_ekg=False
        print(Chart(
            name=name,
            dob=dob,
            has_valid_ekg=has_valid_ekg,
            )
        )


def convert_all_pdfs_to_dict():
    pdfs_list = get_loaded_pdfs_list()
    for pdf in pdfs_list:
        page_to_words = pdf_to_dict(pdfplumber_pdf=pdf)
        print(page_to_words)


if __name__ == '__main__':
    convert_all_pdfs_to_dict()
    get_chart_info()

