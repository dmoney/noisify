# noisify

A script to infinitely scroll a piece of text or ascii art, with added textual noise.  Useful for decoration, meditation, etc.

The script reads the input, pads it so all lines are of equal length, and then scrolls an infinitely repeating grid of the input.  The added noise takes the form of a set of noise characters that randomly replace input characters, as well as randomly dropped lines.  The rate at which this happens will vary randomly over time.

## Basic Usage:

    $ python3 noisify.py [FILENAME]

Text can be read in via standard input or a file.

For best results, add rainbow colors to the text by piping the result through [lolcat](https://github.com/busyloop/lolcat):

    $ python3 noisify.py --term-width=80 example.txt | lolcat

## Example Output:

![Screenshot showing ascii smiley faces in rainbow colors with text noise](https://user-images.githubusercontent.com/30746/99932780-18530300-2d27-11eb-96a3-b5694b9c8d9b.png)

Or after the noise ramps up a bit more:

![Screenshot showing a lot more text noise in rainbow colors, with some smiley faces poking through.](https://user-images.githubusercontent.com/30746/99933039-d8405000-2d27-11eb-84ba-f0e9ef3ea923.png)

## Randomly Varying Parameters

Several parameters will randomly vary (increase or decrease by an internally defined increment) after each line is printed:

* The **rate** of scrolling (number of seconds to sleep between each line)
* The level of **noise** (chance of replacing an input character with a noise character)
* The **chance** of a line not being dropped (masked by spaces)
* A parameter called **bumper**, which, when above a certain threshold, causes `rate` to decrease (speed up) and `chance` to increase

The values of these parameters can be displayed with the `--debug` option.

## Command-Line Options

### -h

  Show help message and exit.

### --no-noise

Don't add noise, and don't drop lines.  Useful for verifying that the input is being read in correctly.

### --debug

Add a running display of the values of Rate (R), Chance (C), Bumper (B), and Noise (N) to each printed line.  It will look like:

    R2.0 C0.25 B0.51 N0.61|  (noisified output...)

### --term-width and --show-term-width

When displaying directly to the terminal, it will get the terminal's width in order to determine how many repeating columns of the input it can display.  If the output is being piped to another program (such as `lolcat`), it won't be able to get the terminal width, so it will need to be explicitly set with `--term-width`.  In order to easily determine what value to use, the `--show-term-width` option will cause noisify to print the terminal width and exit.

    $ python3 noisify.py example.txt | lolcat
    Couldn't get terminal width.  If you're sending the
    output to another program, you may need to explicitly
    specify the terminal width using --term-width=<number>.  
    You can find the terminal width with --show-term-width.

    $ python3 noisify.py --show-term-width
    126

    $ python3 noisify.py example.txt --term-width=126 | lolcat
    (noisified, rainbow colored output)

## Limitations

Before producing output, noisify.py reads in the entire file or standard input
until end of file (Ctrl+D if you're typing the input directly),
so it won't currently handle an infinite stream of input.
