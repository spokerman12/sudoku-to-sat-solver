from SAT import solve_sat


if __name__ == '__main__':
	if len(sys.argv) != 1:
		print ("Loading file %s" % (sys.argv[1]))
	else:
		print ("No input provided. Cya")
		sys.exit(1)

	try:
		file = open(sys.argv[1],"r")
	except Exception as e:
		print("Could not load file")
		sys.exit(1)

	output = solve_sat(file.read())