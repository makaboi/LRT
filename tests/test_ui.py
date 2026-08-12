import unittest

from roads_beneath_shadow.ui import InputClosed, TerminalUI


class TerminalUITests(unittest.TestCase):
    def test_eof_raises_input_closed_instead_of_looping(self) -> None:
        def closed_input(_: str) -> str:
            raise EOFError

        ui = TerminalUI(color=False, fast=True, input_fn=closed_input, output_fn=lambda _: None)

        with self.assertRaises(InputClosed):
            ui.choose("Menu", ["One", "Two"])


if __name__ == "__main__":
    unittest.main()
