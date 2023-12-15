import unittest
import tictactoe


class MyTestCase(unittest.TestCase):
    def test_accept_action(self):
        EMPTY = tictactoe.EMPTY
        X = tictactoe.X

        expection = [[EMPTY, EMPTY, EMPTY],
                     [EMPTY, X, EMPTY],
                     [EMPTY, EMPTY, EMPTY]]

        self.assertEqual(tictactoe.accept_action(X, tictactoe.initial_state(), (1, 1)), expection)

    def test_player(self):
        self.assertEqual(tictactoe.player(tictactoe.initial_state()), tictactoe.X)

    def test_player2(self):
        EMPTY = tictactoe.EMPTY
        X = tictactoe.X
        O = tictactoe.O

        board = [[X, EMPTY, EMPTY],
                 [EMPTY, O, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]

        self.assertEqual(tictactoe.player(board), tictactoe.X)

    def test_winner_row(self):
        EMPTY = tictactoe.EMPTY
        X = tictactoe.X
        O = tictactoe.O

        board = [[X, O, X],
                 [EMPTY, O, O],
                 [X, X, X]]

        self.assertEqual(tictactoe.winner(board), X)

    def test_winner_column(self):
        EMPTY = tictactoe.EMPTY
        X = tictactoe.X
        O = tictactoe.O

        board = [[X, O, X],
                 [X, O, O],
                 [X, EMPTY, X]]

        self.assertEqual(tictactoe.winner(board), X)

    def test_winner_diagonal_right(self):
        EMPTY = tictactoe.EMPTY
        X = tictactoe.X
        O = tictactoe.O

        board = [[X, O, X],
                 [O, X, O],
                 [O, O, X]]

        self.assertEqual(tictactoe.winner(board), X)

    def test_winner_diagonal_left(self):
        EMPTY = tictactoe.EMPTY
        X = tictactoe.X
        O = tictactoe.O

        board = [[X, O, X],
                 [O, X, O],
                 [X, O, O]]

        self.assertEqual(tictactoe.winner(board), X)

    def test_terminal_not_full(self):
        EMPTY = tictactoe.EMPTY
        X = tictactoe.X
        O = tictactoe.O

        board = [[X, X, X],
                 [EMPTY, X, O],
                 [X, EMPTY, O]]

        self.assertEqual(tictactoe.terminal(board), True)

    def test_terminal_not_full2(self):
        EMPTY = tictactoe.EMPTY
        X = tictactoe.X
        O = tictactoe.O

        board = [[X, X, X],
                 [O, EMPTY, O],
                 [EMPTY, EMPTY, EMPTY]]

        self.assertEqual(tictactoe.terminal(board), True)

    def test_minimax1(self):
        EMPTY = tictactoe.EMPTY
        X = tictactoe.X
        O = tictactoe.O

        board = [[X, O, X],
                 [O, EMPTY, O],
                 [X, O, X]]

        self.assertEqual(tictactoe.minimax(board), (1,1))

    def test_minimax2(self):
        EMPTY = tictactoe.EMPTY
        X = tictactoe.X
        O = tictactoe.O

        board = [[X, EMPTY, X],
                 [O, EMPTY, O],
                 [EMPTY, EMPTY, EMPTY]]

        self.assertEqual(tictactoe.minimax(board), (0,1))

    def test_minimax_initial(self):
        expectations = [(0, 0), (0, 2), (2, 0), (2, 2)]
        self.assertIn(tictactoe.minimax(tictactoe.initial_state()), expectations)

if __name__ == '__main__':
    unittest.main()
