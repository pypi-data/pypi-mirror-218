# Keith Briggs 2022-03-07
# Self-test (makes a plot): python3 InH_pathloss_model_00.py

from sys import exit,stderr
from math import log10
from numpy.linalg import norm

class InH_pathloss:
  '''
  3D-InH indoor pathloss model, from 3GPP standard 36.873, Table 7.2-1.
  Indoor Hotspot cell with high (indoor) UE density.

  The model is defined in 36873-c70.doc from https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=2574.

  LOS    = line-of-sight.
  NLOS   = non-line-of-sight.

  '''
  def __init__(s,fc_GHz=3.5,h_UT=2.0,h_BS=4.0,LOS=True):
    '''
    Initialize a pathloss model instance.

    Parameters
    ----------
    fc_GHz : float
      Centre frequency in GigaHertz (default 3.5).
    h_UT : float
      Height of User Terminal (=UE) in metres (default 2).
    h_BS : float
      Height of Base Station in metres (default 25).
    '''
    s.fc=fc_GHz # in GHz
    s.log10fc=log10(s.fc)
    s.h_UT=h_UT
    s.h_BS=h_BS
    s.LOS=LOS
    # pre-compute constants to speed up calls...
    s.const_LOS =32.8+20.0*s.log10fc
    s.const_NLOS=11.5+20.0*s.log10fc

  def __call__(s,xyz_cell,xyz_UE):
    '''
    Return the pathloss between 3-dimensional positions xyz_cell and
    xyz_UE (in metres).
    Note that the distances, heights, etc. are not checked
    to ensure that this pathloss model is actually applicable.
    '''
    # TODO: could we usefully vectorize this, so that xyz_cell,xyz_UE have shape (n,3) to compute n pathlosses at once?
    d3D_m=norm(xyz_cell-xyz_UE)
    if s.LOS:
      return s.const_LOS+16.9*log10(d3D_m)
    # else NLOS:
    return s.const_NLOS+43.3*log10(d3D_m)

def plot():
  ' Plot the pathloss model predictions, as a self-test. '
  import numpy as np
  import matplotlib.pyplot as plt
  from fig_timestamp_00 import fig_timestamp
  fig=plt.figure(figsize=(8,6))
  ax=fig.add_subplot()
  ax.grid(color='gray',alpha=0.7,lw=0.5)
  d=np.linspace(10,150,100) # NLOS valid from 10m
  PL=InH_pathloss(LOS=False)
  NLOS=np.array([PL(0,di) for di in d])
  ax.plot(d,NLOS,lw=2,label='NLOS ($\sigma=4$)') # or semilogx
  ax.fill_between(d,NLOS-4.0,NLOS+4.0,alpha=0.2) # sigma_{SF}=4 for NLOS case
  d=np.linspace(3,150,100) # NLOS valid from 3m
  PL=InH_pathloss(LOS=True)
  LOS=np.array([PL(0,di) for di in d])
  ax.plot(d,LOS,lw=2,label='LOS ($\sigma=3$)') # or semilogx
  ax.fill_between(d,LOS-3.0,LOS+3.0,alpha=0.2) # sigma_{SF}=3 for LOS case
  ax.set_xlabel('distance (metres)')
  ax.set_ylabel('pathloss (dB)')
  ax.set_xlim(0,np.max(d))
  ax.set_ylim(40)
  ax.legend()
  ax.set_title('3GPP Indoor Hotspot cell with high (indoor) UE density')
  fig.tight_layout()
  fig_timestamp(fig,rotation=0,fontsize=6,author='Keith Briggs')
  fnbase='img/InH_pathloss_model_01'
  fig.savefig(f'{fnbase}.png')
  print(f'eog {fnbase}.png &',file=stderr)
  fig.savefig(f'{fnbase}.pdf')
  print(f'evince {fnbase}.pdf &',file=stderr)

if __name__=='__main__':
  plot()
