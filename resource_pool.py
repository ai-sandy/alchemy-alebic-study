"""
resource_pool.py - Resource Pool CRUD 함수

역할:
  - get_resource_pool_info : 단건/전체 조회
  - create                 : 신규 리소스 풀 생성
  - modify                 : 기존 리소스 풀 수정
  - delete                 : 리소스 풀 삭제

모든 함수는 SQLAlchemy Session 객체를 받아서 동작하며,
트랜잭션 관리(commit/rollback)를 내부에서 처리합니다.
"""

from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import ResourcePool


# ──────────────────────────────────────────────
# 1. 조회 (Read)
# ──────────────────────────────────────────────
def get_resource_pool_info(
        db: Session,
        resource_id: Optional[int] = None,
        name: Optional[str] = None,
) -> list[dict] | dict | None:
    """
    리소스 풀 정보를 조회합니다.

    Args:
        db          : SQLAlchemy DB 세션
        resource_id : 특정 ID로 조회 (단건)
        name        : 특정 이름으로 조회 (단건)
        (둘 다 None이면 전체 조회)

    Returns:
        dict       : 단건 조회 결과
        list[dict] : 전체 조회 결과
        None       : 조회 결과 없음
    """
    # ID로 단건 조회
    if resource_id is not None:
        pool = db.query(ResourcePool).filter(
            ResourcePool.resource_id == resource_id
        ).first()
        return pool.to_dict() if pool else None

    # 이름으로 단건 조회
    if name is not None:
        pool = db.query(ResourcePool).filter(
            ResourcePool.name == name
        ).first()
        return pool.to_dict() if pool else None

    # 전체 조회
    pools = db.query(ResourcePool).order_by(ResourcePool.resource_id).all()
    return [p.to_dict() for p in pools]


# ──────────────────────────────────────────────
# 2. 생성 (Create)
# ──────────────────────────────────────────────
def create(
        db: Session,
        name: str,
        pool_range: str,
        description: Optional[str] = None,
) -> dict:
    """
    새 리소스 풀을 생성합니다.

    Args:
        db          : SQLAlchemy DB 세션
        name        : 리소스 풀 이름 (unique)
        pool_range  : 풀 범위 문자열
        description : 설명 (선택)

    Returns:
        dict : 생성된 리소스 풀 정보

    Raises:
        ValueError    : 중복 이름 등 무결성 위반 시
        RuntimeError  : 기타 DB 오류 시
    """
    new_pool = ResourcePool(
        name=name,
        description=description,
        pool_range=pool_range,
    )

    try:
        db.add(new_pool)  # 세션에 추가 (INSERT 준비)
        db.commit()  # 트랜잭션 커밋 (실제 DB 반영)
        db.refresh(new_pool)  # DB에서 자동 생성된 값(id, created_at 등) 다시 로드
        return new_pool.to_dict()

    except IntegrityError as e:
        db.rollback()  # 실패 시 트랜잭션 롤백
        raise ValueError(f"리소스 풀 생성 실패 (중복 이름 등): {e.orig}") from e

    except Exception as e:
        db.rollback()
        raise RuntimeError(f"리소스 풀 생성 중 오류 발생: {e}") from e


# ──────────────────────────────────────────────
# 3. 수정 (Update)
# ──────────────────────────────────────────────
def modify(
        db: Session,
        resource_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        pool_range: Optional[str] = None,
) -> dict | None:
    """
    기존 리소스 풀 정보를 수정합니다.

    Args:
        db          : SQLAlchemy DB 세션
        resource_id : 수정할 리소스 ID (필수)
        name        : 변경할 이름 (선택)
        description : 변경할 설명 (선택)
        pool_range  : 변경할 범위 (선택)

    Returns:
        dict : 수정된 리소스 풀 정보
        None : 해당 ID가 존재하지 않을 때
    """
    pool = db.query(ResourcePool).filter(
        ResourcePool.resource_id == resource_id
    ).first()

    if pool is None:
        return None

    # 전달된 값만 업데이트 (None이 아닌 필드만)
    if name is not None:
        pool.name = name
    if description is not None:
        pool.description = description
    if pool_range is not None:
        pool.pool_range = pool_range

    try:
        db.commit()
        db.refresh(pool)
        return pool.to_dict()

    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"리소스 풀 수정 실패: {e.orig}") from e

    except Exception as e:
        db.rollback()
        raise RuntimeError(f"리소스 풀 수정 중 오류 발생: {e}") from e


# ──────────────────────────────────────────────
# 4. 삭제 (Delete)
# ──────────────────────────────────────────────
def delete(db: Session, resource_id: int) -> bool:
    """
    리소스 풀을 삭제합니다.

    Args:
        db          : SQLAlchemy DB 세션
        resource_id : 삭제할 리소스 ID

    Returns:
        True  : 삭제 성공
        False : 해당 ID가 존재하지 않음
    """
    pool = db.query(ResourcePool).filter(
        ResourcePool.resource_id == resource_id
    ).first()

    if pool is None:
        return False

    try:
        db.delete(pool)
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        raise RuntimeError(f"리소스 풀 삭제 중 오류 발생: {e}") from e


# ──────────────────────────────────────────────
# 사용 예시 (standalone 실행 시)
# ──────────────────────────────────────────────
if __name__ == "__main__":
    from database import get_db

    db = next(get_db())

    try:
        # 1) 생성
        result = create(db, name="GPU Pool A", pool_range="1-50", description="GPU 리소스 풀")
        print(f"[CREATE] {result}")

        # 2) 조회 (단건)
        info = get_resource_pool_info(db, resource_id=result["resource_id"])
        print(f"[GET]    {info}")

        # 3) 수정
        updated = modify(db, resource_id=result["resource_id"], pool_range="1-100")
        print(f"[MODIFY] {updated}")

        # 4) 전체 조회
        all_pools = get_resource_pool_info(db)
        print(f"[ALL]    {all_pools}")

        # 5) 삭제
        deleted = delete(db, resource_id=result["resource_id"])
        print(f"[DELETE] success={deleted}")

    finally:
        db.close()
