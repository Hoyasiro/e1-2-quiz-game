"""퀴즈 한 문제를 표현하는 Quiz 클래스."""

CHOICE_COUNT = 4


class Quiz:
    """문제(question), 선택지 4개(choices), 정답 번호(answer, 1~4)를 가진 퀴즈 한 문제."""

    def __init__(self, question, choices, answer):
        if len(choices) != CHOICE_COUNT:
            raise ValueError(f"선택지는 {CHOICE_COUNT}개여야 합니다. (받은 개수: {len(choices)})")
        if not 1 <= answer <= CHOICE_COUNT:
            raise ValueError(f"정답 번호는 1-{CHOICE_COUNT} 사이여야 합니다. (받은 값: {answer})")

        self.question = question
        self.choices = list(choices)
        self.answer = answer

    def display(self, number):
        """문제 번호, 문제, 번호를 붙인 선택지를 출력한다."""
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답이면 True를 돌려준다."""
        return user_answer == self.answer

    def correct_choice(self):
        """정답 선택지의 내용을 돌려준다. (오답일 때 정답을 알려 주는 용도)"""
        return self.choices[self.answer - 1]
