from requests_html import HTMLSession
import mysql.connector as sql
from datetime import datetime
from multiprocessing import Process
import argparse


class animeGrabber():
        def __init__(self, *args, **kwargs):
                try:
                        self.conn = self.connection()
                        self.cur = self.conn.cursor()
                except:
                        self.conn.close()


        def fnd(self, sesh, ele):
                return sesh.html.find(ele)

        def getIframe(self,newS):
                iframe = list()
                try:
                        iframe.append(self.fnd(newS, "iframe.embed-responsive-item")[0].html)
                        mirrors = self.fnd(newS, "div#episode_mirrors > div.row > div")
                except:
                        pass
                for m in range(0, 2):
                        try:
                                if m == 0:
                                         pass
                                elif mirrors[m]:
                                        mir = mirrors[m].find("a")[0].attrs["href"]
                                        req1 = HTMLSession().get(mir) 
                                        iframe.append(self.fnd(req1, "iframe.embed-responsive-item")[0].html)
                        except IndexError:
                                pass
                iframe = ", ".join(iframe)
                return iframe

        def updateDB(self):
                session = HTMLSession()
                sel = "div#latest_anime > div.row > div > div > a"
                req = session.get("http://www.animeshow.tv")
                latest = self.fnd(req, sel)
                for l in latest:
                        href = l.attrs["href"]
                        series = l.text
                        print(series)
                        newR = session.get(href)
                        title = self.fnd(newR, "div#episode > h1")[0].text
                        select = "SELECT title FROM episodes WHERE title = '{}'".format(title)
                        self.cur.execute(select)
                        result = self.cur.fetchone()
                        if result is not None:
                                print("[-]Already Exists!!")
                                exit(1)
                        else:
                                now = datetime.now()
                                day = now.strftime("%d %b %Y")
                                links = self.getIframe(newR)
                                sub = "sub"
                                self.insert(self.cur, "episodes",title, series, sub, day, links )
                                print("[+] Update Completed!")

        def grabAllData(self):
                session = HTMLSession()
                sel = "div.l_r > ul > li > a"
                req = session.get("http://www.animeshow.tv/anime-list.html")
                series = self.fnd(req, sel)

                for x in series:
                        info = list()
                        smry = list()
                        s = list(x.links)[0]
                        rse = session.get(s)
                        title = self.fnd(rse,"div#anime > h1")[0].text
                        title = title.replace("'", "\\'")
                        print(title)
                        poster = self.fnd(rse,"img.img-responsive")[0].attrs['src']
                        summary = self.fnd(rse, "div.anime_discription")
                        for a in summary:
                                smry.append(a.text)
                        summary = "\n\n".join(smry)
                        summary = summary.replace("'", "\\'")
                        show = self.fnd(rse, "div.a_in > div.row > div")
                        for i in range(0, 9):
                                if i % 2 == 0:
                                        pass
                
                                else:
                                        info.append(show[i].text)
                        tip = info[0].split(",")

                        year = info[1]
                        status = info[2]
                        genres = info[3]
        
                        episode_list = self.fnd(rse, "div.e_l_r")
                        if len(tip) > 1:
    
                                episodes = tip[1]
                                typ = tip[0]
                        else:
                                typ = info[0]
                                episodes = str(len(episode_list)) + " Episodes"
                        select = "SELECT title FROM series WHERE title = '{}'".format(title)
                        self.cur.execute(select)
                        se = self.cur.fetchone()

                        if se is not None:
                                print("[-]Already Got this Series")
                                continue
                        else:
                                insert(self.cur,"series",title, typ , year , status , genres, summary,poster, episodes)
                                print("[+] Inserted {} into Series".format(title)) 

                        for ep in episode_list:
                                anc = ep.find("a")
                                ep_link = anc[0].attrs["href"]
                                ep_title = anc[0].text
                                ep_title = ep_title.replace("'", "\\'")
                                row = ep.find("div.row > div")
                                sub_dub = 'sub'
                                date = row[2].text
                                newS = HTMLSession().get(ep_link)
                                iframe = self.getIframe(newS)
                                select = "SELECT title FROM episodes WHERE title='{}'".format(ep_title)
                                self.cur.execute(select)
                                se = self.cur.fetchone() 
                                if se[0] is not None:
                                        pass
                                else:
                                        insert(self.cur, "episodes", ep_title, title, sub_dub, date, iframe)
                                        print("[+] Inserted {} into Episodes".format(ep_title)) 
                        

                
                
        

    

        def connection(self, host="localhost", user="root", passwd="Lilcrazy91", database="myanime"):

                config = {
                        "host" : host,

                        "user" : user,

                        "passwd" : passwd,

                        "database" : database
                        }
    
                try:
                        conn = sql.connect(**config)

                        return conn
                except:
                        print("Connection Failed!")
                        exit(1)


        def insert(self,cur, table, *args):
                if table == "series":
                        insert = "INSERT INTO series (title, type, year, status, genres, summary, poster, episodes) VALUES ('{}', '{}', '{}', '{}', '{}', '{}',  '{}' , '{}')".format(*args)
                        self.cur.execute(insert)

                elif table == "episodes":
                        insert = "INSERT INTO episodes(title,series, `sub_dub`, date, link) VALUES('{}', '{}', '{}', '{}', '{}')".format(*args)
                        self.cur.execute(insert)

        def update(self, cur, table, *args):
                if table == "series":
                        update = "UPDATE series SET title = {}, type = {}, year = {}, status = {}, genres = {}, summary = {}, poster = {}, episodes = {} ".format(*args)
                        self.cur.execute(update)

                elif table == "episodes":
                        update = "UPDATE episodes SET 'title','series', 'sub_dub', 'date', 'link' ".format(*args)
                        self.cur.execute(update)

if __name__ == "__main__":
        parser = argparse.ArgumentParser("animeGrabber")
        parser.add_argument("-i", help="run in insert mode", action="store_true")
        parser.add_argument("-u", help="run in update mode", action="store_true")
        args = parser.parse_args()
        grab = animeGrabber()
        if args.i == True and args.u == False:   
                grab.grabAllData()
                grab.conn.close()
        elif args.u == True and args.i == False:
                grab.updateDB()
                grab.conn.close()
        else:
                print("Please Select to update (-u) or insert (-i), but NEVER both!!")

