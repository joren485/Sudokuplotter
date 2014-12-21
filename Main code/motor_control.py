import pifacecommon.mcp23s17
import time

## Init the mcp23s17 chip on the Piface.
mcp = pifacecommon.mcp23s17.MCP23S17()

mcp.iocon.value = (
            pifacecommon.mcp23s17.BANK_OFF |
            pifacecommon.mcp23s17.INT_MIRROR_OFF |
            pifacecommon.mcp23s17.SEQOP_OFF |
            pifacecommon.mcp23s17.DISSLW_OFF |
            pifacecommon.mcp23s17.HAEN_ON |
            pifacecommon.mcp23s17.ODR_OFF |
            pifacecommon.mcp23s17.INTPOL_LOW
        )

mcp.gpioa.value = 0x00
mcp.iodira.value = 0x00

## This is where the magic happens, 0xAA means that the inputs 0, 2, 4 and 6 are outputs.
## Because 0xAA means that only pins 1 3 5 7 are inputs.  
mcp.iodirb.value = 0xAA 

### Main class for motors.
class motor():
    """Motor class that is used for init and rotation of the motors."""
    def __init__(self, pin_range, GPIOX, mcp):
        self.rotate_pins = [pifacecommon.mcp23s17.MCP23S17RegisterBit(i, GPIOX, mcp) for i in pin_range]
                
    def clockwise_rotate(self, rotations):
        """Rotate the motor clockwise."""
        wait = 3/1000
        for i in range(int(rotations)):
              
            self.rotate_pins[3].set_high()
            time.sleep(wait)
            self.rotate_pins[0].set_low()
            time.sleep(wait)
            self.rotate_pins[2].set_high()
            time.sleep(wait)
            self.rotate_pins[3].set_low()
            time.sleep(wait)
            self.rotate_pins[1].set_high()
            time.sleep(wait)
            self.rotate_pins[2].set_low()
            time.sleep(wait)
            self.rotate_pins[0].set_high()
            time.sleep(wait)
            self.rotate_pins[1].set_low()
            time.sleep(wait)
        self.rotate_pins[0].set_low()
    
    def counter_clockwise_rotate(self, rotations):
        """Rotate the motor counter clockwise."""
        wait = 3/1000
        for i in range(int(rotations)):
            
            self.rotate_pins[0].set_high()
            time.sleep(wait)
            self.rotate_pins[3].set_low()
            time.sleep(wait)
            self.rotate_pins[1].set_high()
            time.sleep(wait)
            self.rotate_pins[0].set_low()
            time.sleep(wait)
            self.rotate_pins[2].set_high()
            time.sleep(wait)
            self.rotate_pins[1].set_low()
            time.sleep(wait)
            self.rotate_pins[3].set_high()
            time.sleep(wait)
            self.rotate_pins[2].set_low()
        self.rotate_pins[3].set_low()


def steps_calc(point_A, point_B):
    "Calculate the path between point A and point B."
    ### Each digit gets 2 points, 1 high and 1 low. This way the program can write from low to high to low. 
    ### This is more efficient.
    ### If the (column) is even it means the writing ended on the high point.
    sPoint,ePoint = None, None
    if point_A:
        ## Calc start point
        yA,xA,nA = point_A 
        sPoint = [ xA * 6, (8 - yA) * 6 ]

        ## High point
        if xA % 2 == 0:
            if nA in (1,5,6):
                sPoint[0] += 4
                sPoint[1] += 5

            elif nA in (2,3,4,7):
                sPoint[0] += 2
                sPoint[1] += 5

            elif nA == 8:
                sPoint[0] += 2 
                sPoint[1] += 3

            else: ## 9
                sPoint[0] += 4
                sPoint[1] += 3

        ## Low Point 
        else:
            if nA in (1,2,4,7):
                sPoint[0] += 4
                sPoint[1] += 1
                
            elif nA in (3,5,9):
                sPoint[0] += 2
                sPoint[1] += 1
                
            elif nA in (6,8):
                sPoint[0] += 2
                sPoint[1] += 3
            

## Calc end point
    if point_B:
        yB,xB,nB = point_B
        ePoint = [ xB * 6, (8 - yB) * 6 ]

        ## Low point
        if xB % 2 == 0:
            if nB in (1,2,4,7):
                ePoint[0] += 4
                ePoint[1] += 1
                
            elif nB in (3,5,9):
                ePoint[0] += 2
                ePoint[1] += 1
                
            elif nB in (6,8):
                ePoint[0] += 2
                ePoint[1] += 3

        ## High Point  
        else:
            if nB in (1,5,6):
                ePoint[0] += 4
                ePoint[1] += 5

            elif nB in (2,3,4,7):
                ePoint[0] += 2
                ePoint[1] += 5

            elif nB == 8:
                ePoint[0] += 2 
                ePoint[1] += 3

            else: #9
                ePoint[0] += 4
                ePoint[1] += 3
        
    if point_A and point_B:
        return (ePoint[0] - sPoint[0], ePoint[1] - sPoint[1])
    
    else:
        return (ePoint,sPoint)



def write_number(point, x):
    """Write a number."""
    
    y_co, x_co, n = point
    pen_down(30)

## start point is low
    if x_co % 2 == 0:
        if n == 1:
            up(4 * x)
            
        if n == 2:
            left(2 * x)
            up(2 * x)
            right(2 * x)
            up(2 * x)
            left(2 * x)
            
        if n == 3:
            right(2 * x)
            up(2 * x)
            left(2 * x)
            right(2 * x)
            up(2 * x)
            left(2 * x)
            
        if n == 4:
            up(4 * x)
            down(2 * x)
            left(2 * x)
            up(2 * x)
            
        if n == 5:
            right(2 * x)
            up(2 * x)
            left(2 * x)
            up(2 * x)
            right(2 * x)
            
        if n == 6:
            down(2 * x)
            right(2 * x)
            up(2 * x)
            left(2 * x)
            up(2 * x)
            right(2 * x)
            
        if n == 7:
            up(4 * x)
            left(2 * x)
            
        if n == 8:
            down(2 * x)
            right(2 * x)
            up(2 * x)
            left(2 * x)
            up(2 * x)
            right(2 * x)
            down(2 * x)
	    left(2 * x)            

        if n == 9:
            right(2 * x)
            up(2 * x)
            left(2 * x)
            up(2 * x)
            right(2 * x)
            down(2 * x)

## start point is high
    else:
        if n == 1:
            down(4 * x)
            
        if n == 2:
            right(2 * x)
            down(2 * x)
            left(2 * x)
            down(2 * x)
            right(2 * x)
            
        if n == 3:
            right(2 * x)
            down(2 * x)
            left(2 * x)
            right(2 * x)
            down(2 * x)
            left(2 * x)
            
        if n == 4:
            down(2 * x)
            right(2 * x)
            up(2 * x)
            down(4 * x)
            
        if n == 5:
            left(2 * x)
            down(2 * x)
            right(2 * x)
            down(2 * x)
            left(2 * x)
            
        if n == 6:
            left(2 * x)
            down(2 * x)
            right(2 * x)
            down(2 * x)
            left(2 * x)
            up(2 * x)

        if n == 7:
            right(2 * x)
            down(4 * x)
            
        if n == 8:
            down(2 * x)
            right(2 * x)
            up(2 * x)
            left(2 * x)
            up(2 * x)
            right(2 * x)
            down(2 * x)
            left(2 * x)

        if n == 9:
            up(2 * x)
            left(2 * x)
            down(2 * x)
            right(2 * x)
            down(2 * x)
            left(2 * x)
    pen_up(30)

def set_step(translation, x):
    "Do steps in a certain direction."
    xTr, yTr = translation[0], translation[1]

    if xTr < 0:
        left( abs(xTr) * x)
    if xTr > 0:
        right(xTr * x)

    if yTr < 0:
        down(abs(yTr) * x)
    if yTr > 0:
        up(yTr * x)
        
## Here we init the motors using the Piface input and output pins. 
## Output pins 0 - 3
motor1 = motor(range(0,4), pifacecommon.mcp23s17.GPIOA, mcp)

## Output pins 4 - 7
motor2 = motor(range(4,8), pifacecommon.mcp23s17.GPIOA, mcp)

## Input pins 0, 2, 4, 6
motor3 = motor(range(0,8,2), pifacecommon.mcp23s17.GPIOB, mcp)

## To make it a bit easier for us, we put the rotation direction in a variable corresponding.
down = motor1.counter_clockwise_rotate
up = motor1.clockwise_rotate

right = motor2.clockwise_rotate
left = motor2.counter_clockwise_rotate

pen_down = motor3.clockwise_rotate
pen_up = motor3.counter_clockwise_rotate




