import unittest
import os

from roads_beneath_shadow.ui import InputClosed, TerminalUI


class TerminalUITests(unittest.TestCase):
    def test_eof_raises_input_closed_instead_of_looping(self) -> None:
        def closed_input(_: str) -> str:
            raise EOFError

        ui = TerminalUI(color=False, fast=True, input_fn=closed_input, output_fn=lambda _: None)

        with self.assertRaises(InputClosed):
            ui.choose("Menu", ["One", "Two"])

    def test_wasd_navigation_selects_highlighted_option(self) -> None:
        answers = iter(["s", ""])
        output: list[str] = []
        ui = TerminalUI(
            color=False,
            fast=True,
            input_fn=lambda _: next(answers),
            output_fn=output.append,
        )

        self.assertEqual(ui.choose("Menu", ["One", "Two", "Three"]), 2)
        self.assertIn("> [2] Two", output)

    def test_arrow_sequence_and_right_key_select_an_option(self) -> None:
        answers = iter(["\x1b[B", "d"])
        ui = TerminalUI(
            color=False,
            fast=True,
            input_fn=lambda _: next(answers),
            output_fn=lambda _: None,
        )

        self.assertEqual(ui.choose("Menu", ["One", "Two"]), 2)

    def test_left_key_returns_from_a_menu_that_allows_back(self) -> None:
        ui = TerminalUI(
            color=False,
            fast=True,
            input_fn=lambda _: "a",
            output_fn=lambda _: None,
        )

        self.assertIsNone(ui.choose("Menu", ["One"], allow_back=True))

    def test_text_speed_controls_narration_delay(self) -> None:
        delays: list[float] = []
        ui = TerminalUI(
            color=False,
            text_speed="slow",
            output_fn=lambda _: None,
            sleep_fn=delays.append,
        )

        ui.narrate("First paragraph.\n\nSecond paragraph.")

        self.assertEqual(delays, [0.22, 0.22])
        ui.set_text_speed(0.5)
        self.assertEqual(ui.narration_delay, 0.5)

    def test_reduced_motion_collapses_animation_to_last_frame(self) -> None:
        output: list[str] = []
        ui = TerminalUI(
            color=False,
            reduced_motion=True,
            output_fn=output.append,
            terminal_size_fn=lambda _: os.terminal_size((40, 24)),
        )

        ui.animate(("FIRST", "FINAL"))

        self.assertNotIn("FIRST", "\n".join(output))
        self.assertIn("FINAL", "\n".join(output))

    def test_screen_reader_replaces_art_with_short_alt_text(self) -> None:
        output: list[str] = []
        ui = TerminalUI(color=False, fast=True, screen_reader=True, output_fn=output.append)

        ui.art("###\n###", alt_text="A rider blocks the buried road")

        self.assertEqual(output, ["[Scene: A rider blocks the buried road]"])

    def test_art_uses_a_centered_viewport_in_a_narrow_terminal(self) -> None:
        output: list[str] = []
        ui = TerminalUI(
            color=False,
            fast=True,
            output_fn=output.append,
            terminal_size_fn=lambda _: os.terminal_size((24, 24)),
        )

        ui.art("+--------------------------------------+\n|                 *                    |")

        self.assertTrue(output)
        self.assertTrue(all(len(line) <= 24 for line in output))

    def test_direct_prose_is_word_wrapped_in_a_narrow_terminal(self) -> None:
        output: list[str] = []
        ui = TerminalUI(
            color=False,
            fast=True,
            output_fn=output.append,
            terminal_size_fn=lambda *_: os.terminal_size((32, 24)),
        )

        ui.write("Ghorak raises the broken blade while the ancient doorway wakes behind him.")

        self.assertGreater(len(output), 1)
        self.assertTrue(all(len(line) <= 32 for line in output))

    def test_custom_sound_handler_can_fall_back_to_terminal_bell(self) -> None:
        output: list[str] = []
        cues: list[str] = []

        def unavailable(cue: str) -> bool:
            cues.append(cue)
            return False

        ui = TerminalUI(color=False, fast=True, sound=True, sound_fn=unavailable, output_fn=output.append)
        ui.sound("danger")

        self.assertEqual(cues, ["danger"])
        self.assertEqual(output, ["\a\a"])

    def test_empty_choice_list_is_rejected(self) -> None:
        ui = TerminalUI(color=False, fast=True, output_fn=lambda _: None)

        with self.assertRaises(ValueError):
            ui.choose("Menu", [])


if __name__ == "__main__":
    unittest.main()
