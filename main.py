# main.py
# 퀴즈 게임의 진입점(엔트리 포인트)
# 이 파일을 실행하면 퀴즈 게임이 시작된다.

import sys
import io

# Windows 환경에서 이모지 등 유니코드 출력이 깨지는 문제를 방지
# 표준 출력과 표준 입력의 인코딩을 UTF-8로 강제 설정한다
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

from quiz_game import QuizGame


def main():
    """퀴즈 게임을 생성하고 실행한다."""
    game = QuizGame()
    game.run()


# 이 파일이 직접 실행될 때만 main() 호출
# 다른 파일에서 import할 때는 실행되지 않는다
if __name__ == '__main__':
    main()
