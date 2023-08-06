from scipy.fft import fft, fftfreq

def power_transfer(inputs, outputs, step): pass
def response_transfer(inputs, outputs, step): pass
def fourier_transfer(inputs, outputs, step): pass

def pspec(series, step):
    import scipy.signal
def rspec(series, step):
    pass
def fspec(series, step):
    assert len(series.shape) == 1
    N = len(series)
    return (fftfreq(N,step)[:N//2], fft(series))

def _newmark():
    pass
