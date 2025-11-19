"""
Main service for Saju & MBTI analysis
"""
from typing import Dict, Any
from .vector_store import vector_store_service
from .llm_service import llm_service
import logging

logger = logging.getLogger(__name__)


class SajuAnalyzer:
    """사주 MBTI 분석기"""

    def __init__(self):
        self.vector_store = vector_store_service
        self.llm = llm_service

    async def analyze(
        self,
        birth_date: str,
        birth_time: str,
        gender: str,
        name: str,
        mbti: str
    ) -> Dict[str, Any]:
        """
        사주와 MBTI 복합 분석 수행

        Args:
            birth_date: 생년월일 (YYYY-MM-DD)
            birth_time: 출생 시간 (HH:MM)
            gender: 성별 (남성/여성)
            name: 이름
            mbti: MBTI 유형

        Returns:
            분석 결과 딕셔너리
        """
        try:
            logger.info(f"🔍 Starting analysis for {name} ({mbti})")

            # 1. 벡터 스토어에서 관련 문서 검색
            context_documents = []
            if self.vector_store.is_loaded():
                query = f"사주 MBTI {mbti} 성격 {gender} {birth_date}"
                context_documents = self.vector_store.search(query, k=3)
                logger.info(f"📚 Retrieved {len(context_documents)} context documents")
            else:
                logger.warning("⚠️ Vector store not loaded, proceeding without context")

            # 2. LLM으로 분석 생성
            analysis_result = self.llm.generate_analysis(
                birth_date=birth_date,
                birth_time=birth_time,
                gender=gender,
                name=name,
                mbti=mbti,
                context_documents=context_documents if context_documents else None
            )

            logger.info(f"✅ Analysis completed for {name}")

            return {
                "success": True,
                "result": analysis_result,
                "used_context": len(context_documents) > 0,
                "context_count": len(context_documents)
            }

        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}")
            return {
                "success": False,
                "result": f"분석 중 오류가 발생했습니다: {str(e)}",
                "used_context": False,
                "context_count": 0
            }


# 싱글톤 인스턴스
saju_analyzer = SajuAnalyzer()
