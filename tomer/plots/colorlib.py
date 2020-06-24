import os, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col

#==============================================================================
# Version 0.7, universally upated 10/26/17
#==============================================================================
    
def rgb(r,g,b):
    r = int(r)
    g = int(g)
    b = int(b)
    return '#%02x%02x%02x' % (r, g, b)
    
def getColor(val,rng,col1,col2):
    r1,g1,b1 = col1
    r2,g2,b2 = col2
    
    #168,0,168 to 0,0,230 = -168,0,+62
    #rng = (-16 - value)
    rdif = float(r2 - r1)
    gdif = float(g2 - g1)
    bdif = float(b2 - b1)
    
    r3 = r2 + (-1.0 * val * (rdif / float(rng)))
    g3 = g2 + (-1.0 * val * (gdif / float(rng)))
    b3 = b2 + (-1.0 * val * (bdif / float(rng)))

    return rgb(r3,g3,b3)
    
#==============================================================================
# Color Lists
#==============================================================================

def precip():
    
    cols1 = ['#ffffff','#EBEBEB','#D7D7D7','#C3C3C3','#00F000','#00DC00','#00C800','#009600','#008200','#006E00','#324196','#3255A5','#2869B4','#1E87C3','#14A5D2','#00FFFF','#1EE6FF','#3CCDFF','#5AB4FF','#789BFF','#FF00FF','#E100E1','#AA00AA','#960096','#820082','#FF0000','#DC0000','#B40000','#FF8C00','#FFCD00','#FFF800']

    cmap3 = col.ListedColormap(cols1)
    
    return cmap3

def precip2():
    
    cols = ['#ffffff','#EBEBEB','#D7D7D7','#C3C3C3','#00F000','#00DC00','#00C800','#009600','#008200','#006E00','#324196','#3255A5','#2869B4','#1E87C3','#14A5D2','#00FFFF','#1EE6FF','#3CCDFF','#5AB4FF','#789BFF','#FF00FF','#E100E1','#AA00AA','#960096','#820082','#FF0000','#DC0000','#B40000','#FF8C00','#FFCD00','#FFF800']
    
    cols = ['#ffffff','#EBEBEB','#D7D7D7','#C3C3C3','#00F000','#00DC00','#00C800','#009600','#008200','#006E00','#324196','#3255A5','#2869B4','#1E87C3','#14A5D2','#00FFFF','#1EE6FF','#3CCDFF','#5AB4FF','#789BFF','#FF00FF','#E100E1','#AA00AA','#960096','#820082','#FF0000','#DC0000','#B40000','#FF7C00','#FFA600','#FFC000','#FFDE00','#FFFF00']
    
    cols = ['#ffffff','#EBEBEB','#D7D7D7','#C3C3C3','#00F000','#00DC00','#00C800','#009600','#008200','#006E00','#324196','#3255A5','#2869B4','#1E87C3','#14A5D2','#00FFFF','#1EE6FF','#3CCDFF','#5AB4FF','#789BFF','#FF00FF','#E100E1','#AA00AA','#960096','#820082','#FF0000','#DC0000','#B40000','#FF7C00','#FFA600','#FFC000','#FFDE00','#FFFF00','#9FFF55','#D5FFB5']

    cols1 = []
    for icol in cols:
        icol2 = icol[1:]
        r2 = 255
        g2 = 255
        b2 = 255
        a1 = 0.84 #1 solid, 0 blank, previously 0.80

        r1,g1,b1 = tuple(int(icol2[i:i+2], 16) for i in (0, 2 ,4))
        r3 = r2 + (r1-r2)*a1
        g3 = g2 + (g1-g2)*a1
        b3 = b2 + (b1-b2)*a1
        cols1.append(rgb(r3,g3,b3))
    
    cmap3 = col.ListedColormap(cols1)
    
    return cmap3
    
def wind():
    
    #clevs = [50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
    cmap3 = col.ListedColormap(['#00FFFF','#00EBFF','#00AAFF','#0096FF','#003CFF','#0000FF','#9600FF','#B400FF','#FF00FF','#FF3CFF','#FFABD9','#FFB9DF','#FF9393','#FF7575','#FF0000','#EA0000'])
    
    return cmap3

def shear():
    
    #clevs = 5,10,15,20,25,30,35,40,45,50,55,60,65,70,
    cmap3 = col.ListedColormap(['#72EBFF','#15B5FF','#0096FF','#115ED2','#0B4FB6','#3DA550','#3CCE4A','#9EEB19','#C4FD09','#FFFC00','#FFEB00','#FFB300','#FF9500','#FF4D00','#FF0000'])
    cmap3 = col.ListedColormap(['#8BEFFF','#00AFFF','#008DFF','#0E58C7','#0947A3','#339745','#37AB4C','#98D62E','#B4E121','#FFFC00','#FFEB00','#FFB300','#FF9500','#FF4D00','#E50000'])
    
    return cmap3
    
def wind2():
    
    #clevs = [50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
    #         40    50    60     70      80      90      100     110
    cmap3 = col.ListedColormap(['#99E3FB','#47B6FB','#0F77F7','#AC97F5','#A267F4','#9126F5','#E118F3','#E118F3'])

    return cmap3
    
def pwatanom():
    
    #clevs = [-6,-5,-4,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,4,5,6]
    cmap3 = col.ListedColormap(['#772C00','#94400F','#A84F1B','#C76730','#E28C5A','#EB996A','#','#','#','#','#','#','#','#','#','#'])
    
    return cmap3

def stdanom():
    
    #clevs = [-7,-6,-5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,3.5,4,5,6,7]
    cmap3 = col.ListedColormap(['#772C00','#94400F','#A84F1B','#C76730','#E28C5A','#EB996A','#','#','#','#','#','#','#','#','#','#'])
    
    return cmap3

def vorticity():

    cdict = {'red':   [(0.0, 1.0, 1.0),
                       (0.5, 1.0, 1.0),
                       (1.0, 0.4, 0.4)],
    
             'green': [(0.0, 1.0, 1.0),
                       (0.5, 0.0, 0.0),
                       (1.0, 0.0, 0.0)],
    
             'blue':  [(0.0, 0.0, 0.0),
                       (0.5, 0.0, 0.0),
                       (1.0, 0.0, 0.0)]}
               
    #Define colormap as cmap3
    cmap3 = col.LinearSegmentedColormap('my_colormap',cdict,256)
    
    return cmap3
 
#==============================================================================

def std_anom(clevs):
    
    cool = ['#cdedff','#53c4ff','#0093ff','#0057ff','#2900f4','#4c00d6','#5800b9','#5c009f','#7b24a8','#a84dc4','#d474e1','#ff9dff']

    cool = ['#ffd5ff','#ff9dff','#dc66f0','#a71cd2','#8f18b4','#4e00a4','#2c009a','#2900f4','#004dff','#3babff','#53c4ff','#cdedff']
    warm = ['#FFEEA5','#ffac6d','#ff8857','#ff2929','#e50009','#b40008','#960008','#a61464','#bb1771','#e30bc9','#f86ce7','#fbb3f2']
    
    colors = cool + ['#ffffff'] + warm
    
    return colors    
  
#==============================================================================

def ir(clevs):
    
    colors = []
    for value in clevs:
    
        if value < -95:
            colors.append(rgb(238,165,237))
            
        elif value < -80:
            rng = 15
            val = (-80 - value)
            colors.append(getColor(val,rng,[238,165,237],[245,245,245]))
            
        elif value < -70:
            rng = 10
            val = (-70 - value)
            colors.append(getColor(val,rng,[245,245,245],[20,20,20]))
            
        elif value < -60:
            rng = 10
            val = (-60 - value)
            colors.append(getColor(val,rng,[20,20,20],[255,0,0]))
            
        elif value < -50:
            rng = 10
            val = (-50 - value)
            colors.append(getColor(val,rng,[255,0,0],[255,255,0]))
            
        elif value < -40:
            rng = 10
            val = (-40 - value)
            colors.append(getColor(val,rng,[255,255,0],[0,240,0]))
            
        elif value < -30:
            rng = 10
            val = (-30 - value)
            colors.append(getColor(val,rng,[0,240,0],[0,0,155]))
            
        elif value < -20:
            rng = 10
            val = (-20 - value)
            colors.append(getColor(val,rng,[0,0,155],[0,255,255]))
            
        elif value < -10:
            rng = 10
            val = (-10 - value)
            colors.append(getColor(val,rng,[255,255,255],[180,180,180]))
            
        elif value < 0:
            rng = 10
            val = (0 - value)
            colors.append(getColor(val,rng,[180,180,180],[90,90,90]))
            
        elif value < 20:
            rng = 20
            val = (20 - value)
            colors.append(getColor(val,rng,[90,90,90],[0,0,0]))
            
        else:
            colors.append(rgb(0,0,0))
            
    return colors

def ir2(clevs):
    
    colors = []
    for value in clevs:
    
        if value < -95:
            colors.append(rgb(238,165,237))
            
        elif value < -80:
            rng = 15
            val = (-80 - value)
            colors.append(getColor(val,rng,[238,165,237],[245,245,245]))
            
        elif value < -70:
            rng = 10
            val = (-70 - value)
            colors.append(getColor(val,rng,[245,245,245],[20,20,20]))
            
        elif value < -60:
            rng = 10
            val = (-60 - value)
            colors.append(getColor(val,rng,[20,20,20],[255,0,0]))
            
        elif value < -50:
            rng = 10
            val = (-50 - value)
            colors.append(getColor(val,rng,[255,0,0],[255,255,0]))
            
        elif value < -40:
            rng = 10
            val = (-40 - value)
            colors.append(getColor(val,rng,[255,255,0],[0,240,0]))
            
        elif value < -30:
            rng = 10
            val = (-30 - value)
            colors.append(getColor(val,rng,[0,240,0],[0,0,155]))
            
        elif value < -20:
            rng = 10
            val = (-20 - value)
            colors.append(getColor(val,rng,[0,0,155],[0,255,255]))
            
        elif value < -5:
            rng = 15
            val = (-5 - value)
            colors.append(getColor(val,rng,[255,255,255],[180,180,180]))
            
        elif value < 40:
            rng = 45
            val = (40 - value)
            colors.append(getColor(val,rng,[180,180,180],[0,0,0]))
            
        else:
            colors.append(rgb(0,0,0))
            
    return colors
    
#==============================================================================

def cape(clevs):
    
    colors = []
    for value in clevs:
    
        if value < 100:
            colors.append(rgb(255,255,255))
            
        elif value < 1000:
            rng = 900
            val = (1000 - value)
            colors.append(getColor(val,rng,[241,241,241],[160,160,160]))
            
        elif value < 2000:
            rng = 1000
            val = (2000 - value)
            colors.append(getColor(val,rng,[185,222,255],[0,89,178]))
            
        elif value < 3000:
            rng = 1000
            val = (3000 - value)
            colors.append(getColor(val,rng,[158,255,254],[0,129,127]))
            
        elif value < 4000:
            rng = 1000
            val = (4000 - value)
            colors.append(getColor(val,rng,[152,255,145],[8,110,0]))
            
        elif value < 5000:
            rng = 1000
            val = (5000 - value)
            colors.append(getColor(val,rng,[255,255,111],[128,107,0]))
            
        elif value < 6000:
            rng = 1000
            val = (6000 - value)
            colors.append(getColor(val,rng,[255,166,141],[115,0,0]))
            
        elif value < 7000:
            rng = 1000
            val = (7000 - value)
            colors.append(getColor(val,rng,[255,147,254],[114,0,110]))
            
        else:
            colors.append(rgb(69,0,115))
            
    return colors
    
#==============================================================================
  
def pvu(clevs):
    
    colors = []
    for value in clevs:
    
        if value < 0:
            #colors.append(rgb(7,95,172))
            colors.append(rgb(49,122,186))
            
        elif value < 1:
            rng = 1
            val = (1 - value)
            colors.append(getColor(val,rng,[66,137,199],[190,218,243]))
            
        elif value < 2:
            rng = 1
            val = (2 - value)
            colors.append(getColor(val,rng,[190,218,243],[242,245,228]))
            
        elif value < 3.5:
            rng = 1.5
            val = (3.5 - value)
            colors.append(getColor(val,rng,[242,245,55],[229,171,46]))
            
        elif value < 6:
            rng = 2.5
            val = (6 - value)
            colors.append(getColor(val,rng,[229,171,46],[235,0,0]))
            
        elif value < 8:
            rng = 2
            val = (8 - value)
            colors.append(getColor(val,rng,[235,0,0],[185,0,0]))
            
        elif value < 14:
            rng = 6
            val = (14 - value)
            colors.append(getColor(val,rng,[185,0,0],[248,155,231])) #246,110,221
            
        else:
            colors.append(rgb(248,155,231))
            
    return colors

#==============================================================================

def mslp(clevs):
    
    colors = []
    for value in clevs:
    
        if value < 930:
            colors.append(rgb(255,255,255))
            
        elif value < 950:
            rng = 20
            val = (950 - value)
            colors.append(getColor(val,rng,[255,255,255],[255,0,255]))
            
        elif value < 975:
            rng = 25
            val = (975 - value)
            colors.append(getColor(val,rng,[255,0,255],[0,15,255]))
            
        elif value < 995:
            rng = 20
            val = (995 - value)
            colors.append(getColor(val,rng,[0,15,255],[0,255,255]))
            
        elif value < 1010:
            rng = 15
            val = (1010 - value)
            colors.append(getColor(val,rng,[0,255,255],[0,205,0]))
            
        elif value < 1020:
            rng = 10
            val = (1020 - value)
            colors.append(getColor(val,rng,[0,205,0],[255,255,0]))
            
        elif value < 1040:
            rng = 20
            val = (1040 - value)
            colors.append(getColor(val,rng,[255,255,0],[255,0,0]))
            
        elif value < 1060:
            rng = 20
            val = (1060 - value)
            colors.append(getColor(val,rng,[255,0,0],[150,0,0]))
            
        else:
            colors.append(rgb(255,255,255))
            
    return colors
    
#==============================================================================

def conv(clevs):
    
    colors = []
    for value in clevs:
    
        if value < 4:
            colors.append(rgb(255,255,255))
            
        elif value < 14:
            rng = 10
            val = (14 - value)
            colors.append(getColor(val,rng,[230,230,230],[150,150,150]))
            
        else:
            colors.append(rgb(160,160,160))
            
    return colors
    
#==============================================================================
  
def mixr(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 0:
            colors.append(rgb(94,61,32))
            
        elif value < 8:
            rng = 8
            val = (8 - value)
            colors.append(getColor(val,rng,[77,48,23],[249,215,185]))
            
        elif value < 13:
            rng = 5
            val = (13 - value)
            colors.append(getColor(val,rng,[185,249,190],[0,105,8])) #121
            
        elif value < 18:
            rng = 5
            val = (18 - value)
            colors.append(getColor(val,rng,[142,203,255],[0,76,142])) #[0,86,162]
            
        elif value < 23:
            rng = 5
            val = (23 - value)
            colors.append(getColor(val,rng,[195,166,252],[75,26,174]))
            
        elif value < 28:
            rng = 5
            val = (28 - value)
            colors.append(getColor(val,rng,[255,0,255],[120,0,120]))

        else:
            colors.append(rgb(0,0,130))
            
        
    return colors
    
#==============================================================================
    
def windsfc(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 3:
            colors.append(rgb(255,255,255))
            
        elif value < 10:
            rng = 7
            val = (10 - value)
            colors.append(getColor(val,rng,[250,250,250],[180,180,180]))
            
        elif value < 20:
            rng = 10
            val = (20 - value)
            colors.append(getColor(val,rng,[0,255,255],[0,105,255])) #0,140,255 -->
            
        elif value < 30:
            rng = 10
            val = (30 - value)
            colors.append(getColor(val,rng,[178,169,255],[72,0,216])) #168,180,255 <--
            
        elif value < 40:
            rng = 10
            val = (40 - value)
            colors.append(getColor(val,rng,[255,0,255],[110,0,110])) #160
                    
        elif value < 50:
            rng = 10
            val = (50 - value)
            colors.append(getColor(val,rng,[255,0,0],[120,0,0])) #150
            
        elif value < 60:
            rng = 10
            val = (60 - value)
            colors.append(getColor(val,rng,[255,148,148],[124,39,39]))
            
        elif value < 70:
            rng = 10
            val = (70 - value)
            colors.append(getColor(val,rng,[255,198,146],[165,77,0]))

        else:
            colors.append(rgb(255,255,0))
            
        
    return colors  

#==============================================================================

def omega(clevs):
    
    colors = []
    for value in clevs:
        
        if value < -40:
            colors.append(rgb(131,0,0))
            
        elif value < -34:
            rng = 6
            val = (-34 - value)
            colors.append(getColor(val,rng,[131,0,0],[255,0,0]))
            
        elif value < -28:
            rng = 6
            val = (-28 - value)
            colors.append(getColor(val,rng,[255,0,0],[255,0,255]))
            
        elif value < -22:
            rng = 6
            val = (-22 - value)
            colors.append(getColor(val,rng,[255,0,255],[168,0,168]))
            
        elif value < -16:
            rng = 6
            val = (-16 - value)
            colors.append(getColor(val,rng,[168,0,168],[0,0,230]))
            
        elif value < -7:
            rng = 9
            val = (-7 - value)
            colors.append(getColor(val,rng,[0,0,230],[0,230,255]))
            
        elif value < 0:
            rng = 7
            val = (0 - value)
            colors.append(getColor(val,rng,[0,230,255],[216,255,255]))
            
        elif value < 5:
            rng = 5
            val = (5 - value)
            colors.append(getColor(val,rng,[255,255,255],[225,225,225]))

        elif value < 15:
            rng = 10
            val = (15 - value)
            colors.append(getColor(val,rng,[225,225,225],[170,170,170]))

        else:
            colors.append(rgb(170,170,170))  
        
        
    return colors
    
    
#==============================================================================
    
def fgen(clevs):
    
    colors = []
    for value in clevs:
        
        if value < -14:
            colors.append(rgb(150,150,150))
            
        elif value < -9:
            rng = 5
            val = (-9 - value)
            colors.append(getColor(val,rng,[150,150,150],[180,180,180]))
            
        elif value < -0.5:
            rng = 8.5
            val = (-0.5 - value)
            colors.append(getColor(val,rng,[180,180,180],[242,242,242]))
            
        elif value < 0.5:
            colors.append(rgb(255,255,255))
            
        elif value < 6:
            rng = 5.5
            val = (6 - value)
            colors.append(getColor(val,rng,[255,234,188],[255,0,0]))
            
        elif value < 12:
            rng = 6
            val = (12 - value)
            colors.append(getColor(val,rng,[255,0,0],[140,0,0]))
            
        elif value < 24:
            rng = 12
            val = (24 - value)
            colors.append(getColor(val,rng,[140,0,0],[255,0,255]))
            
        else:
            colors.append(rgb(255,0,255))
        
       
    return colors
    
#==============================================================================

def theta_dt(clevs):
    #260 to 400
    colors = []
    for value in clevs:
        
        if value < 250:
            colors.append(rgb(113,215,239))
            
        elif value < 270:
            rng = 20
            val = (270 - value)
            colors.append(getColor(val,rng,[113,215,239],[255,255,255]))
            
        elif value < 285:
            rng = 15
            val = (285 - value)
            colors.append(getColor(val,rng,[255,255,255],[255,0,255]))
            
        elif value < 300:
            rng = 15
            val = (300 - value)
            colors.append(getColor(val,rng,[255,0,255],[0,30,255]))
            
        elif value < 320:
            rng = 20
            val = (320 - value)
            colors.append(getColor(val,rng,[0,30,255],[0,255,255]))
            
        elif value < 340:
            rng = 20
            val = (340 - value)
            colors.append(getColor(val,rng,[0,255,255],[0,170,0]))
            
        elif value < 355:
            rng = 15
            val = (355 - value)
            colors.append(getColor(val,rng,[0,170,0],[255,255,0]))
            
        elif value < 375:
            rng = 20
            val = (375 - value)
            colors.append(getColor(val,rng,[255,255,0],[255,0,0]))
            
        elif value < 400:
            rng = 25
            val = (400 - value)
            colors.append(getColor(val,rng,[255,0,0],[120,0,0]))

        else:
            colors.append(rgb(120,0,0))  
        
        
    return colors

#==============================================================================

def theta_sfc(clevs):
    #260 to 400
    #230 to 330 (100 instead of 140)
    colors = []
    for value in clevs:
        
        if value < 230:
            colors.append(rgb(255,255,255))
            
        elif value < 247:
            rng = 17
            val = (247 - value)
            colors.append(getColor(val,rng,[255,255,255],[255,0,255]))
            
        elif value < 258:
            rng = 11
            val = (258 - value)
            colors.append(getColor(val,rng,[255,0,255],[0,30,255]))
            
        elif value < 272:
            rng = 14
            val = (272 - value)
            colors.append(getColor(val,rng,[0,30,255],[0,255,255]))
            
        elif value < 287:
            rng = 15
            val = (287 - value)
            colors.append(getColor(val,rng,[0,255,255],[0,150,0]))
            
        elif value < 297:
            rng = 10
            val = (297 - value)
            colors.append(getColor(val,rng,[0,150,0],[255,255,0]))
            
        elif value < 312:
            rng = 15
            val = (312 - value)
            colors.append(getColor(val,rng,[255,255,0],[255,0,0]))
            
        elif value < 330:
            rng = 18
            val = (330 - value)
            colors.append(getColor(val,rng,[255,0,0],[120,0,0]))

        else:
            colors.append(rgb(120,0,0))  
        
        
    return colors

#==============================================================================

def thetae_sfc(clevs):
    #260 to 400
    #230 to 400 (170 instead of 140)
    #now to 380
    
    colors = []
    for value in clevs:
        
        if value < 230:
            colors.append(rgb(255,255,255))
            
        elif value < 260:
            rng = 30
            val = (260 - value)
            colors.append(getColor(val,rng,[255,255,255],[255,0,255]))
            
        elif value < 276: #2
            rng = 16
            val = (276 - value)
            colors.append(getColor(val,rng,[255,0,255],[0,30,255]))
            
        elif value < 298: #4
            rng = 22
            val = (298 - value)
            colors.append(getColor(val,rng,[0,30,255],[0,255,255]))
            
        elif value < 319: #8
            rng = 21
            val = (319 - value)
            colors.append(getColor(val,rng,[0,255,255],[0,150,0]))
            
        elif value < 333: #12
            rng = 14
            val = (333 - value)
            colors.append(getColor(val,rng,[0,150,0],[255,255,0]))
            
        elif value < 353: #16
            rng = 20
            val = (353 - value)
            colors.append(getColor(val,rng,[255,255,0],[255,0,0]))
            
        elif value < 380:
            rng = 27
            val = (380 - value)
            colors.append(getColor(val,rng,[255,0,0],[120,0,0]))

        else:
            colors.append(rgb(120,0,0))  
        
        
    return colors
    
#==============================================================================

def pwat(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 0:
            colors.append(rgb(94,61,32))
            
        elif value < 12:
            rng = 12
            val = (12 - value)
            colors.append(getColor(val,rng,[77,48,23],[249,215,185]))
            
        elif value < 24:
            rng = 12
            val = (24 - value)
            colors.append(getColor(val,rng,[185,249,190],[0,105,8]))
            
        elif value < 36:
            rng = 12
            val = (36 - value)
            colors.append(getColor(val,rng,[142,203,255],[0,76,142]))
            
        elif value < 48:
            rng = 12
            val = (48 - value)
            colors.append(getColor(val,rng,[195,166,252],[67,19,164]))
            
        elif value < 60:
            rng = 12
            val = (60 - value)
            colors.append(getColor(val,rng,[255,87,255],[120,0,120]))
            
        elif value < 72:
            rng = 12
            val = (72 - value)
            colors.append(getColor(val,rng,[255,166,166],[114,23,23]))

        else:
            colors.append(rgb(100,0,0))
            
        
    return colors



def pwat2(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 0:
            colors.append(rgb(112,56,0))
            
        elif value < 15:
            rng = 15
            val = (15 - value)
            colors.append(getColor(val,rng,[112,56,0],[255,236,217]))
            
        elif value < 30:
            rng = 15
            val = (30 - value)
            colors.append(getColor(val,rng,[255,255,147],[0,222,0]))
            
        elif value < 45:
            rng = 15
            val = (45 - value)
            colors.append(getColor(val,rng,[0,208,0],[0,105,142]))
            
        elif value < 60:
            rng = 15
            val = (60 - value)
            #colors.append(getColor(val,rng,[0,90,122],[144,0,208]))
            colors.append(getColor(val,rng,[0,96,130],[195,0,234]))
            
        elif value < 75:
            rng = 15
            val = (75 - value)
            #colors.append(getColor(val,rng,[164,0,238],[245,197,255]))
            colors.append(getColor(val,rng,[215,17,255],[246,201,255]))

        else:
            colors.append(rgb(246,201,255))
            
        
    return colors



def iv(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 0:
            colors.append(rgb(94,61,32))
            
        elif value < 4:
            rng = 4
            val = (4 - value)
            colors.append(getColor(val,rng,[77,48,23],[249,215,185]))
            
        elif value < 8:
            rng = 4
            val = (8 - value)
            colors.append(getColor(val,rng,[185,249,190],[0,105,8]))
            
        elif value < 12:
            rng = 4
            val = (12 - value)
            colors.append(getColor(val,rng,[142,203,255],[0,76,142]))
            
        elif value < 16:
            rng = 4
            val = (16 - value)
            colors.append(getColor(val,rng,[195,166,252],[67,19,164]))
            
        elif value < 20:
            rng = 4
            val = (20 - value)
            colors.append(getColor(val,rng,[255,87,255],[120,0,120]))
            
        elif value < 24:
            rng = 4
            val = (24 - value)
            colors.append(getColor(val,rng,[255,166,166],[114,23,23]))

        else:
            colors.append(rgb(100,0,0))
            
        
    return colors
    
    
def lance_pwat(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 20:
            colors.append(rgb(255,255,255))
            
        elif value < 34:
            rng = 14
            val = (34 - value)
            colors.append(getColor(val,rng,[205,255,205],[0,255,0]))
            
        elif value < 67:
            rng = 33
            val = (67 - value)
            colors.append(getColor(val,rng,[0,255,0],[0,115,0]))

        else:
            colors.append(rgb(0,115,0))  
        
        
    return colors

def synopsis_pwat(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 67:
            colors.append(colorlib.rgb(255,255,255))
            
        elif value < 71:
            rng = 4
            val = (71 - value)
            colors.append(colorlib.getColor(val,rng,[205,255,205],[0,255,0]))
            
        elif value < 82:
            rng = 11
            val = (82 - value)
            colors.append(colorlib.getColor(val,rng,[0,255,0],[0,115,0]))

        else:
            colors.append(colorlib.rgb(0,115,0))  
        
        
    return colors
    
def ivt_pwat(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 20:
            colors.append(rgb(255,255,255))
            
        elif value < 32:
            rng = 12
            val = (32 - value)
            colors.append(getColor(val,rng,[220,255,205],[70,255,70]))
            
        elif value < 55:
            rng = 23
            val = (55 - value)
            colors.append(getColor(val,rng,[70,255,70],[50,163,50]))

        else:
            colors.append(rgb(50,163,50))  
        
        
    return colors

#==============================================================================

def tempdiff(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 6:
            colors.append(rgb(255,255,255))
            
        elif value < 13:
            rng = 7
            val = (13 - value)
            colors.append(getColor(val,rng,[159,230,255],[0,100,255])) #119
            
        elif value < 24:
            rng = 11
            val = (24 - value)
            colors.append(getColor(val,rng,[0,0,255],[255,0,255])) #222
            
        elif value < 30:
            rng = 6
            val = (30 - value)
            colors.append(getColor(val,rng,[230,0,0],[180,0,0]))
            
        else:
            colors.append(rgb(200,0,0))  
        
        
    return colors

#==============================================================================

def lapse(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 5.5:
            colors.append(rgb(255,255,255))
            
        elif value < 6.0:
            rng = 0.5
            val = (6.0 - value)
            colors.append(getColor(val,rng,[245,245,245],[190,190,190])) #119
            
        elif value < 6.5:
            rng = 0.5
            val = (6.5 - value)
            colors.append(getColor(val,rng,[0,255,0],[0,190,0])) #222
            
        elif value < 7.0:
            rng = 0.5
            val = (7.0 - value)
            colors.append(getColor(val,rng,[0,180,0],[0,140,0])) #222
            
        elif value < 7.5:
            rng = 0.5
            val = (7.5 - value)
            colors.append(getColor(val,rng,[255,255,0],[255,190,0]))
            
        elif value < 8.0:
            rng = 0.5
            val = (8.0 - value)
            colors.append(getColor(val,rng,[255,170,0],[255,95,0]))
            
        elif value < 8.5:
            rng = 0.5
            val = (8.5 - value)
            colors.append(getColor(val,rng,[255,0,0],[190,0,0]))
            
        elif value < 9.0:
            rng = 0.5
            val = (9.0 - value)
            colors.append(getColor(val,rng,[180,0,0],[135,0,0]))
            
        elif value < 9.5:
            rng = 0.5
            val = (9.5 - value)
            colors.append(getColor(val,rng,[255,0,255],[190,0,190]))
            
        elif value < 10.0:
            rng = 0.5
            val = (10.0 - value)
            colors.append(getColor(val,rng,[170,0,170],[125,0,125]))
            
        else:
            colors.append(rgb(140,0,140))
        
        
    return colors
    
#==============================================================================

def tempf(clevs):
    
    crng = 10
    
    colors = []
    for value in clevs:
        
        #we go from bottom to top, so left value (115) is starting, right side is adjustment
        #towards the final state
    
        if value < -50:
            colors.append(rgb(31,80,169))
            
        elif value < -40:
            rng = crng
            val = (-40 - value)
            colors.append(getColor(val,rng,[49,105,173],[24,165,176]))
            
        elif value < -30:
            rng = crng
            val = (-30 - value)
            colors.append(getColor(val,rng,[26,184,188],[113,232,235]))

        elif value < -20:
            rng = crng
            val = (-20 - value)
            colors.append(getColor(val,rng,[113,215,239],[250,30,255]))
            
        elif value < -10:
            rng = crng
            val = (-10 - value)
            colors.append(getColor(val,rng,[206,11,239],[115,41,213]))
            
        elif value < 0:
            rng = crng
            val = (0 - value)
            colors.append(getColor(val,rng,[144,84,222],[212,183,249]))
            
        elif value < 10:
            rng = crng
            val = (10 - value)
            colors.append(getColor(val,rng,[230,230,255],[52,52,219]))
            
        #dark blue 10-20
        elif value < 20:
            rng = crng
            val = (20 - value)
            colors.append(getColor(val,rng,[0,0,222],[0,132,255]))
            
        #light blue 20-30
        elif value < 30:
            rng = crng
            val = (30 - value)
            colors.append(getColor(val,rng,[0,159,255],[0,255,255]))
            
        #turquoise 30-32
        elif value < 32:
            rng = 2
            val = (32 - value)
            colors.append(getColor(val,rng,[0,184,148],[0,140,99]))
            
        #dark green 32-40
        elif value < 40:
            rng = 8
            val = (40 - value)
            colors.append(getColor(val,rng,[0,65,0],[0,147,0]))
            
        #light green 40-50
        elif value < 50:
            rng = crng
            val = (50 - value)
            colors.append(getColor(val,rng,[0,167,0],[0,255,0]))
            
        #yellow 50-60
        elif value < 60:
            rng = crng
            val = (60 - value)
            colors.append(getColor(val,rng,[255,255,0],[255,165,0]))
            
        elif value < 70:
            rng = crng
            val = (70 - value)
            colors.append(getColor(val,rng,[255,148,0],[255,68,0]))
            
        elif value < 80:
            rng = crng
            val = (80 - value)
            colors.append(getColor(val,rng,[255,13,0],[181,0,0]))
            
        elif value < 90:
            rng = crng
            val = (90 - value)
            colors.append(getColor(val,rng,[157,0,0],[87,0,0]))
            
        elif value < 100:
            rng = crng
            val = (100 - value)
            colors.append(getColor(val,rng,[112,0,112],[205,0,204]))
            
        elif value < 110:
            rng = crng
            val = (110 - value)
            colors.append(getColor(val,rng,[229,48,209],[255,127,229]))
            
        elif value < 120:
            rng = crng
            val = (120 - value)
            colors.append(getColor(val,rng,[255,161,229],[255,255,255]))
            
        else:
            colors.append(rgb(255,255,255))


    return colors
    
#==============================================================================
    
def tempc(clevs):
    
    crng = 5
    
    colors = []
    for value in clevs:
        
        #we go from bottom to top, so left value (115) is starting, right side is adjustment
        #towards the final state
    
        if value < -40:
            colors.append(rgb(31,80,169))
            
        elif value < -35:
            rng = crng
            val = (-35 - value)
            colors.append(getColor(val,rng,[49,105,173],[24,165,176]))
            
        elif value < -30:
            rng = crng
            val = (-30 - value)
            colors.append(getColor(val,rng,[26,184,188],[113,232,235]))

        elif value < -25:
            rng = crng
            val = (-25 - value)# - 0.5)
            colors.append(getColor(val,rng,[113,215,239],[250,30,255]))
            
        elif value < -20:
            rng = crng
            val = (-20 - value)# - 0.5)
            colors.append(getColor(val,rng,[206,11,239],[115,41,213]))
            
        elif value < -15:
            rng = crng
            val = (-15 - value)
            colors.append(getColor(val,rng,[144,84,222],[212,183,249]))
            
        elif value < -10:
            rng = crng
            val = (-10 - value)
            colors.append(getColor(val,rng,[230,230,255],[52,52,219])) #40,40,180
            
        #dark blue 10-20
        elif value < -5:
            rng = crng
            val = (-5 - value)
            colors.append(getColor(val,rng,[0,0,222],[0,132,255])) #19
            
        #light blue 20-30
        elif value < 0:
            rng = crng
            val = (0 - value)
            colors.append(getColor(val,rng,[0,159,255],[0,255,255]))
            
        #dark green 32-40
        elif value < 5:
            rng = 5
            val = (5 - value)
            colors.append(getColor(val,rng,[0,65,0],[0,147,0]))
            
        #light green 40-50
        elif value < 9.5:
            rng = 4.5
            val = (9.5 - value)
            colors.append(getColor(val,rng,[0,167,0],[0,255,0]))
            
        elif value < 10.0:
            rng = 0.5
            val = (10.0 - value)
            colors.append(getColor(val,rng,[0,167,0],[0,255,0]))
            
        #yellow 50-60
        elif value < 15:
            rng = crng
            val = (15 - value)
            colors.append(getColor(val,rng,[255,255,0],[255,150,0]))
            
        elif value < 20:
            rng = crng
            val = (20 - value)
            colors.append(getColor(val,rng,[255,129,0],[255,10,0]))
            
        elif value < 25:
            rng = crng
            val = (25 - value)
            #colors.append(getColor(val,rng,[225,0,0],[140,0,0]))
            colors.append(getColor(val,rng,[225,0,0],[255,45,195]))
            
        elif value < 30:
            rng = crng
            val = (30 - value)
            #colors.append(getColor(val,rng,[112,0,112],[205,0,204]))
            colors.append(getColor(val,rng,[255,71,255],[163,41,255]))
            
        elif value < 35:
            rng = crng
            val = (35 - value)
            #colors.append(getColor(val,rng,[229,48,209],[255,127,229]))
            colors.append(getColor(val,rng,[128,41,255],[207,143,255]))
            
        elif value < 40:
            rng = crng
            val = (40 - value)
            #colors.append(getColor(val,rng,[255,161,229],[255,255,255]))
            colors.append(getColor(val,rng,[217,167,255],[255,255,255]))

        else:
            colors.append(rgb(255,255,255))


    return colors
    
#==============================================================================

def snowhr(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 0.2:
            colors.append(rgb(255,255,255))
            
        elif value < 1:
            rng = 0.8
            val = (1 - value)
            colors.append(getColor(val,rng,[235,235,235],[135,135,135]))
            
        elif value < 2:
            rng = 1
            val = (2 - value)
            #colors.append(getColor(val,rng,[153,227,251],[15,119,247]))
            colors.append(getColor(val,rng,[153,227,251],[4,74,215]))
            
        elif value < 3:
            rng = 1
            val = (3 - value)
            #colors.append(getColor(val,rng,[172,151,245],[145,38,245]))
            colors.append(getColor(val,rng,[172,151,245],[120,12,221]))
            
        elif value < 4:
            rng = 1
            val = (4 - value)
            #colors.append(getColor(val,rng,[255,0,255],[160,0,160])) #193
            colors.append(getColor(val,rng,[255,0,255],[130,0,130])) #193
            
        elif value < 5:
            rng = 1
            val = (5 - value)
            #colors.append(getColor(val,rng,[165,11,95],[255,0,0]))
            colors.append(getColor(val,rng,[255,166,166],[114,23,23]))
            
        else:
            colors.append(rgb(114,23,23))

    return colors

def snow_old(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 0.5:
            colors.append(rgb(255,255,255))
            
        elif value < 3:
            rng = 2.5
            val = (3 - value)
            colors.append(getColor(val,rng,[235,235,235],[135,135,135]))
            
        elif value < 6:
            rng = 3
            val = (6 - value)
            #colors.append(getColor(val,rng,[153,227,251],[15,119,247]))
            colors.append(getColor(val,rng,[153,227,251],[4,74,215]))
            
        elif value < 12:
            rng = 6
            val = (12 - value)
            #colors.append(getColor(val,rng,[172,151,245],[145,38,245]))
            colors.append(getColor(val,rng,[172,151,245],[120,12,221]))
            
        elif value < 24:
            rng = 12
            val = (24 - value)
            colors.append(getColor(val,rng,[255,0,255],[145,0,145]))
            
        else:
            colors.append(rgb(145,0,145))

    return colors

def snow(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 0.5:
            colors.append(rgb(255,255,255))
            
        elif value < 3:
            rng = 2.5
            val = (3 - value)
            colors.append(getColor(val,rng,[235,235,235],[135,135,135]))
            
        elif value < 6:
            rng = 3
            val = (6 - value)
            #colors.append(getColor(val,rng,[153,227,251],[15,119,247]))
            colors.append(getColor(val,rng,[153,227,251],[4,74,215]))
            
        elif value < 12:
            rng = 6
            val = (12 - value)
            #colors.append(getColor(val,rng,[172,151,245],[145,38,245]))
            colors.append(getColor(val,rng,[172,151,245],[120,12,221]))
            
        elif value < 24:
            rng = 12
            val = (24 - value)
            #colors.append(getColor(val,rng,[255,0,255],[160,0,160])) #193
            colors.append(getColor(val,rng,[255,0,255],[130,0,130])) #193
            
        elif value < 48:
            rng = 24
            val = (48 - value)
            #colors.append(getColor(val,rng,[165,11,95],[255,0,0]))
            colors.append(getColor(val,rng,[255,166,166],[114,23,23]))
            
        else:
            colors.append(rgb(114,23,23))

    return colors

def snow2(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 0.5:
            colors.append(rgb(255,255,255))
            
        elif value < 6:
            rng = 5.5
            val = (6 - value)
            colors.append(getColor(val,rng,[235,235,235],[135,135,135]))
            
        elif value < 12:
            rng = 6
            val = (12 - value)
            #colors.append(getColor(val,rng,[153,227,251],[15,119,247]))
            colors.append(getColor(val,rng,[153,227,251],[4,74,215]))
            
        elif value < 24:
            rng = 12
            val = (24 - value)
            #colors.append(getColor(val,rng,[153,227,251],[15,119,247]))
            colors.append(getColor(val,rng,[164,167,248],[62,43,218]))
            
        elif value < 48:
            rng = 24
            val = (48 - value)
            #colors.append(getColor(val,rng,[172,151,245],[145,38,245]))
            #colors.append(getColor(val,rng,[172,151,245],[120,12,221]))
            colors.append(getColor(val,rng,[202,152,246],[131,11,223]))
            
        elif value < 72:
            rng = 24
            val = (72 - value)
            #colors.append(getColor(val,rng,[255,0,255],[160,0,160])) #193
            colors.append(getColor(val,rng,[255,0,255],[130,0,130])) #193
            
        elif value < 144:
            rng = 72
            val = (144 - value)
            #colors.append(getColor(val,rng,[165,11,95],[255,0,0]))
            colors.append(getColor(val,rng,[255,166,166],[114,23,23]))
            
        else:
            colors.append(rgb(114,23,23))

    return colors

#==============================================================================

def prob(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 10:
            colors.append(rgb(255,255,255))
            
        elif value < 41:
            rng = 31
            val = (41 - value)
            colors.append(getColor(val,rng,[210,231,245],[22,149,240])) #119
            
        elif value < 71:
            rng = 30
            val = (71 - value)
            colors.append(getColor(val,rng,[28,191,6],[245,245,0]))
            
        elif value < 91:
            rng = 20
            val = (91 - value)
            colors.append(getColor(val,rng,[245,245,6],[255,89,0]))
            
        else:
            colors.append(rgb(240,0,0))  
        
        
    return colors

#==============================================================================

def freezing(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 51:
            colors.append(rgb(25,25,180))
            
        elif value < 300:
            rng = 249
            val = (300 - value)
            colors.append(getColor(val,rng,[25,25,218],[20,65,255])) #210 -- 20,40
            
        elif value < 1100:
            rng = 800
            val = (1100 - value)
            colors.append(getColor(val,rng,[30,105,255],[40,255,255])) #[30,95,255]
            
        elif value < 1700:
            rng = 600
            val = (1700 - value)
            colors.append(getColor(val,rng,[40,255,255],[20,235,60]))
            
        elif value < 2300:
            rng = 600
            val = (2300 - value)
            colors.append(getColor(val,rng,[20,235,60],[255,255,0]))
            
        elif value < 3000:
            rng = 700
            val = (3000 - value)
            colors.append(getColor(val,rng,[255,255,0],[255,0,0]))
            
        elif value < 5000:
            rng = 2000
            val = (5000 - value)
            colors.append(getColor(val,rng,[255,0,0],[150,0,0]))

        else:
            colors.append(rgb(150,0,0))
            
        
    return colors

def black(clevs):
    
    colors = []
    for value in clevs:
        colors.append(rgb(0,0,0))
        
    return colors

def hght(clevs):
    
    colors = []
    for value in clevs:
        
        if value < 480:
            colors.append(rgb(255,255,255))
            
        elif value < 500:
            rng = 20
            val = (500 - value)
            colors.append(getColor(val,rng,[255,255,255],[255,0,255]))
            
        elif value < 520:
            rng = 20
            val = (520 - value)
            colors.append(getColor(val,rng,[255,0,255],[30,40,255]))
            
        elif value < 538:
            rng = 18
            val = (538 - value)
            colors.append(getColor(val,rng,[30,40,255],[0,255,255]))
            
        elif value < 552:
            rng = 14
            val = (552 - value)
            colors.append(getColor(val,rng,[0,230,155],[0,160,0]))
            
        elif value < 570:
            rng = 18
            val = (570 - value)
            colors.append(getColor(val,rng,[0,160,0],[255,255,0]))
            
        elif value < 590:
            rng = 20
            val = (590 - value)
            colors.append(getColor(val,rng,[255,255,0],[255,0,0]))
            
        elif value < 605:
            rng = 15
            val = (605 - value)
            colors.append(getColor(val,rng,[255,0,0],[120,0,0]))

        else:
            colors.append(rgb(120,0,0))
        
        
    return colors

def add_alpha(r1,g1,b1,a1):
    r2 = 255
    g2 = 255
    b2 = 255

    r3 = r2 + (r1-r2)*a1
    g3 = g2 + (g1-g2)*a1
    b3 = b2 + (b1-b2)*a1
    
    return [r3,g3,b3]

def reflectivity(clevs):
    
    r1,g1,b1 = add_alpha(160,168,180,0.05)
    r2,g2,b2 = add_alpha(67,94,159,0.85)
    
    colors = []
    for value in clevs:
        
        if value < 0:
            colors.append(rgb(r1,g1,b1))
            #colors.append(rgb(120,137,174))
            
        elif value < 12:
            rng = 12
            val = (12 - value)
            colors.append(getColor(val,rng,[r1,g1,b1],[r2,g2,b2]))
            
        elif value < 20:
            rng = 8
            val = (20 - value)
            colors.append(getColor(val,rng,[r2,g2,b2],[111,214,232]))
            
        elif value < 24:
            rng = 4
            val = (24 - value)
            colors.append(getColor(val,rng,[111,214,232],[17,213,24]))
            
        elif value < 33: #37
            rng = 9
            val = (33 - value)
            colors.append(getColor(val,rng,[17,213,24],[9,94,9]))
            
        elif value < 40: #42.5
            rng = 7
            val = (40 - value)
            colors.append(getColor(val,rng,[9,94,9],[255,226,0]))
            
        elif value < 50:
            rng = 10
            val = (50 - value)
            colors.append(getColor(val,rng,[255,226,0],[255,128,0]))
            
        elif value < 60:
            rng = 10
            val = (60 - value)
            colors.append(getColor(val,rng,[255,0,0],[113,0,0]))
            
        elif value < 65:
            rng = 5
            val = (65 - value)
            colors.append(getColor(val,rng,[255,245,255],[255,146,255]))
            
        elif value < 70:
            rng = 5
            val = (70 - value)
            colors.append(getColor(val,rng,[255,117,255],[225,11,227]))
            
        elif value < 75:
            rng = 5
            val = (75 - value)
            colors.append(getColor(val,rng,[178,0,255],[99,0,214]))

        else:
            colors.append(rgb(99,0,214))
            
        
    return colors


#Bolder for ASOS purposes (transparency)
def reflectivity2(clevs):
    
    r1,g1,b1 = add_alpha(160,168,180,0.15)
    r2,g2,b2 = add_alpha(67,94,159,0.98)
    
    colors = []
    for value in clevs:
        
        if value < 0:
            colors.append(rgb(r1,g1,b1))
            #colors.append(rgb(120,137,174))
            
        elif value < 12:
            rng = 12
            val = (12 - value)
            colors.append(getColor(val,rng,[r1,g1,b1],[r2,g2,b2]))
            
        elif value < 20:
            rng = 8
            val = (20 - value)
            colors.append(getColor(val,rng,[r2,g2,b2],[111,214,232]))
            
        elif value < 24:
            rng = 4
            val = (24 - value)
            colors.append(getColor(val,rng,[111,214,232],[17,213,24]))
            
        elif value < 33: #37
            rng = 9
            val = (33 - value)
            colors.append(getColor(val,rng,[17,213,24],[9,94,9]))
            
        elif value < 40: #42.5
            rng = 7
            val = (40 - value)
            colors.append(getColor(val,rng,[9,94,9],[255,226,0]))
            
        elif value < 50:
            rng = 10
            val = (50 - value)
            colors.append(getColor(val,rng,[255,226,0],[255,128,0]))
            
        elif value < 60:
            rng = 10
            val = (60 - value)
            colors.append(getColor(val,rng,[255,0,0],[113,0,0]))
            
        elif value < 65:
            rng = 5
            val = (65 - value)
            colors.append(getColor(val,rng,[255,245,255],[255,146,255]))
            
        elif value < 70:
            rng = 5
            val = (70 - value)
            colors.append(getColor(val,rng,[255,117,255],[225,11,227]))
            
        elif value < 75:
            rng = 5
            val = (75 - value)
            colors.append(getColor(val,rng,[178,0,255],[99,0,214]))

        else:
            colors.append(rgb(99,0,214))
            
        
    return colors