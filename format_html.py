import os
import re
import time
import base64
import slugify
import MySQLdb as mdb

base_dir = os.path.dirname(os.path.abspath(__file__))
htmls = os.listdir(base_dir)
if not os.path.exists('images'):
    os.mkdir('images')
weight = 0
visible = 1
author_id = 1
for html in htmls:
    if html.endswith('.html'):
        print 'processing', html
        dir_name = html[:-5]
        dir_path = 'images/' + dir_name
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_path = dir_path + '/%02d.%s'
        link = '/s/upload/blog/' + dir_name + '/%02d.%s'
        with open(html, 'r') as src:
            content = src.read()
        index = 1
        portrait = ''
        while True:
            match = re.search(r'<img src="(data:image/(.*?);base64,(.*?))"', content)
            if match:
                extends = match.group(2)
                data = match.group(3)
                file_name = file_path % (index, extends)
                content = content.replace(match.group(1), link % (index, extends))
                img_data = base64.b64decode(data)
                with open(file_name, 'wb') as img:
                    print 'storing', file_name
                    img.write(img_data)
                if index == 1:
                    portrait = link[9:] % (index, extends)
                index += 1
            else:
                break
        #print portrait
        content = re.sub(r'<!DOCTYPE.*?>', '', content)
        content = content.replace('<html>', '')
        content = content.replace('</html>', '')
        content = re.sub(r'(?s)<head>.*?</head>', '', content)
        content = re.sub(r'<body.*?>', '', content)
        content = content.replace('</body>', '')
        content = content.replace('<br>', '')
        content = content.replace('</font>', '')
        content = content.replace('</span>', '')
        content = content.replace('</a>', '')
        content = re.sub(r'<p .*?>', '<p>', content)
        content = re.sub(r'<font .*?>', '', content)
        content = re.sub(r'<span .*?>', '', content)
        content = re.sub(r'<a .*?>', '', content)
        content = re.sub(r'(<img src=".*?") .*?>', r'\g<1>>', content)
        content = content.strip()
        content = content.replace('>\n', '>')
        content = re.sub('(?<!>)\n(?!<)', ' ')
        content = re.sub(r'<p><b>', '<h1>', content, 1)
        content = re.sub(r'</p></b>', '</h1>', content, 1)
        content = content.replace('<p><b>', '<h2>')
        content = content.replace('</b></p>', '</h2>')
        content = content.replace('<b>', '')
        content = content.replace('</b>', '')
        content = re.sub(r'(?<!p>)<img', '</p>\n<p><img', content)
        content = re.sub(r'(<img .*?>)(?!<)', r'\g<1></p><p>', content)
        title = re.search(r'<h1>(.*?)</h1>', content).group(1)
        #print title
        slug = slugify.slugify(title)
        match = re.search(r'<p>([^<].*?)</p>', content)
        abstract = match.group(1)
        #print abstract
        publish_date = time.strftime('%Y-%m-%d %H:%M:%S')
        #print content
        print 'title:', title
        print 'portrait:', portrait
        print 'slug:', slug
        print 'abstract:', abstract
        print 'publish_date:', publish_date
        print 'weight:', weight
        print 'visible:', visible
        print 'author_id:', author_id
        with open('modified/' + html, 'w') as dest:
            dest.write(content)
        con = mdb.connect(user='mingdatrade', passwd='trade@mingDA123', db='bestfinds')
        with con:
            cur = con.cursor()
            sql = 'select id from blog_blog'
            cur.execute(sql)
            ids = [d for d in cur]
            for id_no in ids:
                sql = 'insert blog_blogtag set (name, blog_id) value("apparel", "%s")'
                cur.execute(sql % id_no)
            #sql = ('insert blog_blog (title, portrait, slug, abstract, content,'
            #       ' publish_date, weight, visible, author_id) value("%s", "%s", "%s"'
            #       ', "%s", "%s", "%s", "%s", "%s", "%s")')
            #content = con.escape_string(content)
            #cur.execute(sql % (title, portrait, slug, abstract, content, publish_date, weight, visible, author_id))
            #sql = 'select id from blog_blog where slug = "%s"'
            #cur.execute(sql % slug)
            #(id_no, ) = cur.fetchone()
            #sql = 'insert blog_blogtag (name, blog_id) value("apparel", "%s")'
            #cur.execute(sql % id_no)
