import glob
import os
import matplotlib.pyplot as plt
import sys

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
        mapfreqs.append([fname,ffreqs[it]])
        allfreqs.append(ffreqs[it])
    fh.close()

print("minimum frequency : " + str(min(allfreqs)))
print("maximum frequency : " + str(max(allfreqs)))

plt.figure()
plt.subplot(121)
plt.title("frequencies as read in consecutive VCRAFT files")
plt.plot(allfreqs)
plt.ylabel("frequency [MHz]")
plt.subplot(122)
plt.plot(sorted(allfreqs))
plt.title("frequencies sorted")
plt.ylabel("frequency [MHz]")
plt.show()
