# 📚 학습 가이드

## 사주 & MBTI 분석 시스템 개발 학습 가이드

이 문서는 본 프로젝트를 통해 배울 수 있는 기술과 개념을 정리한 학습 가이드입니다.

---

## 목차

1. [학습 목표](#학습-목표)
2. [기술 스택별 학습](#기술-스택별-학습)
3. [단계별 학습 로드맵](#단계별-학습-로드맵)
4. [실습 과제](#실습-과제)
5. [추가 학습 리소스](#추가-학습-리소스)

---

## 학습 목표

### 🎯 이 프로젝트를 통해 배울 수 있는 것

#### 백엔드 개발
- ✅ FastAPI로 RESTful API 구축
- ✅ 비동기 프로그래밍 (async/await)
- ✅ Pydantic을 이용한 데이터 검증
- ✅ 모듈화된 서비스 아키텍처 설계

#### AI/ML
- ✅ OpenAI GPT API 통합
- ✅ LangChain 프레임워크 활용
- ✅ 벡터 데이터베이스 (FAISS) 구축
- ✅ 프롬프트 엔지니어링

#### 프론트엔드
- ✅ Streamlit으로 빠른 프로토타입 개발
- ✅ API 클라이언트 구현
- ✅ 사용자 경험(UX) 설계

#### DevOps
- ✅ 클라우드 배포 (Railway, Render)
- ✅ 환경 변수 관리
- ✅ CI/CD 파이프라인 이해
- ✅ Docker 컨테이너화 (선택)

#### 소프트웨어 공학
- ✅ 프로젝트 구조 설계
- ✅ 문서화 작성
- ✅ Git 버전 관리
- ✅ API 설계 원칙

---

## 기술 스택별 학습

### 1. FastAPI 마스터하기

#### 기초 개념

**FastAPI란?**
- Python 기반 최신 웹 프레임워크
- 자동 API 문서 생성 (Swagger UI)
- 빠른 성능 (비동기 처리)
- 타입 힌팅 기반 검증

#### 핵심 파일 분석: `backend/main.py`

```python
# 1. FastAPI 인스턴스 생성
app = FastAPI(
    title="사주 & MBTI 분석 API",
    description="API 설명",
    version="1.0.0"
)

# 2. CORS 설정 (프론트엔드 연동)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (개발용)
)

# 3. 엔드포인트 정의
@app.post("/api/v1/analyze")
async def analyze_saju_mbti(request: AnalysisRequest):
    # 비즈니스 로직
    pass
```

#### 학습 과제

1. **기본 엔드포인트 추가**
   ```python
   @app.get("/api/v1/test")
   async def test_endpoint():
       return {"message": "Hello, World!"}
   ```

2. **쿼리 파라미터 처리**
   ```python
   @app.get("/api/v1/mbti/{mbti_type}")
   async def get_mbti_info(mbti_type: str):
       return {"mbti": mbti_type, "description": "..."}
   ```

3. **에러 핸들링**
   ```python
   from fastapi import HTTPException

   @app.get("/api/v1/users/{user_id}")
   async def get_user(user_id: int):
       if user_id < 0:
           raise HTTPException(status_code=400, detail="Invalid user ID")
       return {"user_id": user_id}
   ```

#### 추천 학습 자료
- [공식 문서](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial - YouTube](https://www.youtube.com/results?search_query=fastapi+tutorial)
- 실습: FastAPI로 간단한 CRUD API 만들기

---

### 2. LangChain & Vector DB

#### 핵심 개념

**LangChain이란?**
- LLM 애플리케이션 개발 프레임워크
- 문서 로딩, 분할, 임베딩, 검색을 쉽게 구현

**FAISS (Facebook AI Similarity Search)**
- 고속 벡터 유사도 검색 라이브러리
- 수백만 개의 벡터에서 빠른 검색

#### 핵심 파일 분석: `scripts/build_vector_store.py`

```python
# 1. PDF에서 텍스트 추출
text = extract_text_from_pdf(pdf_path)

# 2. 텍스트를 청크로 분할
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # 청크 크기
    chunk_overlap=200,    # 중복 크기 (문맥 유지)
)
chunks = text_splitter.split_text(text)

# 3. OpenAI 임베딩으로 벡터화
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(chunks, embeddings)

# 4. 벡터 스토어 저장
vectorstore.save_local("data/vector_store")
```

#### 왜 벡터 DB를 사용하나?

**문제**: PDF 전체를 GPT에 넣으면 토큰 한계 초과
```
PDF 전체 (10만 토큰) → GPT 입력 불가능 ❌
```

**해결**: 필요한 부분만 검색해서 사용
```
사용자 쿼리 → 벡터 검색 → 관련 텍스트 3개 (3천 토큰) → GPT ✅
```

#### 학습 과제

1. **벡터 검색 이해하기**
   ```python
   # 유사도 검색
   query = "INFJ 성격의 특징"
   docs = vectorstore.similarity_search(query, k=3)

   for doc in docs:
       print(doc.page_content)
   ```

2. **다른 임베딩 모델 실험**
   ```python
   from langchain.embeddings import HuggingFaceEmbeddings

   embeddings = HuggingFaceEmbeddings(
       model_name="sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens"
   )
   ```

3. **청크 크기 최적화**
   - chunk_size를 500, 1000, 2000으로 변경하며 실험
   - 검색 품질과 속도 비교

#### 추천 학습 자료
- [LangChain 공식 문서](https://python.langchain.com/docs/get_started/introduction)
- [FAISS 튜토리얼](https://github.com/facebookresearch/faiss/wiki)
- 실습: 자신의 문서로 QA 시스템 만들기

---

### 3. OpenAI API & 프롬프트 엔지니어링

#### 핵심 파일 분석: `backend/services/llm_service.py`

```python
def generate_analysis(self, birth_date, birth_time, gender, name, mbti, context_documents):
    # 1. 시스템 롤 정의
    system_role = """
    당신은 사주와 MBTI 전문가입니다.
    다음을 분석해주세요:
    1. 사주 분석
    2. MBTI 분석
    3. 복합 분석
    """

    # 2. 사용자 입력 구성
    user_content = f"""
    생년월일: {birth_date}
    MBTI: {mbti}

    참고 문서:
    {context_documents}
    """

    # 3. OpenAI API 호출
    response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": user_content}
        ],
        temperature=0.7,  # 창의성 수준
        max_tokens=2000   # 최대 출력 길이
    )

    return response.choices[0].message.content
```

#### 프롬프트 엔지니어링 팁

**좋은 프롬프트의 특징**

1. **명확한 역할 정의**
   ```
   ❌ "분석해줘"
   ✅ "당신은 20년 경력의 사주 명리학 전문가입니다"
   ```

2. **구체적인 지시사항**
   ```
   ❌ "성격 분석해줘"
   ✅ "다음 5가지를 분석해주세요: 1) 사주 기본 분석 2) MBTI 특성..."
   ```

3. **컨텍스트 제공**
   ```python
   # 참고 문서를 함께 제공
   user_content = f"다음 논문을 참고하여 분석하세요:\n{documents}"
   ```

4. **출력 형식 지정**
   ```
   "한국어로 답변하며, 이모지를 적절히 사용하여 가독성을 높여주세요"
   ```

#### 학습 과제

1. **Temperature 실험**
   - 0.1 (논리적) ~ 1.5 (창의적) 범위에서 테스트
   - 분석 결과의 일관성 vs 창의성 비교

2. **시스템 프롬프트 개선**
   - 더 전문적인 톤으로 변경
   - 특정 분석 관점 추가 (심리학적, 철학적 등)

3. **Few-shot Learning 적용**
   ```python
   system_role = """
   예시 1:
   입력: INFJ, 1990년생
   출력: INFJ는 옹호자 유형으로...

   예시 2:
   입력: ENTP, 1985년생
   출력: ENTP는 변론가 유형으로...

   이제 사용자 정보를 분석해주세요:
   """
   ```

#### 추천 학습 자료
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Prompt Engineering 101](https://www.youtube.com/results?search_query=prompt+engineering+tutorial)
- 실습: 다양한 프롬프트로 결과 비교

---

### 4. Streamlit UI 개발

#### 핵심 파일 분석: `frontend/app.py`

```python
import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="사주 & MBTI 분석",
    page_icon="🔮",
    layout="wide"
)

# 2. 입력 위젯
name = st.text_input("이름", placeholder="홍길동")
birth_date = st.date_input("생년월일")
mbti = st.selectbox("MBTI", ["INFJ", "ENFP", ...])

# 3. 버튼 클릭 처리
if st.button("분석 시작"):
    with st.spinner("분석 중..."):
        result = call_api(name, birth_date, mbti)
        st.success("완료!")
        st.markdown(result)

# 4. 결과 다운로드
st.download_button(
    label="💾 결과 다운로드",
    data=result,
    file_name=f"analysis_{name}.txt"
)
```

#### Streamlit 핵심 개념

**위젯 종류**
- `st.text_input()` - 텍스트 입력
- `st.selectbox()` - 드롭다운
- `st.slider()` - 슬라이더
- `st.radio()` - 라디오 버튼
- `st.checkbox()` - 체크박스

**레이아웃**
```python
# 컬럼 나누기
col1, col2 = st.columns(2)
with col1:
    st.write("왼쪽")
with col2:
    st.write("오른쪽")

# 사이드바
with st.sidebar:
    st.header("설정")
    option = st.selectbox("옵션", ["A", "B"])
```

**상태 관리**
```python
# Session State 사용
if 'count' not in st.session_state:
    st.session_state.count = 0

if st.button('증가'):
    st.session_state.count += 1

st.write(f"Count: {st.session_state.count}")
```

#### 학습 과제

1. **UI 개선**
   - 탭으로 섹션 나누기
   - 프로그레스 바 추가
   - 차트로 오행 분포 시각화

2. **히스토리 기능 추가**
   ```python
   if 'history' not in st.session_state:
       st.session_state.history = []

   # 분석 결과 저장
   st.session_state.history.append({
       'name': name,
       'result': result,
       'timestamp': datetime.now()
   })

   # 히스토리 표시
   for item in st.session_state.history:
       st.write(f"{item['name']}: {item['timestamp']}")
   ```

3. **다크 모드 지원**
   ```python
   st.markdown("""
   <style>
   .stApp {
       background-color: #1E1E1E;
       color: white;
   }
   </style>
   """, unsafe_allow_html=True)
   ```

#### 추천 학습 자료
- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery) - 예제 모음
- 실습: 대시보드 앱 만들기

---

### 5. 클라우드 배포

#### Railway 배포 과정 이해

**배포 흐름**
```
GitHub Push → Railway 자동 감지 → Docker 빌드 → 배포 → 도메인 할당
```

**설정 파일 분석: `railway.json`**
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "cd backend && pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT"
  }
}
```

#### 환경 변수 관리

**로컬 환경 (.env)**
```env
OPENAI_API_KEY=sk-local-key
PORT=8000
```

**프로덕션 환경 (Railway)**
```
Settings → Variables → Add Variable
OPENAI_API_KEY=sk-prod-key
```

#### 학습 과제

1. **Docker 이미지 만들기**
   ```dockerfile
   FROM python:3.10-slim

   WORKDIR /app
   COPY backend/requirements.txt .
   RUN pip install -r requirements.txt

   COPY backend/ .

   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **CI/CD 파이프라인 구축**
   - GitHub Actions로 자동 테스트
   - 테스트 통과 시 자동 배포

3. **모니터링 설정**
   - Sentry로 에러 추적
   - Uptime Robot으로 서버 상태 모니터링

#### 추천 학습 자료
- [Railway 공식 문서](https://docs.railway.app/)
- [Docker 튜토리얼](https://docs.docker.com/get-started/)
- 실습: 간단한 Flask 앱 배포하기

---

## 단계별 학습 로드맵

### 🌱 초급 (1-2주)

**목표**: 프로젝트 실행 및 기본 수정

- [ ] Python 기초 복습
- [ ] Git 기본 명령어 학습
- [ ] 프로젝트 로컬 실행 성공
- [ ] FastAPI 엔드포인트 1개 추가
- [ ] Streamlit UI 텍스트 수정

**학습 자료**
- Python 공식 튜토리얼
- Git 기초 강의
- FastAPI 공식 튜토리얼 (Intro)

### 🌿 중급 (3-4주)

**목표**: 기능 추가 및 커스터마이징

- [ ] 새로운 분석 기능 추가 (예: 궁합 분석)
- [ ] PDF 벡터 스토어 커스터마이징
- [ ] 프롬프트 엔지니어링 실험
- [ ] UI/UX 개선
- [ ] Railway 배포 성공

**학습 자료**
- LangChain 공식 문서
- OpenAI API 가이드
- Streamlit 고급 기능

### 🌳 고급 (1-2개월)

**목표**: 확장 및 최적화

- [ ] 사용자 인증 시스템 추가
- [ ] 데이터베이스 통합 (PostgreSQL)
- [ ] 캐싱 전략 구현 (Redis)
- [ ] API Rate Limiting
- [ ] 성능 최적화
- [ ] 모바일 앱 개발 (Flutter/React Native)

**학습 자료**
- PostgreSQL 튜토리얼
- Redis 캐싱 전략
- Flutter 공식 문서

---

## 실습 과제

### 과제 1: 새로운 MBTI 정보 엔드포인트 추가

```python
# backend/main.py에 추가

@app.get("/api/v1/mbti/{mbti_type}")
async def get_mbti_info(mbti_type: str):
    """MBTI 유형별 정보 반환"""
    mbti_info = {
        "INFJ": {"name": "옹호자", "traits": ["통찰력", "이상주의", "헌신"]},
        "ENFP": {"name": "활동가", "traits": ["열정", "창의성", "사교성"]},
        # 나머지 14개 유형 추가
    }

    if mbti_type not in mbti_info:
        raise HTTPException(status_code=404, detail="Invalid MBTI type")

    return mbti_info[mbti_type]
```

**테스트**
```bash
curl http://localhost:8000/api/v1/mbti/INFJ
```

### 과제 2: 오행 균형 계산 기능 추가

```python
# backend/services/saju_analyzer.py

def calculate_element_balance(birth_date: str) -> dict:
    """오행 균형 계산"""
    # 생년월일로부터 오행 추출
    year = int(birth_date.split('-')[0])

    # 간단한 예시 (실제로는 더 복잡한 계산 필요)
    elements = {
        '木': 20,
        '火': 15,
        '土': 25,
        '金': 20,
        '水': 20
    }

    return elements
```

### 과제 3: Streamlit에 차트 추가

```python
# frontend/app.py

import plotly.graph_objects as go

# 오행 분포 차트
elements = {'木': 20, '火': 15, '土': 25, '金': 20, '水': 20}

fig = go.Figure(data=[
    go.Bar(
        x=list(elements.keys()),
        y=list(elements.values()),
        marker_color=['green', 'red', 'brown', 'gold', 'blue']
    )
])

st.plotly_chart(fig)
```

### 과제 4: 분석 히스토리 저장

```python
# SQLite 데이터베이스 사용

import sqlite3

def save_analysis(name, birth_date, mbti, result):
    conn = sqlite3.connect('analysis_history.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY,
        name TEXT,
        birth_date TEXT,
        mbti TEXT,
        result TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    INSERT INTO history (name, birth_date, mbti, result)
    VALUES (?, ?, ?, ?)
    ''', (name, birth_date, mbti, result))

    conn.commit()
    conn.close()
```

---

## 추가 학습 리소스

### 📖 추천 도서

1. **FastAPI**
   - "Building Python Web APIs with FastAPI" - Abdulazeez Abdulazeez

2. **AI/ML**
   - "LangChain AI Handbook" - James Briggs
   - "Prompt Engineering Guide" - DAIR.AI

3. **Python**
   - "Fluent Python" - Luciano Ramalho
   - "Python Cookbook" - David Beazley

### 🎥 추천 강의

1. **FastAPI**
   - [FastAPI - The Complete Course](https://www.youtube.com/results?search_query=fastapi+complete+course)

2. **LangChain**
   - [LangChain Crash Course](https://www.youtube.com/results?search_query=langchain+crash+course)

3. **Streamlit**
   - [Streamlit for Data Science](https://www.youtube.com/results?search_query=streamlit+tutorial)

### 🌐 유용한 웹사이트

- **FastAPI**: https://fastapi.tiangolo.com/
- **LangChain**: https://python.langchain.com/
- **Streamlit**: https://docs.streamlit.io/
- **OpenAI**: https://platform.openai.com/docs/
- **Railway**: https://docs.railway.app/

### 💬 커뮤니티

- **Discord**
  - FastAPI Discord
  - LangChain Discord

- **Reddit**
  - r/FastAPI
  - r/MachineLearning
  - r/learnpython

- **GitHub Discussions**
  - 본 프로젝트 Discussions 탭

---

## 학습 평가

### 자가 진단 체크리스트

#### 기초 레벨
- [ ] 프로젝트를 로컬에서 실행할 수 있다
- [ ] FastAPI 엔드포인트의 역할을 이해한다
- [ ] Streamlit UI를 수정할 수 있다
- [ ] 환경 변수의 개념을 이해한다

#### 중급 레벨
- [ ] 새로운 API 엔드포인트를 추가할 수 있다
- [ ] 벡터 스토어의 작동 원리를 설명할 수 있다
- [ ] 프롬프트를 수정하여 결과를 개선할 수 있다
- [ ] Railway에 배포할 수 있다

#### 고급 레벨
- [ ] 전체 아키텍처를 설명할 수 있다
- [ ] 성능 병목 지점을 찾고 최적화할 수 있다
- [ ] 보안 이슈를 파악하고 해결할 수 있다
- [ ] 새로운 기능을 독립적으로 추가할 수 있다

---

## 다음 단계

학습을 마치셨다면:

1. **포트폴리오 작성**
   - GitHub README 정리
   - 기술 블로그 글 작성
   - LinkedIn 프로젝트 추가

2. **오픈소스 기여**
   - 본 프로젝트에 PR 제출
   - 다른 FastAPI/LangChain 프로젝트 기여

3. **심화 프로젝트**
   - 모바일 앱 개발
   - 다른 도메인 적용 (타로, 점성술 등)
   - SaaS 제품으로 발전

---

**즐거운 학습 되세요!** 📚✨

궁금한 점은 GitHub Issues에 남겨주세요!
