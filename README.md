# Math-Worksheet-Generator

This tool generates randomized math worksheets, and optionally sends them directly to the system's default printer.

The "preview sample" button is mostly for debugging. The sample is not the same as what will be printed. It generates and prints all at once, because I intend for my 6yo son to generate these and hand them to me. My intent is to not give him an (easy) way to modify the papers before he prints them.

For now, it just does basic math. The "simple" problems revolve around numbers 1-20. The "long" problems have arbitrarily large numbers with some constraints (e.g. the dividend is a multiple of the divisor). If this works out, I'll be adding more types of problems in the future.

The problem count in each type of problem is divided evenly among all the selected problem types. For example, if you select long add, long subtract, and long multiply, and set total problems to 30, you'll get 10 each. If this doesn't divide evenly, the last group (highest difficulty) will be truncated; for example, if you select simple add and simple subtract with 3 total problems, you'll get 2 add and 1 subtract.

Here's a screenshot:

<img width="798" height="626" alt="image" src="https://github.com/user-attachments/assets/b6f99aab-1d65-439a-b7f4-a6d466c9431d" />
