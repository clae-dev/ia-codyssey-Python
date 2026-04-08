# 🎯 나만의 퀴즈 게임

Python으로 만든 콘솔 기반 퀴즈 게임입니다.  
터미널에서 퀴즈를 풀고, 새로운 퀴즈를 추가하고, 점수를 기록할 수 있습니다.  
프로그램을 종료해도 데이터가 `state.json` 파일에 저장되어 다음 실행 시 그대로 유지됩니다.

- **GitHub 저장소**: https://github.com/clae-dev/ia-codyssey-Python

---

## 📌 퀴즈 주제 및 선정 이유

**주제: Python 프로그래밍 기초**

Python을 처음 배우면서 학습한 내용을 퀴즈로 만들면 복습 효과가 있다고 생각했습니다.  
변수, 자료형, 함수, 주석 등 기본 문법을 자연스럽게 반복 학습할 수 있도록 구성했습니다.

---

## 🚀 실행 방법

### 요구 사항
- Python 3.10 이상

### 실행
```bash
python main.py
```

외부 라이브러리 설치가 필요 없습니다. Python 표준 라이브러리만 사용합니다.

---

## 📋 기능 목록

| 번호 | 기능 | 설명 |
|------|------|------|
| 1 | 퀴즈 풀기 | 등록된 퀴즈를 랜덤 순서로 출제, 힌트 사용 가능 (감점 적용) |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호, 힌트(선택)를 입력하여 새 퀴즈 등록 |
| 3 | 퀴즈 삭제 | 등록된 퀴즈를 번호로 선택하여 삭제 |
| 4 | 퀴즈 목록 | 등록된 모든 퀴즈의 문제 텍스트를 번호와 함께 표시 |
| 5 | 점수 확인 | 최고 점수와 전체 게임 기록(날짜, 문제 수, 점수) 표시 |
| 6 | 종료 | 데이터를 저장하고 프로그램 종료 |

### 입력 예외 처리
- 빈 입력, 문자 입력, 범위 밖 숫자 입력 시 안내 메시지 출력 후 재입력
- `Ctrl+C` 또는 EOF 발생 시 데이터 저장 후 안전 종료
- 데이터 파일이 없거나 손상된 경우 기본 퀴즈로 자동 복구

---

## 📁 파일 구조

```
ia-codyssey-Python/
├── main.py           # 프로그램 진입점 (실행 파일)
├── quiz.py           # Quiz 클래스 (개별 퀴즈 표현)
├── quiz_game.py      # QuizGame 클래스 (게임 전체 관리)
├── state.json        # 데이터 저장 파일 (자동 생성)
├── .gitignore        # Git 추적 제외 파일 목록
├── README.md         # 프로젝트 설명 문서
└── docs/
    └── screenshots/  # 실행 화면 스크린샷
```

---

## 🧩 클래스 설계 — Quiz vs QuizGame 책임 분리

클래스를 나눈 기준은 **"무엇을 알고 있는가"**입니다.

### Quiz 클래스 (`quiz.py`)

퀴즈 **한 문제**의 데이터와 동작을 담당합니다.

- **속성**: question(문제), choices(선택지 4개), answer(정답 번호), hint(힌트)
- **메서드**: display(출력), check_answer(정답 확인), to_dict/from_dict(JSON 변환)

### QuizGame 클래스 (`quiz_game.py`)

**게임 전체 흐름**을 관리합니다.

- **속성**: quizzes(퀴즈 목록), best_score(최고 점수), history(기록), file_path(저장 경로)
- **메서드**: show_menu, play_quiz, add_quiz, delete_quiz, show_quiz_list, show_score, save_data, load_data, run

### 클래스 사용 vs 함수만 사용 — 왜 클래스를 사용했는가

함수만으로 구현하면 `question`, `choices`, `answer`를 항상 따로따로 전달해야 합니다:

```python
# 함수만 사용할 경우
def display_quiz(question, choices, answer, number):
    ...
def check_answer(answer, user_answer):
    ...
# → 매개변수가 많아지고, 함수 간 의존성이 복잡해짐
```

클래스를 사용하면 관련 데이터와 기능이 하나로 묶여서 관리가 편합니다:

```python
# 클래스 사용
quiz.display(1)           # self.question, self.choices를 알아서 사용
quiz.check_answer(3)      # self.answer와 비교
# → 데이터가 객체 안에 캡슐화되어 깔끔함
```

**확장할 때의 차이**: 힌트 기능을 추가할 때, 클래스에서는 Quiz에 `hint` 속성 하나만 추가하면 됩니다. 함수만 쓰면 관련 함수 전부에 `hint` 매개변수를 추가해야 합니다.

---

## 📝 기본 퀴즈 데이터 (5개)

`quiz_game.py`의 `DEFAULT_QUIZZES`에 Python 프로그래밍 기초 주제의 퀴즈 5개가 포함되어 있습니다. state.json 파일이 없는 첫 실행 시 또는 파일 손상 시 이 기본 데이터가 자동으로 사용됩니다.

| # | 문제 | 정답 |
|---|------|------|
| 1 | Python에서 변수에 값을 저장할 때 사용하는 기호는? | `=` (2번) |
| 2 | 다음 중 Python의 기본 자료형이 아닌 것은? | `array` (3번) |
| 3 | Python에서 리스트의 길이를 구하는 함수는? | `len()` (3번) |
| 4 | Python에서 여러 줄 주석을 작성할 때 주로 사용하는 것은? | `''' '''` (3번) |
| 5 | Python에서 "Hello"의 자료형은? | `str` (3번) |

---

## 💾 데이터 파일 설명

### state.json

- **경로**: 프로젝트 루트 디렉터리 (`./state.json`)
- **인코딩**: UTF-8
- **역할**: 퀴즈 데이터, 최고 점수, 게임 기록을 영구 저장
- **생성 시점**: 프로그램에서 데이터가 변경될 때 자동 생성/갱신

#### 스키마

```json
{
    "quizzes": [
        {
            "question": "문제 텍스트",
            "choices": ["선택지1", "선택지2", "선택지3", "선택지4"],
            "answer": 1,
            "hint": "힌트 텍스트 (선택)"
        }
    ],
    "best_score": 80,
    "history": [
        {
            "date": "2026-04-07 14:30:00",
            "total": 5,
            "correct": 4,
            "score": 80
        }
    ]
}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `quizzes` | 배열 | 등록된 퀴즈 목록. 동적으로 추가/삭제되므로 배열이 적합 |
| `quizzes[].question` | 문자열 | 퀴즈 문제 |
| `quizzes[].choices` | 배열 | 선택지 4개 |
| `quizzes[].answer` | 정수 | 정답 번호 (1~4) |
| `quizzes[].hint` | 문자열 | 힌트 (없으면 생략) |
| `best_score` | 정수/null | 최고 점수. null은 아직 플레이하지 않은 상태 (0점과 구분) |
| `history` | 배열 | 게임 기록 히스토리. 날짜순으로 누적 |

#### 왜 JSON 형식을 선택했는가

1. **사람이 읽을 수 있는 텍스트 형식**: state.json을 직접 열어서 데이터를 확인하거나 수동 수정이 가능합니다.
2. **Python과의 자연스러운 변환**: `json.dump()`/`json.load()` 한 줄로 Python의 dict, list와 바로 변환됩니다.
3. **중첩 구조 표현**: 퀴즈 안에 선택지 배열이 있는 중첩 구조를 자연스럽게 표현할 수 있습니다.
4. **표준 라이브러리**: 외부 설치 없이 Python 내장 `json` 모듈만으로 사용 가능합니다.
5. **범용성**: Python뿐 아니라 거의 모든 프로그래밍 언어에서 지원하는 데이터 형식입니다.

#### 파일 손상 시 동작
- JSON 파싱 실패 시 → 손상 파일을 `state.json.bak`으로 백업 → 기본 퀴즈로 초기화

#### 대용량 데이터 시 한계

현재 방식은 `load_data()` 시 state.json **전체를 메모리에 읽어오고**, `save_data()` 시 **전체를 다시 파일에 쓰는** 구조입니다. 퀴즈가 1000개 이상이 되면:

- **읽기/쓰기 속도 저하**: 퀴즈 1개만 추가해도 전체를 다시 JSON으로 변환하고 파일에 씁니다.
- **메모리 사용량 증가**: 모든 퀴즈 데이터를 한 번에 메모리에 올려야 합니다.
- **검색 비효율**: 특정 퀴즈를 찾으려면 리스트를 처음부터 끝까지 순회해야 합니다.

대안으로는 SQLite 같은 데이터베이스로 전환하면 필요한 행만 조회/수정할 수 있고, 인덱스로 빠른 검색이 가능합니다. Python 표준 라이브러리에 `sqlite3` 모듈이 포함되어 있어 외부 설치 없이 사용할 수 있습니다.

#### 요구사항 변경 시 수정 범위

**정답 채점 방식(점수 계산)이 바뀌는 경우**:
- `quiz_game.py`의 `play_quiz()` 메서드에서 점수 계산 부분만 수정합니다.
- 현재는 `int((correct_count / total) * 100)`으로 100점 만점 비율 계산인데, 문제별 배점이나 연속 정답 보너스가 추가된다면 이 계산식만 바꾸면 됩니다.

**퀴즈 구조(선택지 개수 등)가 바뀌는 경우**:
1. `quiz.py`의 `Quiz.__init__()` — choices의 길이 제한 변경
2. `quiz_game.py`의 `play_quiz()` — 정답 입력 범위를 `get_valid_input('정답 입력: ', 1, 4)`에서 4를 새 개수로 변경
3. `quiz_game.py`의 `add_quiz()` — 선택지 입력 루프 `for i in range(1, 5)`에서 5를 새 개수+1로 변경

클래스로 분리했기 때문에, Quiz의 데이터 구조 변경은 `quiz.py`에서, 게임 진행 로직 변경은 `quiz_game.py`에서 독립적으로 수정할 수 있습니다.

---

## 🔀 Git 워크플로우

### 커밋 히스토리

```
* 840b338 Docs: clone 실습 - README에 한 줄 추가
* 720359b Docs: 실행 화면 스크린샷 추가 및 README 이미지 삽입
* e432948 Create Read.md
* 2042d78 Create Q&A.md
* add14a8 Docs: README 작성 완료
* b725001 Fix: Windows 환경 유니코드 출력 깨짐 수정
* 84354ca Feat: 힌트 기능 추가 (사용 시 10점 감점)
* a979bdb Feat: 점수 기록 히스토리 기능 추가
* 93c2eda Feat: 퀴즈 삭제 기능 추가
* 3694829 Feat: state.json 파일 저장/불러오기 설정
*   4063c8f Merge: feature/play-quiz 브랜치 병합
|\  
| * 3e5e0fc Feat: 퀴즈 풀기 기능에 랜덤 출제 추가
|/  
* c4a8483 Feat: 메뉴 화면 및 메인 루프 구현
* 02cf3c6 Feat: Python 기초 주제 기본 퀴즈 5개 추가
* 3668cde Feat: Quiz 클래스 정의
* 345ba9f Init: 프로젝트 초기 설정
```

총 **16개 커밋** (merge 포함), `feature/play-quiz` 브랜치의 분기와 병합 그래프가 확인됩니다.

### 커밋 분할 기준 및 메시지 규칙

**커밋 분할 기준**: 하나의 기능이 완성될 때마다 커밋했습니다. Quiz 클래스 작성, 메뉴 구현, 퀴즈 풀기, 퀴즈 추가 등 각각이 독립된 커밋입니다. 이렇게 하면 나중에 특정 기능에 문제가 생겼을 때 해당 커밋만 확인하면 됩니다.

**메시지 규칙**: 접두사로 변경 종류를 구분했습니다.

| 접두사 | 용도 | 예시 |
|--------|------|------|
| `Init:` | 초기 설정 | `Init: 프로젝트 초기 설정` |
| `Feat:` | 새 기능 추가 | `Feat: 퀴즈 풀기 기능에 랜덤 출제 추가` |
| `Fix:` | 버그 수정 | `Fix: Windows 환경 유니코드 출력 깨짐 수정` |
| `Docs:` | 문서 작성/수정 | `Docs: README 작성 완료` |
| `Merge:` | 브랜치 병합 | `Merge: feature/play-quiz 브랜치 병합` |

### 브랜치 전략 — 왜 브랜치를 분리했는가

```
main ──●──●──●──●──────●──●──●──●──●──●──●
                \      /
feature/play-quiz ●──●
```

**분리한 이유**: 퀴즈 풀기 기능은 랜덤 출제, 힌트, 점수 계산 등 가장 복잡한 기능이었습니다. 이 기능을 개발하는 동안 main 브랜치는 메뉴와 기본 구조가 이미 동작하는 안정적인 상태를 유지해야 했습니다. feature 브랜치에서 작업하면 실수가 생겨도 main에 영향을 주지 않습니다.

**병합(merge)의 의미**: feature 브랜치에서 기능이 완성되고 검증이 끝나면, 그 변경사항을 main에 합치는 것입니다. `--no-ff` 옵션을 사용하여 merge commit을 명시적으로 생성했기 때문에, `git log --graph`에서 "어디서 브랜치가 갈라졌다가 합쳐졌는지" 이력이 남습니다. 실무에서는 이 과정에서 PR(Pull Request)과 코드 리뷰를 거칩니다.

---

## 🔧 Git 실습 기록

### clone 실습
```bash
# 원격 저장소를 별도 디렉터리에 복제
git clone https://github.com/clae-dev/ia-codyssey-Python.git quiz-game-clone
cd quiz-game-clone
```

### 변경 후 push
```bash
# 복제된 저장소에서 README에 한 줄 추가 후 커밋
echo "# clone 실습 완료" >> README.md
git add README.md
git commit -m "Docs: clone 실습 - README에 한 줄 추가"
git push
```

### pull로 변경사항 가져오기
```bash
# 기존 작업 디렉터리로 돌아와서 pull
cd ../ia-codyssey-Python
git pull
```

pull 후 README.md에 변경 내용이 정상 반영되었음을 확인했습니다.

---

## 📸 실행 화면 스크린샷

### 메뉴 화면
![메뉴 화면](docs/screenshots/menu.png)

### 퀴즈 풀기
![퀴즈 풀기](docs/screenshots/play.png)

### 퀴즈 추가
![퀴즈 추가](docs/screenshots/add_quiz.png)

### 점수 확인
![점수 확인](docs/screenshots/score.png)
