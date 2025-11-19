# 🤝 기여 가이드

## 사주 & MBTI 분석 프로젝트에 기여하기

프로젝트에 관심을 가져주셔서 감사합니다! 모든 기여를 환영합니다.

---

## 목차

1. [기여 방법](#기여-방법)
2. [개발 환경 설정](#개발-환경-설정)
3. [브랜치 전략](#브랜치-전략)
4. [커밋 컨벤션](#커밋-컨벤션)
5. [Pull Request](#pull-request)
6. [코드 스타일](#코드-스타일)
7. [테스트](#테스트)
8. [문서화](#문서화)

---

## 기여 방법

### 🐛 버그 제보

버그를 발견하셨나요?

1. **GitHub Issues** 확인
   - 이미 제보된 버그인지 확인
   - https://github.com/pplkjh/saju_mbti_bot/issues

2. **새 Issue 생성**
   - "Bug Report" 템플릿 사용
   - 다음 정보 포함:
     - 버그 설명
     - 재현 단계
     - 예상 동작 vs 실제 동작
     - 환경 정보 (OS, Python 버전 등)
     - 스크린샷/로그 (가능하면)

---

### ✨ 기능 제안

새로운 기능을 제안하고 싶으신가요?

1. **GitHub Discussions**에서 먼저 논의
   - 커뮤니티 의견 수렴
   - 타당성 검토

2. **Issue 생성**
   - "Feature Request" 템플릿 사용
   - 다음 정보 포함:
     - 기능 설명
     - 사용 사례
     - 구현 아이디어 (선택)

---

### 💻 코드 기여

코드를 직접 기여하고 싶으신가요?

**작은 기여부터 시작하세요!**

초보자 친화적인 이슈:
- `good first issue` 라벨
- `documentation` 라벨
- `help wanted` 라벨

---

## 개발 환경 설정

### 1. Fork & Clone

```bash
# 1. GitHub에서 Fork 클릭

# 2. Fork한 저장소 클론
git clone https://github.com/YOUR_USERNAME/saju_mbti_bot.git
cd saju_mbti_bot

# 3. upstream 원격 저장소 추가
git remote add upstream https://github.com/pplkjh/saju_mbti_bot.git
```

### 2. 가상환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. 의존성 설치

```bash
# 백엔드
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 개발 도구

# 프론트엔드
cd ../frontend
pip install -r requirements.txt
```

### 4. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# OpenAI API 키 설정
# .env 파일 편집
```

### 5. 벡터 스토어 생성

```bash
python scripts/build_vector_store.py
```

### 6. 서버 실행

```bash
# 백엔드 (터미널 1)
cd backend
python main.py

# 프론트엔드 (터미널 2)
cd frontend
streamlit run app.py
```

---

## 브랜치 전략

### 브랜치 명명 규칙

```
feature/기능명        # 새 기능
bugfix/버그명         # 버그 수정
hotfix/긴급수정명     # 긴급 수정
docs/문서명          # 문서 작업
refactor/리팩토링명   # 리팩토링
test/테스트명        # 테스트 추가
```

### 예시

```bash
# 새 기능 추가
git checkout -b feature/compatibility-analysis

# 버그 수정
git checkout -b bugfix/api-timeout

# 문서 개선
git checkout -b docs/update-readme
```

---

## 커밋 컨벤션

### 커밋 메시지 형식

```
<타입>: <제목>

<본문> (선택)

<푸터> (선택)
```

### 타입

| 타입 | 설명 | 예시 |
|------|------|------|
| `feat` | 새 기능 | `feat: Add compatibility analysis` |
| `fix` | 버그 수정 | `fix: Resolve API timeout issue` |
| `docs` | 문서 변경 | `docs: Update API reference` |
| `style` | 코드 포맷 | `style: Format with black` |
| `refactor` | 리팩토링 | `refactor: Simplify vector search` |
| `test` | 테스트 추가 | `test: Add unit tests for analyzer` |
| `chore` | 기타 작업 | `chore: Update dependencies` |
| `perf` | 성능 개선 | `perf: Optimize embedding generation` |

### 제목 작성 규칙

- 50자 이내
- 동사로 시작 (Add, Fix, Update 등)
- 명령형 사용 (Added ❌, Add ✅)
- 마침표 없음

### 예시

✅ **좋은 커밋**:
```
feat: Add compatibility analysis feature

- Implement saju-mbti compatibility logic
- Add new API endpoint /api/v1/compatibility
- Update frontend UI with compatibility section

Closes #42
```

❌ **나쁜 커밋**:
```
update code
```

---

## Pull Request

### PR 생성 전 체크리스트

- [ ] 코드가 정상 작동하는지 테스트
- [ ] 린터/포매터 실행 (black, flake8)
- [ ] 커밋 메시지가 컨벤션을 따름
- [ ] 관련 이슈 번호 포함
- [ ] 문서 업데이트 (필요시)

### PR 생성

1. **변경사항 커밋**:
```bash
git add .
git commit -m "feat: Add new feature"
```

2. **Fork한 저장소에 푸시**:
```bash
git push origin feature/your-feature
```

3. **GitHub에서 PR 생성**:
   - Base: `pplkjh/saju_mbti_bot:main`
   - Compare: `your-username/saju_mbti_bot:feature/your-feature`

### PR 템플릿

```markdown
## 변경 사항
<!-- 무엇을 변경했는지 설명 -->

## 동기 및 맥락
<!-- 왜 이 변경이 필요한지 설명 -->

## 스크린샷 (선택)
<!-- UI 변경이 있다면 스크린샷 첨부 -->

## 테스트 방법
<!-- 리뷰어가 테스트할 수 있는 방법 -->

## 체크리스트
- [ ] 코드가 정상 작동함
- [ ] 테스트 추가/업데이트
- [ ] 문서 업데이트
- [ ] 커밋 메시지가 컨벤션을 따름

## 관련 이슈
Closes #이슈번호
```

### PR 리뷰 과정

1. **자동 체크**:
   - CI/CD 테스트 통과
   - 린터 체크 통과

2. **코드 리뷰**:
   - 유지보수자가 리뷰
   - 피드백 반영

3. **승인 & 머지**:
   - 승인되면 main 브랜치에 머지
   - Squash merge 사용

---

## 코드 스타일

### Python 스타일 가이드

**PEP 8** 준수

### 포매터: Black

```bash
# 설치
pip install black

# 실행
black backend/
black frontend/
```

### 린터: Flake8

```bash
# 설치
pip install flake8

# 실행
flake8 backend/
```

### 설정 파일: `.flake8`

```ini
[flake8]
max-line-length = 100
exclude = .git,__pycache__,venv
ignore = E203, W503
```

### 타입 힌팅

```python
# ✅ 타입 힌팅 사용
def analyze_saju(birth_date: str, mbti: str) -> dict:
    return {"result": "..."}

# ❌ 타입 힌팅 없음
def analyze_saju(birth_date, mbti):
    return {"result": "..."}
```

### Docstring

Google 스타일 docstring 사용:

```python
def calculate_elements(birth_date: str) -> dict:
    """
    생년월일로부터 오행 균형을 계산합니다.

    Args:
        birth_date (str): 생년월일 (YYYY-MM-DD 형식)

    Returns:
        dict: 오행별 비율 {'木': 20, '火': 15, ...}

    Raises:
        ValueError: 잘못된 날짜 형식

    Example:
        >>> calculate_elements("1990-05-21")
        {'木': 20, '火': 15, '土': 25, '金': 20, '水': 20}
    """
    pass
```

---

## 테스트

### 테스트 프레임워크: pytest

```bash
# 설치
pip install pytest pytest-asyncio

# 실행
pytest tests/
```

### 테스트 작성

**파일 구조**:
```
tests/
├── test_api.py
├── test_analyzer.py
└── test_vector_store.py
```

**예시**:
```python
# tests/test_analyzer.py
import pytest
from backend.services.saju_analyzer import SajuAnalyzer

@pytest.fixture
def analyzer():
    return SajuAnalyzer()

def test_analyze_basic(analyzer):
    """기본 분석 테스트"""
    result = analyzer.analyze(
        birth_date="1990-05-21",
        birth_time="14:30",
        gender="여성",
        name="테스트",
        mbti="INFJ"
    )

    assert result["success"] is True
    assert "INFJ" in result["result"]

@pytest.mark.asyncio
async def test_analyze_async(analyzer):
    """비동기 분석 테스트"""
    result = await analyzer.analyze(...)
    assert result["success"] is True
```

### 테스트 커버리지

```bash
# 설치
pip install pytest-cov

# 실행
pytest --cov=backend tests/

# HTML 리포트
pytest --cov=backend --cov-report=html tests/
```

---

## 문서화

### 코드 문서화

- **모든 public 함수/클래스**에 docstring 작성
- **복잡한 로직**에 주석 추가
- **타입 힌팅** 사용

### 마크다운 문서

- README.md 업데이트
- API_REFERENCE.md 업데이트
- CHANGELOG.md에 변경사항 추가

### 예시 문서 업데이트

```markdown
## [Unreleased]

### Added
- 궁합 분석 API 엔드포인트 (#42)
- 오행 균형 시각화 차트 (#45)

### Fixed
- API timeout 문제 해결 (#38)
- 벡터 스토어 로딩 버그 수정 (#40)

### Changed
- 프롬프트 개선으로 분석 품질 향상 (#43)
```

---

## 개발 워크플로우

### 1. 이슈 확인

```bash
# upstream 최신 상태 가져오기
git fetch upstream

# main 브랜치 업데이트
git checkout main
git merge upstream/main
```

### 2. 브랜치 생성

```bash
git checkout -b feature/your-feature
```

### 3. 개발

```bash
# 코드 작성
# ...

# 테스트
pytest tests/

# 린터 실행
black .
flake8 .
```

### 4. 커밋

```bash
git add .
git commit -m "feat: Add new feature"
```

### 5. 푸시

```bash
git push origin feature/your-feature
```

### 6. PR 생성

GitHub에서 Pull Request 생성

---

## 커뮤니티 가이드라인

### 행동 강령

- 존중과 배려
- 건설적인 피드백
- 다양성 존중
- 협력적 태도

### 질문하기

- **GitHub Discussions** 사용
- 명확하고 구체적으로
- 관련 코드/로그 포함
- 이미 답변된 질문인지 검색

### 피드백 주고받기

- 코드에 대한 비판, 사람에 대한 비판 ❌
- 구체적인 제안
- 긍정적인 태도

---

## 라이선스

기여하신 코드는 프로젝트의 MIT 라이선스를 따릅니다.

---

## 도움이 필요하신가요?

- **GitHub Discussions**: 질문 및 토론
- **GitHub Issues**: 버그 제보 및 기능 제안
- **이메일**: (추가 예정)

---

## 감사합니다! 🎉

모든 기여에 감사드립니다. 여러분의 기여로 프로젝트가 더 나아집니다!

**Contributors**:
<!-- 기여자 목록이 자동으로 추가됩니다 -->

---

**Happy Contributing!** 💻✨
