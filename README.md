Sudokuplotter
=============

Code used to run an automatic sudoku solver.
Created by Jos Feenstra and my self, our supervisor was Dov Scheinowitz.

####Media:

* Jos and I won the 1st place 3i Award. The 3i Award is an award for the best ICT related schoolprojects. It is an initiave of [Instruct](http://www.instruct.nl/): [3i Award](http://www.instruct.nl/product/298//informaticaprijs)
* **Het Profielwerkstuk.pdf**: The paper we wrote about the plotter, describing how the plotter works and how we built it. (It is written in Dutch)
* **Jong_Geleerd_2.0_Maker_in_het_onderwijs.pdf**: [Kennisnet](http://www.kennisnet.nl/) made an folder about maker education. Jos and I were lucky enough to be in it.
* A blog post about our plotter on [Makered.nl](http://makered.nl/): [De sudokuplotter](http://makered.nl/?p=599) (Thanks to [@arjanvandermeij](https://twitter.com/arjanvandermeij))
* Video of the plotter in action: [Sudoku plotter time lapse ](https://www.youtube.com/watch?v=0O7KezpXGDY)

#### Main code:

* Comb.py: The main program, it combines all the different parts
* Finder.py: OCR for to recognize the sudoku from a photo.
* Algx.py: Algorithm X, used to solve the sudoku. 
* Motor_control.py: Code used to control the motors through Piface.

#### Algx:

Sudoku Solver using Knuth's Algorithm X

Simple Suduko Solver using Knuth's Algorithm X. Only it is not recursive. 

Hard sudoku's take about .2~.3 seconds to solve on a modern computer. And about 5 seconds on a Raspberry Pi.

Sudoku Cloud is the Sudoku solver, but in server form. You can run the actual solving code on a 8-core VPS and connect the Raspberry Pi to the VPS via the internet.

TODO:
 * use multi-threading or multiprocessing (probably the latter because of the GIL)

#### Finder:

Dependencies:
 * Numpy
 * OpenCV2
 * Python-Tesseract



P.S. Sorry, the code is bit of a mess.
