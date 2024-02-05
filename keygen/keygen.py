"""
Purpose: Pseudorandom password generation, customized to your liking.
Author: VladinXXV
Date: November 4, 2023

KEYGEN - A Pseudorandom password generation script.
Copyright (C) 2023  VladinXXV

This program is not open source. See <https://github.com/VladinXXV/VladinXXV/blob/main/LICENSE>.
"""

# Imports
import random as rng
import string as txt

# Function Definitions
def blacklistCharacters(numbers: list, letters: list, symbols: list, blacklist: list = None, printToConsole: bool = False):
	"""
    Removes characters from the provided lists based on a blacklist, for use with keygen().

    This function takes in three lists of characters (numbers, letters, symbols) and a blacklist of
	characters. It removes any characters present in the blacklist from the numbers, letters, and
	symbols lists. The blacklist is then updated to only include characters that were not removed.

    Args:
        numbers (list): A list of number characters.
        letters (list): A list of letter characters.
        symbols (list): A list of symbol characters.
        blacklist (list, optional): A list of characters to be removed. If not provided, the user
									is prompted to input it.
        printToConsole (bool, optional): If True, the function will print the characters that were
										 not blacklisted because they were not going to be used
										 anyway.

    Returns:
        list: The updated blacklist containing only characters that were not removed from the
			  provided lists (numbers, letters, symbols).

    Raises:
        TypeError: If printToConsole is False and blacklist is None.
        TypeError: If printToConsole is not a boolean.
        TypeError: If blacklist is not None and is not a list.
        TypeError: If any of the list arguments (numbers, letters, symbols) are not
				   lists. (blacklist has a special condition, see above)
        ValueError: If any of the list arguments (numbers, letters, symbols, blacklist) contain
					strings greater than length 1.
    """
	
	# Create a dictionary to store the list argument names and their corresponding values
	listArgumentNames = {'numbers': numbers, 'letters': letters, 'symbols': symbols, 'blacklist': blacklist}

	# Check the type of printToConsole, it should be a boolean
	if not isinstance(printToConsole, bool):
		raise TypeError("Input argument 'printToConsole' has incorrect type. Must be 'bool'.")

	# Check the type of blacklist, it should be a list if it's not None
	if blacklist != None and not isinstance(blacklist, list):
		raise TypeError("Input argument 'blacklist' has incorrect type. Must be 'list'.")
	
	# Initialize lists to store the names of list arguments that fail the type checks
	listFails = []
	characterFails = []

	# Check that all list arguments are lists and contain only single-character strings
	for listArgumentName, listArgument in listArgumentNames.items():
		if listArgumentName != 'blacklist':
			if not isinstance(listArgument, list):
				listFails.append(listArgumentName)
		if listArgument != None and not all(isinstance(string, str) and len(string) == 1 for string in listArgument):
			characterFails.append(listArgumentName)

	# If any list arguments are not lists, raise a TypeError
	if listFails:
		raise TypeError(f"Input argument(s): {', '.join(f'{chr(39)}{listFailure}{chr(39)}' for listFailure in listFails)} have incorrect type(s). Must be 'list'.")

	# If any list arguments contain strings greater than length 1, raise a ValueError
	if characterFails:
		raise ValueError(f"Input argument(s): {', '.join(f'{chr(39)}{characterFailure}{chr(39)}' for characterFailure in characterFails)} contain strings greater than length 1. Must contain only single-character strings.")

	# If printToConsole is True, prompt the user to input the blacklist if it wasn't given already
	if printToConsole and not isinstance(blacklist, list):
		while True:
			blacklist = list(input("Enter all English ASCII letters, punctuation (bar whitespace), and/or digits prohibited from being in your password:\n"))
			if len((set(numbers) | set(letters) | set(symbols)) - set(blacklist)) == 0:
				print("You must allow at least one character to be used to generate a key.")
			else:
				break
	# If printToConsole is False and blacklist is None, raise a ValueError
	elif blacklist == None:
		raise TypeError("Input argument 'blacklist' cannot be None if the argument 'printToConsole' is False. Must be 'list' or 'printToConsole' must be True.")
	
	# Convert lists to sets for efficient operations
	numbersSet = set(numbers)
	lettersSet = set(letters)
	symbolsSet = set(symbols)
	blacklistSet = set(blacklist)

	# Remove the blacklist characters from the numbers, letters, and symbols sets
	numbersSet -= blacklistSet
	lettersSet -= blacklistSet
	symbolsSet -= blacklistSet

	# Update the blacklist to only include characters that were not removed
	blacklistSet = blacklistSet - (set(numbers) | set(letters) | set(symbols))

	# Convert the sets back to lists
	numbers[:] = list(numbersSet)
	letters[:] = list(lettersSet)
	symbols[:] = list(symbolsSet)
	blacklist[:] = list(blacklistSet)
	
	# If there are any characters left in the blacklist and printToConsole is True, print these
	# characters
	if len(blacklist) > 0 and printToConsole:
		print(f"The characters:\n\t{''.join(blacklist)}\n...were not blacklisted because they were not going to be used anyway.")

	# Return whatever remains of the blacklist, if anything
	return blacklist
			

def keygen(numbers: list, letters: list, symbols: list, keyLength: int = None, printToConsole: bool = False):
	"""
    Generates a pseudorandom password based on the provided character sets and length.

    This function takes in three lists of characters (numbers, letters, symbols) and a desired
	password length. It generates a password of the specified length using a random selection of
	characters from the non-empty lists.

    Args:
        numbers (list): A list of number characters.
        letters (list): A list of letter characters.
        symbols (list): A list of symbol characters.
        keyLength (int, optional): The desired length of the password. If not provided, the user
								   is prompted to input it.
        printToConsole (bool, optional): If True, the function will print the generated password to
										 the console.

    Returns:
        tuple: The generated password as a string and the key length as an integer.

    Raises:
        TypeError: If printToConsole is not a boolean.
        TypeError: If keyLength is not an integer and is not None.
        TypeError: If any of the list arguments (numbers, letters, symbols) are not lists.
        ValueError: If any of the list arguments contain strings greater than length 1.
        ValueError: If keyLength is less than or equal to 0 and printToConsole is False.
        ValueError: If all character sets are empty.
    """

	# Create a dictionary to store the list argument names and their corresponding values
	listArgumentNames = {'numbers': numbers, 'letters': letters, 'symbols': symbols}

	# Check the type of printToConsole, it should be a boolean
	if not isinstance(printToConsole, bool):
		raise TypeError("Input argument 'printToConsole' has incorrect type. Must be 'bool'.")

	# Check the type of keyLength, it should be an integer if it's not None
	if keyLength != None and not isinstance(keyLength, int):
		raise TypeError("Input argument 'keyLength' has incorrect type. Must be 'int'.")
	
	# Initialize lists to store the names of list arguments that fail the type checks
	listFails = []
	characterFails = []

	# Check that all list arguments are lists and contain only single-character strings
	for listArgumentName, listArgument in listArgumentNames.items():
		if not isinstance(listArgument, list):
			listFails.append(listArgumentName)
		if not all(isinstance(string, str) and len(string) == 1 for string in listArgument):
			characterFails.append(listArgumentName)

	# If any list arguments are not lists, raise a TypeError
	if listFails:
		raise TypeError(f"Input argument(s): {', '.join(f'{chr(39)}{listFailure}{chr(39)}' for listFailure in listFails)} have incorrect type(s). Must be 'list'.")

	# If any list arguments contain strings greater than length 1, raise a ValueError
	if characterFails:
		raise ValueError(f"Input argument(s): {', '.join(f'{chr(39)}{characterFailure}{chr(39)}' for characterFailure in characterFails)} contain strings greater than length 1. Must contain only single-character strings.")

	# If printToConsole is True, prompt the user to input the keyLength
	if printToConsole:
		while True:
			if keyLength != None and keyLength > 0:
					break
			try:
				keyLength = int(input("Enter the desired length of your password (integer > 0):\n"))
				if keyLength > 0:
					break
				else:
					print("Invalid input. Please enter a positive integer.")
			except ValueError:
				print("Invalid input. Please enter a positive integer.")
	# If printToConsole is False and keyLength is None, raise a TypeError
	elif keyLength == None:
		raise TypeError("Input argument 'keyLength' cannot be None if the argument 'printToConsole' is False. Must be 'int' or 'printToConsole' must be True.")
	# If keyLength is less than or equal to 0 and printToConsole is False, raise a ValueError
	elif keyLength <= 0:
		raise ValueError("Input argument 'keyLength' cannot be an integer less than 1 if the argument 'printToConsole' is False. Must be an integer greater than 0 or 'printToConsole' must be True.")
	
	# If all character sets are empty, raise a ValueError
	if not numbers and not letters and not symbols:
		raise ValueError("All character sets are empty. At least one character set must contain characters.")

	# Initialize the key as an empty list
	key = []

	# Remove empty character sets
	characterSets = [numbers, letters, symbols]
	for characterSet in characterSets.copy():
		if len(characterSet) == 0:
			characterSets.remove(characterSet)
	
	# Generate the key by randomly selecting a character from a randomly selected character set
	for keyCharacter in range(keyLength):
		key.append(rng.choice(rng.choice(characterSets)))
	
	# If printToConsole is True, print the generated key
	if printToConsole:
		print(f"Your password is:\n{''.join(key)}\n")
	
	# Return the generated key as a string and keyLength as an integer in a tuple
	return ''.join(key), keyLength

# If standalone...		
if __name__ == '__main__':
	# Define main()
	def main():
		"""
    	The main function of the keygen program.

    	This function initializes the character sets (numbers, letters, symbols) and welcomes the
		user to the program. It then calls the blacklistCharacters function to remove any
		blacklisted characters from the character sets. After that, it calls the keygen function to
		generate a password based on the provided character sets and length.

    	The function then enters a loop where it provides the user with several options:
    	1. Regenerate the password with the same settings.
    	2. Regenerate the password with the same blacklist but a new length.
    	3. Regenerate the password with the same length but a new blacklist.
		4. Regenerate but with completely new settings.
    	5. Exit the program.

    	The user's selection is processed, and the appropriate actions are taken based on the
		selection.

    	Args:
        	None

    	Returns:
        	None
    	"""

		# Initialize character sets
		numbers = list(txt.digits)
		letters = list(txt.ascii_letters)
		symbols = list(txt.punctuation)

		# Welcome message
		print("\n\n")
		print("╔══════════════════════════════════════════════════╗")
		print("║░░░░░░░░░░░░░████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║")
		print("║░░░░░░░░░░░██░░░░░░░░██░░░░░░░░░░░░░░░░░░░░░░░░░░░║")
		print("║░░░░░░░░░██░░░░░░░░░░░░██████████████████░░░░░░░░░║")
		print("║░░░░░░░░░██░░████░░░░░░░░░░░░░░░░░░░░░░██░░░░░░░░░║")
		print("║░░░░░░░░░██░░████░░░░░░░░░░██░░██░░██░░██░░░░░░░░░║")
		print("║░░░░░░░░░██░░░░░░░░░░░░████░░██░░██░░██░░░░░░░░░░░║")
		print("║░░░░░░░░░░░██░░░░░░░░██░░░░░░░░░░░░░░░░░░░░░░░░░░░║")
		print("║░░░░░░░░░░░░░████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║")
		print("╠══════════════════════════════════════════════════╣")
		print("║Welcome to KEYGEN! Thank you for using my program!║")
		print("║                                   -VladinXXV     ║")
		print("╚══════════════════════════════════════════════════╝\n\n")

		# Call blacklistCharacters function to remove blacklisted characters from character sets
		blacklistCharacters(numbers, letters, symbols, printToConsole = True)
		# Call keygen function to generate a password and save the key and keyLength
		key, keyLength = keygen(numbers, letters, symbols, printToConsole = True)

		# Enter a loop to provide user with several options
		while True:
			# Easter egg for when the key is "Spamton"... crazy lucky, or just a bit clever?
			if key == "Spamton":
				print("\n\nHEY\tEVERY\t!! IT'S ME!!!")
				print("EV3RY\tBUDDY\t'S FAVORITE [[Number 1 Rated Salesman1997]]\n\n")

			# Display options to the user
			print("\nOptions:")
			print("1. Regenerate with the same settings")
			print("2. Regenerate with the same blacklist but a new length")
			print("3. Regenerate with the same length but a new blacklist")
			print("4. Regenerate with completely new settings")
			print("5. Exit")

			# Get user's selection
			option = input("Enter your selection: ")

			# Process user's selection
			if option == '1':
				# Regenerate with the same settings (use that keyLength we saved at the start!)
				key, keyLength = keygen(numbers, letters, symbols, keyLength, True)
			elif option == '2':
				# Regenerate with the same blacklist but a new length
				keyLength = None
				key, keyLength = keygen(numbers, letters, symbols, keyLength, True)
			elif option == '3':
				# Regenerate with the same length but a new blacklist (gotta reset character sets)
				numbers = list(txt.digits)
				letters = list(txt.ascii_letters)
				symbols = list(txt.punctuation)
				blacklistCharacters(numbers, letters, symbols, printToConsole = True)
				key, keyLength = keygen(numbers, letters, symbols, keyLength, True)
			elif option == '4':
				# Regenerate but with completely new settings
				keyLength = None
				numbers = list(txt.digits)
				letters = list(txt.ascii_letters)
				symbols = list(txt.punctuation)
				blacklistCharacters(numbers, letters, symbols, printToConsole = True)
				key, keyLength = keygen(numbers, letters, symbols, keyLength, True)
			elif option == '5':
				# Exit the program
				break
			else:
				# Invalid option
				print("Invalid option. Please enter a valid option.")

	# Call to main()
	main()
