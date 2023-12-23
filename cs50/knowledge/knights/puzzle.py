from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

A = {'knight': AKnight, 'knave': AKnave}
B = {'knight': BKnight, 'knave': BKnave}
C = {'knight': CKnight, 'knave': CKnave}


def XOr(p, q):
    return And(Or(p, q), Not(And(p, q)))


def asserted(speaker, sentence):
    return And(
        Implication(speaker['knight'], sentence),
        Implication(speaker['knave'], Not(sentence))
    )


# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    XOr(AKnight, AKnave),
    asserted(A, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    XOr(AKnight, AKnave),
    XOr(BKnight, BKnave),
    asserted(A, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    XOr(AKnight, AKnave),
    XOr(BKnight, BKnave),
    asserted(A, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    asserted(B, And(Not(And(AKnight, BKnight)), Not(And(AKnave, BKnave))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    XOr(AKnight, AKnave),
    XOr(BKnight, BKnave),
    XOr(CKnight, CKnave),
    Or(asserted(A, AKnight), asserted(A, AKnave)),
    asserted(B, asserted(A, BKnave)),
    asserted(B, CKnave),
    asserted(C, AKnight)
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
