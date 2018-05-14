### MicroBit에서 PC에 시리얼로 정보보내기

> MicroBit에서 기울기 센서를 통해 자리찾아가기 게임을 구현. 그 정보를 PC에 시리얼로 보낸다. PC에서는 시리얼 정보를 파싱하고 화면에 출력한다. 



MicroBit 소스(javascript에디터. 실제 프로젝트 확장자명은 컴파일된 후, hex임)

~~~javascript
let 보물Y좌표 = 0
let 보물X좌표 = 0
let 내위치Y = 0
let 내위치X = 0
input.onGesture(Gesture.TiltLeft, () => {
    내위치X = 내위치X - 1
})
input.onGesture(Gesture.LogoUp, () => {
    내위치Y = 내위치Y + 1
})
input.onGesture(Gesture.LogoDown, () => {
    내위치Y = 내위치Y - 1
})
input.onButtonPressed(Button.AB, () => {
    basic.clearScreen()
    보물X좌표 = Math.random(5)
    보물Y좌표 = Math.random(5)
    내위치X = Math.random(5)
    내위치Y = Math.random(5)
})
input.onGesture(Gesture.TiltRight, () => {
    내위치X = 내위치X + 1
})
basic.forever(() => {
    basic.pause(1000)
    if (내위치X < 보물X좌표) {
        led.toggle(4, 2)
    } else if (내위치X > 보물X좌표) {
        led.toggle(0, 2)
    }
    if (내위치Y < 보물Y좌표) {
        led.toggle(2, 4)
    } else if (내위치Y > 보물Y좌표) {
        led.toggle(2, 0)
    }
    if (내위치X == 보물X좌표 && 내위치Y == 보물Y좌표) {
        basic.showIcon(IconNames.Heart)
        basic.pause(3000)
        basic.clearScreen()
        보물X좌표 = Math.random(5)
        보물Y좌표 = Math.random(5)
        내위치X = Math.random(5)
        내위치Y = Math.random(5)
    }
    serial.writeNumbers([내위치X, 내위치Y, 보물X좌표, 보물Y좌표])
})
~~~
프로젝트 주소:
https://makecode.microbit.org/_cDTEjmdRg4Jj



PC의 시리얼통신 프로그램(Python, PySerial)

~~~python
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
    
~~~



PC 통신화면 

![](microbit.gif)



- 참고사항
  - 버그있음. 그런데  고치니까 재미없어짐. 그래서 버그가 재미로 둔갑함.
  - 마이크로비트 센서의 오동작이 미세하게 있음.