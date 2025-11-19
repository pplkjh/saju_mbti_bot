"""
FastAPI backend for Saju & MBTI Analysis Service
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
import os

from models.schemas import AnalysisRequest, AnalysisResponse, HealthResponse
from services.saju_analyzer import saju_analyzer
from services.vector_store import vector_store_service

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI 앱 초기화
app = FastAPI(
    title="사주 & MBTI 분석 API",
    description="생년월일과 MBTI를 기반으로 사주와 성격을 분석하는 API",
    version="1.0.0"
)

# CORS 설정 (프론트엔드 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """서버 시작 시 벡터 스토어 로드"""
    logger.info("🚀 Starting Saju & MBTI Analysis API...")

    # 벡터 스토어 로드 시도
    vector_store_loaded = vector_store_service.load()

    if vector_store_loaded:
        logger.info("✅ Vector store loaded successfully")
    else:
        logger.warning("⚠️ Vector store not found - will proceed without context documents")

    logger.info("✅ API is ready!")


@app.get("/", response_model=HealthResponse)
async def health_check():
    """서버 상태 확인"""
    return HealthResponse(
        status="healthy",
        message="사주 & MBTI 분석 API가 정상 작동 중입니다.",
        vector_store_loaded=vector_store_service.is_loaded()
    )


@app.post("/api/v1/analyze", response_model=AnalysisResponse)
async def analyze_saju_mbti(request: AnalysisRequest):
    """
    사주와 MBTI 복합 분석 API

    생년월일, 출생 시간, 성별, 이름, MBTI를 입력받아
    사주와 MBTI를 종합적으로 분석한 결과를 반환합니다.
    """
    try:
        logger.info(f"📨 Analysis request received: {request.name} ({request.mbti})")

        # 분석 수행
        result = await saju_analyzer.analyze(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            gender=request.gender,
            name=request.name,
            mbti=request.mbti
        )

        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["result"])

        return AnalysisResponse(
            success=True,
            result=result["result"],
            timestamp=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"분석 중 오류가 발생했습니다: {str(e)}")


@app.get("/api/v1/health")
async def api_health():
    """API 상태 확인 (간단 버전)"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "vector_store": "loaded" if vector_store_service.is_loaded() else "not loaded"
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
