'''
Created on 22.10.2017

@author: andreas weichslgartner
'''
import re
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *
from bibtexparser.bwriter import BibTexWriter

inputfile = "../bib/me.bib"
outputFile = "../bib/me.md"
str_convert_list = [("""{\\"a}""","ä"),
                    ("""\\"a""","ä"),
                    ("""\\"{a}""","ä"),
                    ("""{\\"o}""","ö"),
                    ("""\\"o""","ö"),
                    ("""\\"{o}""","ö"),
                    ("""{\\ss}""","ß"), 
                    ("""\\ss""","ß"),   
                    ("""{\\"u}""","ü"),
                    ("""\\"u""","ü"),
                    ("""\\"{u}""","ü"),
                    ("""\"u""","ü"),
                    ("""\\-""",""),
                    ("""\n"""," "),
                    ("""{""",""),
                    ("""}""",""),
    ]

def convert_authors(author_str):
    author_new = ""
    if "," in  author_str:
        results = re.findall("(\w+), (\w+)", author_str)
        for i,m in enumerate(results):
            author_new += "{} {}" .format(m[1], m[0])
            if i < len(results)-1:
             author_new += ", "
    else:
        author_new = author_str.replace(" and ", ",")
    return author_new
    
    
def convert_bibtex_special_char_to_unicode(bibtex_str):
    for str_tuple in str_convert_list:
        bibtex_str = bibtex_str.replace(str_tuple[0],str_tuple[1])
    
    return bibtex_str

def convert_entry(entry):
    author = convert_authors(convert_bibtex_special_char_to_unicode (entry['author'])) 
    title = convert_bibtex_special_char_to_unicode (entry['title'])
    booktitle = ""
    if 'booktitle' in entry:
        booktitle = entry['booktitle']
    elif 'journal' in entry:
        booktitle = entry['journal']
    pages = ""
    if 'pages' in entry:
        pages = entry['pages']
    if entry['ENTRYTYPE'] == 'phdthesis':
        entry_string = "<sub>Dissertation</sub>   \n{0}: **{1}.** {2}. {3}." .format(author, title, entry['school'], entry['year'])
    #'ENTRYTYPE': 'article' , inproceedings, conference, phdthesis
    elif entry['ENTRYTYPE'] == 'book':
        entry_string = "<sub>Book</sub>   \n{0}: **{1}.** Pages {2}. {3}. {4}." .format(author, title, pages, entry['publisher'], entry['year'])

    elif entry['ENTRYTYPE'] == 'article' or entry['ENTRYTYPE'] == 'ARTICLE':
        entry_string = "<sub>Journal article</sub>   \n{0}: **{1}.** {2}, pp. {3}. {4}. {5}." .format(author, title, booktitle, pages, entry['publisher'], entry['year'])

    elif entry['ENTRYTYPE'] == 'inproceedings' or entry['ENTRYTYPE'] == 'conference':
        entry_string = "<sub>Conference paper</sub>   \n{0}: **{1}.**  In {2}, pp. {3}. {4}." .format(author, title, booktitle, pages, entry['year'])
    else:
        entry_string = "{0}: **{1}.**  Pages {2}. {3}." .format(author, title, pages, entry['year'])

    if 'note' in entry:
        entry_string += " {}." .format(entry['note'])

    return entry['year'], convert_bibtex_special_char_to_unicode (entry_string)

def print_entry(entry):
    print("{} {} {}".format(entry['author'],entry['title'], entry['year']))

converted_entries ={}

with open(inputfile) as bibtex_file:
    parser = BibTexParser()
    bib_database = bibtexparser.load(bibtex_file, parser=parser)
    converted_entries = [convert_entry(entry) for entry in bib_database.entries]
    
    
#writer = BibTexWriter()   
with open(outputFile, 'w') as markdown_file:
    year_list = []
    markdown_file
    for entry in sorted(converted_entries, reverse = True):
        if entry[0] not in year_list:
            markdown_file.write("## {}\n".format(entry[0]))
            year_list.append(entry[0])
        markdown_file.write("{}\n\n".format(entry[1]))
 #   bibtexparser.dump(bib_database, bibfile)