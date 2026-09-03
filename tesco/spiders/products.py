from ..utils import headers, get_payload
import os
import pandas as pd
import json
import scrapy
from datetime import datetime, timedelta


class ProductsSpider(scrapy.Spider):
    name = 'products'
    cmp = []
    dup = set()
    count = 1

    def __init__(self, categories=None, output=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not categories:
            raise ValueError(
                'You must pass category IDs, e.g. -a categories="101,102,103"'
            )
        self.category_ids = [c.strip() for c in str(categories).split(',') if c.strip()]

        # -a output="path/to/file.csv" lets each AWS chunk write its own file.
        # Falls back to the old default if not given (e.g. running locally).
        self.output_path = output or f"Output/tescoie_{datetime.now().strftime('%Y%m%d')}.csv"

    def start_requests(self):
        for id in self.category_ids:
            payload = get_payload(id, 1)
            yield scrapy.Request(url="https://xapi.tesco.com/", headers=headers, method='POST',
             body=json.dumps(payload), callback=self.parse_products, dont_filter=True, meta={'id': id})

    def parse_products(self, response):
        data = json.loads(response.text)
        productItems = data[0]['data']['category']['results']
        for item in productItems:
                product = item['node']
                
                barcode = product.get('gtin')+"\t"
                tpnb = product['id']
                url = f"https://www.tesco.ie/groceries/en-IE/products/{tpnb}"
                title = product['title']
                category = product['superDepartmentName']
                if 'marketplace' in product['defaultImageUrl']:
                    print(":::Skipping Marketplace Product::: ",title)
                    continue
                department = product['departmentName']
                aisle = product['aisleName']
                price = product['sellers']['results'][0]['price']['price']
                unit_price = product['sellers']['results'][0]['price']['unitPrice']
                unit_measure = product['sellers']['results'][0]['price']['unitOfMeasure']

                item1 = item['node']
                promotions = item1['sellers']['results'][0].get('promotions', [])
                if len(promotions) > 0:
                    start_date = adjust_start_date(promotions[0]['startDate'])
                    end_date = adjust_end_date(promotions[0]['endDate'])
                    promo_dates =  start_date + " To " + end_date
                    promo = promotions[0]['description']
                else:
                    start_date = 'NA'
                    end_date = 'NA'
                    promo_dates = 'NA'
                    promo = 'NA'
                try:
                    if product['restrictions'][0]['message'] == 'Aldi Price Match':
                        aldi_price_match = 'Yes'
                    else:
                        aldi_price_match = 'No'
                except:
                    aldi_price_match = 'No'
                status = 'TRUE' if product['sellers']['results'][0]['status'] == 'AvailableForSale' else 'False'
                charges = product['charges']
                if charges:
                    deposit1 = int(charges[0]['amount'] * 100)
                    if deposit1 > 100:
                        deposit_euros = deposit1 / 100
                        deposit = f'+ €{str(deposit_euros)}0'
                    else:
                        deposit = f'+ {deposit1}c'
                else:
                    deposit = ''
                base_id = product['baseProductId']
                data1 = {
                    'Category' : department,
                    'Sub Category' : aisle,
                    'ProductDescription' : title,
                    'Barcode' : barcode,
                    'TescoProductID' : tpnb,
                    'BaseID': base_id,
                    'Price (£)' : price,
                    'Unit Price (£)' : unit_price,
                    'Unit Of Measure' : unit_measure,
                    'SpecialOffer' : promo,
                    'OfferStartDate' : start_date,
                    'OfferEndDate' : end_date,
                    'CurrentlyAvailable' : status,
                    'DateScraped' : datetime.now().strftime("%d/%m/%Y"),
                    'WebLink':url,
                    'Aldi Price Match' : aldi_price_match,
                    'Deposit' : deposit
                }
                
                if str(barcode) not in self.dup:
                    self.cmp.append(data1)
                    self.dup.add(str(barcode))
                    print(f"{self.count}: Scraping :: {title}")
                    self.count += 1
                else:
                    pass

        page_info = data[0]['data']['category']['pageInformation']
        offset = page_info['offset']
        count = page_info['count']
        total = page_info['totalCount']

        if offset + count < total:
            page = page_info['pageNo'] + 1
            url = response.url
            payload = get_payload(response.meta['id'],page)
            yield scrapy.Request(url, method='POST', headers=headers, body=json.dumps(payload), callback=self.parse_products,dont_filter=True,meta={'id':response.meta['id']})
        else:
            return

    def closed(self, reason):
        out_dir = os.path.dirname(self.output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)
        df = pd.DataFrame(self.cmp)
        if not df.empty:
            df = df[df['Category'] != 'Marketplace']
        df.to_csv(self.output_path, index=False)
        print(f"Saved {len(df)} rows to {self.output_path}")


def adjust_start_date(start_date: str) -> str:
    dt = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
    if dt.strftime("%H") == "00":
        return dt.strftime("%d/%m/%Y")
    else:
        new_dt = dt + timedelta(days=1)
        return new_dt.strftime("%d/%m/%Y")

def adjust_end_date(end_date: str) -> str:
    dt = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ")
    if dt.strftime("%H") == "00":
        new_dt = dt - timedelta(days=1)
        return new_dt.strftime("%d/%m/%Y")
    else:
        return dt.strftime("%d/%m/%Y")
