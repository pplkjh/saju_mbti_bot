# 🚀 빠른 시작 가이드

## ⚡ 5분 만에 시작하기

### 1️⃣ OpenAI API 키 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집 (원하는 에디터 사용)
nano .env  # 또는 vim .env
```

`.env` 파일 내용:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
PORT=8000
API_URL=http://localhost:8000
```

### 2️⃣ 백엔드 실행

```bash
# 의존성 설치
cd backend
pip install -r requirements.txt

# PDF 벡터 스토어 생성 (최초 1회, 약 2-3분 소요)
cd ..
python scripts/build_vector_store.py

# 백엔드 서버 실행
cd backend
python main.py
```

✅ 백엔드가 http://localhost:8000 에서 실행됩니다.

### 3️⃣ 프론트엔드 실행 (새 터미널)

```bash
# 의존성 설치
cd frontend
pip install -r requirements.txt

# Streamlit 앱 실행
streamlit run app.py
```

✅ 프론트엔드가 http://localhost:8501 에서 자동으로 열립니다!

---

## 🐳 Docker로 실행하기 (선택사항)

```bash
# 백엔드 이미지 빌드
docker build -t saju-backend -f backend/Dockerfile .

# 컨테이너 실행
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-key-here \
  saju-backend
```

---

## 🔍 테스트

### API 테스트

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-05-21",
    "birth_time": "14:30",
    "gender": "여성",
    "name": "테스트",
    "mbti": "INFJ"
  }'
```

### API 문서 확인

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## ⚠️ 문제 해결

### OpenAI API 키 오류
```
❌ OPENAI_API_KEY environment variable not set!
```
→ `.env` 파일에 API 키가 제대로 설정되었는지 확인

### 포트 충돌
```
❌ Address already in use
```
→ `.env` 파일에서 PORT 변경

### 벡터 스토어 오류
```
⚠️ Vector store not found
```
→ `python scripts/build_vector_store.py` 실행

---

## 💡 다음 단계

1. ✅ 로컬에서 정상 작동 확인
2. 📱 UI 커스터마이징 (frontend/app.py)
3. 🚀 Railway/Vercel에 배포
4. 📊 사용자 피드백 수집
5. 🎨 모바일 앱 개발

---

**즐거운 개발 되세요!** 🎉
