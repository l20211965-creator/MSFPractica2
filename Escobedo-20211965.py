# -*- coding: utf-8 -*-
"""
Práctica 2: sistema cardiovascular 

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Pamela Escobedo Sandoval 
Número de control: 20211965
Correo institucional:l20211965@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal 
import pandas as pd 

u= np.array(pd.read_excel('signal.xlsx', header=None))
x0,t0,tend,dt,w,h= 0,0,15,1e-3,10,5
N=round((tend-t0)/dt)+1
t=np.linspace(t0,tend,N)
u=np.reshape(signal.resample(u,len(t)),-1)


def cardio (Z,C,R,L):
    num= [L*R,R*Z]
    den= [C*L*R*Z,L*R+L*Z,R*Z]
    sys= ctrl.tf(num,den)
    return sys


# funcion de tranferencia : Normotenso 


Z,C,R,L= 0.33,1.5,0.95,0.01
sysnormo= cardio (Z,C,R,L)
print(f'funcion de tranferencia del normotenso (control): {sysnormo}')

# funcion de tranferencia : Hipotenso
Z,C,R,L= 0.02,0.25,0.6,0.005
syshipo= cardio (Z,C,R,L)
print(f'funcion de tranferencia del Hipotenso (caso 1): {syshipo}')

# funcion de tranferencia : Hipertenso 
Z,C,R,L= 0.05,2.5,1.4,0.02
syshiper= cardio (Z,C,R,L)
print(f'funcion de tranferencia del Hipertenso (caso 2): {syshiper}')



_,Pp0= ctrl.forced_response(sysnormo,t,u,x0)
_,Pp1= ctrl.forced_response(syshipo,t,u,x0)
_,Pp2= ctrl.forced_response(syshiper,t,u,x0)

fg1= plt.figure()
plt.plot(t,Pp0,'-',linewidth=1,color= [0.721, 0.859, 0.502], label='Pp(t)=Normotenso')
plt.plot(t,Pp0,'-',linewidth=1,color= [0.969, 0.965, 0.827], label='Pp(t)=Hipotenso')
plt.plot(t,Pp0,'-',linewidth=1,color= [1.000, 0.894, 0.937], label='Pp(t)=Hipertenso')
plt.grid(False)
plt.xlim(0,15); plt.xticks(np.arrange(0,16,1))
plt.ylim(-0.6,1.4); plt.xticks(np.arrange(-0.6,1.6,0.2))
plt.xlabes('t[s]')
plt.ylabel('Pp(t)[]v]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center ',ncol=3)
plt.show()
fg1.set_size_inches(w,h)
fg1.tigt_layout()
fg1.savefig('cardiovascular lazo abierto python.pdf ')



def controlador (kP,kI,kD,sys):
    
 Cr=1e-6
 Re=1/(kI*Cr)
 Rr=kP/Re
 Ce=kD/Rr
 numPID=[Re*Rr*Ce*Cr,(Re*Ce+Rr*Cr),+1]
 denPID=[Re*Cr,0]
 PID=ctrl.tf(numPID,denPID)
 x=ctrl.series(PID,sys)
 sysPID= ctrl.feedback (x,1,sign=-1)
 return sysPID

hipoPID= controlador(1.49397900518606,352.000659394334,0.00049119206492278,syshipo)
print(f'funcion de trenferencia del hipotenso en laza cerrado: {hipoPID}')

hiperPID= controlador(12.7154893348189,363.894411463659,0.0343454696960019,syshipo)
print(f'funcion de trenferencia del Hipertenso en laza cerrado: {hiperPID}')


_,PID1= ctrl.forced_response (hipoPID,t,Pp0,x0)
_,PID2= ctrl.forced_response (hipoPID,t,Pp0,x0)


