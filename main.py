# main.py
# 퀴즈 게임의 진입점(엔트리 포인트)
# 이 파일을 실행하면 퀴즈 게임이 시작된다.

from quiz_game import QuizGame


def main():
    """퀴즈 게임을 생성하고 실행한다."""
    game = QuizGame()
    game.run()


# 이 파일이 직접 실행될 때만 main() 호출
# 다른 파일에서 import할 때는 실행되지 않는다
if __name__ == '__main__':
    main()
