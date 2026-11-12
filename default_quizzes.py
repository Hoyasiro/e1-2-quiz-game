"""기본 퀴즈 데이터: 개발 입문 용어(터미널·Docker·Git·Python) 6문제.

state.json이 없거나 손상됐을 때도 이 데이터로 게임을 시작한다.
"""

from quiz import Quiz


def create_default_quizzes():
    """기본 퀴즈 6개를 Quiz 인스턴스 목록으로 새로 만들어 돌려준다."""
    return [
        Quiz(
            "`docker run -p 8080:80 nginx`에서 8080은 무엇인가?",
            ["컨테이너 안 포트", "호스트(내 PC) 포트", "nginx 버전", "컨테이너 ID"],
            2,
        ),
        Quiz(
            "컨테이너를 지우고 새로 만들어도 데이터가 남게 하려면?",
            ["docker restart", "Dockerfile에 RUN 추가", "볼륨(-v 이름:경로) 연결", "이미지 태그 변경"],
            3,
        ),
        Quiz(
            "`chmod 600 hello.txt` 실행 후 `ls -l`에 보이는 권한은?",
            ["rw-------", "rwxr-xr-x", "rw-r--r--", "r--------"],
            1,
        ),
        Quiz(
            "Docker 이미지와 컨테이너의 관계로 옳은 것은?",
            [
                "둘은 같은 것이다",
                "이미지는 실행 중인 프로세스, 컨테이너는 설계도",
                "이미지는 읽기 전용 틀, 컨테이너는 그 틀을 실행한 것",
                "컨테이너를 지우면 이미지도 지워진다",
            ],
            3,
        ),
        Quiz(
            "수정한 파일을 다음 커밋에 넣기 위해 스테이징 영역에 올리는 명령은?",
            ["git commit", "git push", "git pull", "git add"],
            4,
        ),
        Quiz(
            "Python에서 `input()`이 돌려주는 값의 자료형은?",
            ["int", "str", "bool", "입력한 값에 따라 다르다"],
            2,
        ),
    ]
