class LineLog(object):
    """
    
     CREATE TABLE "guard"("id" integer NOT NULL PRIMARY KEY,"name" varchar(50) NOT NULL,"password" varchar(50));
     
    """
    def __init__(self,id=None,logtime=None,info=None,type=None,component=None,detail=None):
        self.id = id
        self.logtime = logtime
        self.info = info
        self.type = type
        self.component =component
        self.detail = detail
        
        