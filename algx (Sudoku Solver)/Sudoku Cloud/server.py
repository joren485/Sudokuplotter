from flask import Flask, request
from algX62SE import *

app = Flask(__name__)

@app.route('/')
def home():
	if request.method == "GET":
		sudo = request.args.get("sudo")
		if sudo != None and  len(sudo) == 81:
			sudoku = formatsudoku(sudo)
			solutions = solve(sudoku)
			
			returnstring = "".join(solution + ";" for solution in solutions)
			return returnstring

	return "You know nothing, Jon Snow."
	
app.run(host= '0.0.0.0')
