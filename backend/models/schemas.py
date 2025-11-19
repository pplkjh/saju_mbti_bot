"""
Pydantic models for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AnalysisRequest(BaseModel):
    """사주 MBTI 분석 요청 모델"""
    birth_date: str = Field(..., description="생년월일 (YYYY-MM-DD)", example="1990-05-21")
    birth_time: str = Field(..., description="출생 시간 (HH:MM)", example="14:30")
    gender: str = Field(..., description="성별 (남성/여성)", example="여성")
    name: str = Field(..., description="이름", example="홍길동")
    mbti: str = Field(..., description="MBTI 유형", example="INFJ")

    class Config:
        schema_extra = {
            "example": {
                "birth_date": "1990-05-21",
                "birth_time": "14:30",
                "gender": "여성",
                "name": "홍길동",
                "mbti": "INFJ"
            }
        }


class AnalysisResponse(BaseModel):
    """사주 MBTI 분석 응답 모델"""
    success: bool
    result: str
    timestamp: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "result": "홍길동님의 사주와 MBTI 분석 결과...",
                "timestamp": "2025-01-19T10:30:00"
            }
        }


class HealthResponse(BaseModel):
    """서버 상태 응답 모델"""
    status: str
    message: str
    vector_store_loaded: bool
