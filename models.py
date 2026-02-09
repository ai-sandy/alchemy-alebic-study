"""
models.py - SQLAlchemy ORM 모델 정의

역할:
  - DB 테이블 스키마를 Python 클래스로 정의
  - Alembic이 이 모델을 기반으로 마이그레이션 스크립트를 자동 생성
  - 모델 변경 시 → alembic revision --autogenerate → alembic upgrade head
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from database import Base


class ResourcePool(Base):
    """
    resource_pool 테이블 모델

    Columns:
        resource_id  : PK, 자동 증가 정수
        name         : 리소스 풀 이름 (unique, not null)
        description  : 리소스 풀 설명 (nullable)
        pool_range   : 풀 범위 (예: "10.0.0.1-10.0.0.254", "1-100" 등)
        created_at   : 생성 시각 (자동)
        updated_at   : 수정 시각 (자동)
    """
    __tablename__ = "resource_pool"

    resource_id = Column(Integer, primary_key=True, autoincrement=True, comment="리소스 고유 ID")
    name = Column(String(255), unique=True, nullable=False, comment="리소스 풀 이름")
    description = Column(Text, nullable=True, comment="리소스 풀 설명")
    pool_range = Column(String(255), nullable=False, comment="풀 범위 (예: 1-100)")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성 시각")
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="수정 시각",
    )

    def __repr__(self):
        return (
            f"<ResourcePool(resource_id={self.resource_id}, "
            f"name='{self.name}', pool_range='{self.pool_range}')>"
        )

    def to_dict(self):
        """모델 인스턴스를 딕셔너리로 변환"""
        return {
            "resource_id": self.resource_id,
            "name": self.name,
            "description": self.description,
            "pool_range": self.pool_range,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None,
        }
