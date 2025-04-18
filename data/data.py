import sqlite3
from datetime import date

db = 'data/users.db'    
conn = sqlite3.connect(db)
cursor = conn.cursor()
print("database was connected")

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    userid TEXT PRIMARY KEY,
    date TEXT,
    videos INT
)
''')

            
async def checkVids(userid):
    try:
        curdate = str(date.today())
        cursor.execute("SELECT date FROM users WHERE userid = ?", (userid,))
        dateindb = cursor.fetchone()
        print(dateindb[0], " ----- ", curdate)
        if dateindb[0] == curdate:
            cursor.execute("SELECT videos FROM users WHERE userid = ?", (userid,))
            curvids = cursor.fetchone()
            if curvids[0] > 0:
                print("vids t", curvids[0])
                return True
            else:
                print("vids f", curvids[0])
                return False
        else:
            await updateUser(userid)
            print("date wasnt fresh t")
            return True   
    except Exception as e:
        print(e)
        return False 

async def getVids(userid):
    try:
        cursor.execute("SELECT videos FROM users WHERE userid = ?", (userid,))
        result = cursor.fetchone()
        print("vids: ", result[0])
        return result[0]
    except Exception as e:
        print(e)
        return False
        

async def decrVideos(userid):
    try:
        cursor.execute("UPDATE users SET videos = videos - 1 WHERE userid = ?", (userid,))
        conn.commit()
        print("sucsess decr vids")
        return True 
    except Exception as e:
        print(e)
        return False 

async def checkUser(userid):
    try:
        cursor.execute("SELECT COUNT(1) FROM users WHERE userid = ?", (userid,))
        result = cursor.fetchone()[0] > 0
        print("user in db true")
        return result  
    except Exception as e:
        print(e)
        return False 

async def updateUser(userid):
    try:
        curdate = str(date.today())
        cursor.execute("UPDATE users SET date = ?, videos = ? WHERE userid = ?", (curdate, 5, userid))
        conn.commit()
        print("s wr db")
        return True  
    except Exception as e:
        print(e)
        return False     

async def addUser(userid):
    try:
        curdate = str(date.today())
        cursor.execute("INSERT INTO users (userid, date, videos) VALUES (?, ?, ?)", (userid, curdate, 5))
        conn.commit()
        print("s wr db")
        return True  
    except Exception as e:
        print(e)
        return False 
    