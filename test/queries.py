from src.db import fetch_all, fetch_dataframe, fetch_one, execute

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
