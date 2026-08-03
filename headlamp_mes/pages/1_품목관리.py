import streamlit as st
import pandas as pd

from src.ui import setup_page, page_title, show_database_status, show_dataframe
from src.queries import (get_item_list, insert_item,
update_item ,deactivate_item, activate_item, get_reactivate_item_list )

setup_page("Item-품목관리")

page_title(
    title = "품목관리",
    description="품목 정보를 조회하고 관리하는 화면\n",
    tables="item\n",
    task="품목 조회 및 CRUD"
)

show_database_status()

# ==================================== read================================
st.divider()
st.header("📦품목관리")

items=get_item_list()
items_dict=[dict(item) for item in items]
df=pd.DataFrame(items_dict)

show_dataframe(df, empty_message="등록된 품목 데이터가 없습니다.")

# ==================================== create ================================
st.divider()
st.subheader("➕품목 등록")

item_code=st.text_input("품목 코드")
item_name=st.text_input("품목명")
item_type=st.selectbox("품목 종류",['FG', 'RM'])
unit = st.text_input("단위", value='EA')

if st.button("등록"):
    insert_item(
        item_code,
        item_name,
        item_type,
        unit
    )

    st.success("품목이 등록되었습니다.")
    st.rerun()

# ==================================== update ================================
st.divider()
st.subheader("✏️품목 수정")

selected_item = st.selectbox("수정할 품목 선택", items_dict, 
                             format_func=lambda x:
                                f'{x['item_id']} - {x['item_name']}'
)

if selected_item:
    item_id=selected_item['item_id']

    update_name = st.text_input('수정할 품목명', value=selected_item['item_name'])
    update_type = st.selectbox('수정할 품목 타입',['FG','RM'], index=0 if selected_item['item_type']=='FG' else 1)
    update_unit = st.text_input('수정할 단위', value=selected_item['unit'])
    if st.button("수정"):
        update_item(item_id, update_name, update_type, update_unit)
        st.success('품목 정보가 수정되었습니다.')

        st.rerun()

# ==================================== delete ================================
st.divider()
st.subheader("✏️품목 사용 중지")

selected_deactivate=st.selectbox(
    '사용 중지할 품목',
    items_dict,
    format_func=lambda x:
        f'{x['item_code']} - {x['item_name']}',
    key='deactivate_item'
)

if st.button('사용중지'):
    deactivate_item(selected_deactivate['item_id'])

    st.warning('품목이 비활성화 되었습니다.')
    st.rerun()

# ==================================== 사용 재개 ================================
st.divider()
st.subheader("🔄 품목 사용재개")

reactivate_items = [dict(item) for item in get_reactivate_item_list()]
if reactivate_items:
    selected_item = st.selectbox(
        "사용재개할 품목",
        reactivate_items,
        format_func=lambda x:
            f"{x['item_code']} - {x['item_name']}",
        key="reactivate_item"
    )
    if st.button("사용재개"):
        activate_item(selected_item["item_id"])
        st.success("품목 사용이 재개 되었습니다.")
        st.rerun()
else:
    st.info("현재 비활성화된 품목이 없습니다.")
