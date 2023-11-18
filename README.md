# Slopify

Welcome to the kitchen of coding chaos, where Slopify takes your meticulously crafted source code and blends it into a fine puree of potential and possibilities. It's like a culinary adventure for your codebase, except the chef is a language model with a taste for the unpredictable.

## What's Slopify?

Slopify is the digital equivalent of a food fight, but with code. It's a tool that slurps up your source code, feeds it to a ravenous Language Learning Model (LLM), and waits for the LLM to regurgitate a new concoction of code suggestions. Then, with the grace of a starved hyena, Slopify gobbles up the LLM's output and smears it back into your project.

## Installation

Installing Slopify is as easy as pie, which, coincidentally, might be what your code resembles after using it:

```bash
# Install via Poetry
poetry add slopify
```

## Usage

To copy your codebase into the system clipboard for Slopify, just run:

```bash
# Copy your code into the system clipboard
slopify slop /path/to/your/code
```

If you prefer to dump your code into a Markdown file instead of the clipboard, use the `-o` flag:

```bash
# Dump your code into a Markdown file
slopify slop /path/to/your/code -o slop_bucket.md
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

- [] accept diffs in apply markdown
- [] allow configurable token limit for dump with graceful failure when overbudget
- [] allow specifying sets of interdependent files commonly needed to be assessed jointly.
    - shell command e.g. `slopify set create my_set ...`
    - config file e.g. `slopify dump -c my_set`
- [] automatically generate relevant context from dependent modules with some static code analysis? (nice to have)

## Disclaimer

Slopify is not responsible for any indigestion, nausea, or existential dread that may result from its use. It's recommended to keep a defibrillator handy for your codebase, just in case.

## Bon Appétit!

Now go forth and let Slopify turn your code into the ultimate potluck, where every line is a surprise and every function is a mystery dish. Who knows, you might just discover the secret sauce that's been missing all along—or you'll end up with a Franken-code monster. Either way, it'll be a meal to remember!

Remember, Slopify is all about embracing the chaos in the quest for coding excellence—or at least some good laughs along the way. Enjoy the mess!
