
import sqlite3 as sqlite
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
# This pipeline takes the Item and stuffs it into scrapedata.db
class EuroJobsPipeline(object):
    def __init__(self):
        self.connection = sqlite.connect(settings.get('DB_PATH'))
        self.cursor = self.connection.cursor()
        #self.cursor.execute('DROP TABLE IF EXISTS myscrapedata')
        
        self.cursor.execute('CREATE TABLE IF NOT EXISTS joburls (id INTEGER PRIMARY KEY, url VARCHAR(255),country VARCHAR(255))')
        
        self.cursor.execute('CREATE TABLE IF NOT EXISTS jobdetails (id INTEGER PRIMARY KEY, url VARCHAR(255), title VARCHAR(255) ,date_posted VARCHAR(255) ,category VARCHAR(255) ,location VARCHAR(255) ,job_type VARCHAR(255) ,description TEXT ,html_blob TEXT ,expired VARCHAR(255) ,salary VARCHAR(255))')

    # Take the item and put it in database - do not allow duplicates
    def process_item(self, item, spider):
                
        if(spider.name == 'euroJobsGetJobURLs'): #for saving the urls
            self.cursor.execute("select * from joburls where url=?", (item['url'],)) #checking for duplicate entry
            if not self.cursor.fetchone(): #not save duplicate url job posting
                self.cursor.execute("insert into joburls (url, country) values (?, ?)",(item['url'],item['country']))
                
        elif(spider.name == 'euroJobsGetJobPostingDetails'): #for saving the job postings
            self.cursor.execute("select * from jobdetails where url=?", (item['url'],)) #checking for duplicate entry
            if not self.cursor.fetchone(): #not save duplicate url job posting
                self.cursor.execute("insert into jobdetails (url, title, date_posted, category, location, job_type, description, html_blob, expired, salary) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(item['url'], item['title'], item['date_posted'], item['category'], item['location'], item['job_type'], item['description'], item['html_blob'], item['expired'], item['salary']))
                
        self.connection.commit()
        
        return item
                
    def handle_error(self, e):
        log.err(e)