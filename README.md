# Resource Pool - SQLAlchemy + Alembic 예제 프로젝트

---

## 1. Alembic이란?

Alembic은 SQLAlchemy용 **DB 마이그레이션(스키마 버전 관리) 도구**입니다.

| 개념               | 설명                                     |
|------------------|----------------------------------------|
| **마이그레이션**       | DB 스키마 변경을 코드로 기록한 것 (Git의 commit과 유사) |
| **revision**     | 하나의 마이그레이션 단위 (고유 해시 ID 보유)            |
| **upgrade**      | 스키마를 최신 버전으로 올림                        |
| **downgrade**    | 스키마를 이전 버전으로 되돌림                       |
| **autogenerate** | 모델과 실제 DB를 비교하여 차이를 자동 감지              |

---

## 2. SQLAlchemy와 Alembic의 관계

```
┌──────────────────────────────────┐
│         models.py                │
│  class ResourcePool(Base):       │  ← SQLAlchemy가 모델 정의
│      resource_id = Column(...)   │
│      name = Column(...)          │
└──────────┬───────────────────────┘
           │
           │  Base.metadata (테이블 정보)
           ▼
┌──────────────────────────────────┐
│       alembic/env.py             │
│  target_metadata = Base.metadata │  ← Alembic이 메타데이터를 읽음
└──────────┬───────────────────────┘
           │
           │  autogenerate로 비교
           ▼
┌──────────────────────────────────┐
│  alembic/versions/               │
│  xxxx_create_resource_pool.py    │  ← 마이그레이션 스크립트 생성
│  xxxx_add_status_column.py       │
└──────────┬───────────────────────┘
           │
           │  alembic upgrade head
           ▼
┌──────────────────────────────────┐
│       PostgreSQL DB              │  ← 실제 DB에 반영
│  resource_pool 테이블             │
└──────────────────────────────────┘
```

---

## 3. 파일별 역할 요약

| 파일                      | 역할                                           |
|-------------------------|----------------------------------------------|
| `database.py`           | DB 연결(Engine), 세션(SessionLocal), Base 클래스 정의 |
| `models.py`             | ORM 모델 정의 → Alembic이 이 모델을 기준으로 마이그레이션 생성    |
| `resource_pool.py`      | CRUD 비즈니스 로직 (get, create, modify, delete)   |
| `alembic.ini`           | Alembic 설정 (DB URL, 로깅 등)                    |
| `alembic/env.py`        | Alembic이 SQLAlchemy 모델을 인식하도록 연결하는 핵심 파일     |
| `alembic/versions/*.py` | 각 마이그레이션 스크립트 (upgrade/downgrade 함수 포함)      |

---

## 4. Alembic 사용법 (명령어)

### 초기 설정 (최초 1회)

```bash
pip install sqlalchemy alembic psycopg2-binary

# 프로젝트 디렉토리에서 Alembic 초기화
# (이 예제에서는 이미 구조가 만들어져 있음)
alembic init alembic
```

### 마이그레이션 워크플로우

```bash
# ① 모델 변경 감지 → 마이그레이션 스크립트 자동 생성
alembic revision --autogenerate -m "create resource_pool table"

# ② 생성된 스크립트 확인 (alembic/versions/ 디렉토리)
#    → upgrade()와 downgrade() 함수가 올바른지 반드시 확인!

# ③ 마이그레이션 실행 (DB에 반영)
alembic upgrade head          # 최신 버전까지 전부 적용
alembic upgrade +1            # 한 단계만 적용

# ④ 롤백 (되돌리기)
alembic downgrade -1          # 한 단계 되돌리기
alembic downgrade base        # 전부 되돌리기 (초기 상태)

# ⑤ 현재 상태 확인
alembic current               # 현재 DB가 어느 revision인지
alembic history               # 전체 마이그레이션 이력
```

---

## 5. 스키마 변경 실전 예시

### 시나리오: `status` 컬럼을 추가하고 싶다

**Step 1)** `models.py`에 컬럼 추가:

```python
class ResourcePool(Base):
    __tablename__ = "resource_pool"
    # ... 기존 컬럼들 ...
    status = Column(String(50), nullable=False, server_default="active")  # ← 추가
```

**Step 2)** 마이그레이션 자동 생성:

```bash
alembic revision --autogenerate -m "add status column"
```

→ Alembic이 models.py와 실제 DB를 비교하여 `add_column` 스크립트를 자동 생성

**Step 3)** 생성된 스크립트 확인 후 적용:

```bash
alembic upgrade head
```

### Alembic이 자동 감지하는 변경 사항:

- 테이블 추가/삭제
- 컬럼 추가/삭제
- 인덱스, 외래키 추가/삭제
- 컬럼 타입 변경 (일부)

### Alembic이 자동 감지하지 못하는 것 (수동 작성 필요):

- 테이블/컬럼 이름 변경 (rename)
- 기존 데이터 마이그레이션 (data migration)
- 컬럼 순서 변경

---

## 6. 설치 및 실행

```bash
# 의존성 설치
pip install sqlalchemy alembic psycopg2-binary

# PostgreSQL DB 생성
createdb resource_db

# 마이그레이션 실행 (테이블 생성)
cd resource_pool_project
alembic upgrade head

# CRUD 테스트
python resource_pool.py
```
