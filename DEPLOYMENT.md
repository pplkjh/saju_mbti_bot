# 🚀 배포 가이드

## 📋 배포 옵션 비교

| 옵션 | 비용 | 난이도 | 추천 용도 |
|------|------|--------|-----------|
| **Railway** | $5-20/월 | ⭐ 쉬움 | MVP, 초기 런칭 |
| **Render** | $7-25/월 | ⭐ 쉬움 | 소규모 서비스 |
| **Vercel + Railway** | $5-15/월 | ⭐⭐ 중간 | 프론트/백엔드 분리 |
| **AWS (EC2/Lambda)** | $10-50/월 | ⭐⭐⭐ 어려움 | 확장 필요시 |
| **GCP/Azure** | $10-50/월 | ⭐⭐⭐ 어려움 | 엔터프라이즈 |

---

## 1️⃣ Railway 배포 (추천)

### 왜 Railway?
- ✅ 가장 간단한 배포
- ✅ GitHub 연동 자동 배포
- ✅ 무료 $5 크레딧 (첫 달)
- ✅ 환경 변수 관리 쉬움

### 배포 단계

#### 1. Railway 계정 생성
https://railway.app 에서 GitHub로 로그인

#### 2. 새 프로젝트 생성
```
Dashboard → New Project → Deploy from GitHub repo
→ saju_mbti_bot 선택
```

#### 3. 환경 변수 설정
```
Settings → Variables → Add Variable
```

필수 환경 변수:
```env
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL=gpt-3.5-turbo
PORT=8000
```

#### 4. 벡터 스토어 업로드 (중요!)

로컬에서 벡터 스토어 생성:
```bash
python scripts/build_vector_store.py
```

Railway에 업로드:
```bash
# Railway CLI 설치
npm i -g @railway/cli

# 로그인
railway login

# 프로젝트 연결
railway link

# 벡터 스토어 업로드
railway up --service backend
```

또는 수동으로:
1. `data/vector_store/` 폴더를 압축
2. Railway Volume에 업로드
3. 백엔드 서비스에 마운트

#### 5. 배포 확인
```
Deployments → 최신 배포 클릭 → Logs 확인
✅ "API is ready!" 메시지 확인
```

#### 6. 도메인 확인
```
Settings → Domains → Generate Domain
예: saju-mbti-production.up.railway.app
```

---

## 2️⃣ Render 배포

### 1. Render 계정 생성
https://render.com 에서 GitHub로 로그인

### 2. Web Service 생성
```
New → Web Service → Connect GitHub repo
→ saju_mbti_bot 선택
```

### 3. 설정
```yaml
Name: saju-mbti-backend
Environment: Python 3
Build Command: cd backend && pip install -r requirements.txt
Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 4. 환경 변수
```env
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-3.5-turbo
```

### 5. 벡터 스토어 설정
Render Disk 사용:
```
Settings → Disks → Add Disk
Name: vector-store
Mount Path: /opt/render/project/src/data/vector_store
Size: 1GB
```

---

## 3️⃣ Vercel (프론트엔드) + Railway (백엔드)

### 프론트엔드 → Vercel

#### 1. Streamlit을 Next.js로 변환 (선택사항)
또는 Streamlit Cloud 사용:

```
https://streamlit.io/cloud
→ Deploy an app
→ GitHub repo 연결
→ frontend/app.py 선택
```

환경 변수:
```env
API_URL=https://your-railway-backend.up.railway.app
```

### 백엔드 → Railway
위의 Railway 가이드 참조

---

## 4️⃣ AWS 배포 (고급)

### 옵션 A: EC2

```bash
# EC2 인스턴스 접속
ssh -i key.pem ubuntu@your-ec2-ip

# 프로젝트 클론
git clone https://github.com/pplkjh/saju_mbti_bot.git
cd saju_mbti_bot

# 의존성 설치
cd backend
pip install -r requirements.txt

# 벡터 스토어 생성
cd ..
python scripts/build_vector_store.py

# PM2로 백엔드 실행
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name saju-backend
```

### 옵션 B: Lambda + API Gateway (서버리스)

1. Zappa 사용:
```bash
pip install zappa
zappa init
zappa deploy production
```

2. 환경 변수 설정
3. API Gateway 도메인 설정

---

## 📊 배포 후 확인 사항

### ✅ 체크리스트

- [ ] API 엔드포인트 정상 작동
  ```bash
  curl https://your-domain.com/api/v1/health
  ```

- [ ] OpenAI API 키 작동 확인
  ```bash
  curl -X POST https://your-domain.com/api/v1/analyze \
    -H "Content-Type: application/json" \
    -d '{"birth_date":"1990-01-01","birth_time":"12:00","gender":"남성","name":"테스트","mbti":"INFP"}'
  ```

- [ ] 벡터 스토어 로드 확인 (로그 확인)
  ```
  ✅ Vector store loaded successfully
  ```

- [ ] 프론트엔드 → 백엔드 연결 확인

- [ ] HTTPS 적용 (자동)

- [ ] 커스텀 도메인 연결 (선택)

---

## 🔒 보안 설정

### 환경 변수 보호
```bash
# 절대 Git에 커밋하지 말 것!
.env
.env.local
.env.production
```

### CORS 설정 (프로덕션)
`backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # 특정 도메인만
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Rate Limiting 추가 (선택)
```bash
pip install slowapi

# main.py에 추가
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/v1/analyze")
@limiter.limit("10/minute")  # 분당 10회 제한
async def analyze_saju_mbti(request: Request, ...):
    ...
```

---

## 💰 비용 최적화

### OpenAI API 비용 절감

1. **모델 선택**:
   - GPT-3.5-turbo: $0.002/1K tokens
   - GPT-4: $0.03/1K tokens
   → GPT-3.5로 시작

2. **캐싱 전략**:
   ```python
   # Redis 캐싱 추가
   # 동일한 생년월일+MBTI는 캐시에서 반환
   ```

3. **토큰 최적화**:
   - max_tokens 제한 (2000 → 1500)
   - 시스템 프롬프트 간소화

### 인프라 비용 절감

1. **무료 티어 활용**:
   - Railway: $5 크레딧/월
   - Render: 750시간/월 무료
   - Vercel: 무료 (취미 프로젝트)

2. **오토 스케일링 설정**:
   - 사용량 적을 때 인스턴스 축소

---

## 📈 모니터링 & 로깅

### Railway 로그 확인
```bash
railway logs --service backend
```

### Sentry 에러 추적 (선택)
```bash
pip install sentry-sdk

# main.py
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

### Uptime 모니터링
- UptimeRobot (무료): https://uptimerobot.com
- Pingdom
- 헬스체크 엔드포인트: `/api/v1/health`

---

## 🎯 다음 단계

배포 완료 후:

1. **DNS 설정**: 커스텀 도메인 연결
2. **SSL 인증서**: 자동으로 생성됨 (Let's Encrypt)
3. **사용자 피드백**: 분석 품질 개선
4. **A/B 테스팅**: 다양한 프롬프트 실험
5. **모바일 앱**: API 연동

---

## 💡 문제 해결

### 벡터 스토어 로드 실패
```
⚠️ Vector store not found
```
→ Railway Volume에 벡터 스토어 업로드 확인

### OpenAI API 오류
```
❌ Invalid API key
```
→ 환경 변수에 올바른 키 설정 확인

### 메모리 부족
```
❌ MemoryError
```
→ Railway Plan 업그레이드 (8GB RAM)

---

**배포 성공을 기원합니다!** 🚀
