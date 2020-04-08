
import io
import pandas as pd
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import re 
from tabula import read_pdf

def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
 
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
 
        text = fake_file_handle.getvalue()
 
    # close open handles
    converter.close()
    fake_file_handle.close()
 
    if text:
        return text
 
    
    
def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
 
            text = fake_file_handle.getvalue()
            yield text
 
            # close open handles
            converter.close()
            fake_file_handle.close()
 
def extract_text(pdf_path):
    for page in extract_text_by_page(pdf_path):
        print(page)
        print()

a = extract_text_from_pdf('DistrictWiseList324.pdf')
district_wise_data = pd.DataFrame(columns = ['State','No. of districts infected',
                                             'District','Infected Count'])
states = list(pd.read_csv('states.csv')['Name'])
data = a.lower().split ('no of positive cases')[1]
indexes = {}

for state in states:
    state=state.lower()
    if state in data:
        indexes[int(data.find(state))] = state

pos = sorted(indexes.items())

for i,value in enumerate(pos):
    if i != len(pos)-1:
        data_new = data.split(value[1])[1]
        temp = data_new.split(pos[i+1][1])[0].strip()

    else:
        data_new = data.split(value[1])[1]
        temp = data_new.split('total')[0].strip()


    temp = temp.replace('*','')
    temp_no_of_districts = re.split(' +',temp)[0]
    new_temp = temp[len(temp_no_of_districts):]
    temp_infected_cases = re.findall("([0-9]+)",new_temp) 
    temp_districts = re.findall("[0-9]?([a-z ]+)[0-9]",temp)
#    print(temp_districts)
    for n,v in enumerate(temp_districts):
        district_wise_data.loc[len(district_wise_data)]= [value[1].strip(),temp_no_of_districts,v.strip(),temp_infected_cases[n].strip()]

district_wise_data.loc[district_wise_data['District'].isin(['north','south']),'Infected Count'] = district_wise_data[district_wise_data['District'] == 'parganas']['Infected Count'].values
district_wise_data.loc[district_wise_data['District'].isin(['north']),'District'] = ['north 24 parganas']
district_wise_data.loc[district_wise_data['District'].isin(['south']),'District'] = ['south 24 parganas']
district_wise_data = district_wise_data[district_wise_data['District']!='parganas']

district_wise_data.to_csv('districts_wise_data.csv',index=False)
