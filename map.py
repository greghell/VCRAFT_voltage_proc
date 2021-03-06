import glob
import os
import matplotlib.pyplot as plt
import sys
import operator
import numpy as np

if len(sys.argv) < 2:
    print("indicate path to directory as argument")
    sys.exit()

os.chdir(sys.argv[1])
fnames = glob.glob("*.vcraft")

mapfreqs = []
allfreqs = []
for fname in fnames:
    fh = open(fname, "r")#, encoding="ISO-8859-1")
    head_beg = str(fh.read(4096))
    idx = head_beg.find("\nFREQS ")
    idx2 = head_beg.find("# Comma separated list")
    fh.seek(7+idx, 0)
    ffreqs = fh.read(idx2 - idx - 7)
    ffreqs = ffreqs.split(",")
    ffreqs = map(int, ffreqs)
    for it in range(len(ffreqs)):
        mapfreqs.append([fname,ffreqs[it],it])
        allfreqs.append(ffreqs[it])
    fh.close()

print("minimum frequency : " + str(min(allfreqs)))
print("maximum frequency : " + str(max(allfreqs)))

mapfreqs = sorted(mapfreqs, key=operator.itemgetter(1))

fh = open(mapfreqs[0][0], "r")
head_beg = str(fh.read(4096))

idx = head_beg.find("HDR_SIZE ")
fh.seek(9+idx, 0)
hdrsize = int(str(fh.read(5)))

idx = head_beg.find("NSAMPS_REQUEST ")
fh.seek(15+idx, 0)
nSam = int(str(fh.read(8)))
fh.close()

if int(sys.argv[2]) > nSam:
    print("warning, number of time samples truncated to " + str(nSam))
    nSamchosen = nSam
else:
    nSamchosen = int(sys.argv[2])

data = np.zeros((len(allfreqs),nSamchosen), dtype=complex)
lut = np.array([0.,1.,2.,3.,4.,5.,6.,7.,-8.,-7.,-6.,-5.,-4.,-3.,-2.,-1.])
print("size of data array : "+str(data.shape))
for k in range(len(allfreqs)):
    print("processing channel #"+str(k))
    fh = open(mapfreqs[k][0], "rb")
    fh.seek(hdrsize+mapfreqs[k][2]*nSam, 0)
    sams = np.fromfile(fh, dtype='int8',count=nSamchosen)
    fh.close()
    sigreal = lut[np.array(np.bitwise_and(sams, 0x0f))]
    sigimag = lut[np.array(np.bitwise_and(sams >> 4, 0x0f))]
    sig = sigreal + 1j*sigimag
    if int(sys.argv[3]):
        sig = (sig - np.mean(sig)) / np.var(sig)
    data[k,:] = sig
