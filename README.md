# noisify
Script to infinitely scroll a piece of text or ascii art, with added textual noise.  Useful for decoration, meditation, etc. 

## Usage:

    $ python3 noisify.py [FILENAME]

Text can be read in via standard input or a file.

For best results, add rainbow colors to the text by piping the result through [lolcat](https://github.com/busyloop/lolcat):

    $ python3 noisify.py filename.txt | lolcat
    
Before producing output, noisify.py reads in the entire file or standard input 
until end of file (Ctrl+D if you're typing the input directly), 
so it won't currently handle an infinite stream of input.
