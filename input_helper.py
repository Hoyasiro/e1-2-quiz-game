"""사용자 입력을 받아 검증하는 함수 모음."""


def read_number(prompt, minimum, maximum):
    """minimum~maximum 범위의 정수를 입력받아 돌려준다.

    앞뒤 공백은 지우고, 빈 입력·숫자가 아닌 입력·범위 밖 숫자는
    안내 메시지를 보여 준 뒤 다시 묻는다.
    """
    while True:
        raw = input(prompt).strip()

        if raw == "":
            print(f"⚠️ 입력이 비어 있습니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
            continue

        try:
            number = int(raw)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
            continue

        if number < minimum or number > maximum:
            print(f"⚠️ 범위를 벗어났습니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
            continue

        return number


def read_text(prompt):
    """비어 있지 않은 문자열을 입력받아 앞뒤 공백을 지우고 돌려준다."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")
