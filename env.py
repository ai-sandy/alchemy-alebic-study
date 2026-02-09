"""
alembic/env.py - Alembic 마이그레이션 환경 설정

역할:
  - SQLAlchemy 모델의 metadata를 Alembic에 연결
  - --autogenerate 시 모델 변경 사항을 자동 감지할 수 있게 함
  - 온라인/오프라인 마이그레이션 모드 지원

핵심 포인트:
  ★ target_metadata = Base.metadata 를 설정해야
    alembic revision --autogenerate 가 모델 변경을 감지할 수 있음
"""

import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# ─── 프로젝트 루트를 Python path에 추가 ───
# alembic/ 디렉토리 안에서 실행되므로, 상위 디렉토리를 path에 추가해야
# database.py, models.py를 import할 수 있음
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from database import Base  # noqa: E402

# alembic.ini 설정 읽기
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ★ 핵심: Alembic이 자동 감지할 메타데이터 설정
# Base.metadata에는 Base를 상속한 모든 모델의 테이블 정보가 담겨 있음
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    오프라인 모드: DB 연결 없이 SQL 스크립트만 생성
    사용 예: alembic upgrade head --sql > migration.sql
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    온라인 모드: DB에 직접 연결하여 마이그레이션 실행 (기본 모드)
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
