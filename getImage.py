import urllib.request
import mysql.connector as sql



def conn(host, user, passwd, database):
    config = {
    "host" : host,

    "user" : user,

    "passwd" : passwd,

    "database" : database
                        }
    try:
        connect = sql.connect(**config)
        return connect
    except:
        print("Connection Failed")
        exit(1)

con = conn()
cursor = con.cursor()
query = "SELECT title, poster from series ORDER BY id"
cursor.execute(query)
data = cursor.fetchall()

for x in data:
    title = x[0]
    url = str(x[1])
    title = title.replace("'", "\\'")
    if "assets" in url:
        fileName = url.split("assets")[-1]
    else:
        fileName = url.split("/series")[-1]

    savefolder = "assets/{}".format(fileName)
    print(fileName)
    urllib.request.urlretrieve(url, savefolder)
    update = "UPDATE series SET poster = '{}' WHERE title = '{}'".format(savefolder, title)
    cursor.execute(update)
