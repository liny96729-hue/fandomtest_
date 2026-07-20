import streamlit as st
from questions import questions
from results import results
import urllib.parse


# 테스트 링크 (배포 후 변경)
TEST_URL = "https://example.com"


st.set_page_config(
    page_title="팬덤 성향 테스트",
    page_icon="🎤",
    layout="centered"
)


# =====================
# UI STYLE
# =====================

st.markdown(
    """
    <style>

    .stApp {
        background-color:#fff7fb;
    }


    h1, h2, h3 {
        color:#222222 !important;
    }


    p {
        color:#222222;
    }


    .main-title {

        text-align:center;
        font-size:42px;
        font-weight:800;
        color:#222222;

    }


    .sub-title {

        text-align:center;
        font-size:18px;
        color:#777777;
        margin-bottom:40px;

    }


    .question-card {

        background:white;
        padding:35px;
        border-radius:25px;
        box-shadow:0px 5px 20px rgba(0,0,0,0.08);
        margin-top:20px;

    }


    .question-number {

        text-align:center;
        color:#ff5c8a;
        font-weight:bold;

    }


    div[data-testid="stRadio"] {

        background:white;
        padding:20px;
        border-radius:20px;
        margin-top:25px;

    }


    div[data-testid="stRadio"] label {

        color:#222222 !important;
        font-size:18px !important;

    }


    div.stButton > button {

        width:100%;
        height:55px;
        border-radius:30px;
        font-size:17px;
        font-weight:bold;
        color:#222222 !important;
        background:white;

    }


    div.stButton > button:hover {

        color:#ff5c8a !important;
        border:2px solid #ff5c8a;

    }


    .result-card {

        background:white;
        padding:40px;
        border-radius:30px;
        box-shadow:0px 5px 20px rgba(0,0,0,0.08);
        text-align:center;

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
    <div class="main-title">
    🎤 나의 K-POP 팬덤 찾기
    </div>

    <div class="sub-title">
    7개의 질문으로 알아보는<br>
    나와 가장 잘 맞는 팬덤 스타일 ✨
    </div>
    """,
    unsafe_allow_html=True
)



# =====================
# SESSION
# =====================

if "page" not in st.session_state:

    st.session_state.page = 0



if "answers" not in st.session_state:

    st.session_state.answers = []



# =====================
# QUESTION
# =====================

if st.session_state.page < len(questions):


    q = questions[st.session_state.page]


    st.progress(
        st.session_state.page / len(questions)
    )



    st.markdown(
        f"""
        <div class="question-card">

        <div class="question-number">
        QUESTION {st.session_state.page + 1} / {len(questions)}
        </div>


        <h2 style="
        text-align:center;
        margin-top:20px;
        ">
        {q["question"]}
        </h2>


        </div>
        """,
        unsafe_allow_html=True
    )



    previous_answer = ""


    if st.session_state.page < len(st.session_state.answers):

        previous_answer = st.session_state.answers[
            st.session_state.page
        ]



    choice = st.radio(
        "선택해주세요",
        [
            q["A"],
            q["B"]
        ],
        index=(
            0 if previous_answer == q["A"]
            else 1 if previous_answer == q["B"]
            else 0
        )
    )



    col1, col2 = st.columns(2)



    with col1:

        if st.button("⬅️ 이전"):


            if st.session_state.page > 0:

                st.session_state.page -= 1


            st.rerun()



    with col2:

        if st.button("다음 ➡️"):


            if st.session_state.page < len(st.session_state.answers):

                st.session_state.answers[
                    st.session_state.page
                ] = choice


            else:

                st.session_state.answers.append(choice)



            st.session_state.page += 1


            st.rerun()

# =====================
# RESULT
# =====================

else:


    score_a = 0
    score_b = 0



    for i, answer in enumerate(st.session_state.answers):

        if answer == questions[i]["A"]:

            score_a += 1

        else:

            score_b += 1



    # 결과 결정

    if score_a >= 5:

        result = results["A"]


    elif score_b >= 5:

        result = results["B"]


    elif score_a == score_b:

        result = results["D"]


    else:

        result = results["C"]



    # =====================
    # 결과 카드
    # =====================

    st.markdown(
        """
        <div class="result-card">

        <h1>
        🎉 테스트 완료!
        </h1>

        </div>
        """,
        unsafe_allow_html=True
    )



    st.write("")



    # 결과 제목

    st.success(
        result["title"]
    )



    st.subheader(
        result["catchphrase"]
    )



    st.write(
        result["description"]
    )



    st.divider()



    # 특징

    st.subheader("✨ 당신의 특징")


    for feature in result["features"]:

        st.info(feature)



    st.divider()



    # 추천 스타일

    st.subheader("💡 추천 덕질 스타일")


    st.success(
        result["style"]
    )



    st.divider()



    # =====================
    # 하단 버튼
    # =====================

    col1, col2, col3 = st.columns(3)



    # 다시 하기

    with col1:


        if st.button("🔄 다시 하기"):

            st.session_state.page = 0

            st.session_state.answers = []

            st.rerun()



    # 팬덤스테이지

    with col2:


        st.markdown(
            f"""
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
            color:#222222;
            text-decoration:none;
            font-size:15px;
            font-weight:bold;
            border:1px solid #dddddd;
            ">
            🎬 <팬덤스테이지> 보러가기
            </a>
            """,
            unsafe_allow_html=True
        )



    # X 공유

    with col3:


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
            color:#222222;
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