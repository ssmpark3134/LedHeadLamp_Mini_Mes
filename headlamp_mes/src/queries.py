from src.db import fetch_all, fetch_dataframe, fetch_one, execute
from datetime import datetime
# item 조회
def get_item_list():
    sql = """
        select * from item where is_active = 'Y' order by item_id;
    """
    return fetch_all(sql)
# item 등록
def insert_item(item_code, item_name, item_type,unit):
    sql = """
        insert into item(item_code, item_name, item_type, unit)
        values (?,?,?,?);
    """
    return execute(sql,(item_code, item_name, item_type,unit))
# item 수정
def update_item(item_id, item_name, item_type, unit):
    sql = """
        update item set item_name=?, item_type=?, unit=? where item_id=?;
    """
    return execute(sql,(item_name, item_type, unit, item_id))
# item 삭제(삭제라긴 보다는 사용안함으로 변경)
def deactivate_item(item_id):
    sql = """
        update item set is_active='N' where item_id=?;
    """
    return execute(sql,(item_id,))
# item 사용재개
def activate_item(item_id):
    sql="""
        update item set is_active='Y' where item_id=?;
    """
    return execute(sql,(item_id,))
# 사용 N인 제품만 보기
def get_reactivate_item_list():
    sql = """
        select * from item where is_active='N' order by item_id;
    """
    return fetch_all(sql)

# BOM
# 선택한 완제품에 어떤 원자재가 들어가는지 조회
def get_bom_by_product(product_item_id):

    sql = """
        SELECT
            b.bom_id,
            b.product_item_id,
            b.material_item_id,
            m.item_code AS material_code,
            m.item_name AS material_name,
            b.required_qty
        FROM bom b

        INNER JOIN item m
            ON b.material_item_id = m.item_id

        WHERE b.product_item_id = ?

        ORDER BY b.bom_id;
    """

    return fetch_all(
        sql,
        (product_item_id,)
    )
# 완제품(FG) 목록만 조회
def get_fg_item_list():
    sql = """
        select * from item where item_type='FG'
        and is_active = 'Y'
        order by item_id;
    """
    return fetch_all(sql)
# 원자재(RM) 목록만 조회
def get_rm_item_list():

    sql = """
        SELECT *
        FROM item
        WHERE item_type = 'RM'
          AND is_active = 'Y'
        ORDER BY item_id;
    """

    return fetch_all(sql)
# 선택한 완제품에 대한 원자재 등록
def insert_bom(product_item_id, materials):
    sql = """
        INSERT INTO bom (
            product_item_id,
            material_item_id,
            required_qty
        )
        VALUES (?, ?, ?);
    """
    from src.db import get_connection
    with get_connection() as connection:
        for material in materials:
            connection.execute(
                sql,
                (
                    product_item_id,
                    material["material_item_id"],
                    material["required_qty"]
                )
            )

        connection.commit()
# BOM 필요 수량 수정
def update_bom_qty(bom_id, required_qty):
    sql = """
        UPDATE bom
        SET required_qty = ?
        WHERE bom_id = ?;
    """
    return execute(
        sql,
        (
            required_qty,
            bom_id
        )
    )
# BOM 삭제
def delete_bom(bom_id):
    sql = """
        DELETE FROM bom
        WHERE bom_id = ?;
    """
    return execute(
        sql,
        (bom_id,)
    )

# ============================================
# lot관리
# ============================================
# 완제품 품목별 재고 조회
def get_fg_stock_list():
    # 완제품(FG)의 현재 재고를 품목별로 조회한다.
    # 하나의 완제품에 여러 LOT가 존재할 수 있으므로
    # 각 LOT의 current_qty를 합산한다.
    sql = """
        SELECT
            i.item_code,
            i.item_name,
            i.unit,
            SUM(l.current_qty) AS current_stock
        FROM item AS i
        JOIN lot AS l
            ON i.item_id = l.item_id
        WHERE i.item_type = 'FG'
        GROUP BY
            i.item_id,
            i.item_code,
            i.item_name,
            i.unit
        ORDER BY i.item_id;
    """
    return fetch_all(sql)
# ============================================
# 원자재 품목별 재고 조회
def get_rm_stock_list():
    # 원자재(RM)의 현재 재고를 품목별로 조회한다.
    # 하나의 원자재에 여러 LOT가 존재할 수 있으므로
    # 각 LOT의 current_qty를 합산한다.
    sql = """
        SELECT
            i.item_code,
            i.item_name,
            i.unit,
            SUM(l.current_qty) AS current_stock
        FROM item AS i
        JOIN lot AS l
            ON i.item_id = l.item_id
        WHERE i.item_type = 'RM'
        GROUP BY
            i.item_id,
            i.item_code,
            i.item_name,
            i.unit
        ORDER BY i.item_id
    """
    return fetch_all(sql)
# ============================================
# LOT 상세 목록 조회
def get_lot_list():
    # 전체 LOT 정보를 조회한다.
    # lot 테이블의 item_id를 이용해서
    # item 테이블과 JOIN한 뒤,
    # LOT 정보와 품목 정보를 함께 가져온다.
    sql = """
        SELECT
            l.lot_id,
            l.lot_no,
            i.item_code,
            i.item_name,
            i.item_type,
            i.unit,
            l.lot_qty,
            l.current_qty,
            l.received_date,
            l.produced_date,
            l.expire_date,
            l.location
        FROM lot AS l
        JOIN item AS i
            ON l.item_id = i.item_id
        ORDER BY i.item_code;
    """
    return fetch_all(sql)
# ============================================
# LOT 번호 자동 생성
def generate_lot_no(item_code):
    # 품목 코드와 오늘 날짜를 이용해서
    # 새로운 LOT 번호를 자동으로 생성한다.
    # 예:
    # RM-PCB-20260803-001
    # RM-PCB-20260803-002
    # 날짜 처리를 위해 datetime을 사용한다.

    # 오늘 날짜를 YYYYMMDD 형식으로 만든다.
    today = datetime.now().strftime("%Y%m%d")
    base_code = item_code.rsplit("-", 1)[0]
    # 오늘 날짜에 생성된 같은 품목의 LOT 개수를 조회한다.
    sql = """
        SELECT COUNT(*)
        FROM lot
        WHERE lot_no LIKE ?
    """
    # LOT 번호 검색용 앞부분을 만든다.
    prefix = f"{base_code}-{today}-%"
    # DB에서 해당 조건의 LOT 개수를 가져온다.
    result = fetch_one(
        sql,
        (prefix,)
    )
    # 조회 결과에서 개수를 가져온다.
    count = result[0] if result else 0
    # 다음에 사용할 순번을 만든다.
    sequence = count + 1
    # 최종 LOT 번호를 만든다.
    return f"{base_code}-{today}-{sequence:03d}"
# ============================================
# LOT 등록
def insert_lot(
    item_id,
    lot_qty,
    received_date=None,
    produced_date=None,
    expire_date=None,
    location=""
):
    # 새로운 LOT을 DB에 등록한다.
    # LOT 번호는 사용자가 입력하지 않고 품목 코드와 날짜를 기준으로 자동 생성한다.
    # item_id:
    #     LOT이 어떤 품목인지 나타내는 ID
    # lot_qty:
    #     LOT이 처음 생성될 때의 전체 수량
    # current_qty:
    #     처음 생성되는 LOT이므로
    #     lot_qty와 동일하게 저장한다.

    # 먼저 item_id에 해당하는 품목 정보를 조회한다.
    item_sql = """
        SELECT
            item_code
        FROM item
        WHERE item_id = ?
    """
    item = fetch_one(
        item_sql,
        (item_id,)
    )
    if item is None:
        raise ValueError("존재하지 않는 품목입니다.")
    # 품목 코드를 이용해서 LOT 번호를 자동 생성한다.
    lot_no = generate_lot_no(
        item["item_code"]
    )
    # 새 LOT을 DB에 저장한다.
    sql = """
        INSERT INTO lot (
            lot_no,
            item_id,
            lot_qty,
            current_qty,
            received_date,
            produced_date,
            expire_date,
            location
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    return execute(
        sql,
        (
            lot_no,
            item_id,
            lot_qty,
            lot_qty,
            received_date,
            produced_date,
            expire_date,
            location
        )
    )

# ============================================
# 생산지시 등록
# ============================================
def insert_production_order(
    product_item_id,
    order_qty,
    due_date
):
    # 새로운 생산지시를 등록한다.
    # 생산지시번호는 시스템에서 자동으로 생성한다.
    # product_item_id:
    #     생산할 완제품의 item_id
    # order_qty:
    #     생산 지시 수량
    # due_date:
    #     생산 완료 예정일
    # status:
    #     처음 등록되는 생산지시는 '대기' 상태로 저장한다.
    # 현재 날짜를 YYYYMMDD 형식으로 가져온다.
    today = datetime.now().strftime("%Y%m%d")
    # 오늘 생성된 생산지시 개수를 조회한다.
    sql = """
        SELECT COUNT(*)
        FROM production_order
        WHERE order_no LIKE ?
    """
    prefix = f"PO-{today}-%"
    result = fetch_one(
        sql,
        (prefix,)
    )
    count = result[0] if result else 0
    # 다음 생산지시 번호를 만든다.
    sequence = count + 1
    order_no = f"PO-{today}-{sequence:03d}"
    # 생산지시를 DB에 저장한다.
    sql = """
        INSERT INTO production_order (
            order_no,
            product_item_id,
            order_qty,
            due_date,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """
    return execute(
        sql,
        (
            order_no,
            product_item_id,
            order_qty,
            due_date,
            "대기"
        )
    )
# ============================================
# 생산지시 목록 조회
def get_production_order_list():
    # 등록된 생산지시 목록을 조회한다.
    # production_order의 product_item_id를
    # item 테이블과 연결해서 완제품 정보를 함께 가져온다.
    sql = """
        SELECT
            po.order_id,
            po.order_no,
            i.item_code,
            i.item_name,
            po.order_qty,
            po.due_date,
            po.status
        FROM production_order AS po
        JOIN item AS i
            ON po.product_item_id = i.item_id
        ORDER BY po.order_id
    """

    return fetch_all(sql)
# ============================================
# 생산실적 등록
# ============================================
def insert_production(
    order_id,
    worker_name,
    equipment_name,
    production_date,
    production_qty
):
    # 생산지시에 대한 실제 생산실적을 등록한다.
    # 생산실적을 등록하면서 완제품 LOT을 자동 생성하고,
    # 생성된 LOT의 lot_id를 production.output_lot_id에 연결한다.
    # order_id:
    #     생산지시 ID
    # worker_name:
    #     생산 작업자
    # equipment_name:
    #     생산 설비
    # production_date:
    #     실제 생산일
    # production_qty:
    #     실제 생산수량

    # ============================================
    # 1. 생산지시 정보 조회
    order_sql = """
        SELECT
            product_item_id,
            order_qty
        FROM production_order
        WHERE order_id = ?
    """
    order = fetch_one(
        order_sql,
        (order_id,)
    )

    # 존재하지 않는 생산지시인지 확인한다.
    if order is None:
        raise ValueError("존재하지 않는 생산지시입니다.")

    product_item_id = order["product_item_id"]

    # ============================================
    # 2. 완제품 품목 코드 조회
    item_sql = """
        SELECT
            item_code
        FROM item
        WHERE item_id = ?
    """
    item = fetch_one(
        item_sql,
        (product_item_id,)
    )
    if item is None:
        raise ValueError("생산할 완제품을 찾을 수 없습니다.")

    # ============================================
    # 3. 생산실적 번호 자동 생성
    today = datetime.now().strftime("%Y%m%d")
    production_sql = """
        SELECT COUNT(*)
        FROM production
        WHERE production_no LIKE ?
    """
    prefix = f"PR-{today}-%"
    result = fetch_one(
        production_sql,
        (prefix,)
    )

    count = result[0] if result else 0
    sequence = count + 1
    production_no = f"PR-{today}-{sequence:03d}"

    # ============================================
    # 4. 완제품 LOT 자동 생성
    lot_no = generate_lot_no(
        item["item_code"]
    )
    lot_sql = """
        INSERT INTO lot (
            lot_no,
            item_id,
            lot_qty,
            current_qty,
            produced_date,
            location
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """
    execute(
        lot_sql,
        (
            lot_no,
            product_item_id,
            production_qty,
            production_qty,
            production_date,
            "완제품창고"
        )
    )

    # ============================================
    # 5. 방금 생성한 LOT 조회
    lot_sql = """
        SELECT
            lot_id
        FROM lot
        WHERE lot_no = ?
    """
    lot = fetch_one(
        lot_sql,
        (lot_no,)
    )
    if lot is None:
        raise ValueError("완제품 LOT 생성에 실패했습니다.")
    output_lot_id = lot["lot_id"]

    # ============================================
    # 6. 생산실적 등록
    insert_sql = """
        INSERT INTO production (
            production_no,
            order_id,
            output_lot_id,
            worker_name,
            equipment_name,
            production_date,
            production_qty,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    execute(
        insert_sql,
        (
            production_no,
            order_id,
            output_lot_id,
            worker_name,
            equipment_name,
            production_date,
            production_qty,
            "완료"
        )
    )

# ============================================
# 생산지시별 생산실적 조회
# ============================================
def get_production_order_progress(order_id):
    # 특정 생산지시의 지시수량과
    # 현재까지 생산된 실제 생산수량을 조회한다.
    sql = """
        SELECT
            po.order_qty,
            COALESCE(
                SUM(p.production_qty),
                0
            ) AS produced_qty
        FROM production_order AS po
        LEFT JOIN production AS p
            ON po.order_id = p.order_id
        WHERE po.order_id = ?
        GROUP BY po.order_id
    """
    return fetch_one(
        sql,
        (order_id,)
    )
# ============================================
# 생산지시 상태 변경
# ============================================
def update_production_order_status(
    order_id,
    status
):
    # 생산지시의 상태를 변경한다.
    sql = """
        UPDATE production_order
        SET status = ?
        WHERE order_id = ?
    """
    return execute(
        sql,
        (
            status,
            order_id
        )
    )

# ============================================
# 품질검사 등록
# ============================================
def insert_quality(
    production_id,
    result,
    good_qty,
    defect_qty,
    defect_reason,
    inspector_name,
    inspection_date
):
    # 생산실적에 대한 품질검사 결과를 등록한다.
    # production_id:
    #     검사할 생산실적 ID
    # result:
    #     품질검사 결과
    #     예: 합격 / 불합격
    # good_qty:
    #     양품 수량
    # defect_qty:
    #     불량 수량
    # defect_reason:
    #     불량 발생 사유
    # inspector_name:
    #     검사자 이름
    # inspection_date:
    #     검사일

    # 해당 생산실적의 실제 생산수량을 조회한다.
    production_sql = """
        SELECT
            production_qty
        FROM production
        WHERE production_id = ?
    """
    production = fetch_one(
        production_sql,
        (production_id,)
    )
    # 존재하지 않는 생산실적인지 확인한다.
    if production is None:
        raise ValueError(
            "존재하지 않는 생산실적입니다."
        )

    production_qty = production["production_qty"]

    # 양품 + 불량 수량이 실제수량과 일치하는지 확인
    if good_qty + defect_qty != production_qty:
        raise ValueError(
            f"양품 수량({good_qty}) + "
            f"불량 수량({defect_qty})은 "
            f"생산수량({production_qty})과 "
            f"같아야 합니다."
        )
    # 품질검사 결과를 DB에 저장한다.
    sql = """
        INSERT INTO quality (
            production_id,
            result,
            good_qty,
            defect_qty,
            defect_reason,
            inspector_name,
            inspection_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    return execute(
        sql,
        (
            production_id,
            result,
            good_qty,
            defect_qty,
            defect_reason,
            inspector_name,
            inspection_date
        )
    )
# ============================================
# 품질검사 대상 생산실적 조회
# ============================================
def get_production_list_for_quality():
    # 아직 품질검사가 등록되지 않은 생산실적을 조회한다.

    # production과 item을 연결해서
    # 생산실적 번호, 완제품 정보, 생산수량 등을 함께 가져온다.

    # 이미 품질검사가 완료된 생산실적은
    # 다시 검사 대상으로 나오지 않는다.
    sql = """
        SELECT
            p.production_id,
            p.production_no,
            i.item_code,
            i.item_name,
            p.production_qty,
            p.production_date
        FROM production AS p
        JOIN production_order AS po
            ON p.order_id = po.order_id
        JOIN item AS i
            ON po.product_item_id = i.item_id
        LEFT JOIN quality AS q
            ON p.production_id = q.production_id
        WHERE q.quality_id IS NULL
        ORDER BY p.production_id
    """
    return fetch_all(sql)

# ============================================
# 품질검사 결과에 따른 완제품 LOT 재고 반영
# ============================================
def update_lot_qty_by_quality(
    production_id,
    good_qty
):
    # 품질검사가 완료된 생산실적의
    # 완제품 LOT 재고를 양품 수량으로 변경한다.
    # production.output_lot_id를 통해
    # 해당 생산실적의 완제품 LOT를 찾는다.
    # good_qty:
    #     품질검사에서 판정된 양품 수량
    sql = """
        SELECT
            output_lot_id
        FROM production
        WHERE production_id = ?
    """
    production = fetch_one(
        sql,
        (production_id,)
    )
    # 생산실적이 존재하지 않는 경우
    if production is None:
        raise ValueError(
            "존재하지 않는 생산실적입니다."
        )
    lot_id = production["output_lot_id"]

    # 완제품 LOT의 현재 재고를 품질검사 양품 수량으로 변경한다.
    update_sql = """
        UPDATE lot
        SET current_qty = ?
        WHERE lot_id = ?
    """
    return execute(
        update_sql,
        (
            good_qty,
            lot_id
        )
    )

# ============================================
# 출하 가능한 완제품 LOT 조회
# ============================================
def get_shippable_lot_list():
    # 출하 가능한 완제품 LOT를 조회한다.
    # 조건:
    # 1. 완제품 품목이어야 한다.
    # 2. 품질검사가 완료된 생산실적의 LOT여야 한다.
    # 3. 현재 출하 가능한 재고가 0보다 커야 한다.
    # 생산실적 → 품질검사 → LOT 관계를 이용해서
    # 검사 완료된 정상 완제품 LOT만 가져온다.
    sql = """
        SELECT
            l.lot_id,
            l.lot_no,
            l.item_id,
            i.item_code,
            i.item_name,
            l.lot_qty,
            l.current_qty,
            l.produced_date
        FROM lot AS l
        JOIN item AS i
            ON l.item_id = i.item_id
        JOIN production AS p
            ON l.lot_id = p.output_lot_id
        JOIN quality AS q
            ON p.production_id = q.production_id
        WHERE i.item_type = 'FG'
          AND q.result = '합격'
          AND l.current_qty > 0

        ORDER BY l.lot_id
    """
    return fetch_all(sql)

# ============================================
# 출하 등록
# ============================================
def insert_shipment(
    lot_id,
    customer_name,
    customer_po,
    shipment_qty,
    shipment_date
):
    # 완제품 LOT의 출하 정보를 등록한다.
    # 출하 등록과 동시에
    # 해당 LOT의 현재 재고(current_qty)를 차감한다.

    # 출하 대상 LOT의 현재 재고를 조회한다.
    lot_sql = """
        SELECT
            current_qty
        FROM lot
        WHERE lot_id = ?
    """
    lot = fetch_one(
        lot_sql,
        (lot_id,)
    )

    if lot is None:
        raise ValueError(
            "존재하지 않는 LOT입니다."
        )

    current_qty = lot["current_qty"]

    # 출하수량이 현재 재고를 초과하는지 확인한다.
    if shipment_qty > current_qty:
        raise ValueError(
            f"현재 재고는 {current_qty:,}개입니다."
        )

    # 출하 이력을 저장한다.
    shipment_sql = """
        INSERT INTO shipment (
            lot_id,
            customer_name,
            customer_po,
            shipment_qty,
            shipment_date
        )
        VALUES (?, ?, ?, ?, ?)
    """
    execute(
        shipment_sql,
        (
            lot_id,
            customer_name,
            customer_po,
            shipment_qty,
            shipment_date
        )
    )
    # LOT 현재 재고를 차감한다.
    update_lot_sql = """
        UPDATE lot
        SET current_qty = current_qty - ?
        WHERE lot_id = ?
    """
    execute(
        update_lot_sql,
        (
            shipment_qty,
            lot_id
        )
    )