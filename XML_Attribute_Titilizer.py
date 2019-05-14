#!/usr/bin/env python
"""
------------------------------------------------------------------------------------------------
XML Attribute Titilizer
------------------------------------------------------------------------------------------------
Helper utility that will identify xml files in a given directory to replaces value of the attribute doc:name in Title case.

License
------------------------------------------------------------------------------------------------
Copyright 2019 NISHANTH K.R

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Disclaimer
------------------------------------------------------------------------------------------------
1) This expect that only attribute of any xml tag to be "doc:name". This will not work if the xml document contains value of any attribute or value of any tag has word "doc:name"
2) This program is tested to work on xml files only
3) Though this program can be modified to pick any other attribute names and format its value to Title case, this has not been tested for different scenarios
-------------------------------------------------------------------------------------------------
"""

import json
import re
import glob
import shutil
import os
import copy

#xml_file_path = "/home/nishanthk/Documents/My Tools/python scripts/xmlparsing/bigparser/"
#filename = "sample.xml"
#to_find = 'doc:name="'

#f = open(filename)
#line = f.readline()

def initialize_report(report_name = "report.html"):
    f = open(report_name, "w")
    f.write("<table border=\"2\">\n<tr><th>File name</th><th>Line No</th><th>Actual text</th><th>Formatted Text</th><th>Valid</th></tr>")
    f.close()

def write_report(reports, report_name = "report.html"):
    f = open(report_name, "a")
    for report in reports:
        f.write("<tr>\n")
        f.write("<td>"+report['filename']+"</td>")
        f.write("<td>"+report['line_no']+"</td>")
        f.write("<td>"+report['actual_text']+"</td>")
        f.write("<td>"+report['formatted_text']+"</td>\n")
        if (report['actual_text'] == report['formatted_text']):
            f.write("<td style=\"background-color:green;\">"+ "True" +"</td>\n")
        else:
            #print("'"+report['actual_text']+"' != '"+report['formatted_text']+"'")
            f.write("<td style=\"background-color:red;\">"+ "False" +"</td>\n")
        f.write("</tr>\n")
    f.close()

def close_report(report_name = "report.html"):
    f = open(report_name, "a")
    f.write("\n</table>")
    f.close()

def get_all_files_with_extension(path, extension='xml'):
    return glob.glob(path+"*."+extension)

def convert_camel_case_to_proper_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)

def proper_case_converter(mystr):
    return str(mystr.title())

def find_all(a_str, sub, start=0):
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

def rewrite_abbreviations(text):
    abbreviations = ["Http","Api", "Json", "Vm", "Db", "Rest", "Etl", "Csv", "Xml", "Url", "Sql"]
    #to_return = copy.deepcopy(text)
    #for word in text:
    #    for an_abbreviation in abbreviations:
    #        if (word == an_abbreviation):
    #            print(word +"=="+ an_abbreviation)
    #            to_return = to_return.replace(word, an_abbreviation.upper())
    #return to_return
    #for an_abbreviation in abbreviations:
    #    redata = re.compile(re.escape(an_abbreviation), re.IGNORECASE)
    #return redata.sub(an_abbreviation, text)
    for a_abbreviation in abbreviations:
        text = text.replace(a_abbreviation, a_abbreviation.upper())
    return text



def backup_files(input_path, backup_filename = 'backup'):
    print("Creating backup of file at :"+input_path)
    shutil.make_archive(backup_filename, 'zip', input_path)


def rename_attribute_values(filename, outputdir, attribute='doc:name="', replace = False, to_find='doc:name="'):
    reports = []
    whole_doc = ""
    f = open(filename)
    line = f.readline()
    i=1
    while line:
        found_pos = list(find_all(line, to_find))
        #print(found_pos)
        if(len(found_pos)==0):
            whole_doc = whole_doc + str(line)
        for a_pos in found_pos:
            doube_quote_pos = line.find('"', a_pos+len(to_find))
            text_to_convert = (str(line[(a_pos+len(to_find)):(doube_quote_pos)]))
            #converted_text = (convert_camel_case_to_proper_case(text_to_convert)).title()
            converted_text = rewrite_abbreviations(text_to_convert.title())
            whole_doc = whole_doc + str(line[:(a_pos+len(to_find))]) + converted_text + str(line[(doube_quote_pos):])
            reports.append({'line_no':str(i), 'actual_text': text_to_convert, 'formatted_text': converted_text, 'filename':os.path.basename(filename)})
        line = f.readline()
        i=i+1
    f.close()
    if(replace):
        f2 = open(filename,"w")
        f2.write(whole_doc)
        f2.close()
    else:
        f2 = open(outputdir+str(os.path.basename(filename)),"w")
        f2.write(whole_doc)
        f2.close()
    print("Processing complete")
    print("Writing reports")
    write_report(reports)

def main():
    with open('config.json') as json_file:
        config = json.load(json_file)
    xmlspath=config['sourceFilesPath']
    outputpath=config['outputPath']
    backup_files(xmlspath, str(outputpath)+"backup")
    print("Backup created successfully at ->"+outputpath)
    initialize_report()
    for filename in get_all_files_with_extension(xmlspath):
        print("Processing file ->"+os.path.basename(filename))
        rename_attribute_values(filename, outputpath)
    close_report()

if __name__=="__main__":
    main()
