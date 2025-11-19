"""
PDF 문서를 벡터화하여 FAISS 벡터 스토어 생성

사용법:
    python scripts/build_vector_store.py
"""
import os
import sys
from pathlib import Path

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import logging

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path: str) -> str:
    """PDF에서 텍스트 추출"""
    logger.info(f"📄 Reading PDF: {pdf_path}")

    try:
        document = fitz.open(pdf_path)
        text = ""

        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()

        logger.info(f"✅ Extracted {len(text)} characters from {pdf_path}")
        return text

    except Exception as e:
        logger.error(f"❌ Failed to read {pdf_path}: {e}")
        return ""


def build_vector_store():
    """PDF 문서들을 읽어서 벡터 스토어 생성"""

    # PDF 파일 목록
    pdf_dir = project_root / "data"
    pdf_files = [
        "사주 명리 일주론과 MBTI성격유형의 상호보완성에 관한 연구.pdf",
        "사주 명리학의 8가지 성격유형과 MBTI기능별 8가지 성격유형의 상관연구.pdf",
        "사주명리학을 통한 성격.pdf",
        "사주명리학의 8가지 성격유형과 MBTI 기능별 8가지 성격유형의 상관연구.pdf",
        "사주와 MBTI 성격이론과의 상관관계 연구.pdf",
        "사주의 오행분포가 성격형성에 미치는 영향.pdf",
        "역과+명리학.pdf"
    ]

    logger.info("🚀 Starting vector store build process...")

    # 1. 모든 PDF에서 텍스트 추출
    all_texts = []
    for pdf_file in pdf_files:
        pdf_path = pdf_dir / pdf_file
        if pdf_path.exists():
            text = extract_text_from_pdf(str(pdf_path))
            if text:
                all_texts.append(text)
        else:
            logger.warning(f"⚠️ PDF not found: {pdf_path}")

    if not all_texts:
        logger.error("❌ No PDF documents found!")
        return False

    logger.info(f"📚 Total {len(all_texts)} PDF documents loaded")

    # 2. 텍스트를 청크로 분할
    logger.info("✂️ Splitting documents into chunks...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    chunks = []
    for i, text in enumerate(all_texts):
        doc_chunks = text_splitter.split_text(text)
        chunks.extend(doc_chunks)
        logger.info(f"  - Document {i+1}: {len(doc_chunks)} chunks")

    logger.info(f"✅ Total {len(chunks)} chunks created")

    # 3. OpenAI 임베딩으로 벡터화
    logger.info("🔄 Creating embeddings (this may take a few minutes)...")

    try:
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_texts(chunks, embeddings)

        logger.info("✅ Embeddings created successfully")

    except Exception as e:
        logger.error(f"❌ Failed to create embeddings: {e}")
        return False

    # 4. 벡터 스토어 저장
    output_dir = project_root / "data" / "vector_store"
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"💾 Saving vector store to {output_dir}...")

    try:
        vectorstore.save_local(str(output_dir))
        logger.info("✅ Vector store saved successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to save vector store: {e}")
        return False


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("📦 Saju & MBTI Vector Store Builder")
    logger.info("=" * 60)

    # OpenAI API 키 확인
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("❌ OPENAI_API_KEY environment variable not set!")
        logger.error("   Please set it in .env file or export it")
        sys.exit(1)

    # 벡터 스토어 빌드
    success = build_vector_store()

    if success:
        logger.info("=" * 60)
        logger.info("🎉 Vector store build completed successfully!")
        logger.info("=" * 60)
        sys.exit(0)
    else:
        logger.error("=" * 60)
        logger.error("💥 Vector store build failed!")
        logger.error("=" * 60)
        sys.exit(1)
