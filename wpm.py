DOTS_IN_WORD=50 # Based on 'PARIS' standard word
CHARS_IN_WORD=5
SECONDS_IN_MIN=60
MS_IN_S = 1000

COMMON_WPM = [5,10,15,20,25,30,35,40,45,50]

def printline(wpm):
    chars_per_min = CHARS_IN_WORD * wpm
    dots_per_min = DOTS_IN_WORD * wpm
    dots_per_s = dots_per_min / SECONDS_IN_MIN
    ms_per_dot = MS_IN_S / dots_per_s
    print(f"{wpm}\t{chars_per_min}\t{round(dots_per_s)}\t{round(ms_per_dot)}ms")

print("wpm\tcpm\tdps\tdot")
for wpm in COMMON_WPM:
    printline(wpm)
