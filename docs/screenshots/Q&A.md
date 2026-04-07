# Python 퀴즈 게임 - 코드 Q&A 정리

이 프로젝트 코드에서 헷갈리기 쉬운 문법과 개념들을 Q&A 형태로 정리한 문서입니다.

---

## 1. 클래스와 객체

### Q: `self`가 뭔데 왜 매번 써야 해?

`self`는 **지금 이 인스턴스(객체) 자기 자신**을 가리키는 변수다.

```python
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question   # 이 객체의 question에 저장
        self.answer = answer       # 이 객체의 answer에 저장
```

`Quiz('문제1', [...], 1)`로 만든 객체와 `Quiz('문제2', [...], 3)`로 만든 객체는 서로 다른 데이터를 갖는다.
`self`가 있어야 "어떤 객체의 데이터인지" 구분할 수 있다.

메서드를 호출할 때 `quiz.display(1)` 이렇게 쓰면 Python이 자동으로 `self` 자리에 `quiz`를 넣어준다.
그래서 정의할 때는 `def display(self, number)`로 쓰지만, 호출할 때는 `quiz.display(1)`로 `self`를 안 쓴다.

---

### Q: `__init__`은 왜 앞뒤로 밑줄이 두 개야?

Python에서 `__이름__` 형태의 메서드는 **특별한 역할을 하는 메서드**다. (매직 메서드 또는 던더 메서드라고 부른다)

- `__init__` : 객체가 생성될 때 **자동으로 호출**되는 초기화 메서드
- 직접 `quiz.__init__(...)` 이렇게 호출하는 게 아니라, `Quiz(...)` 하면 알아서 실행된다

```python
# 이렇게 쓰면
game = QuizGame()

# Python이 내부적으로 이걸 실행한다
# QuizGame.__init__(game)
```

---

### Q: `@classmethod`랑 `cls`는 뭐야?

`quiz.py` 92번째 줄에 있는 코드:

```python
@classmethod
def from_dict(cls, data):
    return cls(
        question=data['question'],
        choices=data['choices'],
        answer=data['answer'],
        hint=data.get('hint', '')
    )
```

- `@classmethod`는 **클래스 자체를 통해 호출하는 메서드**라는 표시다
- `cls`는 `self`와 비슷하지만, 객체가 아니라 **클래스 자체**를 가리킨다
- `cls(...)`는 `Quiz(...)`와 같은 뜻이다

```python
# 이 두 줄은 같은 결과를 만든다
quiz = Quiz(question='...', choices=[...], answer=1)
quiz = Quiz.from_dict({'question': '...', 'choices': [...], 'answer': 1})
```

왜 쓰냐면, JSON에서 읽은 딕셔너리를 바로 Quiz 객체로 변환할 때 편하기 때문이다.

---

## 2. 반복문과 enumerate

### Q: `enumerate(self.choices, 1)`에서 1은 뭐야?

```python
for i, choice in enumerate(self.choices, 1):
    print(f'  {i}. {choice}')
```

`enumerate`는 리스트를 돌면서 **인덱스 번호**를 같이 알려주는 함수다.

- `enumerate(리스트)` → 0부터 시작 (0, 1, 2, 3...)
- `enumerate(리스트, 1)` → **1부터 시작** (1, 2, 3, 4...)

사용자에게 보여줄 때 "0번 선택지"보다 "1번 선택지"가 자연스러우니까 1부터 시작한 것이다.

```python
choices = ['사과', '바나나', '포도', '딸기']

# enumerate 없이 쓰면
for i in range(len(choices)):
    print(f'  {i+1}. {choices[i]}')

# enumerate 쓰면 (같은 결과, 더 깔끔)
for i, choice in enumerate(choices, 1):
    print(f'  {i}. {choice}')
```

---

### Q: `for i in range(1, 5)`에서 왜 5까지 안 가고 4까지야?

```python
for i in range(1, 5):   # i = 1, 2, 3, 4  (5는 포함 안 됨)
```

`range(시작, 끝)`은 **끝 숫자를 포함하지 않는다**. 이게 Python의 규칙이다.

- `range(5)` → 0, 1, 2, 3, 4
- `range(1, 5)` → 1, 2, 3, 4
- `range(0, 10, 2)` → 0, 2, 4, 6, 8 (세 번째 값은 간격)

---

## 3. 문자열 다루기

### Q: `f'문자열 {변수}'`는 뭐야?

**f-string**이라고 부르는 문자열 포매팅 방법이다. 문자열 앞에 `f`를 붙이면 `{}` 안에 변수나 표현식을 직접 넣을 수 있다.

```python
name = '파이썬'
score = 80

# f-string 사용
print(f'{name} 점수는 {score}점입니다.')   # 파이썬 점수는 80점입니다.

# f-string 없이 같은 결과
print(name + ' 점수는 ' + str(score) + '점입니다.')
```

`str(score)`처럼 숫자를 문자열로 변환할 필요가 없어서 훨씬 편하다.

---

### Q: `.strip()`은 왜 쓰는 거야?

```python
raw = input(prompt).strip()
```

사용자가 입력할 때 실수로 앞뒤에 공백을 넣을 수 있다.

```python
' 3 '.strip()    # '3'      (앞뒤 공백 제거)
'  hello '.strip()  # 'hello'
'3'.strip()      # '3'      (공백 없으면 그대로)
```

`.strip()`을 안 쓰면 `' 3'`을 `int()`로 변환할 때 에러가 날 수 있다.

---

## 4. 조건문과 비교

### Q: `if not self.quizzes:`는 뭔 뜻이야?

```python
if not self.quizzes:
    print('등록된 퀴즈가 없습니다.')
```

Python에서 **빈 리스트 `[]`는 False로 취급**된다.

- `self.quizzes = []` → `not []` → `not False` → `True` → "퀴즈 없음"
- `self.quizzes = [quiz1, quiz2]` → `not [quiz1, quiz2]` → `not True` → `False` → 넘어감

이런 식으로 False로 취급되는 값들 (Falsy 값):
- `0`, `0.0` (숫자 0)
- `''` (빈 문자열)
- `[]` (빈 리스트)
- `{}` (빈 딕셔너리)
- `None`
- `False`

---

### Q: `is None`이랑 `== None`은 뭐가 달라?

```python
if self.best_score is None:
```

- `is` : **같은 객체인지** 확인 (메모리 주소가 같은지)
- `==` : **값이 같은지** 확인

`None`은 Python에서 딱 하나만 존재하는 특별한 값이라서, `is None`으로 확인하는 게 관례이자 안전한 방법이다.

```python
a = None
a is None     # True (올바른 방법)
a == None     # True (동작은 하지만 권장하지 않음)
```

---

## 5. 예외 처리 (try/except)

### Q: `try/except`는 왜 필요해?

프로그램 실행 중에 에러가 발생하면 프로그램이 **강제 종료**된다.
`try/except`를 쓰면 에러가 나도 **멈추지 않고 대처**할 수 있다.

```python
try:
    num = int(raw)           # 'abc'를 넣으면 여기서 에러 발생
except ValueError:           # ValueError가 발생하면 여기로 점프
    print('숫자를 입력하세요.')  # 에러 대신 안내 메시지 출력
```

이 프로젝트에서 try/except를 쓰는 상황들:
| 상황 | 발생할 수 있는 에러 |
|------|---------------------|
| `int('abc')` 숫자 변환 실패 | `ValueError` |
| `json.load()` JSON 파싱 실패 | `json.JSONDecodeError` |
| 파일 열기 권한 없음 | `PermissionError` |
| Ctrl+C 누름 | `KeyboardInterrupt` |
| 입력 스트림 종료 | `EOFError` |

---

### Q: `except` 뒤에 에러 이름을 여러 개 쓸 수 있어?

```python
except (KeyboardInterrupt, EOFError):
```

괄호 안에 쉼표로 구분하면 **여러 종류의 에러를 한 번에 처리**할 수 있다.

```python
# 이렇게 따로 쓰는 것과
except KeyboardInterrupt:
    save_data()
except EOFError:
    save_data()

# 이렇게 합쳐서 쓰는 것은 같은 동작이다
except (KeyboardInterrupt, EOFError):
    save_data()
```

---

## 6. 파일 입출력과 JSON

### Q: `with open(...) as f:`에서 `with`는 왜 써?

```python
with open(self.file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
```

`with`를 쓰면 블록이 끝날 때 **파일을 자동으로 닫아준다**.

```python
# with 없이 쓰면 직접 닫아야 한다
f = open('state.json', 'w')
json.dump(data, f)
f.close()          # 이걸 깜빡하면 파일이 손상될 수 있다

# with를 쓰면 자동으로 닫힌다
with open('state.json', 'w') as f:
    json.dump(data, f)
# 여기서 자동으로 f.close() 실행됨
```

---

### Q: `open()`의 `'r'`, `'w'`는 뭐야?

| 모드 | 의미 | 파일 없을 때 |
|------|------|-------------|
| `'r'` | 읽기 (read) | 에러 발생 |
| `'w'` | 쓰기 (write) | 새로 생성 |
| `'a'` | 추가 (append) | 새로 생성 |

`'w'`는 파일 내용을 **완전히 덮어쓴다**. 기존 내용이 사라진다.

---

### Q: `json.dump()`랑 `json.load()`는 뭐가 달라?

| 함수 | 역할 | 방향 |
|------|------|------|
| `json.dump(data, f)` | Python 데이터 → JSON 파일로 저장 | 쓰기 |
| `json.load(f)` | JSON 파일 → Python 데이터로 변환 | 읽기 |

```python
# 저장 (Python dict → JSON 파일)
data = {'name': '파이썬', 'score': 80}
with open('data.json', 'w') as f:
    json.dump(data, f)

# 불러오기 (JSON 파일 → Python dict)
with open('data.json', 'r') as f:
    loaded = json.load(f)
print(loaded['name'])   # '파이썬'
```

---

### Q: `ensure_ascii=False`는 왜 써?

```python
json.dump(data, f, ensure_ascii=False, indent=4)
```

이걸 안 쓰면 한글이 `\uD30C\uC774\uC36C` 이런 식으로 저장된다.
`ensure_ascii=False`를 쓰면 한글이 그대로 `"파이썬"`으로 저장되어서 사람이 읽을 수 있다.

`indent=4`는 JSON을 보기 좋게 들여쓰기 4칸으로 정리해준다.

---

## 7. 리스트 관련

### Q: `list(DEFAULT_QUIZZES)` 이렇게 복사하는 이유는?

```python
self.quizzes = list(DEFAULT_QUIZZES)    # 복사
self.quizzes = DEFAULT_QUIZZES          # 같은 리스트를 가리킴
```

`list()`로 감싸면 **새로운 리스트를 만든다** (얕은 복사).
안 그러면 `self.quizzes`에서 퀴즈를 추가/삭제하면 `DEFAULT_QUIZZES`까지 같이 바뀌어버린다.

```python
a = [1, 2, 3]
b = a            # b와 a는 같은 리스트를 가리킴
b.append(4)
print(a)         # [1, 2, 3, 4]  ← a도 바뀜!

a = [1, 2, 3]
b = list(a)      # b는 새로운 복사본
b.append(4)
print(a)         # [1, 2, 3]     ← a는 안 바뀜
```

---

### Q: `.pop(num - 1)`에서 왜 -1을 해?

```python
removed = self.quizzes.pop(num - 1)
```

리스트의 인덱스는 **0부터 시작**하지만, 사용자에게는 **1부터** 보여주기 때문이다.

```python
quizzes = ['문제A', '문제B', '문제C']
# 인덱스:    0        1        2
# 사용자:    1번      2번      3번

# 사용자가 "2번 삭제"를 선택하면
quizzes.pop(2 - 1)   # quizzes.pop(1) → '문제B' 삭제
```

---

### Q: `[quiz.to_dict() for quiz in self.quizzes]`는 뭐야?

**리스트 컴프리헨션**이라고 부르는 문법이다. 리스트를 한 줄로 만들 수 있다.

```python
# 리스트 컴프리헨션
result = [quiz.to_dict() for quiz in self.quizzes]

# 위 코드는 아래와 같다
result = []
for quiz in self.quizzes:
    result.append(quiz.to_dict())
```

각 Quiz 객체를 딕셔너리로 변환해서 새 리스트를 만드는 것이다.

---

## 8. 딕셔너리 관련

### Q: `data.get('hint', '')`이랑 `data['hint']`는 뭐가 달라?

```python
# data = {'question': '...', 'answer': 1}  (hint 키가 없는 상황)

data['hint']           # KeyError 발생! 프로그램 멈춤
data.get('hint', '')   # '' 반환 (에러 없음)
```

- `dict['키']` : 키가 없으면 **에러**
- `dict.get('키', 기본값)` : 키가 없으면 **기본값 반환**

힌트가 없는 퀴즈도 있을 수 있으니까 `.get()`을 쓴 것이다.

---

## 9. import와 모듈

### Q: `if __name__ == '__main__':` 이게 뭐야?

```python
if __name__ == '__main__':
    main()
```

이 파일을 **직접 실행했을 때만** `main()`을 호출하라는 뜻이다.

- `python main.py`로 실행 → `__name__`이 `'__main__'` → main() 실행됨
- 다른 파일에서 `import main` → `__name__`이 `'main'` → main() 실행 안 됨

이걸 안 쓰면 다른 파일에서 import만 해도 프로그램이 실행돼버린다.

---

### Q: `from quiz import Quiz`랑 `import quiz`는 뭐가 달라?

```python
# 방법 1: 모듈에서 특정 클래스만 가져오기
from quiz import Quiz
q = Quiz(...)               # 바로 사용 가능

# 방법 2: 모듈 전체 가져오기
import quiz
q = quiz.Quiz(...)          # 모듈명.클래스명으로 사용
```

방법 1이 더 짧게 쓸 수 있어서 이 프로젝트에서는 `from quiz import Quiz`를 사용했다.

---

## 10. 기타 헷갈리는 것들

### Q: `while True:`는 무한 루프 아냐? 안 멈춰?

맞다. `while True`는 무한 반복이다. 하지만 **루프 안에서 빠져나가는 조건**이 있다.

```python
while True:
    self.show_menu()
    choice = get_valid_input('선택: ', 1, 6)
    
    if choice == 6:
        break          # 여기서 루프 탈출!
```

- `break` : 반복문을 **즉시 종료**
- `continue` : 이번 반복을 **건너뛰고** 다음 반복으로

---

### Q: `random.shuffle(shuffled)`은 뭘 반환해?

```python
shuffled = list(self.quizzes)
random.shuffle(shuffled)      # 반환값 없음! (None)
```

주의: `shuffle()`은 **원본 리스트를 직접 섞는다**. 새로운 리스트를 반환하는 게 아니다.

```python
a = [1, 2, 3, 4, 5]
result = random.shuffle(a)
print(result)    # None (반환값 없음!)
print(a)         # [3, 1, 5, 2, 4] (원본이 바뀜)
```

그래서 원본을 보존하려면 먼저 `list()`로 복사한 뒤에 섞는 것이다.

---

### Q: `max(0, raw_score - hint_penalty)` 이건 뭐야?

```python
score = max(0, raw_score - hint_penalty)
```

`max()`는 **더 큰 값**을 반환하는 함수다.

힌트를 많이 써서 감점이 원래 점수보다 커지면 음수가 되는데, 점수가 마이너스가 되면 이상하니까 **최소 0점**을 보장하는 것이다.

```python
max(0, 80 - 10)    # max(0, 70)  → 70
max(0, 20 - 30)    # max(0, -10) → 0   (음수 방지)
```

---

### Q: `datetime.now().strftime('%Y-%m-%d %H:%M:%S')`는 뭐야?

현재 날짜와 시간을 **원하는 형식의 문자열**로 바꿔주는 코드다.

```python
from datetime import datetime

now = datetime.now()                              # 현재 시각 객체
text = now.strftime('%Y-%m-%d %H:%M:%S')          # '2026-04-07 14:30:00'
```

| 코드 | 의미 | 예시 |
|------|------|------|
| `%Y` | 연도 (4자리) | 2026 |
| `%m` | 월 (2자리) | 04 |
| `%d` | 일 (2자리) | 07 |
| `%H` | 시 (24시간) | 14 |
| `%M` | 분 | 30 |
| `%S` | 초 | 00 |
