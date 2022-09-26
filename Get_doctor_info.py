from ctypes.wintypes import tagSIZE
import email
from gettext import find
import re
from ssl import CertificateError
from sys import prefix
from tkinter import N
from tkinter.messagebox import YES
from turtle import title
import requests
from pyquery import PyQuery as pq


requests.packages.urllib3.disable_warnings()
import time
import lxml
import pandas as pd
from Get import *

def get_doctor_info(doctor_url):
    response = get(url=doctor_url, headers=headers, timeout=30, try_num=10)
    if response == None:
        return
    try:
        html = pq(response.text)
    except lxml.etree.ParserError:
        return
    a = html(
        '#profileContainer > div:nth-child(2) > div.profile-middle.profile-flag.col-12.col-sm-12.col-md-10.col-lg-10 > div.row.hidden-sm-down.profile-name-phone > div.col-sm-6.col-md-7.col-lg-7.name-title-column > h1').text()


    a = a.split(' ')
    if len(a) == 3:
        firstname = a[0]
        lastname = a[2]
    else:
        firstname = a[0]
        lastname = a[1]

    web = html(
        '#profileContainer > div:nth-child(2) > div.col-12.col-sm-12.col-md-2.col-lg-2.photo-column.no-padding-right > div > div.col-8.col-sm-8.col-md-12.col-lg-12.profile-buttons-column > div > a.btn.btn-md.btn-profile.btn-default.hidden-sm-down').attr(
        'href')
    phone = html('#phone-click-reveal').text()
    d1 = html('.address.address-rank-1 .location-address-phone .address-data').text().replace('\n', ' ')
    d2 = html('.address.address-rank-1 .location-address-phone .address-data>span[itemprop="addressLocality"]').text()
    d2=d2.replace(',','')
    d3 = html('.address.address-rank-1 .location-address-phone .address-data>span[itemprop="addressRegion"]').text()
    d4 = html('.address.address-rank-1 .location-address-phone .address-data>span[itemprop="postalcode"]').text()

    # e=html('.address.address-rank-2 .location-address-phone .address-data').text()

    e1 = html('.address.address-rank-2 .location-address-phone .address-data>span[itemprop="streetAddress"]').text()
    e2 = html('.address.address-rank-2 .location-address-phone .address-data>span[itemprop="addressLocality"]').text()
    e2=e2.replace(',','')
    e3 = html('.address.address-rank-2 .location-address-phone .address-data>span[itemprop="addressRegion"]').text()
    e4 = html('.address.address-rank-2 .location-address-phone .address-data>span[itemprop="postalcode"]').text()

    language = html('.spec-subcat.attributes-language>span:nth-child(2)').text()

    if language == '':
        language = 'English'
    else:
        language = 'English; ' + language

    # itemprop="streetAddress"

    insurance = html('.spec-list.attributes-insurance').text()
    ins = re.findall(r'(?<=Plans\s)[\s\S]*', insurance)
    if not ins:
        insurance = ''
    else:
        insurance = ins[0]
    x=str(insurance).find('Accepted')
    insurance=str(insurance)[0:x]
    if insurance[-6:]=='Networ':
        insurance=insurance.replace('Out of Networ','Out of Network')
    insurance=insurance.replace('\n','; ')


    g = html('.profile-qualifications.details-section.top-border').text()
    # year = re.findall(r'(?<=Years in Practice:)([\s\S]*)Years', g)
    edu = re.findall(r'(?=School:)([\s\S]*)\n', g)
    if not edu:
        edu = ''
    else:
        edu = edu[0]

    # if not year: #years in practice
    #     g2 = ''
    # else:
    #     g2 = year[0]

    h = html('.profile-additional-credentials.details-section.top-border').text() #certification/ certification date etc

    if web == None:
        email = ''
    else:
        response = get(url=web, headers=headers, timeout=30, try_num=10)
        if response == None:
            email = ''
        else:
            try:
                email = re.findall('"mailto:(.*?).com"', response.text, re.S)[0]
                rex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
                a = re.match(rex, email)
                if a == None:
                    email = ''
            except IndexError:
                email = ''
    # s1 = html('.attribute-list.specialties-list').text().replace('\n', '; ') #specialties
    certificate=re.findall(r'(?=Certificate:)([\s\S]*)\n?', h)
    if not certificate:
        pass
    else:
        certificate=str(certificate)[2:-1]
        x=certificate.find('\\n')
        edu=edu+'\n'+certificate[0:x]
    # certificate_date=re.findall(r'(?<=Certificate Date:)([\s\S]*)\n?', h)
    # if g2 == None or not certificate:
    #     s1=None
    # else:
    #     s1 = firstname + ' ' + lastname + ' is a professional psychologist with specialities in '+s1+' and'+g2+' years in practice.'+firstname + ' ' + lastname+' is also certified for '+str(certificate),' back in',str(certificate_date)
    gender=html('.profile-pronouns').text()
    if gender !='':
        if gender[0]=='S':
            gender='Female'
        elif gender[0]=='H':
            gender='Male'
    else:
        gender=''

    online=html('.profile-phone-online-conult.icon-online-therapy.cursor-pointer').text()
    if online=='Offers online therapy Offers online therapy':
        online_therapy='In-Person; Virtual / Video'
    else:
        online_therapy='In-Person'
    new=html('.profile-accepting-appointments.alert-profile').text()
    if new=='':
        new='Yes'
    else:
        new='No'
    
    title=html('.profile-title.contact-title').text()
    title=title.split(',')
    for i in title:
        if i in [' MD',' PhD',' PsyD']:
            prefix='Dr.'
            sufix=i
        elif i in [' MA',' MFT',' LMFT',' AMFT']:
            prefix=None
            sufix=i
        else:
            prefix=None
            sufix=None
    emp1=''
    emp2=''
    emp3=''
    emp4=''
    emp5=''
    emp6=''
    emp7=''
    emp8=''
    # if 'MD' or 'PsyD' or 'PhD' in prefix
    background=html('meta[name="description"]')
    x = str(background).find("-")
    background=str(background)[x+7:-8]
    background=background.replace("'m","'s").replace('I',lastname).replace('you','clients').replace("'ve","'s").replace('My',lastname+"'s").replace('am','is')


    tag='Psychology/ Therapist'
    practice='Integrative Medcine'
    info = [firstname, lastname,email, phone,web,insurance,new,online_therapy, d1,d2,d3,d4, e1, e2, e3, e4, language, emp1,emp2,emp3,emp4,emp5,emp6,emp7,emp8,background, tag, edu, prefix,sufix,gender,practice]
    return info

