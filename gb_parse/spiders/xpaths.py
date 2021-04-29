HH_PAGE_XPATH = {
    "pagination": '//div[@data-qa="pager-block"]//a[@data-qa="pager-page"]/@href',
    "vacancy": '//div[contains(@data-qa, "vacancy-serp__vacancy")]//'
    'a[@data-qa="vacancy-serp__vacancy-title"]/@href',
    "company": "//a[@data-qa='vacancy-company-name']/@href",
}

HH_VACANCY_XPATH = {
    "title": '//h1[@data-qa="vacancy-title"]/text()',
    "salary": '//p[@class="vacancy-salary"]/span/text()',
    "description": '//div[@data-qa="vacancy-description"]//text()',
    "skills": '//div[@class="bloko-tag-list"]//'
    'div[contains(@data-qa, "skills-element")]/'
    'span[@data-qa="bloko-tag__text"]/text()',
    "author": '//a[@data-qa="vacancy-company-name"]/@href',
}

HH_COMPANY_XPATH = {
    "name": '//div[@class="company-header"]//h1/span[@class="company-header-title-name"]/text()',
    "link": '//div[@class="employer-sidebar-content"]//a[@data-qa="sidebar-company-site"]/@href',
    "field": '//div[contains(text(), "Сферы деятельности")]/../p/text()',
    "description": '//div[@data-qa="company-description-text"]//p/text()',
    "vacancy": '//div[contains(text(), "Вакансии")]/../a[@data-qa="employer-page__employer-vacancies-link"]/@href',
}
