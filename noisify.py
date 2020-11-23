import time, sys, random, datetime
import argparse

def read_input(filename=None):
    """Read input into an array of line strings."""
    if filename:
        with open(filename, 'r') as file:
            lines = [line.rstrip('\n') for line in file]
        return lines
    else:
        return [line for line in sys.stdin.read().split("\n")]

class RateManager:
    """A RateManager manages a value (rate) that randomly increases or decreases when the update_rate is called."""
    def __init__(self, initial_rate, min_rate, max_rate, rate_delta):
        self.rate = initial_rate
        self.max_rate = max_rate
        self.min_rate = min_rate
        self.rate_delta = rate_delta

    def update_rate(self):
        """Randomly increse or decrease rate by rate_delta."""
        r = random.random()
        if r > .6:
            self.rate += self.rate_delta
        elif r < .4:
            self.rate -= self.rate_delta
        self.rate = min(self.rate, self.max_rate)
        self.rate = max(self.rate, self.min_rate)

    def bump_rate(self):
        """Increase rate by rate delta."""
        self.rate += self.rate_delta
        self.rate = min(self.rate, self.max_rate)
        self.rate = max(self.rate, self.min_rate)

    def sleep(self):
        time.sleep(self.rate)

def maybe(string, chance=.5):
    """Randomly return either string or an empty string of equal length."""
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
    """Return a copy of string, with characters randomly replaced with noise characters, at a rate determined by factor."""
    out = ""
    for c in string:
        if random.random() < factor:
            out += random.choice(NOISE_CHARS)
        else:
            out += c
    return out

# Bumper rate manager causes speed and noise to increase more,
# if its current rate is above this threshold.
BUMPER_THRESHOLD = .83

def main(filename=None, debug=False):
    num_columns = 8
    if debug:
        num_columns -= 2

    lines = read_input(filename)

    # randomly varying rate of scrolling
    rm = RateManager(1, .1, 2.5, -.1)

    # randomly varying rate of chance of output
    rm_chance = RateManager(.2, .05, .9, .05)

    # randomly varying rate of chance of bumping up other rates
    rm_bumper = RateManager(.01, .01, .95, .1)

    # randomly varying rate of noise
    rm_noise = RateManager(.1, .01, .99, -.007)

    i = 0
    while True:
        if debug:
            # Print current values of rate managers.
            print(f"R{rm.rate:2.1f} "
                f"C{rm_chance.rate:.2f} "
                f"B{rm_bumper.rate:.2f} "
                f"N{rm_noise.rate:.2f}|", end=" ")
        line = "   " + lines[i] + "   "

        def transform(s):
            """Single use function for use in the generator expression below."""
            s = maybe(s, rm_chance.rate)
            if random.random() < rm_noise.rate:
                s = noisify(s, rm_noise.rate)
            return s

        outline = "".join([transform(line) for _ in range(num_columns)])
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script to infinitely scroll a piece of text or ascii art, with added textual noise.")

    parser.add_argument('FILENAME', help="file with input text", nargs='?')

    # parser.add_argument('--screen-width', type=int, default=120, help="screen width in characters (default 120)", metavar="W")

    parser.add_argument('--debug', action="store_true", help="show debugging information")

    args = parser.parse_args()
    filename = args.FILENAME
    debug = args.debug

    try:
        main(filename, debug)
    except KeyboardInterrupt:
        pass
