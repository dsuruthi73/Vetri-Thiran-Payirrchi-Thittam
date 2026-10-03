
import os
import requests
import streamlit as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv

from backend.utils.exporters import (
    format_docx,
    format_pdf,
    format_txt
)

# ==========================================
# CONFIGURATION
# ==========================================

load_dotenv()

API_URL = os.getenv(
    "LEGALEASE_API_URL",
    "http://127.0.0.1:8000/api"
).rstrip("/")

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #f4f6fa;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
}

.hero {
    background: linear-gradient(
        120deg,
        #14213d,
        #274c77
    );
    padding: 30px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 42px;
}

.hero p {
    color: #e8eef8;
    font-size: 17px;
}

.section-title {
    font-size: 24px;
    font-weight: bold;
    color: #14213d;
}

div.stButton > button {
    border-radius: 10px;
    min-height: 44px;
    font-weight: bold;
}

div.stDownloadButton > button {
    width: 100%;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero">
    <h1>⚖️ LegalEase</h1>
    <p>AI-Powered Legal Document Generator</p>
    <p>Create, edit and download legal document drafts</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.title("⚖️ LegalEase")
    st.divider()

    st.subheader("Navigation")
    page = st.radio(
        "Choose a section",
        [
            "🏠 Home",
            "📝 Generate Document",
            "ℹ️ About"
        ]
    )

    st.divider()

    st.subheader("Document Types")
    st.write("""
    - Employment Contract
    - Non-Disclosure Agreement
    - Rental Agreement
    - Freelance Agreement
    - Consulting Agreement
    - Partnership Agreement
    - General Agreement
    """)

    st.divider()
    st.caption("LegalEase | AI Document Assistant")


# ==========================================
# HOME PAGE
# ==========================================

if page == "🏠 Home":

    st.markdown(
        '<p class="section-title">Welcome to LegalEase</p>',
        unsafe_allow_html=True
    )

    st.write(
        "Create editable legal document drafts "
        "with the help of AI."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📄 **Document Drafting**\n\n"
                "Prepare structured legal document drafts.")

    with col2:
        st.info("🤖 **AI Integration**\n\n"
                "Use Gemini AI to assist with drafting.")

    with col3:
        st.info("📥 **Document Export**\n\n"
                "Download drafts in PDF, DOCX or TXT.")

    st.divider()

    if st.button(
        "✨ Start Creating a Document",
        type="primary",
        use_container_width=True
    ):
        st.session_state["navigate_generate"] = True
        st.rerun()

    st.warning(
        "LegalEase is a drafting assistant, not a law firm. "
        "Generated documents are not legal advice and "
        "should be reviewed by a qualified lawyer."
    )


# ==========================================
# DOCUMENT GENERATION PAGE
# ==========================================

elif page == "📝 Generate Document":

    st.markdown(
        '<p class="section-title">📝 Create Your Document</p>',
        unsafe_allow_html=True
    )

    st.write(
        "Fill in the details below to prepare "
        "your legal document draft."
    )

    st.warning(
        "Avoid entering highly sensitive personal "
        "information. Review generated content with "
        "a qualified legal professional."
    )

    document_types = [
        "Employment Contract",
        "Non-Disclosure Agreement (NDA)",
        "Residential Lease Agreement",
        "Freelance Services Agreement",
        "Consulting Agreement",
        "Partnership Agreement",
        "Employment Offer Letter",
        "General Agreement"
    ]

    # --------------------------------------
    # INPUT FORM
    # --------------------------------------

    with st.form("legal_document_form"):

        col1, col2 = st.columns(2)

        with col1:
            document_type = st.selectbox(
                "Select Document Type",
                document_types
            )

            parties = st.text_area(
                "Parties Involved",
                placeholder=(
                    "Example:\n"
                    "First Party: ABC Technologies Pvt Ltd\n"
                    "Second Party: Employee name\n"
                    "Mention the roles of each party."
                ),
                height=150
            )

            effective_date = st.text_input(
                "Effective Date",
                placeholder="Example: 15 October 2026"
            )

        with col2:
            jurisdiction = st.text_input(
                "Jurisdiction / Governing Law",
                placeholder="Example: Tamil Nadu, India"
            )

            terms = st.text_area(
                "Key Terms and Conditions",
                placeholder=(
                    "Enter the important terms separated "
                    "by semicolons.\n\n"
                    "Example:\n"
                    "Responsibilities; Salary; "
                    "Confidentiality; Termination"
                ),
                height=150
            )

            additional_notes = st.text_area(
                "Additional Notes (Optional)",
                placeholder="Enter any additional requirements.",
                height=100
            )

        submitted = st.form_submit_button(
            "🚀 Generate Document",
            type="primary",
            use_container_width=True
        )

    # --------------------------------------
    # CALL BACKEND API
    # --------------------------------------

    if submitted:

        if not parties.strip():
            st.error("Please enter the parties involved.")

        elif not terms.strip():
            st.error("Please enter the key terms.")

        else:
            payload = {
    "document_type": "Non-Disclosure Agreement (NDA)",
    "first_party": "ABC Technologies Pvt Ltd",
    "second_party": "Employee Name",
    "terms": "Confidentiality; Non-disclosure; Protection of confidential information; Use of information; Intellectual property; Data security; Termination; Breach and remedies",
    "effective_date": "02 October 2026",
    "jurisdiction": "Tamil Nadu, India",
    "additional_notes": "The employee must keep all company confidential information strictly confidential during and after employment. Confidential information must not be disclosed to unauthorized persons. Include return or deletion of confidential materials upon termination and appropriate remedies for breach."
}
           

            try:
                with st.spinner(
                    "🤖 Generating your document..."
                ):
                    response = requests.post(
                        f"{API_URL}/generate",
                        json=payload,
                        timeout=120
                    )

                    response.raise_for_status()
                    result = response.json()

                    st.session_state["draft"] = (
                        result["document"]
                    )

                    st.session_state["draft_type"] = (
                        document_type
                    )

                    st.session_state["mode"] = (
                        result.get("mode", "unknown")
                    )

                st.success(
                    "✅ Document generated successfully!"
                )

            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Cannot connect to the backend. "
                    "Start FastAPI in another terminal."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "⏳ Request timed out. Check the "
                    "backend and AI service, then retry."
                )

            except requests.exceptions.HTTPError:
                st.error(
                    f"API error: {response.text[:1000]}"
                )

            except (KeyError, ValueError):
                st.error(
                    "The backend returned an invalid response."
                )

            except requests.exceptions.RequestException as error:
                st.error(f"Request failed: {error}")

    # ======================================
    # DOCUMENT PREVIEW AND EDITOR
    # ======================================

    if "draft" in st.session_state:

        st.divider()

        st.markdown(
            '<p class="section-title">📄 Document Preview</p>',
            unsafe_allow_html=True
        )

        st.caption(
            "Generation mode: "
            + st.session_state.get("mode", "unknown")
        )

        st.info(
            "You can edit the generated draft below "
            "before downloading it."
        )

        edited_document = st.text_area(
            "Edit Document",
            value=st.session_state["draft"],
            height=500,
            key="document_editor"
        )

        st.session_state["draft"] = edited_document

        # ----------------------------------
        # DOWNLOAD DOCUMENTS
        # ----------------------------------

        st.subheader("📥 Download Document")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                label="📃 Download TXT",
                data=format_txt(edited_document),
                file_name="legalease_document.txt",
                mime="text/plain",
                use_container_width=True
            )

        with col2:
            st.download_button(
                label="📝 Download DOCX",
                data=format_docx(
                    edited_document,
                    st.session_state["draft_type"]
                ),
                file_name="legalease_document.docx",
                mime=(
                    "application/"
                    "vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True
            )

        with col3:
            st.download_button(
                label="📕 Download PDF",
                data=format_pdf(
                    edited_document,
                    st.session_state["draft_type"]
                ),
                file_name="legalease_document.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        # ----------------------------------
        # CLEAR DOCUMENT
        # ----------------------------------

        if st.button(
            "🗑️ Clear Document",
            use_container_width=True
        ):
            for key in [
                "draft",
                "draft_type",
                "mode",
                "document_editor"
            ]:
                st.session_state.pop(key, None)

            st.rerun()


# ==========================================
# ABOUT PAGE
# ==========================================

elif page == "ℹ️ About":

    st.markdown(
        '<p class="section-title">ℹ️ About LegalEase</p>',
        unsafe_allow_html=True
    )

    st.write("""
    LegalEase is an AI-assisted legal document
    drafting application built using Python.

    It combines a Streamlit frontend, FastAPI
    backend and optional Google Gemini integration.
    """)

    st.subheader("Technology Stack")

    st.markdown("""
    - **Python:** Application programming
    - **Streamlit:** Frontend interface
    - **FastAPI:** Backend REST API
    - **Google Gemini:** AI-assisted drafting
    - **Python-docx:** Word document export
    - **FPDF2:** PDF generation
    """)

    st.subheader("Application API")

    try:
        health_response = requests.get(
            f"{API_URL}/health",
            timeout=3
        )

        if health_response.ok:
            st.success("🟢 Backend is connected.")
        else:
            st.error("🔴 Backend returned an error.")

    except requests.RequestException:
        st.error(
            "🔴 Backend is offline. Start the FastAPI server."
        )

    st.divider()

    st.subheader("Legal Disclaimer")

    st.write(
        "LegalEase provides AI-assisted document drafts "
        "for educational and productivity purposes. "
        "It does not provide legal advice, establish "
        "a lawyer-client relationship, or guarantee "
        "that a document complies with applicable law. "
        "Consult a qualified lawyer before signing "
        "or relying on any generated document."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="
        text-align: center;
        color: #64748b;
        padding: 15px;
    ">
        <h4>⚖️ LegalEase</h4>
        <p>AI-Powered Legal Document Generator</p>
        <small>
            Educational project | Review generated
            documents with a qualified lawyer.
        </small>
    </div>
    """,
    unsafe_allow_html=True
)