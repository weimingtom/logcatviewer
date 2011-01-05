import sys
import re
import pprint

def Is_LogHeader(buf,pattern):
    result = pattern.findall(buf)
    return result

def main():
    if(len(sys.argv) <=2):
        print "Usage:python oms_filter file tags"

    count = len(sys.argv) - 2 
    
    f = open(sys.argv[1])
#    all_str  = f.read(-1)
#    time_pattern =  re.compile(r"(\[\s{0,}\d{2}\-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d{2,}\s{0,}\d{2,}:\d{2,}\s{0,}[WVDIE]/\w{1,}\s{0,}\]{0,1}\n{0,1})")        
    time_pattern =   re.compile(r"(\[\s{0,}\d{2}\-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d{2,}\s{0,}\d{1,}:0x[0-9a-fA-F]{0,}\s{0,}[WVDIE]/)(\w{1,})(\s{0,}\]\s{0,})",re.DOTALL|re.MULTILINE)    
    
    buf = f.readline()
    cache = buf    
    start = 0
    
    while buf:
        result =Is_LogHeader(buf,time_pattern)                     
        if result:
            if(result[0][1] in sys.argv[2:]):
                if(start == 0):             
                    start = 1
                    cache = buf
                else:
                    if(cache):
                        print cache  
                    start = 1
                    cache = buf

            else:
                if(cache):
                    print cache  
                start = 0
                cache = None
                
        else:
            if(start == 1):
                cache = cache + buf

        buf = f.readline()

        
    f.close()


if __name__ == '__main__':
    main()
