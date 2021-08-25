"""
Random quadtatic eq solver.
generates and solves equation automatically.
no. of roots needed can be given by CLA, default is 100.
can be used to find equations having given roots. 
*****error[0]: all roots are negative?? --- solved
"""
import random 
import time
import sys
import os
 
name = os.path.basename(__file__) #name of program
outfile = "data.csv"  #file to which data is saved
statfile = "stats.csv" #file to which stats is saved

#variables
a = b = c = d = r1 = r2 = 0 

#counters
real = 0  #useful equations
non_real = 0   
count = 0  #total equations solved

start = time.time() #start timer
saved = False   #tracks if data was saved in file
statSaved = False #tracks stat status

#variables for printing status.
status = False
interval = 0  #first status print time
status_delay = 3 #delay in printing statuses like "Working on it"

#help
if len(sys.argv) >= 2:  #checks if help is asked 
	if sys.argv[1].lower() == "help":
		print("----"*20)
		print("Usage: autoquad.py [Equations needed] [preffered root1 preffered root2]")
		print("----"*20)
		print("-> This is a quadratic equation and root generator program")
		print("-> Run with no arguements to generate 100 random quadratic equations")
		print(f"-> Use {name} <number of equations> to generate specified number of equatons")
		print(f"-> Use {name} <number of equations> <root> to generate specified number of equations with a specified root.")
		print(f"-> Use {name} <number of equations> <root1> <root2> to generate specified number of equations with given roots.")
		print(f"-> Generated data is stored in {outfile}")
		print(f"-> Stats are stored in {statfile}")
		print("----"*20)
		sys.exit(0)
print("Running")


#saves data to file
def save():
	global saved, real
	real += 1
	with open(outfile, mode ="a") as file:
		file.write(f"{a}, {b}, {c}, {d}, {r1}, {r2},\n")
		saved = True 


if len(sys.argv) == 1: #first arg is always treated as number of equations.
	total = 100  #total equations
else:
	total = int(sys.argv[1])


#Solver function
def quad():
	global a,b,c,d,r1,r2

	#eq generation a,b,c  ±1000; a != 0
	a = round(int(random.randrange(-1000, 1000,1)))
	while(a == 0):
		a = round(int(random.randrange(-1000,1000,1)))		
	b = round(int(random.randrange(-1000, 1000,1)), 3)
	c = round(float(random.randrange(-1000,1000,1)), 3)
	
	#math part -------- error[0]	
	d = (b**2) - (4*a*c)
	if d >= 0:
		r1 = round(((-b) + (d**(1/2)))/2/a, 3)
		r2 = round(((-b) - (d**(1/2)))/2/a, 3)

		if len(sys.argv) == 3: #if 2 args are given then as specified root
			if r1 == float(sys.argv[2]) or r2 == float(sys.argv[2]):
				save()

		elif len(sys.argv) == 4:  #if 3 args are given then first is treated as number of eq. and second as specified root
			if (r1 == float(sys.argv[2]) and r2 == float(sys.argv[3])) or  (r2 == float(sys.argv[2]) and r1 == float(sys.argv[3])):
				save()
		else:
			save()

#loop to give required number of solutions
while(real < total):
	quad()
	count += 1

	#timer for printing status
	"""
	1: if status = false then print message and set status to true
	2: next message time set as interval+delay
	3: if time to print message has come and status is true change it to false.
	3.1: it is essential to check status==false, due to rounding of time.
	4: back to 1
	"""
	timer = time.time() - start
	if round(timer) == interval and status == True: 
		status = False
	elif status == False:  #print status if not already printed
		print(f"Working on it... {count} equations solved in {round(timer,3)}secs.")
		status = True
		interval += status_delay  #set time for next status print

end = time.time() #timer stop
time = end - start
time = round(time, 4)

#saving Stats
with open(statfile, mode="a") as file:
	if len(sys.argv) == 1:
		file.write(f"{count}, {real}, {count-real}, {time},\n")
	if len(sys.argv) == 2:
		file.write(f"{count}, {real}, {count-real}, {time}, {sys.argv[1]},\n")
	if len(sys.argv) == 3:
		file.write(f"{count}, {real}, {count-real}, {time}, {sys.argv[1]}, {sys.argv[2]},\n")
	if len(sys.argv) == 4:
		file.write(f"{count}, {real}, {count-real}, {time}, {sys.argv[1]}, {sys.argv[2]}, {sys.argv[3]}\n")
	statSaved = True

#Summary printer
print(f"total equations solved:  {count}")
print(f"useful equations solved:  {real}")
print(f"time:  {round(time, 4)} seconds")	
print(f"Data-Saved: {saved}")
print(f"Stat-Saved: {statSaved}")
print(f"use \"{name} help\" for help")
