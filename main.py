import os
from pprint import pprint

from error import preformat_error as error

os.system("clear")
os.system("tabs -4")

essay = \
"""
bruh
moment

line 4
Sentence made up of many words.

		!Indented block.
Ye`s.

`And now "string" lol.
multil"i`
n
e!string"1!
"""[1:-1]




bracket_types = {
	"parentheses": ["(", ")"],
	"brackets": ["[", "]"],
	"braces": ["{", "}"],
	"pipes": ["|", "|"]
	# pipes cannot be nested unless other brackets are used,
	#	for example |(|x - 1| - 1)| != ||x - 1| - 1|, the latter is erroneous
}









def strings_and_comments(essay):
	lines = essay.split("\n")

	delimiters = {
		"string": ["\""],
		"comment": ["`"],
		"line_comment": ["!"]
	}
	delimiters["multi_line"] = delimiters["string"] + delimiters["comment"]
	delimiters["all"] = delimiters["multi_line"] + delimiters["line_comment"]

	delimiter = None
	escaped = False

	formatted = [{
		# lines and columns are zero-indexed
		"line": 0,
		"col": 0,
		"raw": ""
	}]

	for i, raw in enumerate(lines):
		if i:
			formatted[-1]["raw"] += "\n"

		for j, char in enumerate(raw):

			if char == "\t":
				if j != 0 and not delimiter:
					error(
						"indentation",
						"unexpected indent",
						i,
						j,
						raw
					)

			if char in delimiters["all"]:
				if delimiter not in delimiters["all"]:
					string_type = (
						"string" if char in delimiters["string"]
						else "comment"
					)
					delimiter = char
					formatted.append({
						"line": i,
						"col": j,
						"raw": "",
						"type": string_type,
						"delimiter": char
					})
					continue
				elif delimiter in delimiters["multi_line"]:
					if (
						char == delimiter and
						not escaped and
						char not in delimiters["line_comment"]
					):
						delimiter = None
						formatted.append({
							"line": i,
							"col": j + 1,
							"raw": ""
						})
						continue

			formatted[-1]["raw"] += char

		if delimiter in delimiters["line_comment"]:
			delimiter = None
			formatted.append({
				"line": i,
				"col": j + 1,
				"raw": ""
			})

	if delimiter:
		current_string = formatted[-1]
		i = current_string["line"]
		error(
			"punctuation",
			"unclosed " + current_string["type"],
			i,
			current_string["col"],
			lines[i]
		)

	return {
		"formatted": formatted,
		"lines": lines,
		"raw": essay
	}

pprint(strings_and_comments(essay))
