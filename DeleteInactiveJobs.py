#!/usr/bin/env python
# coding: utf-8

# In[83]:


import requests
import sqlite3 as sqlite

class DeleteInactiveJobs:
    
    def __init__(self):
        self.connection = sqlite.connect('scrapedata.db')
        self.connection.row_factory = sqlite.Row
        self.cursor = self.connection.cursor()
    
    def isActive(self,url):
        if requests.get(url).status_code == 200:
            return True
        else:
            return False
        
    def deleteFromDb(self,url):
        for table in self.tables:
            qry = "DELETE FROM " + table + " WHERE url = '" + url + "'"
            self.cursor.execute(qry)
            self.connection.commit()
            print('Inactive URL:',url,'Deleted From',table)

    def deleteOneInactive(self,url,delete_from_tables):
        self.tables = delete_from_tables
        if not self.isActive(url):
            self.deleteFromDb(url)
        else:
            print('Active URL:',url)
            
    def deleteAllIncative(self,check_table,delete_from_tables):
        self.cursor.execute('SELECT * FROM '+check_table)
        for row in self.cursor.fetchall():
            self.deleteOneInactive(row['url'],delete_from_tables)

def delete_inactive_jobs():
    DeleteInactiveJobs = DeleteInactiveJobs()
    DeleteInactiveJobs.deleteAllIncative('jobdetails',['joburls','jobdetails'])

if __name__ == '__main__':
    delete_inactive_jobs()


# In[ ]:




