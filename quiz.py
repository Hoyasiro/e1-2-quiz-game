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

    def to_dict(self):
        """JSON으로 저장할 수 있도록 dict로 바꾼다."""
        return {
            "question": self.question,
            "choices": list(self.choices),
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """state.json에서 읽은 dict 하나를 Quiz로 만든다. 형식이 틀리면 ValueError."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 항목이 객체(dict) 형식이 아닙니다.")

        question = data.get("question")
        choices = data.get("choices")
        answer = data.get("answer")

        if not isinstance(question, str) or not question.strip():
            raise ValueError("question이 비어 있거나 문자열이 아닙니다.")
        if not isinstance(choices, list) or not all(
            isinstance(choice, str) and choice.strip() for choice in choices
        ):
            raise ValueError("choices가 문자열 목록이 아닙니다.")
        # bool도 int의 한 종류(True == 1)라서 type()으로 정확히 int인지 확인한다.
        if type(answer) is not int:
            raise ValueError("answer가 정수가 아닙니다.")

        return cls(question, choices, answer)  # 개수·범위 검사는 __init__이 한다.
