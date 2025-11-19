# 🔧 문제해결 가이드

## 일반적인 문제와 해결 방법

---

## 목차

1. [설치 및 환경 설정](#설치-및-환경-설정)
2. [백엔드 문제](#백엔드-문제)
3. [프론트엔드 문제](#프론트엔드-문제)
4. [벡터 스토어 문제](#벡터-스토어-문제)
5. [배포 문제](#배포-문제)
6. [API 문제](#api-문제)
7. [성능 문제](#성능-문제)

---

## 설치 및 환경 설정

### ❌ 문제: `ModuleNotFoundError: No module named 'fastapi'`

**원인**: 필요한 패키지가 설치되지 않음

**해결 방법**:
```bash
cd backend
pip install -r requirements.txt
```

**여전히 안 된다면**:
```bash
# 가상환경 재생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### ❌ 문제: `OPENAI_API_KEY environment variable not set!`

**원인**: 환경 변수가 설정되지 않음

**해결 방법**:

**1단계**: `.env` 파일 생성
```bash
cp .env.example .env
```

**2단계**: `.env` 파일 편집
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

**3단계**: API 키 확인
```bash
# Linux/Mac
echo $OPENAI_API_KEY

# Windows
echo %OPENAI_API_KEY%
```

**4단계**: Python에서 확인
```python
import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("OPENAI_API_KEY"))
```

---

### ❌ 문제: `Permission denied` 에러

**원인**: 파일 권한 문제

**해결 방법**:
```bash
# Linux/Mac
chmod +x scripts/build_vector_store.py

# Windows
# 관리자 권한으로 실행
```

---

## 백엔드 문제

### ❌ 문제: `Address already in use` (포트 충돌)

**원인**: 8000번 포트가 이미 사용 중

**해결 방법 1**: 다른 포트 사용
```bash
# .env 파일 수정
PORT=8001

# 또는 직접 지정
uvicorn main:app --port 8001
```

**해결 방법 2**: 기존 프로세스 종료
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID번호> /F
```

---

### ❌ 문제: `Pydantic validation error`

**에러 메시지**:
```
detail: [
  {
    "loc": ["body", "birth_date"],
    "msg": "field required",
    "type": "value_error.missing"
  }
]
```

**원인**: API 요청에 필수 필드가 누락됨

**해결 방법**: 모든 필수 필드 포함
```json
{
  "birth_date": "1990-05-21",  // ✅ 필수
  "birth_time": "14:30",        // ✅ 필수
  "gender": "여성",              // ✅ 필수
  "name": "홍길동",              // ✅ 필수
  "mbti": "INFJ"                // ✅ 필수
}
```

---

### ❌ 문제: `OpenAI API timeout`

**에러 메시지**:
```
openai.error.Timeout: Request timed out
```

**원인**:
- 네트워크 문제
- OpenAI 서버 과부하
- 요청이 너무 큼

**해결 방법**:

**1. Timeout 늘리기**:
```python
# backend/services/llm_service.py

response = self.client.chat.completions.create(
    model=self.model,
    messages=[...],
    timeout=60  # 60초로 증가
)
```

**2. max_tokens 줄이기**:
```python
max_tokens=1500  # 2000 → 1500
```

**3. 재시도 로직 추가**:
```python
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        response = self.client.chat.completions.create(...)
        break
    except Exception as e:
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # 지수 백오프
        else:
            raise
```

---

### ❌ 문제: `OpenAI API rate limit exceeded`

**에러 메시지**:
```
Rate limit reached for requests
```

**원인**: API 호출 제한 초과

**해결 방법**:

**1. Rate Limiting 추가**:
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/analyze")
@limiter.limit("10/minute")  # 분당 10회 제한
async def analyze(...):
    pass
```

**2. 캐싱 구현**:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_analysis(birth_date, mbti):
    # 동일한 요청은 캐시에서 반환
    pass
```

**3. 사용량 확인**:
```
https://platform.openai.com/usage
```

---

## 프론트엔드 문제

### ❌ 문제: `ModuleNotFoundError: No module named 'streamlit'`

**해결 방법**:
```bash
cd frontend
pip install -r requirements.txt
```

---

### ❌ 문제: `Connection refused` (백엔드 연결 실패)

**원인**: 백엔드 서버가 실행되지 않음

**해결 방법**:

**1. 백엔드 실행 확인**:
```bash
curl http://localhost:8000/api/v1/health
```

**2. API_URL 확인**:
```python
# frontend/app.py
API_URL = os.getenv("API_URL", "http://localhost:8000")
```

**3. CORS 설정 확인**:
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 모두 허용
)
```

---

### ❌ 문제: Streamlit 화면이 깨짐

**원인**: 브라우저 캐시 문제

**해결 방법**:

**1. 캐시 지우기**:
```bash
streamlit cache clear
```

**2. 하드 리로드**:
- Chrome: `Ctrl + Shift + R` (Windows) / `Cmd + Shift + R` (Mac)

**3. 시크릿 모드에서 테스트**:
```
Ctrl + Shift + N (Chrome)
```

---

## 벡터 스토어 문제

### ❌ 문제: `Vector store not found`

**경고 메시지**:
```
⚠️ Vector store not found at data/vector_store
```

**원인**: 벡터 스토어가 생성되지 않음

**해결 방법**:

**1. 벡터 스토어 생성**:
```bash
python scripts/build_vector_store.py
```

**2. PDF 파일 확인**:
```bash
ls data/*.pdf
```

**3. OpenAI API 키 확인**:
```bash
echo $OPENAI_API_KEY
```

---

### ❌ 문제: `Error reading PDF`

**에러 메시지**:
```
❌ Failed to read document.pdf: [Errno 2] No such file or directory
```

**원인**: PDF 파일 경로 문제

**해결 방법**:

**1. PDF 파일 위치 확인**:
```bash
# data/ 폴더에 PDF가 있어야 함
ls -la data/*.pdf
```

**2. 경로 수정** (scripts/build_vector_store.py):
```python
pdf_dir = project_root / "data"  # 절대 경로 사용
```

---

### ❌ 문제: 벡터 스토어 빌드 중 메모리 부족

**에러 메시지**:
```
MemoryError: Unable to allocate array
```

**원인**: PDF가 너무 크거나 많음

**해결 방법**:

**1. chunk_size 늘리기**:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,  # 1000 → 1500
    chunk_overlap=150,
)
```

**2. PDF를 나눠서 처리**:
```python
# 한 번에 2개씩만 처리
for i in range(0, len(pdf_files), 2):
    batch = pdf_files[i:i+2]
    process_batch(batch)
```

---

## 배포 문제

### ❌ 문제: Railway 배포 실패

**에러**: `Build failed`

**해결 방법**:

**1. 로그 확인**:
```bash
railway logs
```

**2. 빌드 명령어 확인** (railway.json):
```json
{
  "build": {
    "buildCommand": "cd backend && pip install -r requirements.txt"
  }
}
```

**3. Python 버전 확인** (runtime.txt):
```
python-3.10.12
```

---

### ❌ 문제: 환경 변수가 배포 환경에서 작동 안 함

**원인**: Railway에 환경 변수 설정 안 됨

**해결 방법**:

**1. Railway 대시보드**:
```
Settings → Variables → Add Variable
```

**2. 필수 환경 변수**:
```
OPENAI_API_KEY=sk-prod-key-here
OPENAI_MODEL=gpt-3.5-turbo
PORT=$PORT  (자동 설정됨)
```

---

### ❌ 문제: 벡터 스토어가 배포 환경에서 로드 안 됨

**원인**: 벡터 스토어 파일이 배포되지 않음

**해결 방법**:

**옵션 1**: Railway Volume 사용
```bash
# 로컬에서 벡터 스토어 생성 후
railway volume create vector-store
railway volume upload vector-store ./data/vector_store
```

**옵션 2**: S3에 저장
```python
# 벡터 스토어를 S3에 업로드
import boto3

s3 = boto3.client('s3')
s3.upload_file('data/vector_store/index.faiss', 'my-bucket', 'vector_store/index.faiss')
```

**옵션 3**: 배포 시 빌드
```json
{
  "build": {
    "buildCommand": "pip install -r requirements.txt && python scripts/build_vector_store.py"
  }
}
```

---

## API 문제

### ❌ 문제: CORS 에러

**에러 메시지** (브라우저 콘솔):
```
Access to fetch at 'http://localhost:8000/api/v1/analyze' from origin 'http://localhost:8501'
has been blocked by CORS policy
```

**원인**: CORS 설정 문제

**해결 방법** (backend/main.py):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Streamlit
        "https://your-frontend.com",  # 프로덕션
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### ❌ 문제: `422 Unprocessable Entity`

**원인**: 요청 데이터 형식 오류

**해결 방법**:

**1. 날짜 형식 확인**:
```json
{
  "birth_date": "1990-05-21",  // ✅ YYYY-MM-DD
  // "birth_date": "21/05/1990"  // ❌ 잘못된 형식
}
```

**2. MBTI 형식 확인**:
```json
{
  "mbti": "INFJ"  // ✅ 대문자 4자리
  // "mbti": "infj"  // ❌ 소문자
  // "mbti": "IN"    // ❌ 2자리
}
```

---

## 성능 문제

### ❌ 문제: 분석이 너무 느림 (30초 이상)

**원인**:
- OpenAI API 응답 지연
- 벡터 검색 비효율

**해결 방법**:

**1. 벡터 검색 최적화**:
```python
# k 값 줄이기 (3 → 2)
docs = vectorstore.similarity_search(query, k=2)
```

**2. max_tokens 줄이기**:
```python
response = client.chat.completions.create(
    max_tokens=1000  # 2000 → 1000
)
```

**3. 비동기 처리 활용**:
```python
async def analyze_saju_mbti(...):
    # 벡터 검색과 LLM 호출을 병렬 처리
    import asyncio

    results = await asyncio.gather(
        search_vector_store(query),
        some_other_task()
    )
```

---

### ❌ 문제: 메모리 사용량이 높음

**원인**: 벡터 스토어가 메모리에 로드됨

**해결 방법**:

**1. 벡터 스토어 크기 줄이기**:
```python
# chunk 수 줄이기
chunks = chunks[:1000]  # 처음 1000개만
```

**2. 메모리 사용 모니터링**:
```python
import psutil

process = psutil.Process()
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024} MB")
```

**3. 가비지 컬렉션**:
```python
import gc

gc.collect()
```

---

## 디버깅 팁

### 로그 레벨 설정

**개발 환경** (.env):
```env
LOG_LEVEL=DEBUG
```

**프로덕션** (.env):
```env
LOG_LEVEL=INFO
```

**코드**:
```python
import logging

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

logger.debug("디버그 메시지")
logger.info("정보 메시지")
logger.warning("경고 메시지")
logger.error("에러 메시지")
```

---

### API 테스트 도구

**1. cURL**:
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"birth_date":"1990-05-21","birth_time":"14:30","gender":"여성","name":"테스트","mbti":"INFJ"}' \
  -v  # verbose 모드
```

**2. Postman**:
- https://www.postman.com/downloads/
- GUI로 쉽게 API 테스트

**3. HTTPie**:
```bash
pip install httpie

http POST localhost:8000/api/v1/analyze \
  birth_date="1990-05-21" \
  birth_time="14:30" \
  gender="여성" \
  name="테스트" \
  mbti="INFJ"
```

**4. Swagger UI**:
```
http://localhost:8000/docs
```

---

### Python 디버거 사용

**pdb 사용**:
```python
import pdb

def analyze(...):
    pdb.set_trace()  # 브레이크포인트
    result = process_data()
    return result
```

**VS Code 디버거**:
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

---

## 도움 요청하기

문제가 해결되지 않으면:

### 1. GitHub Issues

https://github.com/pplkjh/saju_mbti_bot/issues

다음 정보를 포함해주세요:
- **에러 메시지** (전체 스택 트레이스)
- **재현 방법** (단계별)
- **환경 정보**:
  ```bash
  python --version
  pip list
  # OS 정보
  ```

### 2. 로그 수집

```bash
# 백엔드 로그
python backend/main.py > backend.log 2>&1

# 프론트엔드 로그
streamlit run frontend/app.py > frontend.log 2>&1
```

### 3. 최소 재현 예제

문제를 재현하는 최소한의 코드:
```python
# minimal_reproduce.py
import requests

response = requests.post(
    "http://localhost:8000/api/v1/analyze",
    json={...}
)
print(response.status_code)
print(response.json())
```

---

## 체크리스트

문제 발생 시 다음을 확인하세요:

- [ ] 가상환경 활성화됨
- [ ] 모든 의존성 설치됨
- [ ] .env 파일 존재 및 API 키 설정됨
- [ ] 백엔드 서버 실행 중
- [ ] 벡터 스토어 생성됨
- [ ] 포트가 사용 가능함
- [ ] 인터넷 연결 정상
- [ ] OpenAI API 잔액 확인
- [ ] 로그 확인

---

**문제가 해결되셨기를 바랍니다!** 🎉

더 많은 도움이 필요하면 GitHub Issues에 문의해주세요.
