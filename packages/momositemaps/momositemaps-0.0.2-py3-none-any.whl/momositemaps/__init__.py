import hashlib
import mysql.connector

def listToArray(file):
    list = []
    with open(file) as f:
        for line in f:
            # in alternative, if you need to use the file content as numbers
            # inner_list = [int(elt.strip()) for elt in line.split(',')]
            line = line.strip('\n')
            list.append(line)
    return list


def submitLinks(host, dbuser, dbpassword, database, links):
    file1 = open(links, 'r')
    lines = file1.readlines()
    x = 0
    errors = 0
    print("Starting to submit urls to Yourls script. This may take some time if the list is very long.")
    for line in lines:
        try:
            mydb = mysql.connector.connect(
                host=host,
                user=dbuser,
                password=dbpassword,
                database=database
            )
            result = hashlib.md5(line.encode())
            keyword = result.hexdigest()
            #print(keyword)
            mycursor = mydb.cursor()
            sql = "INSERT INTO yourls_url (keyword, url, ip) VALUES(%s, %s, %s)"
            val = (keyword, line, "1.1.1.1")
            mycursor.execute(sql, val)
            mydb.commit()
            x = x + 1
            print(str(x) + " links submitted.")
        except Exception:
            errors = errors + 1

    print("Submission completed")
    print(str(x) + " urls have been submitted in total")
    print(str(errors) + " errors occured. Either these urls have already been submitted or there is another issue")


def createSitemaps(host, dbuser, dbpassword, database, domain, directory):
    mydb = mysql.connector.connect(
        host= host,
        user= dbuser,
        password= dbpassword,
        database= database
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM yourls_url")
    result = mycursor.fetchone()
    row_count = result[0]
    numberToDo = row_count/5000
    print("Links in database: " + str(row_count))
    print("Sitemaps to make: " + str(numberToDo))
    x = 1
    print("Creating sitemaps. This may take some time depending on the number needed")
    while x - 1 < numberToDo:
        mycursor = mydb.cursor()
        offset = (x-1) * 5000
        mycursor.execute("SELECT * FROM yourls_url LIMIT 5000 OFFSET " + str(offset))
        myresult = mycursor.fetchall()
        with open("sitemap_" + str(x) + ".xml", 'w') as fp:
            fp.writelines('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
            for link in myresult:
                fp.writelines('<url>')
                fp.writelines('<loc>https://' + domain + '/' + str(link[0].decode()) + '</loc>')
                fp.writelines('<lastmod>2023-07-08T15:15:27+00:00</lastmod>')
                fp.writelines('<changefreq>Daily</changefreq>')
                fp.writelines('<priority>0.9</priority>')
                fp.writelines('</url>')

            fp.writelines('</urlset>')
            print("Number of sitemaps created so far: " + str(x))
        x = x + 1
    print("Created " + str(x) + " sitemaps. Now will create the index of the sitemaps, sitemap_index.xml. This is the file to submit to IndexNow")
    x = 1
    with open("sitemap_index.xml", 'w') as fp:
        fp.writelines('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        while x - 1 < numberToDo:
            fp.writelines('<url>')
            fp.writelines('<loc>https://' + domain + '/' + directory +'/sitemap_' + str(x) + '.xml</loc>')
            fp.writelines('<lastmod>2023-07-08T15:15:27+00:00</lastmod>')
            fp.writelines('<changefreq>Daily</changefreq>')
            fp.writelines('<priority>0.9</priority>')
            fp.writelines('</url>')
            x = x + 1
        fp.writelines('</urlset>')


def submitAndBuildSitemaps(host, dbuser, dbpassword, database, domain, directory, links):
    submitLinks(host, dbuser, dbpassword, database, links)
    createSitemaps(host, dbuser, dbpassword, database, domain, directory)
