
from Get import *
from Get_doctor_info import *


if __name__=="__main__":


    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8', 'cache-control': 'max-age=0',
    'cookie': 'CookieConsent={stamp:%27-1%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cver:1%2Cutc:1650510068457%2Cregion:%27US%27}; _gid=GA1.2.626432102.1650678922; _ga_5EMHF6S1M6=GS1.1.1650678920.6.1.1650679285.0; _ga=GA1.2.1986823536.1650510063; _gat_UA-2018330-4=1; _dd_s=logs=1&id=af4c11e4-4458-475e-92cb-792b64987b5e&created=1650678922199&expire=1650680178503',
    'if-modified-since': 'Sat, 27 Jun 2020 11:59:34 GMT',
    'referer': 'https://www.psychologytoday.com/us/therapists/ca/san-francisco?sid=6260c8ea1c68d&page=1',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"', 'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    info_list = []
    for page_num in range(1, 2):
        # time.sleep(3)
        print('*' * 80)
        print('taking page{}'.format(page_num))
        page_url = 'https://www.psychologytoday.com/us/therapists/ca/san-francisco?category=integrative&sid=626601d4220e2&page={}'.format(
            page_num)

        response = get(url=page_url, headers=headers, try_num=10)
        html = pq(response.text)
        divs = html('.results>div.results-row')
        # print(len(divs))
        div_index = 0
        for div in divs.items():
            div_index += 1
            teacher_url = div('.results-row-info>a').attr('href')

            # time.sleep(3)
            ret = get_teacher_info(teacher_url)
            if ret == None:
                continue
            info = [teacher_url] + ret
            # print(info)
            # with open(output_json,'a',encoding='utf-8') as fa:
            #     fa.write(str(info)+'\n')
            info_list.append(info)

    df = pd.DataFrame(data=info_list, columns=['url', 'first name', 'last name', 'email', 'phone_number', 'website','Accepted Insurance','Accepting New Patient','Type of appointments','address_line1',
                                            'city', 'state','zip','additional_address','city','State','zip', 'language','Article Title1','Article1','Article Title2','Article2','Article Title3','Article3','Awards/ Accolades','MedRank Analyst Comments','background','tags',
                                            'education', 'prefix','sufix','gender','Type of practice'])
    df.to_csv('out.csv', index=False)
