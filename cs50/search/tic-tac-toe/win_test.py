import unittest
import tictactoe


class MyTestCase(unittest.TestCase):
    def test_1(self):
        EMPTY = tictactoe.EMPTY
        X = tictactoe.X
        O = tictactoe.O

        board = [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, X, X],
                 [EMPTY, EMPTY, O]]

        self.assertEqual(tictactoe.minimax(board), (1, 0))


if __name__ == '__main__':
    unittest.main()
