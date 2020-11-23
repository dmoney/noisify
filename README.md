# noisify
Script to infinitely scroll a piece of text or ascii art, with added textual noise.  Useful for decoration, meditation, etc.

## Usage:

    $ python3 noisify.py [FILENAME]

Text can be read in via standard input or a file.

For best results, add rainbow colors to the text by piping the result through [lolcat](https://github.com/busyloop/lolcat):

    $ python3 noisify.py --term-width=80 example.txt | lolcat

Example output:

![Screenshot showing ascii smiley faces in rainbow colors with text noise](https://user-images.githubusercontent.com/30746/99932780-18530300-2d27-11eb-96a3-b5694b9c8d9b.png)

Or after the noise ramps up a bit more:

![Screenshot showing a lot more text noise in rainbow colors, with some smiley faces poking through.](https://user-images.githubusercontent.com/30746/99933039-d8405000-2d27-11eb-84ba-f0e9ef3ea923.png)

To see command-line options:

    $ python3 noisify.py -h

Before producing output, noisify.py reads in the entire file or standard input
until end of file (Ctrl+D if you're typing the input directly),
so it won't currently handle an infinite stream of input.
