import sys

# ANSI codes
colors = {
	"red": "\033[31m",
	"green": "\033[32m",
	"yellow": "\033[33m",
	"blue": "\033[34m"
}
end = "\033[0m"

class printcolor:
	def red(string):
		print(colors["red"] + str(string) + end)
	def yellow(string):
		print(colors["yellow"] + str(string) + end)
	def blue(string):
		print(colors["blue"] + str(string) + end)

class preformat_error:
	max_length = 80

	def __init__(
		self,
		error_type,
		message,
		line,
		col,
		raw
	):
		printcolor.red(error_type + " error: " + message)
		print("line " + str(line))
		print(raw)
		whitespace = ""
		for char in raw[:col]:
			whitespace += "\t" if char == "\t" else " "
		print(whitespace + "^")
		sys.exit()
