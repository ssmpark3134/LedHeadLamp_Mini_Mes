import streamlit as st
import pandas as pd
from src.queries import (
    get_fg_item_list,
    get_rm_item_list,
    get_bom_by_product
)
from src.ui import(
    setup_page,
    page_title,
    show_database_status,
    show_dataframe,
)

setup_page("BOM 관리")
page_title(title="BOM 관리", 
           description="완제품과 원자재의 구성 정보를 관리하는 화면\n",
           tables="bom,item\n",
           task="Bom 조회 및 CRUD")
show_database_status()
st.divider()
st.header("🧩 BOM 관리")

# 완제품 선택
fg_items = [
    dict(item)
    for item in get_fg_item_list()
]


if fg_items:

    selected_fg = st.selectbox(
        "완제품 선택",
        fg_items,
        format_func=lambda x:
            f"{x['item_code']} - {x['item_name']}"
    )

else:

    st.warning("등록된 완제품이 없습니다.")
    st.stop()
# 선택한 완제품의 BOM조회
st.divider()

st.subheader(
    f"📦 {selected_fg['item_name']} BOM 구성"
)


bom_list = [
    dict(row)
    for row in get_bom_by_product(
        selected_fg["item_id"]
    )
]


if bom_list:

    bom_df = pd.DataFrame(bom_list)

    bom_df = bom_df[
        [
            "material_code",
            "material_name",
            "required_qty"
        ]
    ]

    bom_df.columns = [
        "원자재 코드",
        "원자재명",
        "필요 수량"
    ]

    st.dataframe(
        bom_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "현재 등록된 BOM 구성품이 없습니다."
    )
# 원자재 추가용 Session State
if "bom_materials" not in st.session_state:
    st.session_state.bom_materials = []

# 원자재 추가화면
st.divider()
st.subheader("➕ 원자재 추가")
rm_items = [
    dict(item)
    for item in get_rm_item_list()
]
if rm_items:
    selected_rm = st.selectbox(
        "원자재 선택",
        rm_items,
        format_func=lambda x:
            f"{x['item_code']} - {x['item_name']}",
        key="selected_rm"
    )
    required_qty = st.number_input(
        "필요 수량",
        min_value=1,
        value=1,
        step=1,
        key="required_qty"
    )
    if st.button("원자재 추가"):
        # 이미 추가된 원자재 인지 확인
        material_item_id = selected_rm['item_id']
        duplicate=any(
            material['material_item_id'] == material_item_id
            for material in st.session_state.bom_materials
        )
        # 이미 존재하면 추가 X
        if duplicate:
            st.warning(f"'{selected_rm['item_name']}'은 이미 BOM 구성에 추가되어 있습니다.")
        # 아직 추가되지 않은 원자재라면 추가
        else:
            new_material = {
                "material_item_id": selected_rm["item_id"],
                "material_code": selected_rm["item_code"],
                "material_name": selected_rm["item_name"],
                "required_qty": required_qty
            }
            # 세션에 원자재 정보 추가
            st.session_state.bom_materials.append(
                new_material
            )
            st.rerun()
else:

    st.warning("등록된 원자재가 없습니다.")
# 추가할 원자재 목록
st.subheader("🧩 BOM 추가 예정")
# 세션에 추가된 원자재가 있는경우
if st.session_state.bom_materials:
    header_cols = st.columns([2, 3, 1, 1])
    header_cols[0].write("**원자재 코드**")
    header_cols[1].write("**원자재명**")
    header_cols[2].write("**필요 수량**")
    header_cols[3].write("**관리**")
    st.divider()
    # 장바구니 원자재 출력
    for index, material in enumerate(
        st.session_state.bom_materials
    ):
        columns = st.columns([2, 3, 1, 1])
        # 원자재 코드 출력
        columns[0].write(
            material["material_code"]
        )
        # 원자재명 출력
        columns[1].write(
            material["material_name"]
        )
        # 필요 수량 출력
        columns[2].write(
            material["required_qty"]
        )
        # 삭제 버튼
        if columns[3].button(
            "삭제",
            key=f"delete_bom_material_{index}"
        ):
            delete_item_id = material[
                "material_item_id"
            ]
            st.session_state.bom_materials = [
                item
                for item in st.session_state.bom_materials
                if item["material_item_id"]
                != delete_item_id
            ]
            st.rerun()
else:

    st.info(
        "추가된 원자재가 없습니다."
    )
