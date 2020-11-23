import time, sys, os, random, datetime
import argparse

def normalize_line_lengths(line_array):
    """Pad all strings in the array to be the same length."""
    max_length = max([len(s) for s in line_array])
    for i, line in enumerate(line_array):
        line_array[i] += " " * (max_length - len(line))

def add_margins(line_array, horizontal_margin_size, vertical_margin_size):
    """Add vertical and horizontal margins to line_array."""
    line_length = len(line_array[0])

    v_margin = " " * line_length
    h_margin = " " * horizontal_margin_size

    for _ in range(vertical_margin_size):
        line_array.append(v_margin)

    for i in range(len(line_array)):
        line_array[i] = f"{h_margin}{line_array[i]}{h_margin}"

def read_input(filename=None):
    """Read input into an array of line strings."""
    if filename:
        with open(filename, 'r') as file:
            lines = [line.rstrip('\n') for line in file]
    else:
        lines = [line for line in sys.stdin.read().split("\n")]
    normalize_line_lengths(lines)
    add_margins(lines, 3, 1)
    return lines

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


def main(filename=None, debug=False, noise=True, term_width=None):
    if not term_width:
        try:
            term_width, _ = os.get_terminal_size()
        except OSError as ose:
            print("Couldn't get terminal width.  If you're sending the "
                "output to another program, you may need to explicitly "
                "specify the terminal width using --term-width=<number>.  "
                "You can find the terminal width with --show-term-width.")
            sys.exit(1)
    DEBUG_OUTPUT_WIDTH = 26
    if debug:
        term_width -= DEBUG_OUTPUT_WIDTH

    lines = read_input(filename)
    if len(lines) == 0:
        raise Exception("No input.")

    num_columns = term_width // len(lines[0])


    # The following rate manager parameters were discovered through
    # experimentation and shouldn't be assumed to have special
    # significance, other than that the program has the kind
    # of feel I was going for.

    # randomly varying rate of scrolling
    rm_speed = RateManager(
        initial_rate = 1,
        min_rate = .1,
        max_rate = 2.5,
        rate_delta = -.1)

    # randomly varying rate of chance of output
    rm_chance = RateManager(
        initial_rate = .2,
        min_rate = .05,
        max_rate = .9,
        rate_delta = .05)

    # randomly varying rate of chance of bumping up other rates
    rm_bumper = RateManager(
        initial_rate = .01,
        min_rate = .01,
        max_rate = .95,
        rate_delta = .1)

    # value of rm_bumper.rate above which other rates will be bumped.
    # The effect is that, above this threshold, the visualization should
    # seem to have more "energy" or be "on fire".
    BUMPER_THRESHOLD = .83

    # randomly varying rate of noise
    rm_noise = RateManager(
        initial_rate = .1,
        min_rate = .01,
        max_rate = .99,
        rate_delta = -.007)

    current_line_num = 0
    while True:
        if debug:
            # Print current values of rate managers.
            print(f"R{rm_speed.rate:2.1f} "
                f"C{rm_chance.rate:.2f} "
                f"B{rm_bumper.rate:.2f} "
                f"N{rm_noise.rate:.2f}|", end=" ")
        # line = "   " + lines[current_line_num] + "   "
        line = lines[current_line_num]

        # Single use function for use in the generator expression below.
        def transform(s, noise):
            """Apply maybe and noisify transformations to string s."""
            if noise:
                s = maybe(s, rm_chance.rate)
                if random.random() < rm_noise.rate:
                    s = noisify(s, rm_noise.rate)
            return s

        outline = "".join([transform(line, noise) for _ in range(num_columns)])
        print(outline)
        sys.stdout.flush()
        current_line_num = (current_line_num + 1) % len(lines)

        rm_bumper.update_rate()
        rm_chance.update_rate()
        rm_noise.update_rate()
        rm_speed.update_rate()

        time.sleep(rm_speed.rate)

        if rm_bumper.rate >= BUMPER_THRESHOLD:
            rm_speed.bump_rate()
            rm_chance.bump_rate()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script to infinitely scroll a piece of text or ascii art, with added textual noise.")

    parser.add_argument('FILENAME', nargs='?',
        help="file with input text")

    parser.add_argument("--no-noise", action="store_true",
        help="don't add noise.")

    parser.add_argument('--debug', action="store_true",
        help="show debugging information")

    parser.add_argument('--show-term-width', action="store_true",
        help="show current terminal window's width and exit")

    parser.add_argument('--term-width', type=int)

    args = parser.parse_args()
    filename = args.FILENAME
    debug = args.debug
    add_noise = not args.no_noise
    term_width = args.term_width

    if args.show_term_width:
        ts_columns, _ = os.get_terminal_size()
        print(ts_columns)
        sys.exit(0)

    try:
        main(filename, debug, add_noise, term_width)
    except KeyboardInterrupt:
        pass
