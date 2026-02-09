"""create resource_pool table

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2026-02-09 10:00:00.000000

이 파일은 alembic revision --autogenerate -m "create resource_pool table" 실행 시
자동 생성되는 마이그레이션 스크립트의 예시입니다.

역할:
  - upgrade()   : 테이블 생성 (alembic upgrade head 시 실행)
  - downgrade() : 테이블 삭제 (alembic downgrade -1 시 실행)
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# ─── 버전 식별자 ───
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = None  # 첫 번째 마이그레이션이므로 None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    스키마를 '다음 버전'으로 올림
    → resource_pool 테이블 생성
    """
    op.create_table(
        "resource_pool",
        sa.Column("resource_id", sa.Integer(), autoincrement=True, nullable=False, comment="리소스 고유 ID"),
        sa.Column("name", sa.String(length=255), nullable=False, comment="리소스 풀 이름"),
        sa.Column("description", sa.Text(), nullable=True, comment="리소스 풀 설명"),
        sa.Column("pool_range", sa.String(length=255), nullable=False, comment="풀 범위 (예: 1-100)"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), comment="생성 시각"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), comment="수정 시각"),
        sa.PrimaryKeyConstraint("resource_id"),
        sa.UniqueConstraint("name"),
    )


def downgrade() -> None:
    """
    스키마를 '이전 버전'으로 되돌림
    → resource_pool 테이블 삭제
    """
    op.drop_table("resource_pool")
