# import RPi.GPIO as GPIO
import time
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(18, GPIO.OUT)


def translator(character):
    dot = 1
    dash = 3

    morse_code = {"A": [dot, "PAUSE", dash],
                  "B": [dash, "PAUSE", dot, "PAUSE", dot, "PAUSE", dot],
                  "C": [dash, "PAUSE", dot, "PAUSE", dash, "PAUSE", dot],
                  "D": [dash, "PAUSE", dot, "PAUSE", dot],
                  "E": [dot],
                  "F": [dot, "PAUSE", dot, "PAUSE", dash, "PAUSE", dot],
                  "G": [dash, "PAUSE", dash, "PAUSE", dot],
                  "H": [dot, "PAUSE", dot, "PAUSE", dot, "PAUSE", dot],
                  "I": [dot, "PAUSE", dot],
                  "J": [dot, "PAUSE", dash, "PAUSE", dash, "PAUSE", dash],
                  "K": [dash, "PAUSE", dot, "PAUSE", dash],
                  "L": [dot, "PAUSE", dash, "PAUSE", dot, "PAUSE", dot],
                  "M": [dash, "PAUSE", dash],
                  "N": [dash, "PAUSE", dot],
                  "O": [dash, "PAUSE", dash, "PAUSE", dash],
                  "P": [dot, "PAUSE", dash, "PAUSE", dash, "PAUSE", dot],
                  "Q": [dash, "PAUSE", dash, "PAUSE", dot, "PAUSE", dash],
                  "R": [dot, "PAUSE", dash, "PAUSE", dot],
                  "S": [dot, "PAUSE", dot, "PAUSE", dot],
                  "T": [dash],
                  "U": [dot, "PAUSE", dot, "PAUSE", dash],
                  "V": [dot, "PAUSE", dot, "PAUSE", dot, "PAUSE", dash],
                  "W": [dot, "PAUSE", dash, "PAUSE", dash],
                  "X": [dash, "PAUSE", dot, "PAUSE", dot, "PAUSE", dash],
                  "Y": [dash, "PAUSE", dot, "PAUSE", dash, "PAUSE", dash],
                  "Z": [dash, "PAUSE", dash, "PAUSE", dot, "PAUSE", dot],
                  "1": [dot, "PAUSE", dash, "PAUSE", dash, "PAUSE", dash, "PAUSE", dash],
                  "2": [dot, "PAUSE", dot, "PAUSE", dash, "PAUSE", dash, "PAUSE", dash],
                  "3": [dot, "PAUSE", dot, "PAUSE", dot, "PAUSE", dash, "PAUSE", dash],
                  "4": [dot, "PAUSE", dot, "PAUSE", dot, "PAUSE", dot, "PAUSE", dash],
                  "5": [dot, "PAUSE", dot, "PAUSE", dot, "PAUSE", dot, "PAUSE", dot],
                  "6": [dash, "PAUSE", dot, "PAUSE", dot, "PAUSE", dot, "PAUSE", dot],
                  "7": [dash, "PAUSE", dash, "PAUSE", dot, "PAUSE", dot, "PAUSE", dot],
                  "8": [dash, "PAUSE", dash, "PAUSE", dash, "PAUSE", dot, "PAUSE", dot],
                  "9": [dash, "PAUSE", dash, "PAUSE", dash, "PAUSE", dash, "PAUSE", dot],
                  "0": [dash, "PAUSE", dash, "PAUSE", dash, "PAUSE", dash, "PAUSE", dash]}

    return morse_code[character]


def sequence_generator(sentence):
    space = "SPACE"
    letter = "LETTER"
    sequence = []

    index = 0
    for character in sentence:
        if character == " ":
            sequence.append(space)
        else:
            sequence.append(translator(character))
            try:
                if sentence[index + 1] != " ":
                    sequence.append(letter)
            except IndexError:
                pass
        index += 1

    return sequence


def sequence_driver(sequence):
    for character in sequence:
        if character == "SPACE":
            time.sleep(7)  # 7 sec pause between words
            # print()
            # print()
            # print()
        elif character == "LETTER":
            time.sleep(3)  # 3 sec pause between letters
            # print()
        else:
            for symbol in character:
                if symbol == "PAUSE":
                    time.sleep(1)  # 1 sec pause between symbols
                else:
                    # GPIO.output(18, True)
                    # print(symbol)
                    time.sleep(symbol)
                    # GPIO.output(18, False


def main():
    """
    Drive the program.
    """
    while True:
        sentence = input("Enter the sentence you want to encode (or Enter to quit the program): ").upper().strip()
        if sentence == "":
            break

        valid_sentence = True

        for word in sentence.split():
            if not word.isalnum():
                print("The sentence must be only constructed using alphanumeric characters (a-z) and (0-9).")
                valid_sentence = False
                break

        if valid_sentence:
            sentence_sequence = sequence_generator(sentence)
            repeat = True
            while repeat:
                print("\n\nTranslating the following sentence: \"" + sentence + "\"")
                print("\nStarting Morse Code sequence (Please look at the LED)...\n")
                sequence_driver(sentence_sequence)

                while True:
                    repeat = input("\nRepeat the sequence? (y/n)").upper().strip()

                    if repeat == "Y":
                        break
                    elif repeat == "N":
                        repeat = False
                        print()
                        print()
                        break
                    else:
                        print("\nPlease enter either 'Y' or 'N'.")

    # GPIO.cleanup()


if __name__ == "__main__":
    main()
