"""
database.py - DB 연결 설정

역할:
  - SQLAlchemy Engine 생성 (DB 커넥션 풀 관리)
  - SessionLocal 팩토리 생성 (각 요청마다 독립된 DB 세션 제공)
  - Base 선언 (모든 모델의 부모 클래스)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL 연결 URL
# 형식: postgresql://<user>:<password>@<host>:<port>/<database>
DATABASE_URL = "postgresql://postgres:password@localhost:5432/resource_db"

# Engine: DB와의 실제 연결을 관리하는 핵심 객체
# - pool_size: 커넥션 풀 크기
# - echo: True로 설정하면 실행되는 SQL을 콘솔에 출력 (디버깅용)
engine = create_engine(DATABASE_URL, pool_size=5, echo=True)

# SessionLocal: DB 세션 팩토리
# - autocommit=False: 명시적으로 commit() 호출 필요
# - autoflush=False: 명시적으로 flush() 호출 필요 (예측 가능한 동작)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: 모든 ORM 모델이 상속받는 베이스 클래스
# Alembic이 이 Base.metadata를 읽어서 마이그레이션 스크립트를 자동 생성함
Base = declarative_base()


def get_db():
    """
    DB 세션을 생성하고 반환하는 제너레이터.
    사용 후 반드시 close()하여 커넥션을 풀에 반환.

    사용 예시:
        db = next(get_db())
        try:
            # DB 작업
        finally:
            db.close()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
