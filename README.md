# euro_jobs (https://www.eurojobs.com/)

## Description 
1. __urls.txt__: File containing urls. This file is generated/overwritten when you run scrapy
2. __euro_jobs/spiders/get_country_wise_job_posting_count.py__: Spider to get country wise job posting listing urls with job count from the portal and populate country-wise-job-posting.csv
3. __euro_jobs/spiders/get_job_urls.py__: Spider to get job posting urls from the portal from all its pages and populate urls.txt
4. __euro_jobs/spiders/get_job_postings.py__: Spider to get job details for each of the job posting url in urls.txt
5. __euro_jobs/items.py__: Class to define extracted job fields/features
6. __euro_jobs/pipelines.py__: Class to insert into database
7. __euro_jobs/settings.py__: Class to establish a connection with database

## How to run the scrapy
1. [Install scrapy](https://docs.scrapy.org/en/latest/intro/install.html#intro-install)

2. To get all the job posting count with assciation of country urls

```scrapy crawl euroJobsCountryWiseJobPostingCount```

3. To get all the job posting urls

```scrapy crawl euroJobsGetJobURLs```


4. To get the job posting details

```scrapy crawl euroJobsGetJobPostingDetails```
