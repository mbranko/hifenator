import os
import re
import shutil
import zipfile
import tempfile
import pyphen
from docx import Document


def zip_directory(folder_path, zip_path):
    """
    Recursively traverse a folder and put everything in a zip file
    """
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        len_dir_path = len(folder_path)
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len_dir_path:])


def insert_fake_hyphens(inputfile, outputfile):
    """
    Insert fake hyphens '#@#' in a docx file. Try Serbian cyrillic hyphenation
    first, then latin hyphenation second
    """
    cyr = pyphen.Pyphen(lang='sr')
    lat = pyphen.Pyphen(lang='sr_Latn')
    document = Document(inputfile)
    for para in document.paragraphs:
        for run in para.runs:
            text = run.text
            words = re.split(r'(\S+)', text)
            for i, word in enumerate(words):
                if len(words[i].strip()) > 0:
                    hyphenated = cyr.inserted(word, '#@#')
                    if words[i] == hyphenated:
                        hyphenated = lat.inserted(word, '#@#')
                    words[i] = hyphenated
            run.text = ''.join(words)
    document.save(outputfile)


def replace_fake_hyphens(inputfile, outputfile):
    """
    Replace fake hyphens '#@#' in a docx file with real <w:softHyphen/>
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(inputfile, 'r') as zipref:
            zipref.extractall(tmpdir)
        with open(os.path.join(tmpdir, 'word/document.xml'), 'r') as reading:
            contents = reading.read()
        contents = contents.replace('#@#', '<w:softHyphen/>')
        with open(os.path.join(tmpdir, 'word/document.xml'), 'w') as writing:
            writing.write(contents)
        zip_directory(tmpdir, outputfile)
        

def hyphenate_file(inputfile, outputfile):
    """
    Hyphenate a docx file
    """
    temp = tempfile.TemporaryFile()
    insert_fake_hyphens(inputfile, temp)
    replace_fake_hyphens(temp, outputfile)
    temp.close()
