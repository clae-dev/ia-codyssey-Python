# quiz_game.py
# 퀴즈 게임 전체 흐름을 관리하는 QuizGame 클래스 정의 파일

import json
import os
import random
import shutil
from datetime import datetime

from quiz import Quiz


# 기본 퀴즈 데이터 (파일이 없을 때 사용)
# 주제: Python 프로그래밍 기초
DEFAULT_QUIZZES = [
    Quiz(
        question='Python에서 변수에 값을 저장할 때 사용하는 기호는?',
        choices=['==', '=', ':=', '->'],
        answer=2
    ),
    Quiz(
        question='다음 중 Python의 기본 자료형이 아닌 것은?',
        choices=['int', 'str', 'array', 'bool'],
        answer=3
    ),
    Quiz(
        question='Python에서 리스트의 길이를 구하는 함수는?',
        choices=['size()', 'count()', 'len()', 'length()'],
        answer=3
    ),
    Quiz(
        question='Python에서 여러 줄 주석을 작성할 때 주로 사용하는 것은?',
        choices=['/* */', '<!-- -->', "''' '''", '// //'],
        answer=3
    ),
    Quiz(
        question='Python에서 "Hello"의 자료형은?',
        choices=['int', 'float', 'str', 'char'],
        answer=3
    ),
]


def get_valid_input(prompt, min_val, max_val):
    """
    숫자 입력을 받아서 유효성을 검사한 뒤 정수로 반환하는 함수.
    공백 제거, 빈 입력, 숫자 변환 실패, 범위 초과 등을 모두 처리한다.
    유효한 값이 입력될 때까지 반복해서 재입력을 요청한다.

    매개변수:
        prompt (str): 입력 안내 메시지
        min_val (int): 허용 최솟값
        max_val (int): 허용 최댓값

    반환값:
        int: 유효한 범위 내의 정수
    """
    while True:
        raw = input(prompt).strip()  # 앞뒤 공백 제거

        # 빈 입력 처리
        if not raw:
            print(f'  ⚠️ 입력이 없습니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.')
            continue

        # 숫자 변환 시도
        try:
            num = int(raw)
        except ValueError:
            print(f'  ⚠️ 잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.')
            continue

        # 범위 확인
        if num < min_val or num > max_val:
            print(f'  ⚠️ 잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.')
            continue

        return num


class QuizGame:
    """
    퀴즈 게임 전체를 관리하는 클래스.
    퀴즈 목록 관리, 게임 진행, 점수 기록, 파일 저장/불러오기 등
    모든 게임 기능을 메서드로 제공한다.
    """

    def __init__(self):
        """
        QuizGame 인스턴스를 초기화한다.
        퀴즈 목록과 최고 점수를 설정하고, 저장 파일에서 데이터를 불러온다.
        """
        self.quizzes = []           # Quiz 인스턴스 목록
        self.best_score = None      # 최고 점수 (None이면 아직 플레이 안 한 상태)
        self.history = []           # 점수 기록 히스토리 (날짜, 문제 수, 점수)
        self.file_path = 'state.json'  # 데이터 저장 파일 경로

        # 프로그램 시작 시 저장된 데이터 불러오기
        self.load_data()

    def show_menu(self):
        """메인 메뉴를 화면에 출력한다."""
        print('\n========================================')
        print('        🎯 나만의 퀴즈 게임 🎯')
        print('========================================')
        print('  1. 퀴즈 풀기')
        print('  2. 퀴즈 추가')
        print('  3. 퀴즈 삭제')
        print('  4. 퀴즈 목록')
        print('  5. 점수 확인')
        print('  6. 종료')
        print('========================================')

    def play_quiz(self):
        """
        퀴즈 풀기 기능.
        등록된 모든 퀴즈를 순서대로 출제하고,
        사용자의 답을 받아 정답/오답을 판정한다.
        모든 문제를 풀면 결과를 표시하고, 최고 점수를 갱신한다.
        """
        # 퀴즈가 없으면 안내 후 복귀
        if not self.quizzes:
            print('\n  📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.')
            return

        # 퀴즈 목록을 복사한 뒤 랜덤으로 섞기 (원본은 유지)
        shuffled = list(self.quizzes)
        random.shuffle(shuffled)

        total = len(shuffled)
        correct_count = 0  # 맞힌 문제 수

        print(f'\n📝 퀴즈를 시작합니다! (총 {total}문제)')
        print('----------------------------------------')

        # 랜덤으로 섞인 순서로 출제
        for i, quiz in enumerate(shuffled, 1):
            quiz.display(i)

            # 정답 입력 받기 (1~4 범위)
            answer = get_valid_input('  정답 입력: ', 1, 4)

            # 정답 확인 후 결과 표시
            if quiz.check_answer(answer):
                print('  ✅ 정답입니다!')
                correct_count += 1
            else:
                print(f'  ❌ 오답입니다. 정답은 {quiz.answer}번입니다.')

            print('----------------------------------------')

        # 점수 계산 (100점 만점 기준)
        score = int((correct_count / total) * 100)

        # 히스토리에 기록 추가 (날짜/시간, 문제 수, 정답 수, 점수)
        record = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total': total,
            'correct': correct_count,
            'score': score
        }
        self.history.append(record)

        print('\n========================================')
        print(f'  🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)')

        # 최고 점수 갱신 여부 확인
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print('  🎉 새로운 최고 점수입니다!')

        # 점수와 히스토리 저장
        self.save_data()
        print('========================================')

    def add_quiz(self):
        """
        새로운 퀴즈를 추가하는 기능.
        문제, 선택지 4개, 정답 번호를 입력받아
        Quiz 인스턴스를 생성하고 목록에 추가한다.
        """
        print('\n📌 새로운 퀴즈를 추가합니다.\n')

        # 문제 입력 (빈 입력 방지)
        while True:
            question = input('  문제를 입력하세요: ').strip()
            if question:
                break
            print('  ⚠️ 문제를 입력해주세요.')

        # 선택지 4개 입력 (빈 입력 방지)
        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f'  선택지 {i}: ').strip()
                if choice:
                    choices.append(choice)
                    break
                print('  ⚠️ 선택지를 입력해주세요.')

        # 정답 번호 입력 (1~4)
        answer = get_valid_input('  정답 번호 (1-4): ', 1, 4)

        # 새 퀴즈 생성 후 목록에 추가
        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)

        # 추가 즉시 파일에 저장
        self.save_data()

        print('\n  ✅ 퀴즈가 추가되었습니다!')

    def show_quiz_list(self):
        """
        등록된 퀴즈 목록을 출력하는 기능.
        각 퀴즈의 번호와 문제 텍스트를 간략하게 보여준다.
        """
        if not self.quizzes:
            print('\n  📭 등록된 퀴즈가 없습니다.')
            return

        total = len(self.quizzes)
        print(f'\n📋 등록된 퀴즈 목록 (총 {total}개)')
        print('----------------------------------------')

        for i, quiz in enumerate(self.quizzes, 1):
            print(f'  [{i}] {quiz.question}')

        print('----------------------------------------')

    def delete_quiz(self):
        """
        등록된 퀴즈를 삭제하는 기능.
        퀴즈 목록을 보여준 뒤 삭제할 번호를 입력받아 해당 퀴즈를 제거한다.
        """
        # 퀴즈가 없으면 안내 후 복귀
        if not self.quizzes:
            print('\n  📭 삭제할 퀴즈가 없습니다.')
            return

        # 현재 퀴즈 목록 표시
        self.show_quiz_list()

        # 삭제할 번호 입력
        total = len(self.quizzes)
        num = get_valid_input(f'\n  삭제할 퀴즈 번호 (1-{total}, 0: 취소): ', 0, total)

        # 0 입력 시 취소
        if num == 0:
            print('  ↩️ 삭제를 취소했습니다.')
            return

        # 해당 퀴즈 삭제 (인덱스는 0부터이므로 -1)
        removed = self.quizzes.pop(num - 1)
        self.save_data()
        print(f'\n  🗑️ [{num}] "{removed.question}" 퀴즈가 삭제되었습니다.')

    def show_score(self):
        """
        최고 점수를 확인하는 기능.
        아직 퀴즈를 풀지 않았으면 안내 메시지를 출력한다.
        """
        if self.best_score is None:
            print('\n  📊 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어보세요!')
            return

        print(f'\n  🏆 최고 점수: {self.best_score}점')

        # 히스토리가 있으면 최근 기록 표시
        if self.history:
            print(f'\n  📜 게임 기록 (총 {len(self.history)}회)')
            print('  ----------------------------------------')
            # 최근 기록부터 보여주기 (역순)
            for record in reversed(self.history):
                date = record['date']
                total = record['total']
                correct = record['correct']
                score = record['score']
                print(f'  {date} | {total}문제 중 {correct}정답 | {score}점')
            print('  ----------------------------------------')

    def save_data(self):
        """
        퀴즈 데이터와 최고 점수를 state.json 파일에 저장한다.
        JSON 형식으로 저장하며, 한글이 깨지지 않도록 ensure_ascii=False를 사용한다.
        """
        # 저장할 데이터 구조 생성
        data = {
            'quizzes': [quiz.to_dict() for quiz in self.quizzes],
            'best_score': self.best_score,
            'history': self.history
        }

        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except (PermissionError, OSError) as e:
            print(f'\n  ⚠️ 데이터 저장 중 오류가 발생했습니다: {e}')

    def load_data(self):
        """
        state.json 파일에서 퀴즈 데이터와 최고 점수를 불러온다.

        - 파일이 없으면 기본 퀴즈 데이터를 사용한다.
        - 파일이 손상되었으면 백업 후 기본 데이터로 복구한다.
        - 정상적으로 불러오면 저장된 퀴즈 수와 최고 점수를 안내한다.
        """
        # 파일이 존재하지 않는 경우 (첫 실행)
        if not os.path.exists(self.file_path):
            print('\n  📂 저장된 데이터가 없습니다. 기본 퀴즈를 불러옵니다.')
            self.quizzes = list(DEFAULT_QUIZZES)  # 기본 퀴즈 복사해서 사용
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # JSON에서 Quiz 인스턴스 목록과 히스토리 복원
            self.quizzes = [Quiz.from_dict(q) for q in data.get('quizzes', [])]
            self.best_score = data.get('best_score', None)
            self.history = data.get('history', [])

            # 불러온 데이터 정보 표시
            quiz_count = len(self.quizzes)
            if self.best_score is not None:
                print(f'\n  📂 저장된 데이터를 불러왔습니다. (퀴즈 {quiz_count}개, 최고점수 {self.best_score}점)')
            else:
                print(f'\n  📂 저장된 데이터를 불러왔습니다. (퀴즈 {quiz_count}개)')

        except json.JSONDecodeError:
            # JSON 파싱 실패 → 파일 손상
            # 손상된 파일을 백업해두고 기본 데이터로 복구
            backup_path = self.file_path + '.bak'
            shutil.copy2(self.file_path, backup_path)
            print(f'\n  ⚠️ 데이터 파일이 손상되었습니다. 백업({backup_path})을 생성하고 기본 퀴즈로 초기화합니다.')
            self.quizzes = list(DEFAULT_QUIZZES)

        except (PermissionError, OSError) as e:
            # 파일 읽기 실패
            print(f'\n  ⚠️ 데이터 파일을 읽을 수 없습니다: {e}')
            print('  기본 퀴즈를 불러옵니다.')
            self.quizzes = list(DEFAULT_QUIZZES)

    def run(self):
        """
        게임의 메인 루프.
        메뉴를 표시하고 사용자의 선택에 따라 기능을 실행한다.
        Ctrl+C(KeyboardInterrupt)나 EOF(EOFError) 발생 시
        데이터를 저장하고 안전하게 종료한다.
        """
        try:
            while True:
                self.show_menu()
                choice = get_valid_input('  선택: ', 1, 6)

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.delete_quiz()
                elif choice == 4:
                    self.show_quiz_list()
                elif choice == 5:
                    self.show_score()
                elif choice == 6:
                    # 정상 종료: 데이터 저장 후 종료 메시지
                    self.save_data()
                    print('\n  👋 퀴즈 게임을 종료합니다. 다음에 또 만나요!')
                    break

        except (KeyboardInterrupt, EOFError):
            # Ctrl+C 또는 입력 스트림 종료 시 안전 종료
            print('\n\n  ⚠️ 프로그램이 중단되었습니다. 데이터를 저장합니다...')
            self.save_data()
            print('  👋 안전하게 종료되었습니다.')
