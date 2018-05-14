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
