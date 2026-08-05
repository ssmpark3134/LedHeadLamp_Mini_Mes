from src.db import fetch_all

# ============================================
# 생산 지시 차트 전용 함수
# ============================================
def get_production_chart_list():
    sql = """
        SELECT
            po.order_id,
            po.order_no,
            i.item_code,
            i.item_name,
            po.order_qty,

            COALESCE(
                SUM(p.production_qty),
                0
            ) AS produced_qty

        FROM production_order AS po

        JOIN item AS i
            ON po.product_item_id = i.item_id

        LEFT JOIN production AS p
            ON po.order_id = p.order_id

        GROUP BY
            po.order_id,
            po.order_no,
            i.item_code,
            i.item_name,
            po.order_qty

        ORDER BY po.order_id
    """

    return fetch_all(sql)

# ============================================
# 품질 불량률 조회
# ============================================
def get_defect_rate_list():
    sql = """
        SELECT
            i.item_code,
            i.item_name,

            COALESCE(
                SUM(q.good_qty),
                0
            ) AS good_qty,

            COALESCE(
                SUM(q.defect_qty),
                0
            ) AS defect_qty,

            COALESCE(
                SUM(q.good_qty),
                0
            )
            +
            COALESCE(
                SUM(q.defect_qty),
                0
            ) AS inspection_qty

        FROM quality AS q

        JOIN production AS p
            ON q.production_id = p.production_id

        JOIN production_order AS po
            ON p.order_id = po.order_id

        JOIN item AS i
            ON po.product_item_id = i.item_id

        GROUP BY
            i.item_id,
            i.item_code,
            i.item_name

        ORDER BY
            i.item_id
    """

    return fetch_all(sql)
