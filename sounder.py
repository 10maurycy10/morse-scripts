import pyaudio
import math
import sys

LATIN_TO_MORSE = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', ' ': '  '}

def gen_morse_code(string):
    return ' '.join([LATIN_TO_MORSE[c.upper()] for c in string])

def sound(string, dot, farnsworth):
    """
    dot = length of a dot in seconds
    farnsworth = How many times longer should the space be then normal
    """
    sample_rate=44000
    frequency=600
    volume=.4

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paUInt8,
        channels=1,  # mono
        rate=sample_rate,
        output=True,
    )
    def sine(length):
        """
        Generates 8 bit samples for a sine wave a freqency for lenght secods
        """
        s = lambda i: volume * math.sin(2 * math.pi * frequency * i / sample_rate)
        samples = bytes(int(s(i) * 0x7F + 0x80) for i in range(int(length*sample_rate)))
        return samples

    def nothing(length):
        return bytes(0x7F for i in range(int(length * sample_rate)))

    for part in gen_morse_code(string):
        match part:
            case "-":
                stream.write(sine(dot*3))
                stream.write(nothing(dot))
            case ".":
                stream.write(sine(dot))
                stream.write(nothing(dot))
            case " ":
                stream.write(nothing(dot*7*farnsworth))
    stream.write(nothing(dot))

    stream.stop_stream()
    stream.close()

if __name__ == "__main__":
    print(gen_morse_code(sys.argv[1]))
    sound(sys.argv[1], 0.06, 1)

