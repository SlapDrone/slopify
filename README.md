# Slopify

Tired of copying and pasting code to and from your favourte LLM while you try to figure out whether its worth making it do your work for you or whether you'd be faster doing it yourself?

Do you reflexively spit at the notion of letting an autoregressive language model fumble around autonomously in your home or on your computer, lest it knock over your vases or forward those e-mails you sent to noam chomsky to your wife? 

Does doing RAG just seem like a picking out a fragile mystery box from a store that sells an assortment of rube-goldberg machines, each bestowed with many adjectives, and then putting it in charge of all your financial decisions?

Do you identify with [the spirit of the barbarian](https://www.cracked.com/blog/the-way-of-the-barbarian-infusing-your-spiritual-life-with-conan) before that of the sorcerer?

If you answered yes to all of the above, you might want to try `slopify`.

## What's Slopify?

Slopify is a blunt instrument that dutifully sucks up all the source code you point it at and smashes it all together in a big markdown sandwich and serves you it up on your ~clipboard~ slop bucket (or to a file). You can let your favourite stochastic parrot loose on this diabolical slurry and, by priming it with an appropriate system message, have it vomit it back up rearranged and mingled with the other contents of its stomach. Slopify will help you slather that hot mess right back in there in all the right places before anybody else notices.

## Installation

Installing Slopify is much cleaner than you may be liable to feel after using it:

```bash
# Install via Poetry
poetry add slopify
```

or:

```bash
# Install with pip
pip install slopify
```

## Usage

To serialise some (or all) of your codebase into a big old markdown sandwich delivered straight to your system clipboard, just run:

```bash
# everything
slopify slop .
```

or:

```bash
# recursive, targeted
slopify slop -r src/preprocessing/
```

or: 

```bash
# glob
slopify slop **/*.h
```

You get the idea.

If you prefer to dump your code into a Markdown file instead of the clipboard, use the `-o` flag:

```bash
slopify slop -o slop.md src/
```

To apply suggestions from the system clipboard back onto your codebase:

```bash
# Apply suggestions from the clipboard
slopify slather
```

If you have suggestions in a file instead of the clipboard, use the `-i` flag:

```bash
# Apply suggestions from a Markdown file
slopify slather -i vomit.md
```
## TODO

- [ ] support line numbers 
- [ ] accept diffs in apply markdown (prerequisite above)
    - or explicit git patches, saving on tokens
- [ ] allow configurable token limit for dump with graceful failure when overbudget
- [ ] allow specifying sets of interdependent files commonly needed to be assessed jointly.
    - shell command e.g. `slopify set create my_set ...`
    - config file e.g. `slopify dump -c my_set`
- [ ] check outputs conform to file system (validation before slather)
    - perhaps anticipate an explicit "new file" flag to deal with cases where new file creation intentional
- [ ] automatically generate relevant context from dependent modules with some static code analysis? (nice to have)
- [ ] support jupyter notebooks (grab code cell contents only - nice to have)
- [ ] use [Outlines](https://github.com/outlines-dev/outlines) to constrain generation to valid slop

## Disclaimer

Slopify is not responsible for any indigestion, nausea, or existential dread that may result from its use. It's recommended to keep a defibrillator handy for your codebase, just in case. Enjoy the absurdity of the era.
