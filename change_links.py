import re
import MySQLdb as mdb
import slugify

con = mdb.connect(user='mingdatrade', passwd='trade@mingDA123', db='bestfinds')
with con:
    cur = con.cursor()
    sql = 'select content from blog_blog where id = 45'
    cur.execute(sql)
    for (content,) in cur:
        #with open('content.txt', 'w') as dest:
        #    dest.write(content)
        content = re.sub(r'son.+?s', "son's", content)
        content = re.sub(r'baby.+?s', "baby's", content)
        #print content
        #content = content.replace('\n', '')
        #content = content.replace('<br>', '')
        #content = content.replace('<p></p>', '')
        #content = content.replace('its</p>', 'its</h2>')
        #content = content.replace('<h1>', '<h2>')
        #content = content.replace('</h1>', '</h2>')
        #content = re.sub(r'<p>', '<h1>', content, 1)
        #content = re.sub(r'</p>', '</h1>', content, 1)
        content = con.escape_string(content)
        #portrait = portrait.replace('/s/images/bestfinds/', '/blog/')
        sql = ('update blog_blog set content = "%s" where id = 45')
        cur.execute(sql % content)
        #print id_no
