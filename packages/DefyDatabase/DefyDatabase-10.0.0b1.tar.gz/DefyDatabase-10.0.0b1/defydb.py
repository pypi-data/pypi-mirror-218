license='''Copyright (C) 2023 Defymen
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'''

#Rules are meant to break by proudest ones.
'''
这是亮天计划的数据库官方API。
'''
import sqlite3,sys,os,datetime,io

tor='DefyDatabase'
version='10.0.0b1'



commands={
    'COUNT_MAIN':'SELECT COUNT(*) FROM LIGHTSKY1',
    'QUERYBIND':'SELECT UID,BIND FROM BIND1 WHERE UID = ?',
    'QUERYUID':'SELECT UID, GRADE, JOB FROM LIGHTSKY1 WHERE UID = ?',
    'QUERYROW':'SELECT UID, GRADE, JOB FROM LIGHTSKY1 WHERE rowid=?',
    'QUERYUP':'SELECT UID,BIND FROM BIND1 WHERE BIND=?',
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
        
    def __query(self,command,thing=None):
        try:
            if thing:
                self.__cur.execute(command,thing)
            else:
                self.__cur.execute(command)
            m=self.__cur.fetchall()
            return m
        except BaseException as e:
            return 0

        
    def __atest(self,command,thing=None):
        try:
            if thing:
                self.__cur.execute(command,thing)
            else:
                self.__cur.execute(command)
            self.__con.commit()
        except BaseException as e:
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

    def clean(self):
        self.__query(commands['CLEAN'])

    def query(self,uid):
        if self.__query(commands['QUERYBIND'],uid)!=[]:
            uid=self.__query(commands['QUERYBIND'],uid)[0][1]
        return self.__query(commands['QUERYUID'],uid)[0]

    def atest(self,*datas):
        for i in datas:
            if len(i)==2:
                if self.__query(commands['QUERYUID'],i[0])!=[]:
                    raise ValueError('It''s in the main table')
                if self.__query(commands['QUERYUID'],i[1])==[]:
                    raise ValueError('You are pointing to a value that is not in the main table')
                
                m=self.__query(commands['QUERYBIND'],i[0])
                if m==[]:
                    self.__atest(commands['ATEST_BIND_1'],i)
                else:
                    self.__atest(commands['ATEST_BIND_2'],i)
                    
            elif len(i)==3:
                if self.__query(commands['QUERYBIND'],i[0])!=[]:
                    raise ValueError('It''s in the bind table')
                m=self.__query(commands['QUERYUID'],i[0])
                if m==[]:
                    self.__atest(commands['ATEST_MAIN_1'],i)
                else:
                    self.__atest(commands['ATEST_MAIN_2'],i)

    def delete(self,uid):
        if self.__query(commands['QUERYUID'],uid)!=0:
            m=self.__query(commands['QUERYUP'],uid)
            for i in m:
                self.__atest(commands['DEL_BIND'],i[0])
            self.__atest(commands['DEL_MAIN'],uid)
        elif self.__query(commands['QUERYBIND'],uid)!=0:
            self.__atest(commands['DEL_BIND'],uid)
            
                    
    def close(self):
        self.__cur.close()
        self.__con.close()
        del self.__cur,self.__con

def open(file):
    return __DefyProject(file)

