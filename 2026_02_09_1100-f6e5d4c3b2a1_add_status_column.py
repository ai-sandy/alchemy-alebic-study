"""add status column to resource_pool

Revision ID: f6e5d4c3b2a1
Revises: a1b2c3d4e5f6
Create Date: 2026-02-09 11:00:00.000000

이 파일은 models.py에 새 컬럼을 추가한 후
alembic revision --autogenerate -m "add status column" 실행 시 생성되는 예시입니다.

★ 스키마 변경 흐름:
  1. models.py에서 ResourcePool 클래스에 status 컬럼 추가
  2. alembic revision --autogenerate -m "add status column" 실행
  3. Alembic이 모델과 실제 DB를 비교하여 차이점 감지
  4. 이 마이그레이션 파일 자동 생성
  5. alembic upgrade head 로 DB에 반영
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "f6e5d4c3b2a1"
down_revision: Union[str, None] = "a1b2c3d4e5f6"  # ← 이전 마이그레이션을 가리킴 (체인)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """status 컬럼 추가"""
    op.add_column(
        "resource_pool",
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="active",
            comment="풀 상태 (active/inactive/maintenance)",
        ),
    )


def downgrade() -> None:
    """status 컬럼 제거"""
    op.drop_column("resource_pool", "status")
