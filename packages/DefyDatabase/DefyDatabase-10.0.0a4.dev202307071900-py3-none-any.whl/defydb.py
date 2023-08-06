#Rules are meant to break by proudest ones.
'''
这是亮天计划的数据库官方API。
'''
import sqlite3,sys,os,datetime,io

tor='DefyDatabase'
version='10.0.0a4.dev202307071900'



commands={
    'COUNT_MAIN':'SELECT COUNT(*) FROM LIGHTSKY1',
    'CHECK_BIND':'SELECT UID,BIND FROM BIND1 WHERE UID = "{}"',
    'QUERYUID':'SELECT UID, GRADE, JOB FROM LIGHTSKY1 WHERE UID = "{}"',
    'QUERYROW':'SELECT UID, GRADE, JOB FROM LIGHTSKY1 WHERE rowid={}',
    'COUNT_BIND':'SELECT COUNT(*) FROM BIND1',
    'ATEST_MAIN_1':'INSERT INTO LIGHTSKY1 (UID,GRADE,JOB) VALUES (?,?,?)',
    'ATEST_MAIN_2':'UPDATE LIGHTSKY1 SET GRADE=?,JOB=? WHERE UID=?',
    'ATEST_BIND_1':'INSERT INTO BIND1 (UID,BIND) VALUES (?,?)',
    'ATEST_BIND_2':'UPDATE BIND1 SET BIND=? WHERE UID=?',
    'DEL_MAIN':'DELETE FROM LIGHTSKY1 WHERE UID=?',
    'DEL_BIND':'DELETE FROM BIND1 WHERE UID=?',
    'CLEAN':'VACUUM'}

tablemaker=[
    """CREATE TABLE "ACTION" (
	"ABOUT"	TEXT
)""",
    """CREATE TABLE "BIND1" (
	"UID"	TEXT NOT NULL,
	"BIND"	TEXT NOT NULL,
	PRIMARY KEY("UID")
)""",
    """
CREATE TABLE "LIGHTSKY1" (
	"UID"	TEXT NOT NULL,
	"GRADE"	INTEGER,
	"JOB"   INTEGER,
	PRIMARY KEY("UID")
)"""]


#数据库管理对象。
class __DefyProject(io.IOBase):   
    def __reset(self):
        self.__con=sqlite3.connect(self.__file)
        self.__cur=self.__con.cursor()
        
    def __query(self,command):
        e=0
        try:
            self.__cur.execute(command)
            e=self.__cur.fetchall()
        except:
            pass
        finally:
            self.__reset()
            return e
        
    def __atest(self,command):
        try:
            self.__cur.execute(command)
            self.__con.commit()
        except:
            self.__con.rollback()
        finally:
            self.__reset()

    def __init__(self,file):
        self.__file=file
        self.__con=sqlite3.connect(self.__file)
        self.__cur=self.__con.cursor()
        a=self.__query(commands['COUNT_MAIN'])
        b=self.__query(commands['COUNT_BIND'])
        if a==0 or b==0:
            for i in tablemaker:
                self.__atest(i)

    def query(self,uid):
        pass

    def atest(self,*datas):
        for i in datas:
            if len(i)==2:
                pass
            elif len(i)==3:
                pass

    def close(self):
        self.__cur.close()
        self.__con.close()
        del self.__cur,self.__con

def open(file):
    return __DefyProject(file)

