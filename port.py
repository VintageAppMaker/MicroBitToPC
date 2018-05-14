#-*- coding: utf-8 -*-
import sys
import glob
import serial
import sys
import os

# 스택오버플로우에서 가장흔한 코드
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = [] 
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def select_port():
    com = raw_input("port:")
    print com
    return com  

# 오랜만의 그지같은 시리얼통신. 윈도우 10에서는 보우레이트를 
# 115200로 픽스해야 함.
def read_comport(comport):
    ser = serial.Serial(comport, 115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
    sLine = ["", "", "", ""]
    nIndx = 0
    bMinus = False
    while True:
        bRead = ser.read()
        if(bRead ==  ""):
            continue

        if(bRead ==  "-"):
            bMinus = True
            continue

        if(bRead ==  " "):
            continue

        if(bRead ==  ","):
            continue

        if(bRead == "\r"):
            continue
        if(bRead == "\n"):
            continue    

        if bMinus == True:
            bRead = bRead * -1
            bMinus = False

        sLine[nIndx] = bRead
        nIndx = nIndx + 1
        if(nIndx > 3): 
            display(sLine)
            nIndx = 0

def display (data):
    os.system('cls')
    print "> bug~! bug! crash!"
            
    grid = [["."]*5 for i in range(5)]
    
    try:
        x  = int ( data[0] )
        y  = int ( data[1] )
        x2 = int ( data[2] )
        y2 = int ( data[3] )
    
        grid[x][y]   = 'A'
        grid[x2][y2] = 'B'
        
        for  i in range(0,5):   
            print str(grid[i]) 

        print "\n\n"
        print data
    
    except:
        print "out of range! come back~" 

if __name__ == '__main__':
    print u"가능한 port 리스트:", serial_ports()
    port = select_port() 
    read_comport(port)
    