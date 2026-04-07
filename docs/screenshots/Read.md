# Git과 함께하는 Python 첫 발자국
## 설계 자료 (Design Document)

| 항목 | 내용 |
|------|------|
| 학습단계 | 입학 연수 |
| 학습주제 | 개발 입문 (Beginner's Course) |
| 미션 | Git과 함께하는 Python 첫 발자국 |
| 작성자 | 조창래 |
| 작성일 | 2026.04.08 |
| GitHub | https://github.com/clae-dev/ia-codyssey-Python |

---

## 1. 프로젝트 개요

본 프로젝트는 Python 기본 문법과 Git 버전 관리를 활용하여 터미널에서 동작하는 콘솔 퀴즈 게임을 처음부터 끝까지 구현하는 것을 목표로 하였습니다. Python의 클래스(객체 지향)로 코드를 역할별로 구조화하고, JSON 파일 저장을 통해 프로그램을 종료해도 퀴즈와 점수가 유지되도록 "데이터 영속성"을 구현하였습니다.

이번 실습의 핵심 목표는 단순히 문법을 아는 것이 아니라, "그 문법으로 하나의 프로그램을 완성하는 것"을 직접 경험하는 것이었습니다. 클래스의 책임 분리, 데이터 영속성, 예외 처리라는 세 가지 개념을 중심으로 프로그램을 설계하였습니다.

---

## 2. 실행 환경

| 항목 | 내용 |
|------|------|
| OS | Windows 11 |
| Shell / Terminal | CMD / PowerShell |
| Python | 3.14.3 |
| Git | 2.x |
| Editor | VSCode |
| 언어 | Python |
| 외부 라이브러리 | 없음 (표준 라이브러리만 사용) |

---

## 3. 프로젝트 디렉토리 구조

디렉토리 구조는 역할에 따라 명확히 분리하는 기준으로 구성하였습니다.

```
ia-codyssey-Python/
├── main.py              # 프로그램 진입점 (실행 파일)
├── quiz.py              # Quiz 클래스 정의
├── quiz_game.py         # QuizGame 클래스 정의
├── state.json           # 데이터 저장 파일 (자동 생성)
├── .gitignore           # Git 추적 제외 파일 목록
├── README.md            # 프로젝트 설명 문서
├── QnA.md               # 코드 Q&A 학습 정리
└── docs/
    └── screenshots/     # 실행 화면 스크린샷
```

| 경로/파일 | 구성 기준 및 이유 |
|----------|----------------|
| main.py | 프로그램의 시작점. `python main.py`로 바로 실행할 수 있도록 루트에 배치 |
| quiz.py | 개별 퀴즈 데이터와 동작을 담당하는 Quiz 클래스를 분리. 단일 책임 원칙 적용 |
| quiz_game.py | 게임 전체 흐름을 관리하는 QuizGame 클래스를 분리. 메뉴/진행/저장 로직 담당 |
| state.json | 퀴즈 데이터와 점수를 저장하는 파일. .gitignore에 등록하여 개인 데이터 보호 |
| docs/screenshots/ | 스크린샷을 별도 분리. 소스 파일과 문서 자산을 구분 |

---

## 4. 수행 항목

### 4-1. 필수 항목

- Git 저장소 설정 (.gitignore, README.md 생성, 첫 commit/push)
- Quiz 클래스 정의 (문제, 선택지, 정답, JSON 변환 메서드)
- 기본 퀴즈 데이터 5개 작성 (주제: Python 프로그래밍 기초)
- 메뉴 기능 구현 (번호 선택, 잘못된 입력 처리, 종료)
- 퀴즈 풀기 기능 (출제, 정답/오답 판정, 결과 표시)
- 퀴즈 추가 기능 (문제, 선택지 4개, 정답 번호 입력)
- 퀴즈 목록 보기 기능
- 점수 확인 기능 (최고 점수 갱신)
- state.json 파일 저장/불러오기 (UTF-8, JSON)
- 공통 입력 검증 (공백/빈입력/문자/범위 처리)
- Ctrl+C / EOF 안전 종료 처리
- 데이터 파일 손상 시 기본 데이터 복구
- feature 브랜치 생성 및 병합 (feature/play-quiz)
- 10개 이상 의미 있는 커밋

### 4-2. 보너스 항목

- 랜덤 출제 (random.shuffle 사용)
- 힌트 기능 (힌트 사용 시 10점 감점)
- 퀴즈 삭제 기능
- 점수 기록 히스토리 (날짜/시간, 문제 수, 점수 기록)

---

## 5. 클래스 설계 — Quiz와 QuizGame의 책임 분리

클래스를 나눈 핵심 기준은 **"무엇을 알고 있는가"**입니다. Quiz는 퀴즈 한 문제의 데이터와 동작을 알고 있고, QuizGame은 게임 전체의 흐름과 상태를 알고 있습니다.

### Quiz 클래스 (quiz.py)

**역할**: 퀴즈 한 문제의 데이터를 보관하고, 출력/정답 확인/JSON 변환을 담당

```python
class Quiz:
    def __init__(self, question, choices, answer, hint=''):
        self.question = question   # 문제 텍스트
        self.choices = choices     # 선택지 4개 (리스트)
        self.answer = answer       # 정답 번호 (1~4)
        self.hint = hint           # 힌트 (선택)
```

| 메서드 | 역할 | 선택 이유 |
|--------|------|---------|
| `display(number)` | 문제와 선택지를 화면에 출력 | 출력 형식을 Quiz 내부에서 관리하여 일관성 확보 |
| `check_answer(user_answer)` | 정답 여부 판정 (True/False 반환) | 정답 비교 로직을 한 곳에서 관리 |
| `to_dict()` | Quiz → 딕셔너리 변환 | JSON 저장 시 직렬화에 사용 |
| `from_dict(data)` | 딕셔너리 → Quiz 생성 (@classmethod) | JSON 로드 시 역직렬화에 사용 |

### QuizGame 클래스 (quiz_game.py)

**역할**: 게임 전체 흐름(메뉴, 진행, 저장)을 관리

```python
class QuizGame:
    def __init__(self):
        self.quizzes = []          # Quiz 인스턴스 목록
        self.best_score = None     # 최고 점수 (None = 미플레이)
        self.history = []          # 점수 기록 히스토리
        self.file_path = 'state.json'
```

| 메서드 | 역할 | 분류 |
|--------|------|------|
| `show_menu()` | 메뉴 화면 출력 | 화면 표시 |
| `play_quiz()` | 퀴즈 풀기 진행 | 게임 진행 |
| `add_quiz()` | 새 퀴즈 등록 | 데이터 관리 |
| `delete_quiz()` | 퀴즈 삭제 | 데이터 관리 |
| `show_quiz_list()` | 퀴즈 목록 출력 | 화면 표시 |
| `show_score()` | 최고 점수/히스토리 표시 | 화면 표시 |
| `save_data()` | state.json에 저장 | 파일 입출력 |
| `load_data()` | state.json에서 불러오기 | 파일 입출력 |
| `run()` | 메인 루프 (메뉴→분기→반복) | 게임 흐름 |

### 왜 클래스를 사용했는가 (함수만 쓰는 것과의 차이)

| 비교 항목 | 함수만 사용 | 클래스 사용 |
|----------|-----------|-----------|
| 데이터 전달 | question, choices, answer를 매번 따로 전달 | self.question으로 객체 내부에서 접근 |
| 상태 관리 | 전역 변수 또는 매개변수로 계속 넘겨야 함 | self.quizzes, self.best_score로 상태 유지 |
| 코드 구조 | 기능이 늘수록 함수 간 의존성이 복잡해짐 | 관련 데이터와 기능이 하나의 클래스에 묶여 관리 용이 |
| 확장성 | 힌트 추가 시 모든 함수에 매개변수 추가 필요 | Quiz에 hint 속성만 추가하면 됨 |

---

## 6. 데이터 영속성 설계 — state.json

프로그램을 종료해도 퀴즈와 점수가 유지되어야 합니다. 이를 위해 JSON 파일 저장 방식을 선택하였습니다.

### JSON을 선택한 이유

| 비교 항목 | JSON | 텍스트 파일 (CSV 등) | 데이터베이스 (SQLite) |
|----------|------|-------------------|-------------------|
| 사람이 읽을 수 있는가 | O | O | X (바이너리) |
| 중첩 구조 표현 | O (리스트, 딕셔너리) | X (행/열만 가능) | O (테이블 관계) |
| Python 변환 | json.load()로 바로 dict/list | 파싱 코드 직접 작성 필요 | SQL 쿼리 필요 |
| 외부 설치 | 불필요 (표준 라이브러리) | 불필요 | 불필요 (sqlite3 표준) |
| 적합한 규모 | 소규모 데이터 | 단순 테이블 | 대규모/복잡한 관계 |

현재 퀴즈 수가 수십 개 수준이므로 JSON이 가장 적합합니다.

### state.json 스키마

```json
{
    "quizzes": [
        {
            "question": "Python에서 변수에 값을 저장할 때 사용하는 기호는?",
            "choices": ["==", "=", ":=", "->"],
            "answer": 2,
            "hint": "비교 연산자(==)와 헷갈리지 않도록 주의하세요."
        }
    ],
    "best_score": 80,
    "history": [
        {
            "date": "2026-04-08 14:30:00",
            "total": 5,
            "correct": 4,
            "score": 80
        }
    ]
}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `quizzes` | 배열 | Quiz 객체를 딕셔너리로 변환한 목록 |
| `best_score` | 정수 / null | 최고 점수. null이면 아직 플레이하지 않은 상태 |
| `history` | 배열 | 게임 기록 (날짜, 문제 수, 정답 수, 점수) |

### state.json 읽기/쓰기 흐름

```
프로그램 시작
  └→ load_data() : state.json 읽기
       ├→ 파일 없음 → 기본 퀴즈 5개로 초기화
       ├→ 파일 손상 → .bak 백업 생성 → 기본 퀴즈로 복구
       └→ 정상 → Quiz 인스턴스 목록 복원

게임 진행 중
  ├→ 퀴즈 추가 후 → save_data()
  ├→ 퀴즈 삭제 후 → save_data()
  └→ 퀴즈 풀기 완료 후 → save_data()

프로그램 종료
  ├→ 정상 종료 (메뉴 6번) → save_data() → 종료
  └→ Ctrl+C / EOF → save_data() → 안전 종료
```

---

## 7. 입력 검증 설계 — get_valid_input()

숫자 입력이 필요한 모든 곳에서 동일한 검증 로직이 반복되므로, 공통 헬퍼 함수로 분리하였습니다.

```python
def get_valid_input(prompt, min_val, max_val):
    while True:
        raw = input(prompt).strip()     # 1. 앞뒤 공백 제거
        if not raw:                      # 2. 빈 입력 처리
            print(f'입력이 없습니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.')
            continue
        try:
            num = int(raw)               # 3. 숫자 변환 시도
        except ValueError:               # 4. 변환 실패 (문자 입력)
            print(f'잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.')
            continue
        if num < min_val or num > max_val:  # 5. 범위 확인
            print(f'잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.')
            continue
        return num                       # 6. 유효한 값 반환
```

| 처리 케이스 | 사용자 입력 예시 | 동작 |
|------------|----------------|------|
| 앞뒤 공백 | `" 3 "` | strip()으로 제거 후 정상 처리 |
| 빈 입력 (Enter만) | `""` | 안내 메시지 → 재입력 |
| 숫자 아닌 문자 | `"abc"` | ValueError 처리 → 재입력 |
| 범위 밖 숫자 | `"9"` (메뉴 범위 1-6) | 안내 메시지 → 재입력 |

### 이 함수를 사용하는 곳

| 호출 위치 | min_val | max_val | 용도 |
|----------|---------|---------|------|
| `run()` 메인 루프 | 1 | 6 | 메뉴 선택 |
| `play_quiz()` | 0 또는 1 | 4 | 정답 입력 (0: 힌트) |
| `delete_quiz()` | 0 | 퀴즈 수 | 삭제 번호 (0: 취소) |
| `add_quiz()` | 1 | 4 | 정답 번호 입력 |

---

## 8. 예외 처리 설계 — 안전 종료와 파일 오류 대응

### Ctrl+C / EOF 안전 종료

```python
def run(self):
    try:
        while True:
            self.show_menu()
            choice = get_valid_input('선택: ', 1, 6)
            # ... 기능 분기 ...
    except (KeyboardInterrupt, EOFError):
        print('프로그램이 중단되었습니다. 데이터를 저장합니다...')
        self.save_data()
        print('안전하게 종료되었습니다.')
```

run() 메서드의 메인 루프 전체를 try/except로 감싸서, 어느 시점에서 Ctrl+C가 발생하더라도 save_data()가 호출되도록 하였습니다.

### 파일 오류 처리 (load_data)

| 상황 | 발생 에러 | 대응 |
|------|---------|------|
| 파일이 없음 (첫 실행) | `os.path.exists()` False | 기본 퀴즈 5개로 초기화 |
| JSON 파싱 실패 (파일 손상) | `json.JSONDecodeError` | 손상 파일을 .bak으로 백업 → 기본 데이터로 복구 |
| 파일 읽기 권한 없음 | `PermissionError` | 안내 메시지 → 기본 데이터로 초기화 |

---

## 9. Git 워크플로우 설계

### 커밋 전략

기능 단위로 커밋하여, 각 커밋이 하나의 완결된 변경을 나타내도록 하였습니다.

| # | 커밋 메시지 | 브랜치 | 변경 내용 |
|---|-----------|--------|---------|
| 1 | `Init: 프로젝트 초기 설정` | main | .gitignore, README.md 생성 |
| 2 | `Feat: Quiz 클래스 정의` | main | quiz.py 작성 |
| 3 | `Feat: Python 기초 주제 기본 퀴즈 5개 추가` | main | quiz_game.py에 기본 데이터 정의 |
| 4 | `Feat: 메뉴 화면 및 메인 루프 구현` | main | main.py, QuizGame.run() 구현 |
| 5 | `Feat: 퀴즈 풀기 기능에 랜덤 출제 추가` | feature/play-quiz | play_quiz() 메서드 구현 |
| 6 | `Merge: feature/play-quiz 브랜치 병합` | main ← feature | --no-ff 병합 |
| 7 | `Feat: state.json 파일 저장/불러오기 설정` | main | .gitignore에 state.json 추가 |
| 8 | `Feat: 퀴즈 삭제 기능 추가` | main | delete_quiz() 메서드 구현 |
| 9 | `Feat: 점수 기록 히스토리 기능 추가` | main | history 속성, 기록 저장/표시 |
| 10 | `Feat: 힌트 기능 추가 (사용 시 10점 감점)` | main | Quiz에 hint 속성 추가 |
| 11 | `Fix: Windows 환경 유니코드 출력 깨짐 수정` | main | sys.stdout UTF-8 설정 |
| 12 | `Docs: README 작성 완료` | main | README 전체 작성 |

### 커밋 메시지 규칙

| 접두사 | 용도 | 예시 |
|--------|------|------|
| `Init:` | 초기 설정 | `Init: 프로젝트 초기 설정` |
| `Feat:` | 새 기능 추가 | `Feat: 퀴즈 풀기 기능에 랜덤 출제 추가` |
| `Fix:` | 버그 수정 | `Fix: Windows 환경 유니코드 출력 깨짐 수정` |
| `Docs:` | 문서 작성 | `Docs: README 작성 완료` |
| `Refactor:` | 코드 구조 개선 | `Refactor: 공통 입력 검증 함수로 통합` |

### 브랜치 전략

```
main ──●──●──●──●──────●──●──●──●──●──●──●
                \      /
feature/play-quiz ●──●
```

- **main**: 안정적인 코드만 유지하는 기본 브랜치
- **feature/play-quiz**: 퀴즈 풀기 기능을 별도 브랜치에서 개발 후 병합
- `--no-ff` 옵션으로 merge commit을 명시적으로 생성하여 병합 이력을 남김

### 브랜치를 분리한 이유

퀴즈 풀기 기능은 가장 복잡한 기능(랜덤 출제, 힌트, 점수 계산)이므로, main 브랜치의 안정성을 유지하면서 별도로 개발하고 검증 완료 후 병합하는 것이 안전합니다. 실무에서도 feature 브랜치에서 작업 → PR → 코드 리뷰 → merge 흐름을 사용합니다.

---

## 10. Git 기초 명령어 사용 기록

| 명령어 | 사용 시점 | 역할 |
|--------|---------|------|
| `git init` | 프로젝트 시작 시 | 로컬 Git 저장소 초기화 |
| `git add` | 매 커밋 전 | 변경 파일을 스테이징 영역에 추가 |
| `git commit` | 기능 완성 시마다 | 스테이징된 변경사항을 저장소에 기록 |
| `git push` | 커밋 후 | 로컬 커밋을 GitHub 원격 저장소에 업로드 |
| `git checkout -b` | 퀴즈 풀기 개발 시 | feature/play-quiz 브랜치 생성 및 전환 |
| `git merge --no-ff` | 기능 완성 후 | feature 브랜치를 main에 병합 |
| `git clone` | 실습 단계 | 원격 저장소를 별도 디렉터리에 복제 |
| `git pull` | clone 실습 후 | 원격 변경사항을 로컬에 반영 |

---

## 11. 트러블슈팅

### 트러블슈팅 1 — Windows 환경 이모지 출력 깨짐

| 단계 | 내용 |
|------|------|
| 문제 | `UnicodeEncodeError: 'cp949' codec can't encode character` 오류로 프로그램 실행 불가 |
| 가설 | Windows 기본 인코딩(cp949)이 이모지 문자를 지원하지 않을 것이다 |
| 확인 | 이모지가 포함된 print() 문에서 오류 발생. cmd 기본 인코딩이 cp949임을 확인 |
| 조치 | main.py에서 `sys.stdout`과 `sys.stdin`의 인코딩을 UTF-8로 강제 설정 |
| 배움 | Windows에서 Python 콘솔 프로그램 개발 시 인코딩 설정을 항상 고려해야 한다 |

```python
# main.py에 추가한 해결 코드
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
```

### 트러블슈팅 2 — Python 인터프리터에서 실행 시도

| 단계 | 내용 |
|------|------|
| 문제 | `>>> python main.py` 입력 시 `SyntaxError: invalid syntax` 발생 |
| 가설 | Python 인터프리터(`>>>`) 안에서 셸 명령어를 입력한 것이다 |
| 확인 | 터미널에서 `python`을 실행하면 `>>>` 프롬프트가 나타나며 인터프리터 모드에 진입 |
| 조치 | `exit()`로 인터프리터 종료 후, 터미널(cmd)에서 `python main.py` 실행 |
| 배움 | `>>>` 프롬프트와 터미널 프롬프트(`C:\>`)는 다른 환경이며, 셸 명령어는 터미널에서 실행해야 한다 |

### 트러블슈팅 3 — git merge 시 Fast-forward로 병합 커밋 미생성

| 단계 | 내용 |
|------|------|
| 문제 | `git merge feature/play-quiz` 실행 시 merge commit이 생기지 않음 |
| 가설 | main과 feature 사이에 분기가 없어서 Fast-forward 병합이 된 것이다 |
| 확인 | `git log --oneline --graph`에서 분기/병합 그래프가 보이지 않음 |
| 조치 | `git reset`으로 되돌린 후 `git merge --no-ff` 옵션으로 명시적 merge commit 생성 |
| 배움 | 브랜치 이력을 남기려면 `--no-ff` 옵션을 사용해야 한다. 실무에서도 PR 병합 시 이 방식을 사용한다 |

---

## 12. 핵심 개념 비교 — 클래스 vs 함수, JSON vs DB

### 클래스 사용 vs 함수만 사용

| 관점 | 함수만 사용 | 클래스 사용 (이 프로젝트) |
|------|-----------|----------------------|
| 데이터 관리 | 변수를 전역으로 관리하거나 매번 매개변수로 전달 | self 속성으로 객체 내부에 보관 |
| 기능 확장 | 힌트 추가 시 관련 함수 모두에 매개변수 추가 | Quiz 클래스에 hint 속성 하나만 추가 |
| 코드 가독성 | 함수가 많아질수록 어떤 데이터가 어디서 쓰이는지 추적 어려움 | 관련 데이터와 기능이 한 클래스에 모여 있어 파악 용이 |
| 재사용성 | 다른 프로젝트에서 쓰려면 함수와 변수를 함께 복사 | Quiz 클래스 파일 하나만 가져가면 됨 |

### JSON 파일 vs 데이터베이스

| 관점 | JSON (현재) | SQLite 등 DB |
|------|-----------|-------------|
| 적합 규모 | 수십~수백 개 | 수천 개 이상 |
| 읽기/쓰기 | 전체 파일을 한 번에 읽고/쓰기 | 필요한 행만 조회/수정 가능 |
| 검색 성능 | 데이터가 많으면 느려짐 | 인덱스를 활용한 빠른 검색 |
| 학습 난이도 | 낮음 (json.load/dump만 사용) | SQL 문법 학습 필요 |

현재 퀴즈 게임은 소규모 데이터이므로 JSON이 적합하지만, 1000개 이상으로 늘어나면 매번 전체 파일을 읽고 쓰는 방식이 느려지므로 DB 전환을 고려해야 합니다.

---

## 13. 미션 회고

미션 시작 전에는 Python 문법을 개별적으로만 알고 있었습니다. 직접 하나의 프로그램을 만들어보면서 "문법을 아는 것"과 "프로그램을 완성하는 것"의 차이를 체감하게 되었습니다.

| 경험 | 배움 |
|------|------|
| JSON 저장 없이 프로그램 종료하면 데이터가 사라지는 경험 | 데이터 영속성의 필요성 이해 |
| 입력 검증 코드가 여러 곳에서 중복되는 경험 | 공통 함수로 분리하는 리팩터링의 가치 체감 |
| Quiz와 QuizGame으로 역할을 나누는 경험 | 클래스의 책임 분리와 객체 지향 설계 이해 |
| feature 브랜치에서 작업하고 병합하는 경험 | 브랜치 전략의 필요성과 안전한 개발 흐름 이해 |
| Windows에서 인코딩 오류를 직접 해결한 경험 | 환경 차이를 고려한 방어적 코딩 습관 형성 |
| state.json 손상 상황을 대비한 복구 로직 구현 | try/except 예외 처리의 실질적 활용법 체득 |

이번 실습을 통해 Python의 기본 문법, 클래스 설계, 파일 입출력, 예외 처리, Git 워크플로우를 통합적으로 경험하였으며, 이후 팀 협업(PR, 코드 리뷰)과 더 큰 규모의 프로젝트로 자연스럽게 확장할 수 있는 기반을 갖추게 되었습니다.
