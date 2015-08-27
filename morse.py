#!/usr/bin/python
"""
fd, wav = wavfile.read("morse-7000khz.wav")
wav1,fd1,s,filter,g,m,p = morse.wav2sq(fd/10, wav[::10], 690, 50)
lt = morse.sq2morse(fd1, p, W=0.1, D=0.15)
print morse.morse2text(lt)
"""
from pylab import *
from matplotlib.pyplot import *
import scipy.io.wavfile as wavfile
import numpy.fft as fft


#fd, wav = wavfile.read("morse-7000khz.wav")

def wav2sq(fd, wav, f, d):
	L = wav.shape[0]
	s = fft.rfft(wav)
	
#	plot(arange(L/2+1)*fd/L, s)
	
	filter = zeros(s.shape[0])
	filter[(f-d)*L/fd:(f+d)*L/fd] = 1
	
	g = fft.irfft(s * filter)
	o = zeros(g.shape[0], dtype=int16)
	o[:] = g[:]
	wavfile.write("/tmp/wav", fd, o)
	
	m = movavg(abs(g), 0.01*fd)
	#plot(arange(m.shape[0])/float(fd), m)
#	plot(arange(m.shape[0])/float(fd), m > m.max()/2)
	
	m[0] = 0
	m[-1] = 0
	p = 1*(m > m.max()/3)
#	e = p[1:] - p[:-1]
#	t = (arange(e.shape[0])[e < 0] - arange(e.shape[0])[e > 0])*1./fd

	return wav, fd, s, filter, g, m, p

def _plot(wav, fd, s, filter, g, m, p):
	subplot(211)
	plot(arange(s.shape[0])*fd/wav.shape[0], s)
	plot(arange(filter.shape[0])*fd/wav.shape[0], filter*s.max(), '-r', linewidth=2)
	subplot(212)
	plot(arange(wav.shape[0])*1./fd, wav)
	plot(arange(g.shape[0])*1./fd, g)
	plot(arange(m.shape[0])*1./fd, m)
	plot(arange(p.shape[0])*1./fd, p*wav.max())
#	plot(arange(wav.shape[0])*1./fd, wav)

def sq2morse(fd, p, W=0.15, D=0.15):
	letters = []
	text = ""
	p[0] = 0
	p[-1] = 0
	edges = p[1:] - p[:-1]
	pe = arange(p.shape[0])[edges > 0]
	ne = arange(p.shape[0])[edges < 0]
	for i in arange(1,pe.shape[0]):
		w = (ne[i] - pe[i]) *1./fd
		d = (pe[i] - ne[i-1]) *1./fd
#		print "w=%.2f, d=%.2f" % (w, d)
		if d > D:
			letters.append(text)
			text = ""
		if d > 5*D:
			letters.append('space')
		if w > W:
			text += '-'
		elif w > W/4:
			text += '.'
		else:
			pass
	return letters


def morse2text(letters):
	s = ""
	for l in letters:
		try:
			s += ITU[l]
		except KeyError:
			s += "[?]"
	return s

ITU = {
	"space":'  ',
	".-":'A',
	"-...":'B',
	"-.-.":'C',
	"-..":'D',
	".":'E',
	"..-.":'F',
	"--.":'G',
	"....":'H',
	"..":'I',
	".---":'J',
	"-.-":'K',
	".-..":'L',
	"--":'M',
	"-.":'N',
	"---":'O',
	".--.":'P',
	"--.-":'Q',
	".-.":'R',
	"...":'S',
	"-":'T',
	"..-":'U',
	"...-":'V',
	".--":'W',
	"-..-":'X',
	"-.--":'Y',
	"--..":'Z',
	"-----":'0',
	".----":'1',
	"..---":'2',
	"...--":'3',
	"....-":'4',
	".....":'5',
	"-....":'6',
	"--...":'7',
	"---..":'8',
	"----.":'9',
	".-.-.-":'.',
	"--..--":',',
	"..--..":'?',
	"-....-":'-',
	"-...-":'=',
	"---...":':',
	"-.-.-.":';',
	"-.--.":'(',
	"-.--.-":')',
	"-..-.":'/',
	".-..-.":'"',
	"...-..-":'$',
	".----.":"'",
	"..--.-":'_',
	".--.-.":'@',
	"---.":'!',
	"-.-.--":'!',
	".-.-.":'+',
	".-...":'~',
	"...-.-":'#',
	". ...": '&',
	"-..-.":'/',
	"......":'\n[Error]\n',
	".-...":'\n[Wait]\n',
	"...-.":'\n[Understood]\n',
	".-.-.":'\n[End of message]\n',
	"...-.-":'\n[End of work]\n',
	"-.-.-":'\n[Starting signal]\n',
	"-.-":'\n[Invitation to transmit]\n'
}
