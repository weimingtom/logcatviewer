import sqlite3
import re

class LogModels(object):
    def __init__(self):
        self.conn = sqlite3.connect(':memory:') 
        self.cursor = self.conn.cursor()
        self.cursor.execute(' CREATE TABLE logtable(id integer NOT NULL PRIMARY KEY,\
        logtime varchar(50),\
        info varchar(50),\
        type varchar(20),\
        component varchar(20),\
        detail string)');
        self.conn.commit()
        
    def execute(self,str):
        print 'execute %s'%(str)
        self.cursor.execute(str)
        result = [];
        for row in self.cursor:
            result.append(row)
            #print row
        return result
    
    def setlogfile(self,filename):
        
        self.cursor.execute('delete from logtable')
        self.conn.commit()
        readline_cnt = 0
        test_parse_cnt = 0
        print 'set log file'
        f = open(filename)
        time_pattern =  re.compile(r"\[{0,1}\s{0,}(\d{2}\-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d{2,})\s{0,}(.{0,})\s{0,}([WVDIE])/(\w{1,})\s{0,}\]{0,1}\n{0,1}")        
        whole_pattern = re.compile(r"\[{0,1}\s{0,}(\d{2}\-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d{2,})\s{0,}(.{0,})\s{0,}([WVDIE])/(\w{1,})\s{0,}\]{0,1}\n{0,1}(.*)")
        
        cache = buf = f.readline()      

        while buf:            
            parse_result = time_pattern.findall(cache)
            if  parse_result:
                #if match contiune read
                buf = f.readline()

                parse_result = time_pattern.findall(buf)
                while not parse_result:
                    cache = cache  + buf
                    buf = f.readline()
                    
                    if not buf:
                        break
                    parse_result = time_pattern.findall(buf)

              #Read the next time stamp
                parse_result = whole_pattern.findall(cache)
                if( parse_result):
                    for item in parse_result:
                      log = (None,item[0],item[1],item[2],item[3],item[4])
                      self.cursor.execute('insert into logtable values (?,?,?,?,?,?)', log)    
                      test_parse_cnt = test_parse_cnt + 1
                cache = buf
            else:
                cache = buf = f.readline()

        print 'the count is %d'%(test_parse_cnt )
        
        self.conn.commit()
        f.close()
