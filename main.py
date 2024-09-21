import aiohttp
import asyncio
from zipfile import ZipFile
from bs4 import BeautifulSoup
import xlwt
import requests
from xlutils.copy import copy 
from xlrd import open_workbook 
import time

def write_data_to_excel(sheet1_headers, sheet1_data, sheet2_data, re_processing = False):
    sheet2_headers = ['Year', 'Winner', 'Winner Num. of Wins', 'Loser', 'Loser Num. of Wins']
    
    if not re_processing:
        n1, n2 = 0, 0
        book = xlwt.Workbook()
        sheet1 = book.add_sheet('NHL Stats 1990-2011')
        sheet2 = book.add_sheet('Winner and Loser per Year')
        for n,k in enumerate(sheet1_headers):        
            sheet1.write(0, n, k)
        n1+=1
        
        for n,k in enumerate(sheet2_headers):        
            sheet2.write(0, n, k)
        n2+=1
    else:        
        file_path = 'excel_file.xls'
        rb = open_workbook(file_path,formatting_info=True)
        book = copy(rb)
        sheet1 = book.get_sheet(0)
        sheet2 = book.get_sheet(1)
        n1 = sheet1.last_used_row + 1
        n2 = 0

        for n,k in enumerate(sheet2_headers):        
            sheet2.write(0, n, k)
        n2+=1

    count = 0
    for n,i in enumerate(sheet1_data, n1):
        for j in range(len(i)):
            sheet1.write(n,j,i[j])
        count += 1
    n1+=count

    for k,v in sheet2_data.items():
        sheet2.write(n2,0,k)
        sheet2.write(n2,1,v.get("Winner"))
        sheet2.write(n2,2,v.get("Winner Num. of Wins"))
        sheet2.write(n2,3,v.get("Loser"))
        sheet2.write(n2,4,v.get("Loser Num. of Wins"))
        n2+=1

    book.save('excel_file.xls')

yearwise_winner_loser_dict = {}
def get_winners_losers(row_vals):
    if yearwise_winner_loser_dict.get(row_vals[1]):
        if yearwise_winner_loser_dict.get(row_vals[1]).get('Winner Num. of Wins')<int(row_vals[2]):
            yearwise_winner_loser_dict[row_vals[1]]['Winner'] = row_vals[0]
            yearwise_winner_loser_dict[row_vals[1]]['Winner Num. of Wins'] = int(row_vals[2])

        elif yearwise_winner_loser_dict.get(row_vals[1]).get('Loser Num. of Wins')>int(row_vals[2]):
            yearwise_winner_loser_dict[row_vals[1]]['Loser'] = row_vals[0]
            yearwise_winner_loser_dict[row_vals[1]]['Loser Num. of Wins'] = int(row_vals[2])
    else:
        yearwise_winner_loser_dict[row_vals[1]] = {'Winner' :  row_vals[0], 'Winner Num. of Wins' :  int(row_vals[2]), 'Loser' :  row_vals[0], 'Loser Num. of Wins' :  int(row_vals[2])}
    return yearwise_winner_loser_dict

def do_processing(responses, re_processing = False):    
    final_data = []
    for response in responses:      
        doc = BeautifulSoup(response, "html.parser")
        table = doc.select('table')[0]
        table_headers = table.find('tr').find_all('th') 
        table_headers = [i.text.strip() for i in table_headers]

        for row in table.find_all('tr'):
            columns = row.find_all('td')

            if(columns != []):
                row_vals = [columns[i].text.strip() for i in range(len(table_headers))]
                final_data.append(row_vals)                
                # get_winners_losers(columns)
                get_winners_losers(row_vals)
                
    write_data_to_excel(table_headers, final_data, yearwise_winner_loser_dict, re_processing)

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    base_url = 'https://www.scrapethissite.com/pages/forms/'
    max_requests = 10
    start_page, end_page = 1, max_requests
    response = requests.get(base_url, verify=False)
    pages = []
    if 'Next'in response.text:
        doc = BeautifulSoup(response.content, "html.parser")
        pages = [k.text.strip() for k in doc.find(class_='pagination').find_all('a') if k.text.strip() != '»']

    if len(pages)<=max_requests:
        urls = [f"{base_url}?page_num={i}" for i in range(start_page, len(pages)+1)]
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_url(session, url) for url in urls]
            responses = await asyncio.gather(*tasks)
        with ZipFile('ZipFile.zip','w') as zipped_f: 
            for i, response in enumerate(responses, start_page):      
                zipped_f.writestr(f'{i}.html', response)
        do_processing(responses)
    else:
        re_processing = False
        with ZipFile('ZipFile.zip','w') as zipped_f:             
            while end_page<=len(pages):
                urls = [f"{base_url}?page_num={i}" for i in range(start_page, end_page+1)]
                async with aiohttp.ClientSession() as session:
                    tasks = [fetch_url(session, url) for url in urls]
                    responses = await asyncio.gather(*tasks)
                for i, response in enumerate(responses, start_page):      
                    zipped_f.writestr(f'{i}.html', response)
                do_processing(responses, re_processing=re_processing)
                if end_page >= len(pages):
                    break
                start_page = end_page + 1
                end_page = end_page + max_requests
                if end_page > len(pages):
                    end_page = len(pages)
                re_processing = True

str_time = time.time()
asyncio.run(main())
print(time.time()-str_time)