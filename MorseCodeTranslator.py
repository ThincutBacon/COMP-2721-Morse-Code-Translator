import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(25, GPIO.IN)


def translator_a_to_m(character):
    dot = 0.5  # 1 sec long for dots (Halved to 0.5)
    dash = 1.5  # 3 sec long for dashes (Halved to 1.5)

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


def translator_m_to_a(sequence):
    dot = 1  # 1 sec long for dots
    dash = 3  # 3 sec long for dashes

    morse_code = {(dot, dash): "A",
                  (dash, dot, dot, dot): "B",
                  (dash, dot, dash, dot): "C",
                  (dash, dot, dot): "D",
                  (dot): "E",
                  (dot, dot, dash, dot): "F",
                  (dash, dash, dot): "G",
                  (dot, dot, dot, dot): "H",
                  (dot, dot): "I",
                  (dot, dash, dash, dash): "J",
                  (dash, dot, dash): "K",
                  (dot, dash, dot, dot): "L",
                  (dash, dash): "M",
                  (dash, dot): "N",
                  (dash, dash, dash): "O",
                  (dot, dash, dash, dot): "P",
                  (dash, dash, dot, dash): "Q",
                  (dot, dash, dot): "R",
                  (dot, dot, dot): "S",
                  (dash): "T",
                  (dot, dot, dash): "U",
                  (dot, dot, dot, dash): "V",
                  (dot, dash, dash): "W",
                  (dash, dot, dot, dash): "X",
                  (dash, dot, dash, dash): "Y",
                  (dash, dash, dot, dot): "Z",
                  (dot, dash, dash, dash, dash): "1",
                  (dot, dot, dash, dash, dash): "2",
                  (dot, dot, dot, dash, dash): "3",
                  (dot, dot, dot, dot, dash): "4",
                  (dot, dot, dot, dot, dot): "5",
                  (dash, dot, dot, dot, dot): "6",
                  (dash, dash, dot, dot, dot): "7",
                  (dash, dash, dash, dot, dot): "8",
                  (dash, dash, dash, dash, dot): "9",
                  (dash, dash, dash, dash, dash): "0"}

    try:
        if not sequence:
            return ""
        return morse_code[sequence]
    except KeyError:
        return "?"


def sequence_generator(sentence):
    space = "SPACE"
    letter = "LETTER"
    sequence = []

    index = 0
    for character in sentence:
        if character == " ":
            sequence.append(space)
        else:
            sequence.append(translator_a_to_m(character))
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
            time.sleep(3.5)  # 7 sec pause between words (Halved to 3.5)
        elif character == "LETTER":
            time.sleep(1.5)  # 3 sec pause between letters (Halved to 1.5)
        else:
            for symbol in character:
                if symbol == "PAUSE":
                    time.sleep(0.5)  # 1 sec pause between symbols (Halved to 0.5)
                else:
                    GPIO.output(18, True)
                    time.sleep(symbol)
                    GPIO.output(18, False)


def alpha_to_morse():
    print("\n\n======== ALPHA TO MORSE ========\n")
    while True:
        sentence = input("Enter the sentence you want to encode (or Enter to quit the program): ").upper().strip()
        if sentence == "":
            print()
            print()
            break

        valid_sentence = True

        for word in sentence.split():
            if not word.isalnum():
                print("The sentence must be only constructed using alphanumeric characters (a-z) and (0-9).")
                valid_sentence = False

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


def morse_to_alpha():
    print("\n\n======== MORSE TO ALPHA ========\n")

    repeat = True
    while repeat:
        print("+++ Button Inputs +++\n"
              "Quick Press: DOT\n"
              "Long Press: DASH\n"
              "1 Sec Release: NEW LETTER\n"
              "3 Sec Release: SPACE\n"
              "10+ Sec Release: END SEQUENCE\n")

        user_input = input("Press Enter if you are ready to start (or X to return to menu): ").strip().upper()

        if user_input == "X":
            return

        print("\nStart entering your sequence\n")

        space = "SPACE"
        letter = "LETTER"
        dash = 3
        dot = 1

        morse_sequence = []
        press_count = 0
        release_count = 0
        while True:
            if not GPIO.input(25):  # If the button is pressed, then...
                if release_count >= 3:
                    morse_sequence.append(space)
                    print("\nSPACE\n")
                elif release_count >= 1:
                    morse_sequence.append(letter)
                    print("NEW LETTER")
                release_count = 0
                press_count += 0.5
            if GPIO.input(25):  # If the button is released (not pressed), then...
                if (press_count != 0 and press_count <= 1):
                    morse_sequence.append(dot)
                    print("DOT")
                elif press_count > 1:
                    morse_sequence.append(dash)
                    print("DASH")
                press_count = 0
                release_count += 0.1
                if release_count >= 10:
                    morse_sequence.append(letter)
                    break
            time.sleep(0.1)

        print("\nEnd of Sequence.\n")

        translated_string = ""
        letter_sequence = []
        for symbol in morse_sequence:
            if symbol == "LETTER" or symbol == "SPACE":
                translated_string += translator_m_to_a(tuple(letter_sequence))
                letter_sequence = []
                if symbol == "SPACE":
                    translated_string += " "
            else:
                letter_sequence.append(symbol)

        print("\n\nTranslated Sentence: \n\"" + translated_string + "\"\n")

        while True:
            repeat = input("\nTranslate another sequence? (y/n)").upper().strip()

            if repeat == "Y":
                break
            elif repeat == "N":
                repeat = False
                print()
                print()
                break
            else:
                print("\nPlease enter either 'Y' or 'N'.")
    print()
    print()


def main():
    """
    Drive the program.
    """
    while True:
        print("======== MORSE CODE TRANSLATOR ========\n"
              "(1) Alpha to Morse\n"
              "(2) Morse to Alpha\n"
              "(3) Exit Program\n")

        mode_select = input("\nSelect Mode (1~3): ").strip()

        if mode_select == "1":
            alpha_to_morse()
        elif mode_select == "2":
            morse_to_alpha()
        elif mode_select == "3":
            break
        else:
            print("Invalid selection. Please try again.")

    GPIO.cleanup()


if __name__ == "__main__":
    main()
