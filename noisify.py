import time, sys, random, datetime
lines = [
    "    O    ",
    "    V    ",
    "O (D*-) O",
    "    U    ",
    "  O   O  ",
    "         ",
    "         ",
    ]


i = 0

class RateManager:
    def __init__(self, initial_rate, min_rate, max_rate, rate_delta):
        self.rate = initial_rate
        self.max_rate = max_rate
        self.min_rate = min_rate
        self.rate_delta = rate_delta

    def update_rate(self):
        r = random.random()
        if r > .6:
            self.rate += self.rate_delta
        elif r < .4:
            self.rate -= self.rate_delta
        self.rate = min(self.rate, self.max_rate)
        self.rate = max(self.rate, self.min_rate)

    def bump_rate(self):
        self.rate += self.rate_delta
        self.rate = min(self.rate, self.max_rate)
        self.rate = max(self.rate, self.min_rate)

    def sleep(self):
        time.sleep(self.rate)

def maybe(string, chance=.5):
    r = random.random()
    if r <= chance:
        return string
    else:
        return " " * len(string)

NOISE_CHARS = "abcdefghijklmnopqrstuvwxyz" + \
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + \
    "1234567890" + \
    ",.<>/?;:\'\"!@#$%^&*()-_=+\`~\\|[]{}"

def noisify(string, factor):
    out = ""
    for c in string:
        if random.random() < factor:
            out += random.choice(NOISE_CHARS)
        else:
            out += c
    return out


# randomly varying rate of scrolling
rm = RateManager(1, .1, 2.5, -.1)

# randomly varying rate of chance of output
rm_chance = RateManager(.2, .05, .9, .05)

# randomly varying rate of chance of bumping up other rates
rm_bumper = RateManager(.01, .01, .95, .1)

rm_noise = RateManager(.1, .01, .99, -.007)

NUM_COLUMNS = 8
DEBUG = False
if DEBUG:
    NUM_COLUMNS -= 2

BUMPER_THRESHOLD = .83

while True:
    if DEBUG:
        print(f"R{rm.rate:2.1f} "
            f"C{rm_chance.rate:.2f} "
            f"B{rm_bumper.rate:.2f} "
            f"N{rm_noise.rate:.2f}|", end=" ")
    line = "   " + lines[i] + "   "

    def transform(s):
        s = maybe(s, rm_chance.rate)
        if random.random() < rm_noise.rate:
            s = noisify(s, rm_noise.rate)
        return s

    outline = "".join([transform(line) for _ in range(NUM_COLUMNS)])
    print(outline)
    sys.stdout.flush()
    i = (i + 1) % len(lines)

    rm_bumper.update_rate()
    rm_chance.update_rate()
    rm_noise.update_rate()
    rm.update_rate()
    rm.sleep()

    if rm_bumper.rate >= BUMPER_THRESHOLD:
        rm.bump_rate()
        rm_chance.bump_rate()
