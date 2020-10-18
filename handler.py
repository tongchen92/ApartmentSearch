import json
import requests
from bs4 import BeautifulSoup
import boto3
from emailHandler import sendEmail

def hello(event, context):
    s3 = boto3.resource('s3')
    s3Obj = s3.Object('apartment-search', 'apartmentList.json')
    apartmentUrl = ['https://www.on-site.com/web/online_app/choose_unit?goal=6&attr=x20&property_id=286650&lease_id=0&unit_id=0&required=']

    page = requests.get(apartmentUrl[0])
    soup = BeautifulSoup(page.content, 'html.parser')

    apartmentList = json.loads(s3Obj.get()['Body'].read().decode('utf-8'))
    apartments = soup.findAll("tr", {"class": "unit_display"})

    for apt in apartments:
        if(apt['data-apartment-number'] not in apartmentList.keys()):
            sendEmail(apt)
        apartmentList[apt['data-apartment-number']] = None

    s3Obj.put(Body=(bytes(json.dumps(apartmentList).encode('UTF-8'))))
    return
