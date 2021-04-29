# AVITO_SECTION_XPATH = {
#     "section": '//a[@class="rubricator-list-item-link-12kOm"]/@href'
# }

AVITO_PAGE_XPATH = {
    "pagination": '//span[@class="pagination-item-1WyVp"]/@href',
    "apartment": '//div[@class="iva-item-titleStep-2bjuh"]//@href',
}

AVITO_APARTMENT_XPATH = {
    "title": "//span[@class='title-info-title-text'].text()",
    "price": "//span[@class='js-item-price'].text()",
    "address": "/span[@class='item-address__string'].text()",
    "parameters": "//ul[@class='item-params-list']//text()",
    "author": "//div[@class='seller-info-name']/text()",
}

# "salary": '//p[@class="vacancy-salary"]/span/text()',

