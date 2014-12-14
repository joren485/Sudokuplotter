## import all the neccessary libraries, os and the custom ones
import os
import algx
import finder
import motor_control

## Take the photo using raspistill.
print "Taking photo"
os.system("sudo raspistill -roi .4,0.05,1,1 -cfx 128:128 -w 600 -h 450 -q 100 -ex night -e jpg -sh 100 -co 100 -o image.jpg")


## Find the sudoku in the image using OCR.
sudoku = finder.OCR("image.jpg")

## Print out the found sudoku.
for row in sudoku:
    string = ""
    for digit in row:
        string += str(digit) + " "
    print string

## Do the necessary preprocessing before solving the sudoku.
Set, keys, values = algx.sudo2set(sudoku)
matrix = {}

for i in xrange(len(keys)):
    key = keys[i]
    matrix[key]=[]
    for value in values:
        if value in Set[key]:
            matrix[key].append(1)
        else:
            matrix[key].append(0)

## Solve the sudoku.
print "solving"
solutions = algx.exactcover(matrix)

## Print out the solved sudoku.
sudostring = ""
for i in sorted(solutions[0]):
    sudostring += str(i[2]) + " "

solved_sudoku = [sudostring[i:i+18] for i in xrange(0, 81*2, 18)]
for i in solved_sudoku:
    print i


### Select first solution and convert it into needed steps

solution = finder.split_len( sorted( solutions[0] )[::-1], 9)

## Filter the points that need to be filled and sort them the right way.

steps = []
for row in range(9):
    if row%2 == 0:
        for digit in solution[row][::-1]:
            row = digit[0]
            column = digit[1]
            if sudoku[row][column] == "x":
                steps.append( digit)

    else:
        for digit in solution[row]:
            row = digit[0]
            column = digit[1]
            if sudoku[row][column] == "x":
                steps.append(digit)

## 1 cell takes 1850 rotations of 1 motor, so 1/6 of 1 cell = 308.33 
## To correct small defects, we rounded 308.33 down to 300
x = 300

## calculate and set step to the first digit start
print motor_control.steps_calc( None, steps[0])[0]
motor_control.set_step( motor_control.steps_calc( None, steps[0])[0], x)

## Move the pen down so it hits the paper.
motor_control.pen_down(90)

for step_i in xrange( len( steps ) ):
## Print out the number and the cell the solver is going to write.
    print steps[step_i]

## Write the number
    motor_control.write_number( steps[step_i], x )

## If the number is not the 81st number the program needs to go to the next number.
## The program calculates the path it needs to take. 
    if step_i < len(steps) - 1 :
        print motor_control.steps_calc( steps[step_i] , steps[ step_i+1] )
        motor_control.set_step( motor_control.steps_calc( steps[step_i] , steps[ step_i+1] ), x )

## Move the pen up because the sudoku is solved.
motor_control.pen_up(90)
