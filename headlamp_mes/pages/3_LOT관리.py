import streamlit as st
import pandas as pd

from src.queries import (
    get_fg_stock_list,
    get_rm_stock_list,
    get_lot_list,
    get_fg_item_list, 
    get_rm_item_list, 
    insert_lot
)
from src.ui import (
    setup_page,
    page_title,
    show_database_status,
    show_dataframe,
)


# ============================================
# 페이지 기본 설정
setup_page("LOT 관리")
page_title(
    title="LOT 관리\n",
    description="품목별 재고와 LOT 정보를 조회하는 화면\n",
    tables="lot,item\n",
    task="재고 및 LOT 조회"
)
show_database_status()
# ============================================
# LOT 상세 조회
st.divider()
st.header("📋 LOT 상세")
lot_list = [
    dict(row)
    for row in get_lot_list()
]
if lot_list:
    lot_df = pd.DataFrame(lot_list)
    lot_df = lot_df[
        [
            "lot_no",
            "item_code",
            "item_name",
            "item_type",
            "lot_qty",
            "current_qty",
            "received_date",
            "produced_date",
            "location"
        ]
    ]
    lot_df.columns = [
        "LOT 번호",
        "품목 코드",
        "품목명",
        "품목 종류",
        "전체 수량",
        "현재 수량",
        "입고일",
        "생산일",
        "보관 위치"
    ]
    st.dataframe(
        lot_df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("등록된 LOT이 없습니다.")

# ============================================
# 완제품 재고 조회
st.divider()
st.header("📦 완제품 재고")
fg_stock = [
    dict(row)
    for row in get_fg_stock_list()
]
if fg_stock:
    fg_df = pd.DataFrame(fg_stock)
    fg_df.columns = [
        "품목 코드",
        "품목명",
        "단위",
        "현재 재고"
    ]
    st.dataframe(
        fg_df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("현재 완제품 재고가 없습니다.")

# ============================================
# 원자재 재고 조회
st.divider()
st.header("🔩 원자재 재고")
rm_stock = [
    dict(row)
    for row in get_rm_stock_list()
]
if rm_stock:
    rm_df = pd.DataFrame(rm_stock)
    rm_df.columns = [
        "품목 코드",
        "품목명",
        "단위",
        "현재 재고"
    ]
    st.dataframe(
        rm_df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("현재 원자재 재고가 없습니다.")

# ============================================
# LOT 자동 생성 테스트
st.divider()
st.header("🧪 LOT 자동 생성 테스트")
fg_items = [
    dict(item)
    for item in get_fg_item_list()
]
rm_items = [
    dict(item)
    for item in get_rm_item_list()
]
all_items = rm_items + fg_items

if all_items:
    selected_item = st.selectbox(
        "LOT을 생성할 품목",
        all_items,
        format_func=lambda x:
            f"{x['item_code']} - {x['item_name']}"
    )
    lot_qty = st.number_input(
        "LOT 수량",
        min_value=1,
        value=1000,
        step=1
    )
    location = st.text_input(
        "보관 위치",
        value="원자재창고"
    )
    # LOT 생성 버튼
    if st.button("LOT 자동 생성"):

        insert_lot(
            item_id=selected_item["item_id"],
            lot_qty=lot_qty,
            location=location
        )

        st.success(
            f"{selected_item['item_name']}의 LOT이 자동 생성되었습니다."
        )
        st.rerun()
else:
    st.warning("등록된 품목이 없습니다.")
