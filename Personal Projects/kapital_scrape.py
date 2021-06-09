'''
Script for scraping the text of Das Kapital from the free Marxists archive, saving each chapter to it's own text file
Meant as a test ground for NLP projects
'''

import requests
import bs4

def kapital_scrape():
    
    values = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33']
    base_url = 'https://www.marxists.org/archive/marx/works/1867-c1/ch{}.htm'
    
    for page in range(len(values)):
        
        res = requests.get(base_url.format(values[page]))
        soup = bs4.BeautifulSoup(res.text,'lxml')
        site_paragraphs = soup.select('p')
        
        f = open('Ch{}.txt'.format(values[page]),'w+',encoding='utf-8')
        
        for i in range(len(site_paragraphs)):
            f.write(site_paragraphs[i].getText())
            
        f.close()
        
kapital_scrape()
