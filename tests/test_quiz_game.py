"""퀴즈 게임 자동 테스트 (표준 라이브러리 unittest만 사용).

실행: python -m unittest discover tests -v   (프로젝트 루트에서)
"""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from input_helper import read_number, read_text  # noqa: E402
from quiz import Quiz  # noqa: E402
from quiz_game import QuizGame  # noqa: E402


def run_quietly(func, *args, inputs=()):
    """input()에 inputs를 차례로 넣고, 출력은 모아서 (반환값, 출력 문자열)로 돌려준다."""
    buffer = io.StringIO()
    with patch("builtins.input", side_effect=list(inputs)), redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


class ReadNumberTest(unittest.TestCase):
    """공통 입력 처리 기준: 공백 제거, 빈 입력, 숫자 아님, 범위 밖."""

    def test_strips_spaces(self):
        result, _ = run_quietly(read_number, "선택: ", 1, 5, inputs=["  3  "])
        self.assertEqual(result, 3)

    def test_retries_until_valid(self):
        # 빈 입력 → 문자 → 소수 → 범위 밖(0, 9, -1) → 정상 값
        inputs = ["", "abc", "1.5", "0", "9", "-1", "4"]
        result, output = run_quietly(read_number, "선택: ", 1, 5, inputs=inputs)
        self.assertEqual(result, 4)
        self.assertIn("입력이 비어 있습니다", output)
        self.assertIn("잘못된 입력입니다", output)
        self.assertEqual(output.count("범위를 벗어났습니다"), 3)

    def test_boundary_values_are_accepted(self):
        self.assertEqual(run_quietly(read_number, "", 1, 4, inputs=["1"])[0], 1)
        self.assertEqual(run_quietly(read_number, "", 1, 4, inputs=["4"])[0], 4)

    def test_read_text_rejects_blank(self):
        result, output = run_quietly(read_text, "문제: ", inputs=["   ", " 질문 "])
        self.assertEqual(result, "질문")
        self.assertIn("입력이 비어 있습니다", output)


class QuizTest(unittest.TestCase):
    def setUp(self):
        self.quiz = Quiz("2+2는?", ["1", "2", "3", "4"], 4)

    def test_is_correct(self):
        self.assertTrue(self.quiz.is_correct(4))
        self.assertFalse(self.quiz.is_correct(1))

    def test_correct_choice(self):
        self.assertEqual(self.quiz.correct_choice(), "4")

    def test_dict_round_trip(self):
        copy = Quiz.from_dict(self.quiz.to_dict())
        self.assertEqual(copy.to_dict(), self.quiz.to_dict())

    def test_invalid_quiz_is_rejected(self):
        with self.assertRaises(ValueError):
            Quiz("문제", ["a", "b", "c"], 1)          # 선택지 3개
        with self.assertRaises(ValueError):
            Quiz("문제", ["a", "b", "c", "d"], 5)     # 정답 범위 밖
        with self.assertRaises(ValueError):
            Quiz.from_dict({"question": "문제", "choices": ["a", "b", "c", "d"], "answer": True})


class StateFileTest(unittest.TestCase):
    """state.json 저장·불러오기와 파일 없음·손상 처리."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.state_file = Path(self.temp_dir.name) / "state.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def new_game(self):
        return QuizGame(state_file=self.state_file)

    def test_first_run_creates_file_with_defaults(self):
        game = self.new_game()
        run_quietly(game.load_state)
        self.assertTrue(self.state_file.exists())
        self.assertEqual(len(game.quizzes), 6)
        self.assertIsNone(game.best_score)

    def test_save_and_load_keep_quiz_and_best_score(self):
        game = self.new_game()
        run_quietly(game.load_state)
        game.quizzes.append(Quiz("한글 문제", ["가", "나", "다", "라"], 2))
        game.update_best_score(86, 6, 7)
        self.assertTrue(run_quietly(game.save_state)[0])

        reloaded = self.new_game()
        _, output = run_quietly(reloaded.load_state)
        self.assertEqual(len(reloaded.quizzes), 7)
        self.assertEqual(reloaded.quizzes[-1].question, "한글 문제")
        self.assertEqual((reloaded.best_score, reloaded.best_correct, reloaded.best_total), (86, 6, 7))
        self.assertIn("최고 점수 86점", output)
        # ensure_ascii=False: 한글이 \uXXXX가 아니라 그대로 저장된다.
        self.assertIn("한글 문제", self.state_file.read_text(encoding="utf-8"))

    def test_broken_json_is_recovered(self):
        self.state_file.write_text("{ 깨진 파일", encoding="utf-8")
        game = self.new_game()
        _, output = run_quietly(game.load_state)
        self.assertIn("손상되어 기본 퀴즈로 복구", output)
        self.assertEqual(len(game.quizzes), 6)
        self.assertTrue(self.state_file.with_name("state.json.broken").exists())
        json.loads(self.state_file.read_text(encoding="utf-8"))  # 새 파일은 올바른 JSON

    def test_wrong_schema_is_recovered(self):
        bad = {"quizzes": [{"question": "q", "choices": ["a", "b", "c", "d"], "answer": 5}],
               "best_score": None}
        self.state_file.write_text(json.dumps(bad), encoding="utf-8")
        game = self.new_game()
        _, output = run_quietly(game.load_state)
        self.assertIn("손상되어", output)
        self.assertEqual(len(game.quizzes), 6)

    def test_minimal_schema_is_accepted(self):
        data = {"quizzes": [{"question": "q", "choices": ["a", "b", "c", "d"], "answer": 1}],
                "best_score": None}
        self.state_file.write_text(json.dumps(data), encoding="utf-8")
        game = self.new_game()
        run_quietly(game.load_state)
        self.assertEqual(len(game.quizzes), 1)

    def test_best_score_updates_only_when_higher(self):
        game = self.new_game()
        self.assertTrue(game.update_best_score(50, 3, 6))
        self.assertFalse(game.update_best_score(50, 3, 6))   # 같은 점수는 갱신 안 함
        self.assertTrue(game.update_best_score(67, 4, 6))
        self.assertEqual(game.best_score, 67)

    def test_score_rounds_half_up(self):
        self.assertEqual(QuizGame.calculate_score(1, 8), 13)   # 12.5 → 13
        self.assertEqual(QuizGame.calculate_score(6, 7), 86)   # 85.7 → 86

    def test_ctrl_c_saves_before_exit(self):
        game = self.new_game()
        _, output = run_quietly(game.run, inputs=[KeyboardInterrupt()])
        self.assertIn("입력이 중단되어", output)
        self.assertIn("데이터를 저장했습니다", output)
        self.assertTrue(self.state_file.exists())

    def test_eof_saves_before_exit(self):
        game = self.new_game()
        _, output = run_quietly(game.run, inputs=[EOFError()])
        self.assertIn("데이터를 저장했습니다", output)


if __name__ == "__main__":
    unittest.main()
