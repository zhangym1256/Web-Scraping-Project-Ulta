import scrapy
import math
from ulta_makeup.items import UltaMakeupItem 

class UltaSpider( scrapy.Spider ):
    name = 'ulta_makeup_spider'
    allowed_domains = ['ulta.com']

    start_urls = ['https://www.ulta.com/makeup?N=26y1']

    def parse( self, response ):
        # This parse method will get the urls for all 13 skincare categories
        categories = response.xpath('//li[@class="cat-sub-nav"]/ul/li') 

        for category in categories:
            try:
                category_url = response.urljoin(category.xpath('.//a/@href').extract()[0])  
                Product_category = category.xpath('.//a/text()').extract_first().strip()         
            except Exception as e:
                print(e)
                #print('category_url, product_category!!!!'*6)
            #print(category_url)
            #print(Product_category)

            yield scrapy.Request(category_url, callback = self.parse_category_page, meta={'Product_category':Product_category}) #meta={'product_category': product_category})
            # print('+'*50,'\n')

    def parse_category_page( self, response ):
    	# This parse method will get the urls for all pages in each product category 
        Product_category = response.meta['Product_category']
        try:
            nproducts=int(response.xpath('//span[@class="search-res-number"]/text()').extract_first())
            npages = math.ceil(nproducts/96)
            next_urls = [response.url+'&No='+str(i*96) +'&Nrpp=96' for i in range(0,npages)]
        except Exception as e:
            print(e)
            #print('parse_category_page!!'*7)

        for page_url in next_urls:
            #print("!"*50, '\n')
            #print(page_url)
            yield scrapy.Request(page_url, callback = self.parse_product_page, meta={'Product_category':Product_category})

    def parse_product_page( self, response):
        # This parse method will get url for each product
        Product_category = response.meta['Product_category']
        try:
            product_containers = response.xpath('//div[@class="productQvContainer"]')
            #print(len(product_containers))
            #print('+++'*20,'\n')
        except Exception as e:
            print(e)
            #print('product_containers!!!'*4)
        
        for product in product_containers:
            
            try:
                product_url = response.urljoin(product.xpath('.//p[@class="prod-desc"]/a/@href').extract()[0]) ############
            except Exception as e:
                print(e)
                #print("product_url!!!!"*5)
            
            try:
                Product_rating = product.xpath('./a//label[@class="sr-only"]/text()').extract_first()
            except:
                Product_rating = None
                #print('Product_rating'*6)

            try:
                Tot_reviews = product.xpath('./span[@class="prodCellReview"]/a/text()').extract_first().strip()[1:]
            except:
                Tot_reviews = None
                #print('Tot_reviews!!!'*6)
            
            # print(product_url)
            # print(Product_rating)
            # print(tot_reviews)
            yield scrapy.Request(product_url, callback = self.parse_detail_page, meta={'Product_category':Product_category, 'Product_rating': Product_rating,'Tot_reviews':Tot_reviews})


    def parse_detail_page( self, response):
    	# This parse method will scrape the information from the product page
        Product_category = response.meta['Product_category']
        Product_rating = response.meta['Product_rating']
        Tot_reviews = response.meta['Tot_reviews']
        #print('SSSSS'*20)
        try:
            Product_brand = response.xpath('//p[@class="Text Text--body-1 Text--left Text--bold Text--small Text--$magenta-50"]/text()').extract_first()
            Product_name = response.xpath('//span[@class="Text Text--subtitle-1 Text--left Text--small Text--text-20"]/text()').extract_first()
            Product_price = response.xpath('//div[@class="ProductPricingPanel"]/span/text()').extract_first()
            Product_size = response.xpath('//div[@class="ProductMainSection__itemNumber"]/p/text()').extract_first()
            Product_details = response.xpath('//div[@class="ProductDetail__productContent"]/text()').extract_first()
        except Exception as e:
            print(e)
            #print("parse_detail_page!!!!!!"*8)
        #print(Product_name)
        
        item = UltaMakeupItem()

        item['Product_category'] = Product_category
        item['Product_brand']= Product_brand
        item['Product_name'] = Product_name
        item['Product_price'] = Product_price
        item['Product_size'] = Product_size
        item['Product_rating'] = Product_rating
        item['Tot_reviews'] = Tot_reviews
        item['Product_details'] = Product_details
        item['Top_category'] = 'Makeup'

        yield item


