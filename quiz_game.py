"""게임 전체 흐름(메뉴, 기능 선택, 종료)을 관리하는 QuizGame 클래스."""

from default_quizzes import create_default_quizzes
from input_helper import read_number
from quiz import CHOICE_COUNT

LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    MENU_ITEMS = ("퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료")

    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None

    def run(self):
        """메뉴를 반복해서 보여 주고, Ctrl+C·입력 종료(EOF)가 와도 안전하게 끝낸다."""
        try:
            self.menu_loop()
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되어 게임을 종료합니다.")
        print("👋 게임을 종료합니다. 다음에 또 만나요!")

    def menu_loop(self):
        """종료를 고를 때까지 메뉴를 보여 주고 선택한 기능을 실행한다."""
        while True:
            self.show_menu()
            choice = read_number("선택: ", 1, len(self.MENU_ITEMS))
            print()

            if choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quizzes()
            elif choice == 4:
                self.show_score()
            else:
                return

    def show_menu(self):
        print()
        print(LINE)
        print("        🎯 개발 입문 용어 퀴즈 🎯")
        print(LINE)
        for number, item in enumerate(self.MENU_ITEMS, start=1):
            print(f"{number}. {item}")
        print(LINE)

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
        print(LINE)

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

    def add_quiz(self):
        print("🚧 퀴즈 추가는 준비 중입니다.")

    def show_quizzes(self):
        print("🚧 퀴즈 목록은 준비 중입니다.")

    def show_score(self):
        print("🚧 점수 확인은 준비 중입니다.")
