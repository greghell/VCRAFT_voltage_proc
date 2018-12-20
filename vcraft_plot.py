import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Plots spectra of all antennas and eigen values of correlation matrix')
parser.add_argument('filename', help='indicate file name')
parser.add_argument("nChan", type=int, help="channel number (0..7)")
parser.add_argument("-nResol", type=int, help="spectral resolution (< 51200)", default = 1024)
parser.add_argument("-show", help="show plot before saving it",action="store_true")
args = parser.parse_args()

fname = args.filename

nResol = int(args.nResol)
nChan = int(args.nChan)

#os.chdir("C:\\Users\\greg\\Desktop\\FRB_analysis\\beam36")
#os.listdir(os.getcwd())
#fname = "ak01_c1_f0.vcraft"
fsize = os.path.getsize(fname)

fh = open(fname, "r", encoding="ISO-8859-1")
head_beg = str(fh.read(4096))

idx = head_beg.find("HDR_SIZE ")
fh.seek(9+idx, 0)
hdrsize = int(str(fh.read(5)))

idx = head_beg.find("SAMP_RATE")
fh.seek(10+idx, 0)
samrate = float(str(fh.read(14)))

idx = head_beg.find("NSAMPS_REQUEST ")
fh.seek(15+idx, 0)
nSam = int(str(fh.read(8)))

idx = head_beg.find("\nFREQS ")
idx2 = head_beg.find("# Comma separated list")
fh.seek(7+idx, 0)
ffreqs = fh.read(idx2 - idx - 7)
ffreqs = ffreqs.split(",")
fh.close()

fc = float(ffreqs[nChan])

specs = np.zeros((nResol))
fh = open(fname, "rb")
fh.seek(hdrsize+nChan*nSam, 0)
sams = np.fromfile(fh, dtype='int8',count=nSam)
fh.close()
sigreal = np.bitwise_and(sams, 0x0f)
sigimag = np.bitwise_and(sams >> 4, 0x0f)
for kk in range(len(sigreal)):
    if sigreal[kk] > 7:
        sigreal[kk] = sigreal[kk] -16
    if sigimag[kk] > 7:
        sigimag[kk] = sigimag[kk] -16
    
sig = sigreal + 1j*sigimag
sig = np.reshape(sig[:int(nResol*int(len(sig)/nResol))],(nResol,int(len(sig)/nResol)),order='F')
sig = np.abs(np.fft.fft(sig,axis=0))**2

specs = np.fft.fftshift(10.*np.log10(np.mean(sig,axis=1)))

plt.figure()
plt.subplot(121)
plt.plot(np.linspace(fc-samrate/2/1e6,fc+samrate/2/1e6,nResol),np.fft.fftshift(10.*np.log10(np.mean(sig,axis=1))))
plt.xlabel('frequency [MHz]')
plt.ylabel('PSD [dB]')
plt.grid()
plt.subplot(122)
plt.imshow(np.fft.fftshift(10.*np.log10((sig))),aspect='auto',extent=[0.,nSam/samrate,fc-samrate/2/1e6,fc+samrate/2/1e6])
plt.xlabel('time [s]')
plt.ylabel('frequency [MHz]')

figure = plt.gcf() # get current figure
figure.set_size_inches(18, 9)

if args.show:
	plt.show()
plt.savefig(fname+"_analysis.png")
plt.close()
