import re
import requests
from pyquery import PyQuery as pq
requests.packages.urllib3.disable_warnings()
import time
import lxml
import pandas as pd


def get(url,params=None,headers=None,proxies=None,verify=True,timeout=30,allow_redirects=True,sleep=0,try_num=0):
    try_index=0
    while True:
        try_index+=1
        # print(try_index,try_num)
        if try_num!=0 and try_index>=try_num:
            return 
        try:
            response=requests.get(url=url,params=params,headers=headers,proxies=proxies,verify=verify,timeout=timeout,allow_redirects=allow_redirects)
            response.encoding=response.apparent_encoding
            break
        except requests.exceptions.ProxyError:
            print('get——ProxyError')
            time.sleep(sleep)
            continue
        except requests.exceptions.ConnectTimeout:
            print('get——ConnectTimeout')
            time.sleep(sleep)
            continue
        except requests.exceptions.ReadTimeout:
            print('get——ReadTimeout')
            time.sleep(sleep)
            continue
        except requests.exceptions.ConnectionError:
            print('get——ConnectionError')
            time.sleep(sleep)
            continue
        except requests.exceptions.ChunkedEncodingError:
            print('get——ChunkedEncodingError')
            time.sleep(sleep)
            continue
        except ConnectionResetError:
            print('get——ConnectionResetError')
            time.sleep(sleep)
            continue
    return response


def get_teacher_info(teacher_url):
    response=get(url=teacher_url,headers=headers,timeout=30,try_num=10)
    if response==None:
        return
    try:
        html=pq(response.text)
    except lxml.etree.ParserError:
        return
    a=html('#profileContainer > div:nth-child(2) > div.profile-middle.profile-flag.col-12.col-sm-12.col-md-10.col-lg-10 > div.row.hidden-sm-down.profile-name-phone > div.col-sm-6.col-md-7.col-lg-7.name-title-column > h1').text()   
    # s1=html('#profile-content > div.row > div.col-xs-12.col-sm-12.col-md-5.col-lg-5.specialties-column > div.specialties-section.top-border > div.spec-list.attributes-top>div.col-split-xs-1.col-split-md-1>div.attribute-list.specialties-list>li:nth-child(1)').text()
    s1=html('.attribute-list.specialties-list').text()
    s1= a1+' '+ a2 +'is a professional psychologist with'

    a=a.split(' ')
    if len(a)==2:
        a1=a[0]
        a2=a[1]
    else:
        a1=a[0]
        a2=a[2]
    b=html('#profileContainer > div:nth-child(2) > div.col-12.col-sm-12.col-md-2.col-lg-2.photo-column.no-padding-right > div > div.col-8.col-sm-8.col-md-12.col-lg-12.profile-buttons-column > div > a.btn.btn-md.btn-profile.btn-default.hidden-sm-down').attr('href')
    c=html('#phone-click-reveal').text()
    d=html('.address.address-rank-1 .location-address-phone .address-data').text().replace('\n',' ')
    
    # e=html('.address.address-rank-2 .location-address-phone .address-data').text()

    e1=html('.address.address-rank-2 .location-address-phone .address-data>span[itemprop="streetAddress"]').text()
    e2=html('.address.address-rank-2 .location-address-phone .address-data>span[itemprop="addressLocality"]').text()
    e3=html('.address.address-rank-2 .location-address-phone .address-data>span[itemprop="addressRegion"]').text()
    e4=html('.address.address-rank-2 .location-address-phone .address-data>span[itemprop="postalcode"]').text()

    e5=html('.spec-subcat.attributes-language>span:nth-child(2)').text()
    if e5 == '':
        e5='English'
    else:
        e5='English; '+e5
    
    # itemprop="streetAddress"

    f=html('.spec-list.attributes-insurance').text()
    ins=re.findall(r'(?<=Plans\s)[\s\S]*', f)
    if not ins:
        f=''
    else:
        f=ins[0].replace('\n','; ')
        f=list(set(f.split('; ')))
        f='; '.join(f)

    g=html('.profile-qualifications.details-section.top-border').text()
    year=re.findall(r'(?=Years in Practice:)[\s\S]*', g)
    edu=re.findall(r'(?=School:)[\s\S]*', g)
    if not edu:
        g1=''
    else:
        g1=edu[0]
    if not year:
        g2=''
    else:
        g2=year[0]

    h=html('.profile-additional-credentials.details-section.top-border').text()

    if b==None:
        i=''
    else:
        response=get(url=b,headers=headers,timeout=30,try_num=10)
        if response==None:
            i=''
        else:
            try:
                i=re.findall('"mailto:(.*?).com"',response.text,re.S)[0]
                rex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
                a=re.match(rex, i)
                if a==None:
                    i=''
            except IndexError:
                i=''

    info=[a1,a2,b,c,d,e1,e2,e3,e4,e5,f,g1,g2,h,i,s1]
    return info



headers={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8', 'cache-control': 'max-age=0', 'cookie': 'CookieConsent={stamp:%27-1%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cver:1%2Cutc:1650510068457%2Cregion:%27US%27}; _gid=GA1.2.626432102.1650678922; _ga_5EMHF6S1M6=GS1.1.1650678920.6.1.1650679285.0; _ga=GA1.2.1986823536.1650510063; _gat_UA-2018330-4=1; _dd_s=logs=1&id=af4c11e4-4458-475e-92cb-792b64987b5e&created=1650678922199&expire=1650680178503', 'if-modified-since': 'Sat, 27 Jun 2020 11:59:34 GMT', 'referer': 'https://www.psychologytoday.com/us/therapists/ca/san-francisco?sid=6260c8ea1c68d&page=1', 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

# output_excel=r'D:\new'


info_list=[]
for page_num in range(1,10):
    # time.sleep(3)
    print('*'*80)
    print('taking page{}'.format(page_num))
    page_url='https://www.psychologytoday.com/us/therapists/ca/san-francisco?category=integrative&sid=626601d4220e2&page={}'.format(page_num)
    
    response=get(url=page_url,headers=headers,try_num=10)
    html=pq(response.text)
    divs=html('.results>div.results-row')
    # print(len(divs))
    div_index=0
    for div in divs.items():
        div_index+=1
        teacher_url=div('.results-row-info>a').attr('href')

        # time.sleep(3)
        ret=get_teacher_info(teacher_url)
        if ret==None:
            continue
        info=[teacher_url]+ret
        print(info)
        # with open(output_json,'a',encoding='utf-8') as fa:
        #     fa.write(str(info)+'\n')
        info_list.append(info)


df=pd.DataFrame(data=info_list, columns=['url','first name','last name','website','phone_number','address_line1','address_line2','city','state','zip','language','Accepted Insurance','education','years in practice','additional','email','specialties'])
df.to_csv('out.csv',index=False)



