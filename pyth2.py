import re
import requests
import streamlit as st

# Page Configurations
st.set_page_config(
    page_title="IssuePilot AI",
    page_icon="🤖",
    layout="wide",
)

# Sidebar
st.sidebar.title("IssuePilot AI 🤖")
st.sidebar.write("Your Open Source Coding Assistant")

PAGES = ["Dashboard", "Analyse Issue", "How it works", "About the project"]

# Initialise navigation state
if "nav" not in st.session_state:
    st.session_state["nav"] = "Dashboard"


def go_to_analyse():
    """Callback: switch the sidebar radio to the Analyse Issue page."""
    st.session_state["nav"] = "Analyse Issue"


page = st.sidebar.radio("Navigation", PAGES, key="nav")

# Dashboard
if page == "Dashboard":
    st.title("Welcome to IssuePilot AI 🤖")
    st.write("Understand GitHub issues and discover how to solve them with AI")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("ISSUE ANALYSER")
        st.write("Convert confusing technical issues into simple explanations")

    with col2:
        st.subheader("SOLUTION PLANNER")
        st.write("Get step by step guidance to investigate and solve coding related problems")

    st.divider()

    st.info("Ready to explore your first GitHub issue?")

    st.button("Analyse an issue", on_click=go_to_analyse)

# Issue Analyser
elif page == "Analyse Issue":
    st.title("GitHub Issue Analyser")

    issue_url = st.text_area(
        "GitHub Issue URL or Description",
        placeholder="Paste the GitHub issue URL or description here",
        height=180,
    )

    experience = st.selectbox(
        "Your coding experience",
        ["Beginner", "Intermediate", "Advanced"],
    )

    if st.button("Analyse Issue"):
        if issue_url.strip():
            with st.spinner("Analyzing issue... Please wait ⏳"):
                title = "Submitted GitHub Issue"
                body = issue_url.strip()

                # Fetch live GitHub data if a link is provided
                pattern = r"github\.com/([^/]+)/([^/]+)/issues/(\d+)"
                match = re.search(pattern, issue_url)
                if match:
                    owner, repo, issue_num = match.groups()
                    gh_api_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_num}"
                    try:
                        resp = requests.get(gh_api_url, timeout=10)
                        if resp.status_code == 200:
                            gh_data = resp.json()
                            title = gh_data.get("title", title)
                            body = gh_data.get("body") or "No description provided."
                        else:
                            st.warning(
                                f"GitHub returned status {resp.status_code}. "
                                "Using the text you entered."
                            )
                    except requests.RequestException as e:
                        st.warning(f"Could not reach GitHub: {e}")

                # Suggest files based on keywords
                lower_body = (title + " " + body).lower()
                if "bug" in lower_body or "error" in lower_body or "fix" in lower_body:
                    suggested_files = ["src/utils.py", "tests/test_main.py"]
                else:
                    suggested_files = ["README.md", "src/main.py"]

            # Output the results
            st.success("Issue details received successfully!")

            st.subheader("ISSUE SUMMARY")
            st.write(f"**Title:** {title}")
            st.write(f"**Explanation:** {body[:250]}...")

            st.subheader("Suggested files")
            for file_path in suggested_files:
                st.code(file_path, language="text")

            st.subheader("ACTION PLAN")
            st.markdown("**1. Understand the problem:** Read through the issue description.")
            st.markdown(f"**2. Examine the code:** Open `{suggested_files[0]}`.")
            st.markdown("**3. Submit PR:** Test and push your changes.")

            st.caption(f"Experience level: {experience}")
        else:
            st.warning("Please enter an issue description or URL")

# How it works
elif page == "How it works":
    st.title("How IssuePilot AI 🤖 works")
    st.write("IssuePilot AI simplifies the process of understanding and working on open source issues")

    st.divider()

    st.subheader("Step 1: Enter a github issue")
    st.write("Paste the url or description of an issue you want to understand")

    st.subheader("Step 2: Understand the problem")
    st.write("The AI analyses the issue and explains the problem in a simple, beginner friendly language")

    st.subheader("Step 3: Discover relevant files")
    st.write("The system examines available repository information to suggest files that might be related to the issue")

    st.subheader("Step 4: Explore possible solutions")
    st.write("The AI recommends approaches and explains relevant programming concepts")

    st.subheader("Step 5: Follow your action plan")
    st.write("Use the suggested steps to investigate the issue, make changes and test your solution")

    st.divider()

    st.info("NOTE:- These AI powered features require github and AI backend integration to work automatically")

# About
elif page == "About the project":
    st.title("About IssuePilot AI 🤖")
    st.write("IssuePilot AI is a beginner friendly assistant designed to help students understand open source github issues")

    st.subheader("Technology Stack")

    st.write("Python")
    st.write("Streamlit")
    st.write("GitHub API")
    st.write("AI/NLP")
    st.info("The interface is built using Python commands and Streamlit components")

    st.divider()

    st.caption("IssuePilot AI 🤖: Built for Open Source Beginners")