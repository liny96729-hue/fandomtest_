import streamlit as st
import urllib.parse

from questions import questions
from results import results


# =====================
# PAGE SETTING
# =====================

st.set_page_config(
    page_title="팬덤 성향 테스트",
    page_icon="🎤",
    layout="centered"
)


# =====================
# STYLE
# =====================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #fff7fb;
    }

    html, body, [class*="css"] {
        color: #222222 !important;
    }

    p, span, div, label {
        color: #222222 !important;
    }

    h1, h2, h3, h4 {
        color: #222222 !important;
    }

    /* 메인 제목 */
    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #222222 !important;
    }

    /* 서브 제목 */
    .sub {
        text-align: center;
        font-size: 18px;
        color: #777777 !important;
        margin-bottom: 40px;
    }

    /* 질문 카드 */
    .card {
        background: white;
        padding: 35px;
        border-radius: 25px;
        box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.08);
    }

    /* 질문 선택 영역 */
    div[data-testid="stRadio"] {
        background: white;
        padding: 20px;
        border-radius: 20px;
    }

    /* 라디오 버튼 안내 문구 */
    div[data-testid="stRadio"] > label > div:first-child {
        font-size: 15px !important;
        color: #777777 !important;
    }

    /* 라디오 선택지 */
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] p {
        color: #222222 !important;
        font-size: 18px !important;
    }

    /* 버튼 */
    div.stButton > button {
        width: 100%;
        height: 55px;
        border-radius: 30px;
        background: white;
        color: #222222 !important;
        font-size: 17px;
        font-weight: bold;
        border: 1px solid #dddddd;
    }

    div.stButton > button:hover {
        color: #ff5c8a !important;
        border: 2px solid #ff5c8a;
    }

    /* 링크 */
    a {
        color: #222222 !important;
    }

    a:hover {
        color: #ff5c8a !important;
    }

    /* 알림 박스 */
    div[data-testid="stAlert"] p {
        color: #222222 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================
# TITLE
# =====================

st.markdown(
    """
    <div class="title">
    🎤 나의 K-POP 팬덤 찾기
    </div>

    <div class="sub">
    10개의 질문으로 알아보는<br>
    나와 가장 잘 맞는 팬덤 스타일 ✨
    </div>
    """,
    unsafe_allow_html=True
)


# =====================
# SESSION STATE
# =====================

if "page" not in st.session_state:
    st.session_state.page = 0

if "answers" not in st.session_state:
    st.session_state.answers = []


# =====================
# QUESTION PAGE
# =====================

if st.session_state.page < len(questions):

    q = questions[st.session_state.page]


    # 진행률
    st.progress(
        st.session_state.page / len(questions)
    )


    # 질문 카드
    st.markdown(
        f"""
        <div class="card">

        <h3>
        QUESTION {st.session_state.page + 1} / {len(questions)}
        </h3>

        <h2>
        {q["question"]}
        </h2>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")


    # =====================
    # ANSWER OPTIONS
    # =====================

    # questions.py의 구조:
    # "answers": [
    #     {"text": "...", "type": "..."},
    #     {"text": "...", "type": "..."}
    # ]

    options = [
        answer["text"]
        for answer in q["answers"]
    ]


    # 이전에 선택한 답변 확인
    previous = None

    if st.session_state.page < len(
        st.session_state.answers
    ):
        previous = st.session_state.answers[
            st.session_state.page
        ]


    # 라디오 버튼
    choice = st.radio(
        "가장 잘 맞는 답을 선택해주세요",
        options,
        index=(
            options.index(previous)
            if previous in options
            else 0
        )
    )


    st.write("")


    # =====================
    # PREVIOUS / NEXT BUTTON
    # =====================

    col1, col2 = st.columns(2)


    # 이전 버튼
    with col1:

        if st.button("⬅️ 이전"):

            if st.session_state.page > 0:

                st.session_state.page -= 1

                st.rerun()


    # 다음 버튼
    with col2:

        if st.button("다음 ➡️"):

            # 기존 답변 수정
            if st.session_state.page < len(
                st.session_state.answers
            ):

                st.session_state.answers[
                    st.session_state.page
                ] = choice

            # 새로운 답변 추가
            else:

                st.session_state.answers.append(
                    choice
                )


            # 다음 질문으로 이동
            st.session_state.page += 1

            st.rerun()


# =====================
# RESULT PAGE
# =====================

else:

    # =====================
    # SCORE CALCULATION
    # =====================

    scores = {}


    # 사용자가 선택한 답변을 하나씩 확인
    for i, answer in enumerate(
        st.session_state.answers
    ):

        q = questions[i]


        # 해당 질문의 답변 목록 확인
        for option in q["answers"]:

            # 사용자가 선택한 답변과 일치하는 경우
            if option["text"] == answer:

                fandom = option["type"]


                # 처음 등장한 팬덤이면 0점으로 시작
                if fandom not in scores:

                    scores[fandom] = 0


                # 해당 팬덤 점수 +1
                scores[fandom] += 1


    # =====================
    # RESULT TYPE
    # =====================

    # 가장 높은 점수의 팬덤 찾기
    result_type = max(
        scores,
        key=scores.get
    )


    # results.py에서 결과 가져오기
    result = results[result_type]


    # =====================
    # RESULT CARD
    # =====================

    st.markdown(
        f"""
        <div class="card">

            <div style="
            text-align:center;
            font-size:22px;
            font-weight:700;
            color:#222222;
            margin-bottom:10px;
            ">
            🎉 나와 가장 잘 맞는 팬덤은?
            </div>


            <div style="
            text-align:center;
            font-size:38px;
            font-weight:800;
            color:#222222;
            margin-bottom:25px;
            ">
            {result["title"]}
            </div>


            <div style="
            text-align:center;
            font-size:26px;
            font-weight:700;
            color:#222222;
            margin-bottom:15px;
            ">
            {result["catchphrase"]}
            </div>


            <div style="
            text-align:center;
            font-size:17px;
            line-height:1.7;
            color:#555555;
            ">
            {result["description"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")


    # =====================
    # FEATURES
    # =====================

    st.subheader("✨ 당신의 특징")


    for feature in result["features"]:

        st.info(feature)


    st.divider()


    # =====================
    # RECOMMENDED STYLE
    # =====================

    st.subheader("💡 추천 덕질 스타일")


    st.success(
        result["style"]
    )


    st.divider()


    # =====================
    # BUTTONS
    # =====================

    col1, col2, col3 = st.columns(3)


    # =====================
    # RETRY BUTTON
    # =====================

    with col1:

        if st.button("🔄 다시 하기"):

            st.session_state.page = 0

            st.session_state.answers = []

            st.rerun()


    # =====================
    # YOUTUBE BUTTON
    # =====================

    with col2:

        st.markdown(
            """
            <a href="https://youtube.com/@pixid?si=nbTiDFyDw95Q6fdk"
            target="_blank"
            style="
            display:flex;
            align-items:center;
            justify-content:center;
            width:100%;
            height:55px;
            border-radius:30px;
            background:white;
            color:#222222 !important;
            text-decoration:none;
            font-size:15px;
            font-weight:bold;
            border:1px solid #dddddd;
            ">
            🎬 팬덤스테이지 보러가기
            </a>
            """,
            unsafe_allow_html=True
        )


    # =====================
    # X SHARE BUTTON
    # =====================

    with col3:

        TEST_URL = "https://fandomstgetest.streamlit.app/"


        share_text = (
            f"🎤 나의 K-POP 팬덤 찾기 결과!\n\n"
            f"나는 {result['title']} 💖\n\n"
            f"너의 팬덤 유형도 찾아보기 ✨\n"
            f"{TEST_URL}"
        )


        share_url = (
            "https://twitter.com/intent/tweet?text="
            + urllib.parse.quote(share_text)
        )


        st.markdown(
            f"""
            <a href="{share_url}"
            target="_blank"
            style="
            display:flex;
            align-items:center;
            justify-content:center;
            width:100%;
            height:55px;
            border-radius:30px;
            background:white;
            color:#222222 !important;
            text-decoration:none;
            font-size:15px;
            font-weight:bold;
            border:1px solid #dddddd;
            ">
            𝕏 공유하기
            </a>
            """,
            unsafe_allow_html=True
        )
