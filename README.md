# Mini MES - Automotive LED Head Lamp Manufacturing Execution System

## 프로젝트 소개

본 프로젝트는 **자동차 LED Head Lamp 제조 공정**을 관리하기 위한 Mini MES(Manufacturing Execution System)입니다.

자동차 헤드램프 생산 공정을 가정하여 원자재 입고부터 생산, 품질검사, 출하까지의 전 과정을 데이터베이스로 관리합니다.

또한 **LOT 기반 Traceability(이력 추적)** 기능을 구현하여 생산 이력을 관리하고, 불량 발생 시 원자재 LOT부터 완제품 출하까지 정방향 및 역방향 추적이 가능하도록 설계하였습니다.

본 프로젝트는 실제 제조업의 업무 흐름을 이해하고, 데이터베이스 모델링, SQL CRUD, 데이터 시각화 및 제조업 도메인 지식을 학습하는 것을 목표로 합니다.

---

# 프로젝트 목표

- 자동차 LED Head Lamp 생산 공정 이해
- 제조업 MES 시스템 구현
- LOT 기반 생산 이력 관리
- SQLite 데이터베이스 설계
- SQL CRUD 구현
- 생산 데이터 시각화
- 제조업 도메인 지식 습득

---

# 생산 제품

본 프로젝트에서는 총 4종의 LED Head Lamp를 생산합니다.

|제품코드|제품명|
|--------|-----------------------------|
|FG-HL100-L|LED Head Lamp Standard Left|
|FG-HL100-R|LED Head Lamp Standard Right|
|FG-HL200-L|LED Head Lamp Premium Left|
|FG-HL200-R|LED Head Lamp Premium Right|

Standard 모델과 Premium 모델은 서로 다른 BOM을 사용하도록 설계하였습니다.

---

# 주요 원자재

각 제품 생산에는 다음과 같은 원자재가 사용됩니다.

- LED Module
- PCB
- Lens
- Housing
- Reflector
- Heat Sink
- Wiring Harness

Premium 모델에는 추가적으로

- Cooling Fan

이 사용됩니다.

---

# 생산 공정

```text
원자재 입고
      │
      ▼
원자재 LOT 생성
      │
      ▼
BOM 확인
      │
      ▼
생산 작업지시
      │
      ▼
원자재 투입
      │
      ▼
LED Head Lamp 생산
      │
      ▼
완제품 LOT 생성
      │
      ▼
품질검사
      │
      ▼
출하
      │
      ▼
LOT 추적
```

---

# 주요 기능

## 기준정보 관리

- 품목(Item) 관리
- BOM 관리

## 작업지시 관리

- 생산 작업지시 등록
- 생산 목표 수량 관리
- 작업 상태 관리

## LOT 관리

- 원자재 LOT 관리
- 완제품 LOT 관리
- LOT별 현재 재고 관리

## 생산관리

- 생산 실적 등록
- 작업자 관리
- 설비 관리
- 생산 수량 관리

## 원자재 사용 관리

- 생산 시 사용된 원자재 LOT 기록
- 원자재 사용 수량 관리

## 품질관리

- 품질검사 등록
- 양품 / 불량 수량 관리
- 불량 사유 관리

## 출하관리

- 제품 출하 등록
- LOT별 출하 관리
- 거래처 관리

## LOT Traceability

### 정방향 추적

원자재 LOT

↓

생산

↓

품질검사

↓

출하

### 역방향 추적

출하 LOT

↓

품질검사

↓

생산

↓

사용된 원자재 LOT

---

# 데이터베이스 구성

프로젝트는 총 8개의 테이블로 구성됩니다.

- Item
- BOM
- LOT
- ProductionOrder
- Production
- ProductionMaterial
- Quality
- Shipment

---

# 데이터 시각화

Matplotlib / Seaborn을 이용하여 다음 정보를 시각화합니다.

- 일별 생산량
- 제품별 생산량
- 제품별 불량률
- 작업자별 생산량
- LOT별 재고 현황
- 품질검사 결과
- 출하 현황

---

# 사용 기술

- Python
- SQLite3
- Pandas
- Matplotlib
- Seaborn
- Streamlit

---

# 프로젝트를 통해 학습하는 내용

- 자동차 부품 제조 공정
- MES(Manufacturing Execution System)
- LOT Traceability
- 관계형 데이터베이스 모델링
- SQL CRUD
- 데이터 시각화
- 제조업 도메인 지식

---

# 향후 확장 기능

- 거래처 관리
- 창고 관리
- 설비 마스터 관리
- 작업자 관리
- 사용자 로그인
- 대시보드 고도화
- 설비 가동률 분석(OEE)
- LOT 단위 세분화 관리(개별 제품 Serial No.)
