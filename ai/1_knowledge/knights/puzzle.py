from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# General rules:
# Knight always is true
# Knave always is false
# Player can only be a Knight or a Knave, not both.

# Puzzle 0
# A says "I am both a knight and a knave."
A_0 = And(AKnight, AKnave)
knowledge0 = And(
    Implication(AKnight, A_0),
    Implication(AKnave, Not(A_0)),
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
A_1 = And(AKnave, BKnave)
knowledge1 = And(
    Implication(AKnight, A_1),
    Implication(AKnave, Not(A_1)),
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
A_2 = Or(And(AKnight, BKnight), And(AKnave, BKnave))
B_2 = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    Implication(AKnight, A_2),
    Implication(AKnave, Not(A_2)),
    Implication(BKnight, B_2),
    Implication(BKnave, Not(B_2)),
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
A_3 = Or(AKnight, AKnave)
B_3 = And(AKnave, CKnave)
C_3 = AKnight
knowledge3 = And(
    Implication(AKnight, A_3),
    Implication(AKnave, Not(A_3)),
    Implication(BKnight, B_3),
    Implication(AKnave, Not(B_3)),
    Implication(CKnight, C_3),
    Implication(CKnave, Not(C_3)),
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
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
