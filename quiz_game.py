"""게임 전체 흐름(메뉴, 기능 선택, 종료)을 관리하는 QuizGame 클래스."""

from default_quizzes import create_default_quizzes
from input_helper import read_number, read_text
from quiz import CHOICE_COUNT, Quiz

LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    """퀴즈 게임 전체를 관리한다.

    속성
        quizzes      : Quiz 객체 목록
        best_score   : 최고 점수(0~100). 아직 풀지 않았으면 None
        best_correct : 최고 점수를 냈을 때 맞힌 개수
        best_total   : 최고 점수를 냈을 때 전체 문제 수
    """

    TITLE = "🎯 개발 입문 용어 퀴즈 🎯"
    QUIT_LABEL = "종료"

    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = 0
        self.best_total = 0

        # 메뉴 번호 순서대로 (이름, 실행할 메서드)를 한곳에 모아 둔다.
        # 메뉴를 늘릴 때는 이 목록에 한 줄만 추가하면 된다.
        self.menu_actions = [
            ("퀴즈 풀기", self.play),
            ("퀴즈 추가", self.add_quiz),
            ("퀴즈 목록", self.show_quizzes),
            ("점수 확인", self.show_score),
        ]

    # ---------- 게임 흐름 ----------

    def run(self):
        """메뉴를 반복해서 보여 주고, Ctrl+C·입력 종료(EOF)가 와도 안전하게 끝낸다."""
        try:
            self.menu_loop()
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되어 게임을 종료합니다.")
        print("👋 게임을 종료합니다. 다음에 또 만나요!")

    def menu_loop(self):
        """종료를 고를 때까지 메뉴를 보여 주고 선택한 기능을 실행한다."""
        quit_number = len(self.menu_actions) + 1
        while True:
            self.show_menu()
            choice = read_number("선택: ", 1, quit_number)
            print()

            if choice == quit_number:
                return
            _, action = self.menu_actions[choice - 1]
            action()

    def show_menu(self):
        print()
        print(LINE)
        print(f"        {self.TITLE}")
        print(LINE)
        for number, (label, _) in enumerate(self.menu_actions, start=1):
            print(f"{number}. {label}")
        print(f"{len(self.menu_actions) + 1}. {self.QUIT_LABEL}")
        print(LINE)

    # ---------- 퀴즈 풀기 ----------

    def play(self):
        """저장된 퀴즈를 순서대로 출제하고, 다 풀면 결과를 보여 준다."""
        total = len(self.quizzes)
        if total == 0:
            print("📭 등록된 퀴즈가 없습니다. 먼저 '2. 퀴즈 추가'로 퀴즈를 등록하세요.")
            return

        print(f"📝 퀴즈를 시작합니다! (총 {total}문제)")

        correct_count = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            if self.ask_quiz(number, quiz):
                correct_count += 1

        self.show_result(correct_count, total)

    @staticmethod
    def calculate_score(correct_count, total):
        """맞힌 개수를 100점 만점 점수(정수, 소수점 첫째 자리에서 반올림)로 바꾼다.

        round()는 12.5를 12로 만드는 '짝수 반올림'이라, 0.5를 더하고 버리는 방식을 쓴다.
        """
        return int(correct_count * 100 / total + 0.5)

    def show_result(self, correct_count, total):
        score = self.calculate_score(correct_count, total)
        print()
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        if self.update_best_score(score, correct_count, total):
            print("🎉 새로운 최고 점수입니다!")
        else:
            print(f"현재 최고 점수는 {self.best_score}점입니다.")
        print(LINE)

    def update_best_score(self, score, correct_count, total):
        """이번 점수가 최고 점수보다 높으면 갱신하고 True를 돌려준다."""
        if self.best_score is not None and score <= self.best_score:
            return False

        self.best_score = score
        self.best_correct = correct_count
        self.best_total = total
        return True

    def ask_quiz(self, number, quiz):
        """퀴즈 한 문제를 보여 주고 답을 받아 정답 여부를 알려 준다."""
        print()
        print(THIN_LINE)
        quiz.display(number)
        user_answer = read_number("정답 입력: ", 1, CHOICE_COUNT)

        if quiz.is_correct(user_answer):
            print("✅ 정답입니다!")
            return True

        print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{quiz.correct_choice()}'입니다.")
        return False

    # ---------- 퀴즈 추가·목록 ----------

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 새 퀴즈를 등록한다."""
        print("📌 새로운 퀴즈를 추가합니다.")
        print()
        question = read_text("문제를 입력하세요: ")
        choices = self.read_choices()
        answer = read_number(f"정답 번호 (1-{CHOICE_COUNT}): ", 1, CHOICE_COUNT)

        self.quizzes.append(Quiz(question, choices, answer))
        print()
        print(f"✅ 퀴즈가 추가되었습니다! (현재 {len(self.quizzes)}개)")

    def read_choices(self):
        """서로 다른 선택지 4개를 입력받는다. 이미 입력한 선택지와 같으면 다시 묻는다."""
        choices = []
        while len(choices) < CHOICE_COUNT:
            choice = read_text(f"선택지 {len(choices) + 1}: ")
            if choice in choices:
                print("⚠️ 이미 입력한 선택지입니다. 다른 내용을 입력하세요.")
                continue
            choices.append(choice)
        return choices

    def show_quizzes(self):
        """등록된 퀴즈의 번호와 문제를 보여 준다. (정답은 보여 주지 않는다)"""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. '2. 퀴즈 추가'로 퀴즈를 등록하세요.")
            return

        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print()
        print(THIN_LINE)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print(THIN_LINE)

    # ---------- 점수 ----------

    def show_score(self):
        """최고 점수를 보여 준다. 아직 풀지 않았으면 안내한다."""
        if self.best_score is None:
            print("📭 아직 퀴즈를 푼 기록이 없습니다. '1. 퀴즈 풀기'로 도전해 보세요!")
            return

        print(f"🏆 최고 점수: {self.best_score}점 "
              f"({self.best_total}문제 중 {self.best_correct}문제 정답)")
