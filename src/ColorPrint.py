#!/usr/bin/python3
# --####--------------------------------------------------------------------------------------------------------####-- #
# --#### Version:       1.3.0R0                                                                                 ####-- #
# --#### Author:        Noah Isbell                                                                             ####-- #
# --#### Date:          11/03/2022                                                                              ####-- #
# --#### Description:   color_print.py is a program that take the supplied parameters and generates the         ####-- #
# --####                the designed colored output to the terminal                                             ####-- #
# --####--------------------------------------------------------------------------------------------------------####-- #
# --####                                                                                                        ####-- #
# --#### Created:       12/10/2021  Created from personal python code I sent to myself to implement use for     ####-- #
# --####                            colored printing to terminal.                                               ####-- #
# --####   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---  ####-- #
# --####                                                                                                        ####-- #
# --#### Updated:       12/28/2021  Created version 1.1, the updated changed the processing of the keyword      ####-- #
# --####                            arguments to include BEGIN, REPLACE, color.                                 ####-- #
# --####         REPLACE: replaces value provided with the provided replacement, a list of of replacements and  ####-- #
# --####                  values can be used as well string = "this is hello" where REPLACE=["is", "123"]       ####-- #
# --####                  string becomes "th123 123 hello"                                                      ####-- #
# --####         color:   replaces "{cps}" and "{cpf}" within the string for color formatting for the start and ####-- #
# --####                  finish of the inline color formatting. a color or a list of colors must be provided   ####-- #
# --####                  string = "This {cps}is{cpf} the val" and color=143 or color=[132, 32, 44, ...]        ####-- #
# --####         BEGIN:   Prepends the provided value to the front of the string to be printed                  ####-- #
# --####   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---  ####-- #
# --####                                                                                                        ####-- #
# --#### Updated:       12/28/2021  Created version 1.1.2, fixed minor bug in dashed_line printing 1 less       ####-- #
# --####                            went from for i in range(1, line_size): --> for i in range(0, line_size):   ####-- #
# --####   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---  ####-- #
# --####                                                                                                        ####-- #
# --#### Updated:       07/13/2022  Created version 1.2.0 which added default timestamping to each printed      ####-- #
# --####                            output. Added function to create table/section headers. Added function to   ####-- #
# --####                            print out all color option in its color code using the color. Updated main  ####-- #
# --####                            and versioning to match standard.                                           ####-- #
# --####   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---  ####-- #
# --####                                                                                                        ####-- #
# --#### Updated:       10/03/2022  Created version 1.2.1 adding get_formatted_num, A function to add the comma ####-- #
# --####                            to numbers for every thousand's place.                                      ####-- #
# --####   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---  ####-- #
# --####                                                                                                        ####-- #
# --#### Updated:       11/03/2022  Created version 1.3.0, added color_print parameter 'lev: int = 1' to be to  ####-- #
# --####                            determine the indent level for the output to be printed at. This frees up   ####-- #
# --####                            keyword argument 'BEGIN' to be used as it was intended as string printing   ####-- #
# --####                            formatter.                                                                  ####-- #
# --####            Example:                                                                                    ####-- #
# --####                [color_print(f"Hello {value}", lev=2, BEGIN=cnt) for pos, value in enumerate(list_val)] ####-- #
# --####--------------------------------------------------------------------------------------------------------####-- #
import datetime
import logging
import os
import sys

# --#### Default Debug logging output format
logging.basicConfig(level=logging.DEBUG, format="(%(processName)-10s) %(message)s", )

# --####-----------------------####-- #
# --#### Version variables
# --####-----------------------####-- #
major_version = "1"
minor_version = "3"
patch_verion = "0"
revision_version = "0"

# --#### Creates the default string values for replacing with color strings
# --#### Creates the color printing start
cps = color_start = "{cps}"
# --#### Creates the color printing end
cpf = color_stop = "{cpf}"
# --#### Default Output Color for ColorPrint
dcp = 83
# --#### Default Directory Color for ColorPrint
directory_colors = 38
# --#### Default Error Color for ColorPrint
error_colors = 196
# --#### Default Value Color for ColorPrint
value_color = 33
# --#### Default Value Color for Level #1
l1 = 208
# --#### Default Value Color for Level #2
l2 = 210
# --#### Default Value Color for Level #3
l3 = 212
# --#### Default Value Color for Level #4
l4 = 214
# --#### Default Value Color for Level #5
l5 = 218


def color_print(
		string_to_print="", use_color="208", lev: int = 1, start="", use_time_stamp: bool = True, *args, **kwargs
) -> None:
	"""
	A function that prints the provided string using the provided color
	:param lev:
	:param use_time_stamp:
	:param start:
	:param string_to_print:
	:param use_color:
	:param args:
	:param kwargs:
	:return None:
	"""
	# --#### Sets up the default color to print (dark orange) and the escape sequence to clear coloring/formatting
	use_color = "\x1b[38;5;" + str(use_color) + "m"
	clear_color = "\x1b[0m"
	# --#### Sets the default value for end to be a newline character
	end = "\n"
	# --#### Reassigns the parameter with the str() function called to ensure it is of a str Object
	string_to_print = str(string_to_print)
	if start:
		string_to_print = str(start) + string_to_print
	# --#### If just the keyword arguments exists, it prints out the string with the passed arguments
	if kwargs:
		# --#### If BEGIN is in the keyword arguments
		if "BEGIN" in kwargs:
			# --#### Sets a variable with the value from the BEGIN keyword argument
			beginning_str = kwargs["BEGIN"]
			# --#### Sets the sting to be printed equal to the string cast typed value passed for the beginning and string
			string_to_print = str(beginning_str) + string_to_print
		# --#### If REPLACE is in the keyword arguments
		if "REPLACE" in kwargs:
			# --#### If the type of the REPLACE dictionary value is of the type list and the length is greater then 1
			# --#### within the passed list verifying two lists were passed
			if type(kwargs["REPLACE"][0]) is list and len(kwargs["REPLACE"][0]) > 1 and len(kwargs["REPLACE"][1]) > 1:
				# --#### iterates though the enumeration of the values within the first list
				for pos, val in enumerate(kwargs["REPLACE"][0]):
					# --#### Creates the replacement string with the value passed in the second list with the same position
					replacement_string = use_color + kwargs["REPLACE"][1][pos] + use_color
					# --#### Creates the string to be printed with the replacement made for the current iteration
					string_to_print = string_to_print.replace(val, replacement_string)
			# --#### If the type isn't a list it makes the replacement string and replacement
			else:
				# --#### Creates the replacement string
				replacement_string = use_color + kwargs["REPLACE"][1] + use_color
				# --#### Creates the string to be printed with the replacement made
				string_to_print = string_to_print.replace(kwargs["REPLACE"][0], replacement_string)
		# --#### If end is in the keyword arguments
		if "end" in kwargs:
			# --#### Sets the variable to be passed to print() for the end value
			end = kwargs["end"]
		# --#### If color is in the keyword arguments
		if "color" in kwargs:
			# --#### If the type of the value of color keyword is of list and the length is greater then 1
			if type(kwargs["color"]) is list and len(kwargs["color"]) > 1:
				# --#### Iterates through the provided list passed in the color keyword argument, the list contains
				# --#### color changes to be applied to the supplied string to give formatting.
				for pos, val in enumerate(kwargs["color"]):
					# --#### creates the new color to be used for the replacement.
					new_use_color = f"\x1b[38;5;{val}m"
					# --#### Replaces the new color placeholder with the new color string.
					string_to_print = string_to_print.replace("{cps}", new_use_color, 1)
					# --#### Replaces the old color placeholder with the old color string to end the new color section
					string_to_print = string_to_print.replace("{cpf}", use_color, 1)
			# --#### If the provided value is not of the list type it just replaces all instances with the specified color
			else:
				# --#### Obtains the new value to be used for the color
				color_val = kwargs["color"]
				# --#### creates the new color to be used for the replacement.
				new_use_color = f"\x1b[38;5;{color_val}m"
				# --#### Replaces the new color placeholder with the new color string.
				string_to_print = string_to_print.replace("{cps}", new_use_color)
				# --#### Replaces the old color placeholder with the old color string to end the new color section
				string_to_print = string_to_print.replace("{cpf}", use_color)
	# --#### If the printed line is supposed to have a time stampand needs to happen after any BEGIN keyword argument
	# --#### in order to ensure all output is placed at the correct level
	if use_time_stamp:
		time_stamp_color = "\x1b[38;5;245m"
		if kwargs and "timeColor" in kwargs:
			time_stamp_color = kwargs["timeColor"]
		time_string = f"{time_stamp_color}{time_stamp(**kwargs)}{use_color}"
		string_to_print = f"{time_string}{string_to_print}"
	# --#### Determines what level the output should be printed at and needs to happen after any BEGIN keyword argument
	# --#### in order to ensure all output is placed at the correct level
	# --#### Decrements 1 from the level so leveling starts at zero but allows user to use 1 as initial level
	lev -= 1
	level_string = "\t" * lev
	string_to_print = f"{level_string}{string_to_print}"
	# --#### If just the tuple arguments exists, it prints out the string with the passed keyword arguments
	if args:
		# --#### Prints out the string with the passed arguments for the print statement
		print(use_color + string_to_print + clear_color, end=end, *args)
		return None
	else:
		# --#### Prints out the string
		print(use_color + string_to_print + clear_color, end=end)
		# --#### Returns None
		return None


def dashed_line(line_size=50, use_color=208, *args, **kwargs):
	"""
	A function that prints a dashed line
	:return:
	"""
	# --#### Initializes the dashed line as an empty string
	dash_string = ""
	# --#### Ensures the value for use_color is a string
	use_color = str(use_color)
	# --#### Iterates through adding a dash to create the dashed line to the specified size
	for i in range(0, line_size):
		# --#### Adds a dash to the end of the dashed string
		dash_string += "-"
	# --#### Calls the color printing function with the generated dashed line and passed arguments
	color_print(dash_string, use_color=use_color, use_time_stamp=False, *args, **kwargs)


def time_stamp(**kwargs):
	"""
	The function that returns the custom datetime string with optional passed arguments that is used for time stamping
	entries.
	:param kwargs:
	:return:
	"""
	try:
		time_stamp_string = ""
		dash_count = 4
		tab_count = 0
		logger_name = ""
		if kwargs:
			if "noDashedLine" in kwargs and kwargs["noDashedLine"]:
				dash_count = 0
			if "tabCount" in kwargs:
				tab_count = kwargs["tabCount"]
			if "loggerName" in kwargs:
				logger_name = f"({kwargs['loggerName']})"
		for cnt in range(tab_count):
			time_stamp_string += "\t"
		time_stamp_string += f"{'-' * dash_count}[{datetime.datetime.now()}] {logger_name}  "
		return time_stamp_string
	except Exception as ex:
		color_print(f"Encountered an Exception in time_stamp function \nException: {ex}")
		logging.debug(f"Encountered an Exception in time_stamp function \nException: {ex}")


def header(header_string: str, text_color: int = 46, line_color: int = 85, line_length: int = 50, **kwargs):
	"""
	The function that prints out a box/table header with the provided string using the provided colors
	:param line_length:
	:param line_color:
	:param text_color:
	:param header_string:
	:param kwargs:
	:return:
	"""
	try:
		center_length = line_length
		dashed_line(line_size=line_length, use_color=line_color)
		color_print(f"{header_string: ^{center_length}}", str(text_color), use_time_stamp=False, **kwargs)
		dashed_line(line_size=line_length, use_color=line_color)
	except Exception as ex:
		color_print(f"Encountered an Exception in header function \nException: {ex}")
		logging.debug(f"Encountered an Exception in header function \nException: {ex}")


def show_colors():
	"""
	A function that prints out all color option with the color number printed in its color
	:return:
	"""
	color_print("", use_time_stamp=False)
	for number in range(1, 256):
		num_str = f"{number: ^3}"
		color_print(num_str, str(number), use_time_stamp=False, end=" ")
		if number % 20 == 0:
			color_print("", use_time_stamp=False)
	color_print("\n", use_time_stamp=False)


def get_formatted_num(number):
	"""
	A function to add the comma to numbers for every thousand's place
	:param number:
	:return:
	"""
	try:
		return "{:,}".format(number)
	except Exception as ex:
		color_print(f"Encountered an Exception in get_formatted_num function \nException: {ex}")
		logging.debug(f"Encountered an Exception in get_formatted_num function \nException: {ex}")


def main():
	"""
	The main function
	"""
	try:
		# --#### If -v or --version is in the passed arguments it prints the version and exits the program
		if "-v" in sys.argv or "--version" in sys.argv:
			# --#### Prints the version and exits the program
			program_version(exit=True)
		dashed_line(use_color=85)
		dashed_line(6, end="", use_color=85)
		program_version()
		dashed_line(use_color=85)
		global start_time, stop_time
		start_time = datetime.datetime.now()
		color_print(f"Program Started at: {start_time}")
		color_print("Showing color printing output", "98")
		show_colors()
		stop_time = datetime.datetime.now()
		total_run_time = stop_time - start_time
		color_print(f"Program Stopped at: {stop_time}", 214)
		color_print(f"Total Run time: {total_run_time}", 226)
	except Exception as ex:
		color_print(f"Encountered an Exception in main function \nException: {ex}")
		logging.debug(f"Encountered an Exception in main function \nException: {ex}")


def program_version(end="\n", **kwargs) -> str or None:
	"""
	A function that prints the version of the program
	:return None:
	"""
	# --####----------------------------------------####-- #
	# --#### The current version of the program     ####-- #
	prog_ver = f"{major_version}.{minor_version}.{patch_verion}R{revision_version}"
	# --#### ----------------------------------------####-- #
	# --#### Creates the string to print before the version number
	header_str = "Ver:"
	# --#### The colors to be used on the replacement of {cps} and {cpf} for inline formatting
	banner_colors = [208, 33, 46]
	if kwargs:
		if "getstring" in kwargs and kwargs["getstring"]:
			# --#### Creates the Program version string
			prog_ver_str = ("-" * 50) + "\n" + ("-" * 6)
			prog_ver_str += f"{header_str: >5}{prog_ver: ^9}\t{os.path.basename(__file__)}"
			prog_ver_str += "\n" + ("-" * 50)
			# --#### Returns the program version string
			return prog_ver_str
	# --#### The format string containing everything combined
	prog_ver_str = f"{color_start}{header_str: >5}{color_stop}{color_start}{prog_ver: ^9}{color_stop}\t{color_start}{os.path.basename(__file__)}{color_stop}"
	# --#### Prints the program version string in color with the inline color replacements and formatting
	color_print(prog_ver_str, color=banner_colors, end=end, use_time_stamp=False)
	if kwargs and "exit" in kwargs:
		exit()
	# --#### Returns None
	return None


if __name__ == '__main__':
	# --#### Tries to run the main function
	try:
		# --#### Moves to the directory of the program file
		os.chdir(os.path.abspath(os.path.dirname(__file__)))
		# --#### Calls the main function
		main()
	# --#### Catches the keyboard interrupt
	except KeyboardInterrupt:
		# --#### Notifies the user the program was interrupted
		color_print(f"Interrupted...", 9, BEGIN="\n\n\n", end="\n\n")
		# --#### Notifies the user the program is exiting
		color_print(f"Exiting...", 81)
		# --#### Tries to run the system exit, otherwise runs the os exit
		try:
			# --#### Runs the system exit
			sys.exit(0)
		# --#### Catches the system exit exception
		except SystemExit:
			# --#### Calls the os exit
			os._exit
