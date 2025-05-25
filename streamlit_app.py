import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_BACKEND_URL = os.getenv("API_BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="InSightMate", layout="wide")
st.markdown("<h1 style='text-align: center; color: #035D87;'> InSightMate: Your AI-Powered Helper</h1>", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("🔍 Search Settings")
    user_prompt = st.text_input("Enter your area of interest:")
    page = st.number_input("Page Number", min_value=1, value=1, step=1)
    if st.button("Get Recommendations"):
        st.session_state.history.append(user_prompt)

if user_prompt:
    with st.spinner("Fetching content..."):
        try:
            res = requests.get(f"{API_BACKEND_URL}/recommend", params={"prompt": user_prompt, "page": page}, timeout=60)
            res.raise_for_status()
            data = res.json()["recommendations"]

            st.markdown("## 📰 News Articles")
            if not data["articles"]:
                st.warning("No articles found.")
            else:
                for rec in data["articles"]:
                    st.markdown(f"### {rec['title']}")
                    st.markdown(f"🗓️ {rec.get('pubDate', '')}")
                    st.markdown(f"📝 {rec.get('description', '')}")
                    st.markdown(f"[Read more]({rec['url']})")
                    st.caption(f"🤖 Why recommended: {rec['why']}")

            st.markdown("---")
            st.markdown("## 💼 Job Openings")
            if not data["jobs"]:
                st.warning("No jobs found.")
            else:
                for job in data["jobs"]:
                    st.markdown(f"### {job['title']} at {job.get('company', '')}")
                    st.markdown(f"📝 {job.get('description', '')}")
                    st.markdown(f"[Apply here]({job['url']})")
                    st.caption(f"🤖 Why recommended: {job['why']}")

        except Exception as e:
            st.error(f"Error fetching recommendations: {e}")

with st.sidebar:
    st.markdown("## 🔎 Recent Searches")
    for i, term in enumerate(reversed(st.session_state.history[-5:]), 1):
        st.markdown(f"{i}. {term}")
    st.markdown("---")
    st.markdown("### About InSightMate")
    st.markdown("InSightMate is an AI-powered recommendation engine helping you discover relevant news articles and jobs.")
    st.markdown("### Contact")
    st.markdown("For feedback, contact [UPBajpayee](mailto:ujjwalprakash02@gmail.com)")
