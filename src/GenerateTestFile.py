f = open("test.log",'wr')
for i in range(0,33333):
    f.write("\n[ 10-31 14:32:35.822     0:0x0 D/Kernel   ]\n%d"%(i))
f.close()    