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
    
    '''Method for checking a job posting active or not'''
    def isActive(self,url):
        if requests.get(url).status_code == 200:
            return True
        else:
            return False
        
    '''Method for deleteing job posting form database tables'''  
    def deleteFromDb(self,url):
        for table in self.tables:
            qry = "DELETE FROM " + table + " WHERE url = '" + url + "'"
            self.cursor.execute(qry)
            self.connection.commit()
            print('Inactive URL:',url,'Deleted From',table)

    '''Method for deleteing single job posting if inactive'''        
    def deleteOneInactive(self,url,delete_from_tables):
        self.tables = delete_from_tables
        if not self.isActive(url):
            self.deleteFromDb(url)
        else:
            print('Active URL:',url)
           
    '''Method for deleteing multiple job posting if inactive'''   
    def deleteAllIncative(self,check_table,delete_from_tables):
        self.cursor.execute('SELECT * FROM '+check_table)
        for row in self.cursor.fetchall():
            self.deleteOneInactive(row['url'],delete_from_tables)

'''Method for deleteing inactive jobs'''   
def delete_inactive_jobs():
    DeleteInactiveJobs().deleteAllIncative('jobdetails',['joburls','jobdetails'])

if __name__ == '__main__':
    delete_inactive_jobs()


# In[ ]:




