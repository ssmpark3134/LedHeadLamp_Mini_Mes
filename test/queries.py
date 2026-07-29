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

# BOM 전체조회 join
def get_bom_list():
    sql = """
        select b.bom_id, 
            p.item_name as product_name,
            m.item_name as material_name,
            b.required_qty
        from bom b
        inner join item p
            on b.product_item_id = p.item_id
        inner join item m
            on b.material_item_id = m.item_id
        order by b.bom_id
    """
    return fetch_all(sql)
