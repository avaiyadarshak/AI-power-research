import streamlit as st
from research import research_company
from ai_agent import generate_report

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet



st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖",
    layout="wide"
)


st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .info-card {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 20px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 45px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)



def create_pdf(report):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    story = []

    for line in report.split("\n"):

        line = line.strip()

        if not line:

            story.append(
                Spacer(1, 10)
            )

            continue

        # Clean Markdown
        clean_line = (
            line
            .replace("### ", "")
            .replace("## ", "")
            .replace("# ", "")
            .replace("**", "")
            .replace("* ", "• ")
        )

        # Main title
        if line.startswith("# "):

            story.append(
                Paragraph(
                    clean_line,
                    styles["Title"]
                )
            )

        # Main headings
        elif line.startswith("## "):

            story.append(
                Paragraph(
                    clean_line,
                    styles["Heading1"]
                )
            )

        # Sub headings
        elif line.startswith("### "):

            story.append(
                Paragraph(
                    clean_line,
                    styles["Heading2"]
                )
            )

        # Normal text
        else:

            story.append(
                Paragraph(
                    clean_line,
                    styles["BodyText"]
                )
            )

        story.append(
            Spacer(1, 6)
        )

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()


with st.sidebar:

    st.title("🤖 AI Research Agent")

    st.markdown("---")

    st.subheader("About")

    st.write(
        """
        This AI-powered agent researches companies
        and generates structured business intelligence
        reports with company-specific AI recommendations.
        """
    )

    st.markdown("---")

    st.subheader("Report Includes")

    st.write("🏢 Company Overview")

    st.write("📊 Key Business Information")

    st.write("⚠️ Potential Business Challenges")

    st.write("💡 AI Opportunities")

    st.write("🎯 Personalized CEO Pitch")

    st.write("🔗 Research Sources")

    st.markdown("---")

    st.caption(
        "Powered by Gemini AI + Tavily Search"
    )



st.markdown(
    """
    <div class="main-title">
    🤖 AI-Powered Research & Recommendation Agent
    </div>

    <div class="sub-title">
    Transform public company information into
    actionable business intelligence and AI opportunities.
    </div>
    """,
    unsafe_allow_html=True
)



with st.expander(
    "ℹ️ How does this AI Agent work?"
):

    st.write(
        """
        **Step 1:** Enter the name of a company.

        **Step 2:** The system performs web research
        using Tavily Search.

        **Step 3:** Gemini AI analyzes the collected
        information.

        **Step 4:** Potential business challenges
        are identified with reasoning.

        **Step 5:** Company-specific AI opportunities
        are generated.

        **Step 6:** A personalized CEO pitch is created.

        **Step 7:** The complete intelligence report
        can be downloaded as a PDF.
        """
    )


st.markdown("### 🔍 Research a Company")

company_name = st.text_input(
    "Enter Company Name",
    placeholder=(
        "Example: Adani Realty, Sobha, "
        "Prestige Group..."
    )
)


generate_button = st.button(
    "🚀 Generate Intelligence Report",
    type="primary"
)


if generate_button:

    if not company_name.strip():

        st.warning(
            "⚠️ Please enter a company name."
        )

    else:

        try:


            with st.status(
                "🔍 Researching company...",
                expanded=True
            ) as status:

                st.write(
                    f"Searching public information "
                    f"about {company_name}..."
                )

                research_data = research_company(
                    company_name
                )

                if not research_data:

                    status.update(
                        label="Research failed",
                        state="error"
                    )

                    st.error(
                        "No research information found."
                    )

                    st.stop()

                st.write(
                    f"✅ Collected "
                    f"{len(research_data)} "
                    f"research results."
                )

             

                st.write(
                    "🧠 Gemini AI is analyzing "
                    "the research..."
                )

                report = generate_report(
                    company_name,
                    research_data
                )

                st.write(
                    "✅ Business challenges identified."
                )

                st.write(
                    "✅ AI opportunities generated."
                )

                st.write(
                    "✅ CEO pitch created."
                )

                status.update(
                    label=(
                        "Intelligence Report "
                        "Generated Successfully!"
                    ),
                    state="complete",
                    expanded=False
                )


            
            st.success(
                f"✅ Intelligence report for "
                f"{company_name} is ready!"
            )


            

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Company",
                    company_name
                )

            with col2:

                st.metric(
                    "Research Results",
                    len(research_data)
                )

            with col3:

                st.metric(
                    "Report Status",
                    "Completed"
                )


            st.markdown("---")


          

            st.markdown(
                "## 📊 Company Intelligence Report"
            )

            st.markdown(report)


            

            st.markdown("---")

            with st.expander(
                "🔗 View Collected Research Sources"
            ):

                unique_urls = set()

                for item in research_data:

                    url = item.get(
                        "url",
                        ""
                    )

                    title = item.get(
                        "title",
                        "Research Source"
                    )

                    if (
                        url
                        and url not in unique_urls
                    ):

                        unique_urls.add(url)

                        st.markdown(
                            f"**{title}**"
                        )

                        st.write(url)

                        st.markdown("---")


        

            st.markdown(
                "### 📥 Export Intelligence Report"
            )

            pdf_data = create_pdf(
                report
            )

            st.download_button(
                label="📄 Download Full Report as PDF",
                data=pdf_data,
                file_name=(
                    f"{company_name.replace(' ', '_')}"
                    "_intelligence_report.pdf"
                ),
                mime="application/pdf",
                type="primary"
            )


        except Exception as e:

            st.error(
                f"❌ An error occurred: {e}"
            )


st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:gray;
        font-size:14px;
    ">
        AI-Powered Research & Recommendation Agent
        <br>
        Built using Python, Streamlit,
        Gemini AI and Tavily Search
    </div>
    """,
    unsafe_allow_html=True
)