import streamlit as st
import pandas as pd
from datetime import date
from src.queries import (
    get_production_order_list,
    insert_production,
    get_production_order_progress,
    update_production_order_status
)
from src.ui import (
    setup_page,
    page_title,
    show_database_status
)
# ============================================
# 페이지 기본 설정
setup_page("생산실적")
page_title(
    title="생산실적\n",
    description="생산지시에 따라 실제 생산된 수량을 등록하는 화면\n",
    tables="production_order,production,lot\n",
    task="생산실적 등록 및 완제품 LOT 자동생성"
)
show_database_status()

# ============================================
# 생산실적 등록
st.divider()
st.header("🏭 생산실적 등록")

order_list = [
    dict(row)
    for row in get_production_order_list()
]

if not order_list:
    st.warning("등록된 생산지시가 없습니다.")
    st.stop()

# ============================================
# 생산지시 선택
selected_order = st.selectbox(
    "생산지시 선택",
    order_list,
    format_func=lambda x:
        f"{x['order_no']} - "
        f"{x['item_name']} "
        f"({x['order_qty']:,}개)"
)

# ============================================
# 선택한 생산지시 조회
progress = get_production_order_progress(
    selected_order["order_id"]
)

order_qty = progress["order_qty"]
produced_qty = progress["produced_qty"]

remaining_qty = order_qty - produced_qty

# ============================================
# 생산지시 진행상황 표시
st.info(
    f"""
    **생산지시 수량:** {order_qty:,}개

    **현재 생산 수량:** {produced_qty:,}개

    **남은 생산 수량:** {remaining_qty:,}개
    """
)
if remaining_qty <= 0:
    st.success("이 생산지시는 생산이 완료되었습니다.")
    st.stop()

# ============================================
# 작업자 입력
worker_name = st.text_input(
    "작업자",
    placeholder="작업자 이름을 입력하세요."
)

# ============================================
# 생산 설비 입력
equipment_name = st.text_input(
    "생산 설비",
    placeholder="예: 조립라인-01"
)

# ============================================
# 생산일
production_date = st.date_input(
    "생산일",
    value=date.today()
)

# ============================================
# 실제 생산수량
production_qty = st.number_input(
    "실제 생산수량",
    min_value=1,
    max_value=max(1, remaining_qty),
    value=min(1000, max(1, remaining_qty)),
    step=1
)

# ============================================
# 생산실적 등록
if st.button(
    "🏭 생산실적 등록",
    type="primary"
):
    # 작업자 입력 여부 확인
    if not worker_name.strip():
        st.warning("작업자 이름을 입력해주세요.")
        st.stop()

    # 설비 입력 여부 확인
    if not equipment_name.strip():
        st.warning("생산 설비를 입력해주세요.")
        st.stop()

    # 실제 생산수량이 생산지시 수량을 초과하는지 확인
    if production_qty > selected_order["order_qty"]:
        st.warning(
            "실제 생산수량이 생산지시 수량을 "
            "초과할 수 없습니다."
        )
        st.stop()
    # 생산실적 db등록
    insert_production(
        order_id=selected_order["order_id"],
        worker_name=worker_name,
        equipment_name=equipment_name,
        production_date=production_date.isoformat(),
        production_qty=production_qty
    )
    if production_qty == remaining_qty:
        update_production_order_status(
            selected_order["order_id"],
            "완료"
        )
    st.success(
        f"{selected_order['item_name']} "
        f"{production_qty:,}개 생산실적이 등록되었습니다."
    )
    st.info(
        "생산실적 등록과 동시에 완제품 LOT가 자동 생성되었습니다."
    )
    st.rerun()
