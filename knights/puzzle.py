from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),                        # A is a knight or a knave but not both
    Not(And(AKnight, AKnave)),
    Implication(AKnight, And(AKnight, AKnave))  # If a is a knight, then A is both a knight and knave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),                            # A is a knight or knave but not both
    Or(BKnight, BKnave),                            # B is a knight or knave but not both
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Implication(AKnight, And(BKnave, AKnave)),      # If A is a knight, A and B are Knaves
    Implication(AKnave, Not(BKnave))                    # If A is a knave, B is a knight
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),              # A is either a knight or knave but not both
    Not(And(BKnight, BKnave)),              # B is either a knight or knave but not both
    Implication(AKnight, BKnight),          # iF A is a knight then B is a knight
    Implication(AKnave, BKnight),           # if A is a knave then B is a knight
    Implication(BKnight, AKnave),           # If B is a Knight, A is a knave
    Implication(BKnave, AKnave)             # If B is a knave, A is a knave
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),                      # A is either a knight or knave
    Not(And(BKnight, BKnave)),                      # B is either a knight or knave
    Not(And(CKnight, CKnave)),                      # C is either a knight or knave

    Implication(BKnight, CKnave),                   # If B is a knight, C is a knave
    Implication(BKnave, CKnight),                   # If B is a knave, C is a knight

    Implication(CKnave, AKnave),                    # If C is a knave, A is a knave
    Implication(CKnight, AKnight),                  # If C is a knight then A is a knight

    # A says either "I am a knight" or "I am a knave"
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave)))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
