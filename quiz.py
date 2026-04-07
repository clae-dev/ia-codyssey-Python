# quiz.py
# 개별 퀴즈 한 문제를 표현하는 클래스 정의 파일


class Quiz:
    """
    퀴즈 한 문제를 나타내는 클래스.
    문제(question), 선택지(choices), 정답 번호(answer), 힌트(hint)를 속성으로 가진다.
    """

    def __init__(self, question, choices, answer, hint=''):
        """
        Quiz 인스턴스를 초기화한다.

        매개변수:
            question (str): 퀴즈 문제 텍스트
            choices (list): 4개의 선택지 문자열 리스트
            answer (int): 정답 번호 (1~4)
            hint (str): 힌트 텍스트 (선택 사항, 기본값은 빈 문자열)
        """
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self, number):
        """
        퀴즈를 화면에 출력한다.
        번호와 함께 문제와 선택지를 보기 좋게 표시한다.

        매개변수:
            number (int): 문제 번호 (몇 번째 문제인지)
        """
        print(f'\n[문제 {number}]')
        print(f'{self.question}\n')

        # 선택지를 번호와 함께 출력
        for i, choice in enumerate(self.choices, 1):
            print(f'  {i}. {choice}')

        # 힌트가 있으면 힌트 사용 가능 안내
        if self.hint:
            print('  (힌트를 보려면 0을 입력하세요)')
        print()

    def check_answer(self, user_answer):
        """
        사용자의 답이 정답인지 확인한다.

        매개변수:
            user_answer (int): 사용자가 입력한 답 번호

        반환값:
            bool: 정답이면 True, 오답이면 False
        """
        return user_answer == self.answer

    def to_dict(self):
        """
        Quiz 인스턴스를 딕셔너리로 변환한다.
        JSON 파일에 저장할 때 사용한다.

        반환값:
            dict: {"question": ..., "choices": [...], "answer": ...}
        """
        result = {
            'question': self.question,
            'choices': self.choices,
            'answer': self.answer
        }
        # 힌트가 있을 때만 저장 (불필요한 빈 값 방지)
        if self.hint:
            result['hint'] = self.hint
        return result

    @classmethod
    def from_dict(cls, data):
        """
        딕셔너리에서 Quiz 인스턴스를 생성하는 클래스 메서드.
        JSON 파일에서 데이터를 불러올 때 사용한다.

        매개변수:
            data (dict): 퀴즈 데이터가 담긴 딕셔너리

        반환값:
            Quiz: 생성된 Quiz 인스턴스
        """
        return cls(
            question=data['question'],
            choices=data['choices'],
            answer=data['answer'],
            hint=data.get('hint', '')
        )
