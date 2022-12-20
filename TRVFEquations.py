import numpy as np
import math
import matplotlib.pyplot as plt


class TRVF(object):
  Kcurve = 5
  d = 3
  alpha = 2*math.pi/Kcurve
  beta = math.pi - alpha
  ms1 = 4
  
  r = staticmethod(lambda s:  (s*math.sin(TRVF.alpha/2) - TRVF.d/2)/(1 - math.sin(TRVF.alpha/2)))
  
  d_r = staticmethod(lambda s: math.sqrt(s*(2*TRVF.r(s) + s) - TRVF.r(s)*TRVF.d)) 
  
  @staticmethod
  def Tstart(vmed,n,D):
    ang = math.atan(TRVF.d/(2*D))
    Num = n*ang/(2*math.pi)
    return TRVF.ms1/((Num+1)*vmed)
  
  TfirstRobot = staticmethod(lambda vmed,s,D: TRVF.d_r(s)/vmed  + (TRVF.r(s))*0.5*TRVF.beta/vmed)
  
  @staticmethod
  def TleavingTarget(vmed,s,D):
    return (TRVF.d_r(s)/vmed + (TRVF.r(s))*0.5*TRVF.beta/vmed)
  
  @staticmethod
  def f1(K,n,I,v,s,D):
    return K*n/TRVF.Kcurve
  
  C3 = staticmethod(lambda vmed,s,I,n,D: TRVF.Tstart(vmed,n,D) + TRVF.TfirstRobot(vmed,s,D) + TRVF.TleavingTarget(vmed,s,D))
  
  @staticmethod
  def bestK(f, xs, ys, vs, Is, s, C0, D, f0, i0=2):
    Cs = [C0(vs[i],s,Is[i],xs[i],D) for i in range(len(vs))]
    A = sum([f(1,xs[i],Is[i],vs[i],s,D)*(ys[i] - Cs[i]) for i in range(i0,f0+1)])
    B = sum([f(1,xs[i],Is[i],vs[i],s,D)**2 for i in range(i0,f0+1)])
    return A/B

  @staticmethod
  def doTheFitting(xs,ys,linear=True,maxIndex=None):
    maxFit = len(xs) - 4 if maxIndex==None else maxIndex
    maxFit = len(xs)
    if linear:
      mymodel0 = np.poly1d(np.polyfit(xs[:maxFit],ys[:maxFit],1))
      print(mymodel0)
      mymodel0values = mymodel0(xs)
    else:
      sqrtData = [math.sqrt(v) for v in xs]
      mymodel0 = np.poly1d(np.polyfit(sqrtData[:maxFit],ys[:maxFit],2))
      print(mymodel0)
      mymodel0values = mymodel0(sqrtData)
    return mymodel0values
  
  @staticmethod
  def plotEstimation(varValues, dataMean, a, option, s, D):
    Imed = 0.5*np.array(dataMean[:,a,13])
    vmed = dataMean[:,a,16]

    K1 = TRVF.bestK(TRVF.f1,varValues,dataMean[:,a,option],vmed,Imed,s,TRVF.C3,D,len(vmed)-1,0)
    print("TRVF K =", K1)
    Y1 = [TRVF.C3(vmed[i],s,Imed[i],varValues[i],D) + TRVF.f1(K1,varValues[i],Imed[i],vmed[i],s,D) for i in range(len(varValues))]
    plt.plot(varValues,Y1,label="Estimation")
  
  @staticmethod
  def plotAndReturnEstimation(varValues, dataMean, a, option, s, D, m, i_sf, Imed2, vmed2, plotIt=True):
    if 0 in dataMean[:,m,a,i_sf,13]:
      Imed = Imed2
    else:
      Imed = 0.5*np.array(dataMean[:,m,a,i_sf,13])
    if 0 in dataMean[:,m,a,i_sf,16]:
      vmed = vmed2
    else:
      vmed = dataMean[:,m,a,i_sf,16]
    K1 = TRVF.bestK(TRVF.f1,varValues,dataMean[:,m,a,i_sf,option],vmed,Imed,s,TRVF.C3,D,len(vmed)-1,0)
    # ~ print("TRVF K =", K1)
    Y1 = [TRVF.C3(vmed[i],s,Imed[i],varValues[i],D) + TRVF.f1(K1,varValues[i],Imed[i],vmed[i],s,D) for i in range(len(varValues))]
    if plotIt: plt.plot(varValues,Y1,label="Estimation")
    
    return Y1

