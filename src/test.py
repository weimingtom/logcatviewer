import re
f = open("logcat-radio.log")
allcontent = f.read()
#print allcontent
pattern = re.compile(r"\[{0,1}\s{0,}(\d{2}\-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d{2,})\s{0,}(.{0,})\s{0,}([WVDIE])/(\w{1,})\s{0,}\]{0,1}\n{0,1}")
#pattern = re.compile(r"\[\s{1,}(\d{2}\-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d{2,})\s{1,}(\d{1,}:0x\d{1,})\s{1,}([WVDIE])/(\w{1,})\s{0,}\]\n(.*)")
result = pattern.findall(allcontent)
#mylog=Models.LogModels(result)
#mylog.execute('SELECT * from logtable')
print result