#!/usr/bin/python
"""
fd, wav = wavfile.read("morse-7000khz.wav")
wav1,fd1,s,filter,g,m,p = morse.wav2sq(fd/10, wav[::10], 690, 50)
lt = morse.sq2morse(fd1, p, W=0.1, D=0.15)
# morse._plot(wav1,fd1,s,filter,g,m,p)
print morse.morse2text(lt)
"""
from pylab import *
from matplotlib.pyplot import *
import scipy.io.wavfile as wavfile
import numpy.fft as fft


#fd, wav = wavfile.read("morse-7000khz.wav")

def wav2sq(fd, wav, f, d):
	"Convert raw waveform to square pulses"
	L = wav.shape[0]

	# apply rectangular filter centered at f, width = 2*d
	s = fft.rfft(wav)
	filter = zeros(s.shape[0])
	filter[(f-d)*L/fd:(f+d)*L/fd] = 1
	g = fft.irfft(s * filter)

	# save wav
	o = zeros(g.shape[0], dtype=int16)
	o[:] = g[:]
	wavfile.write("/tmp/wav", fd, o)

	# moving average
	m = movavg(abs(g), 0.01*fd)

	# convert to square waves
	p = 1*(m > m.max()/3)

	return wav, fd, s, filter, g, m, p

def plot_wav2sq(wav, fd, s, filter, g, m, p):
	"Plot spectrum + filter and intermediate waveforms produced by wav2sq()"
	subplot(211)
	plot(arange(s.shape[0])*fd/wav.shape[0], s)
	plot(arange(filter.shape[0])*fd/wav.shape[0], filter*s.max(), '-r', linewidth=2)
	subplot(212)
	plot(arange(wav.shape[0])*1./fd, wav)
	plot(arange(g.shape[0])*1./fd, g)
	plot(arange(m.shape[0])*1./fd, m)
	plot(arange(p.shape[0])*1./fd, p*wav.max())

def sq2morse(fd, p, W=0.15, D=0.15):
	"Decode square pulses and produce morse code"
	morse = []
	lt = ""
	p[0] = 0
	p[-1] = 0
	edges = p[1:] - p[:-1]
	pe = arange(p.shape[0])[edges > 0]
	ne = arange(p.shape[0])[edges < 0]
	for i in arange(0,pe.shape[0]):
		w = (ne[i] - pe[i]) *1./fd
		if i > 0:
			d = (pe[i] - ne[i-1]) *1./fd
		else:
			d = 0
#		print "w=%.2f, d=%.2f" % (w, d)
		if d > D:
			morse.append(lt)
			lt = ""
		if d > 5*D:
			morse.append('space')
		if w > W:
			lt += '-'
		elif w > W/4:
			lt += '.'
		else:
			pass
	return morse


def morse2text(morse):
	"Convert morse code to letters using ITU coding scheme"
	txt = ""
	for l in morse:
		try:
			txt += ITU[l]
		except KeyError:
			txt += "[%s]" % l
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
	"......":'  <Error>  ',
	".-...":'  <Wait>  ',
	"...-.":'  <Understood>  ',
	".-.-.":'  <End of message>  ',
	"...-.-":'  <End of work>  ',
	"-.-.-":'  <Starting signal>  ',
	"-.-":'  <Invitation to transmit>  '
}
