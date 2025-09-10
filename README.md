The EASIEST way to run:
1. Download .csv and .py and .txt
2. Run .py
3. Enter your first result in terminal




# wordle-bot
Assistant bot that suggests optimal guesses based on feedback patterns.  
Wordle 3-Turn Solver (SOARE opening)

A minimal command-line Wordle helper that aims to solve by the third guess:

Round 1: fixed opening soare

Round 2: uses a precomputed lookup (soare_first_pattern_to_best_second.csv)

Round 3+: auto-suggests from the remaining candidates (presence-based scoring)

You only enter Wordle’s feedback pattern each round (0 gray, 1 yellow, 2 green).
The program always follows its own suggested guess—no manual word entry required.

What’s included

wordle_main.py — interactive solver (runtime)

soare_first_pattern_to_best_second.csv — mapping from first-round feedback to the best second guess for the SOARE opening

Note: The lookup CSV must be consistent with your word list and the soare opening.

Requirements

Python 3.8+

No third-party packages needed

Word list (TXT)

Provide a TXT file named wordle database 3189.txt (same folder), with:

one word per line

exactly 5 letters

letters only (A–Z; case doesn’t matter)

UTF-8 encoding

Example:

eagle
cigar
slate
soare
...


You can change the filename by editing TXT_PATH inside wordle_main.py.

How to run
python3 wordle_main.py


Round 1

The program assumes the guess soare.

You enter the feedback pattern for soare, e.g. 02201.

0 = gray, 1 = yellow, 2 = green

Must be 5 digits.

Round 2

The program looks up the best second guess from soare_first_pattern_to_best_second.csv.

You enter the feedback pattern for that suggested word.

Round 3+

The program auto-suggests the next word from the remaining candidates.

Keep entering feedback patterns until you get 22222 (solved) or candidates run out.

File layout
your-folder/
├─ wordle_main.py
├─ soare_first_pattern_to_best_second.csv
└─ wordle database 3189.txt      # your 5-letter word list

Notes about the lookup CSV

It maps first-round feedback (to SOARE) → best second guess to minimize the expected size of the remaining set after round 2.

If a pattern is missing from the CSV, the solver falls back to a presence-based suggestion—still works.

If you change the word list significantly or change the opening, you should regenerate this CSV accordingly (not included here).

Troubleshooting

“No matching candidates”
The answer may not be in your TXT word list, or a feedback entry was mistyped.
Ensure the target word exists in wordle database 3189.txt (5 letters, letters only, UTF-8), and feedback strings are exactly 5 digits of 0/1/2.

“Pattern not found in CSV”
The solver will automatically fall back to presence-based suggestion. This is OK, but for best results, use a CSV generated with the same word list.

Encoding / weird characters
Make sure your TXT is saved as UTF-8 and contains only A–Z letters per line.
