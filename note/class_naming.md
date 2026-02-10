## Class Naming 제안

호출 흐름과 각 계층의 역할을 고려하면 **Repository 패턴**이 가장 적합합니다.

| # | Class Name | 역할 |
|---|---|---|
| 1 | `ResourcePoolDBService` | WF가 호출하는 **비즈니스 로직 계층** |
| 2 | `ResourcePoolRepository` | DB 구현체를 추상화하는 **인터페이스 계층** (ABC) |
| 3 | `ResourcePoolPostgreSQLRepository` | 실제 쿼리를 수행하는 **구현 계층** |

```
WF ──→ ResourcePoolDBService ──→ ResourcePoolRepository (interface)
                                          │
                                 ResourcePoolPostgreSQLRepository (impl)
```

**선정 이유:**

- **Service** — WF 입장에서 DB 관련 기능을 제공하는 서비스 객체임을 명확히 표현. `Manager`나 `Handler`보다 계층 구조에서의 역할이 분명합니다.
- **Repository** — DB 접근을 추상화하는 패턴으로 업계 표준 네이밍. 인터페이스와 구현체가 동일한 suffix를 공유하면 "같은 계약의 추상/구현" 관계가 직관적으로 드러납니다.

> 향후 MySQL 등 다른 DB를 지원할 때 `ResourcePoolMySQLRepository`만 추가하면 되므로 확장성도 확보됩니다.
