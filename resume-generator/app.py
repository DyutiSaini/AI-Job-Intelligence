import streamlit as st

from chains import generate_resume_content

from jinja2 import Environment, FileSystemLoader

import pdfkit


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Generator",
    page_icon="📄",
    layout="centered",
)


# =========================================================
# HEADER
# =========================================================

st.title("AI Resume Generator")

st.write(
    "Create a professional, ATS-friendly resume "
    "with AI-assisted summary and experience sections."
)


# =========================================================
# RESUME FORM
# =========================================================

with st.form("resume_form"):

    # =====================================================
    # PERSONAL INFORMATION
    # =====================================================

    st.subheader("Personal Information")

    name = st.text_input(
        "Name",
        placeholder="e.g. Your Full Name",
    )

    email = st.text_input(
        "Email",
        placeholder="e.g. yourname@email.com",
    )

    phone = st.text_input(
        "Phone",
        placeholder="e.g. +91 XXXXX XXXXX",
    )

    linkedin = st.text_input(
        "LinkedIn",
        placeholder="e.g. linkedin.com/in/yourname",
    )

    github = st.text_input(
        "GitHub",
        placeholder="e.g. github.com/yourusername",
    )


    # =====================================================
    # CAREER INFORMATION
    # =====================================================

    st.subheader("Career Information")

    job_role = st.text_input(
        "Target Job Role",
        placeholder="e.g. Software Engineer Intern",
    )

    education = st.text_area(
        "Education",
        placeholder=(
            "Enter your educational qualifications.\n\n"
            "Example:\n"
            "Degree | University/College | Duration | CGPA/Percentage\n"
            "Class XII | School Name | Year | Percentage"
        ),
        height=120,
    )


    # =====================================================
    # SKILLS
    # =====================================================

    st.subheader("Technical Skills")

    languages = st.text_input(
        "Languages",
        placeholder="e.g. Python, C++, Java, JavaScript",
    )

    frameworks = st.text_input(
        "Frameworks / Libraries",
        placeholder="e.g. React, FastAPI, Django, Express",
    )

    databases = st.text_input(
        "Databases",
        placeholder="e.g. PostgreSQL, MongoDB, MySQL",
    )

    tools = st.text_input(
        "Tools / Technologies",
        placeholder="e.g. Git, Docker, Postman, AWS",
    )


    # =====================================================
    # EXPERIENCE
    # =====================================================

    st.subheader("Experience")

    st.caption(
        "Add your most relevant experience. "
        "You can leave unused entries empty."
    )

    # -----------------------------------------------------
    # EXPERIENCE 1
    # -----------------------------------------------------

    st.markdown("**Experience 1**")

    exp1_role = st.text_input(
        "Role",
        key="exp1_role",
        placeholder="e.g. Software Engineering Intern",
    )

    exp1_company = st.text_input(
        "Company / Organization",
        key="exp1_company",
        placeholder="e.g. Company Name",
    )

    exp1_dates = st.text_input(
        "Dates",
        key="exp1_dates",
        placeholder="e.g. May 2026 - July 2026",
    )

    exp1_bullets = st.text_area(
        "Responsibilities / Achievements",
        key="exp1_bullets",
        placeholder=(
            "Enter one bullet point per line.\n\n"
            "Example:\n"
            "Developed REST APIs using Python.\n"
            "Improved application performance by 20%.\n"
            "Collaborated with a team of developers."
        ),
        height=120,
    )


    # -----------------------------------------------------
    # EXPERIENCE 2
    # -----------------------------------------------------

    st.markdown("**Experience 2 (Optional)**")

    exp2_role = st.text_input(
        "Role",
        key="exp2_role",
        placeholder="e.g. Research Assistant",
    )

    exp2_company = st.text_input(
        "Company / Organization",
        key="exp2_company",
        placeholder="e.g. University / Organization",
    )

    exp2_dates = st.text_input(
        "Dates",
        key="exp2_dates",
        placeholder="e.g. January 2026 - April 2026",
    )

    exp2_bullets = st.text_area(
        "Responsibilities / Achievements",
        key="exp2_bullets",
        placeholder=(
            "Enter one bullet point per line."
        ),
        height=100,
    )


    # =====================================================
    # PROJECTS
    # =====================================================

    st.subheader("Projects")

    st.caption(
        "Add your projects with technologies and optional links."
    )

    # -----------------------------------------------------
    # PROJECT 1
    # -----------------------------------------------------

    st.markdown("**Project 1**")

    project1_name = st.text_input(
        "Project Name",
        key="project1_name",
        placeholder="e.g. Project Name",
    )

    project1_tech = st.text_input(
        "Technologies",
        key="project1_tech",
        placeholder="e.g. React, FastAPI, PostgreSQL",
    )

    project1_github = st.text_input(
        "GitHub URL",
        key="project1_github",
        placeholder="e.g. github.com/yourusername/project",
    )

    project1_demo = st.text_input(
        "Live Demo URL",
        key="project1_demo",
        placeholder="e.g. yourproject.com",
    )

    project1_description = st.text_area(
        "Project Description",
        key="project1_description",
        placeholder=(
            "Enter one bullet point per line.\n\n"
            "Example:\n"
            "Built a full-stack web application for users.\n"
            "Implemented authentication and database integration.\n"
            "Added search and filtering functionality."
        ),
        height=120,
    )


    # -----------------------------------------------------
    # PROJECT 2
    # -----------------------------------------------------

    st.markdown("**Project 2 (Optional)**")

    project2_name = st.text_input(
        "Project Name",
        key="project2_name",
        placeholder="e.g. Project Name",
    )

    project2_tech = st.text_input(
        "Technologies",
        key="project2_tech",
        placeholder="e.g. Python, Machine Learning, SQL",
    )

    project2_github = st.text_input(
        "GitHub URL",
        key="project2_github",
        placeholder="e.g. github.com/yourusername/project",
    )

    project2_demo = st.text_input(
        "Live Demo URL",
        key="project2_demo",
        placeholder="e.g. yourproject.com",
    )

    project2_description = st.text_area(
        "Project Description",
        key="project2_description",
        placeholder=(
            "Enter one bullet point per line."
        ),
        height=100,
    )


    # -----------------------------------------------------
    # PROJECT 3
    # -----------------------------------------------------

    st.markdown("**Project 3 (Optional)**")

    project3_name = st.text_input(
        "Project Name",
        key="project3_name",
        placeholder="e.g. Project Name",
    )

    project3_tech = st.text_input(
        "Technologies",
        key="project3_tech",
        placeholder="e.g. JavaScript, Node.js, MongoDB",
    )

    project3_github = st.text_input(
        "GitHub URL",
        key="project3_github",
        placeholder="e.g. github.com/yourusername/project",
    )

    project3_demo = st.text_input(
        "Live Demo URL",
        key="project3_demo",
        placeholder="e.g. yourproject.com",
    )

    project3_description = st.text_area(
        "Project Description",
        key="project3_description",
        placeholder=(
            "Enter one bullet point per line."
        ),
        height=100,
    )


    # =====================================================
    # ACHIEVEMENTS & CERTIFICATIONS
    # =====================================================

    st.subheader("Achievements & Certifications")

    achievements_text = st.text_area(
        "Achievements / Certifications",
        placeholder=(
            "Enter one achievement or certification per line.\n\n"
            "Example:\n"
            "Certification Name — Issuing Organization\n"
            "Hackathon Finalist — Event Name\n"
            "Scholarship / Award — Organization"
        ),
        height=120,
    )


    # =====================================================
    # SUBMIT
    # =====================================================

    submitted = st.form_submit_button(
        "Generate Resume",
        use_container_width=True,
    )


# =========================================================
# GENERATE RESUME
# =========================================================

if submitted:

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not name.strip():
        st.error("Please enter your name.")
        st.stop()

    if not email.strip():
        st.error("Please enter your email.")
        st.stop()

    if not job_role.strip():
        st.error("Please enter the target job role.")
        st.stop()


    # =====================================================
    # EDUCATION
    # =====================================================

    education_items = [
        item.strip()
        for item in education.split("\n")
        if item.strip()
    ]


    # =====================================================
    # EXPERIENCE DATA
    # =====================================================

    experiences = []

    if (
        exp1_role.strip()
        or exp1_company.strip()
        or exp1_dates.strip()
        or exp1_bullets.strip()
    ):

        experiences.append(
            {
                "role": exp1_role.strip(),
                "company": exp1_company.strip(),
                "dates": exp1_dates.strip(),
                "bullets": [
                    bullet.strip()
                    for bullet in exp1_bullets.split("\n")
                    if bullet.strip()
                ],
            }
        )


    if (
        exp2_role.strip()
        or exp2_company.strip()
        or exp2_dates.strip()
        or exp2_bullets.strip()
    ):

        experiences.append(
            {
                "role": exp2_role.strip(),
                "company": exp2_company.strip(),
                "dates": exp2_dates.strip(),
                "bullets": [
                    bullet.strip()
                    for bullet in exp2_bullets.split("\n")
                    if bullet.strip()
                ],
            }
        )


    # =====================================================
    # PROJECT DATA
    # =====================================================

    projects = []

    if (
        project1_name.strip()
        or project1_tech.strip()
        or project1_github.strip()
        or project1_demo.strip()
        or project1_description.strip()
    ):

        projects.append(
            {
                "name": project1_name.strip(),
                "technologies": project1_tech.strip(),
                "github": project1_github.strip(),
                "demo": project1_demo.strip(),
                "bullets": [
                    bullet.strip()
                    for bullet in project1_description.split("\n")
                    if bullet.strip()
                ],
            }
        )


    if (
        project2_name.strip()
        or project2_tech.strip()
        or project2_github.strip()
        or project2_demo.strip()
        or project2_description.strip()
    ):

        projects.append(
            {
                "name": project2_name.strip(),
                "technologies": project2_tech.strip(),
                "github": project2_github.strip(),
                "demo": project2_demo.strip(),
                "bullets": [
                    bullet.strip()
                    for bullet in project2_description.split("\n")
                    if bullet.strip()
                ],
            }
        )


    if (
        project3_name.strip()
        or project3_tech.strip()
        or project3_github.strip()
        or project3_demo.strip()
        or project3_description.strip()
    ):

        projects.append(
            {
                "name": project3_name.strip(),
                "technologies": project3_tech.strip(),
                "github": project3_github.strip(),
                "demo": project3_demo.strip(),
                "bullets": [
                    bullet.strip()
                    for bullet in project3_description.split("\n")
                    if bullet.strip()
                ],
            }
        )


    # =====================================================
    # ACHIEVEMENTS
    # =====================================================

    achievements = [
        achievement.strip()
        for achievement in achievements_text.split("\n")
        if achievement.strip()
    ]


    # =====================================================
    # SKILLS
    # =====================================================

    skills = {
        "Languages": [
            skill.strip()
            for skill in languages.split(",")
            if skill.strip()
        ],
        "Frameworks & Libraries": [
            skill.strip()
            for skill in frameworks.split(",")
            if skill.strip()
        ],
        "Databases": [
            skill.strip()
            for skill in databases.split(",")
            if skill.strip()
        ],
        "Tools & Technologies": [
            skill.strip()
            for skill in tools.split(",")
            if skill.strip()
        ],
    }


    # =====================================================
    # AI-GENERATED RESUME CONTENT
    # =========================================================

    experience_text_for_ai = "\n".join(
        [
            f"{experience['role']} | "
            f"{experience['company']} | "
            f"{experience['dates']}\n"
            + "\n".join(
                experience["bullets"]
            )
            for experience in experiences
        ]
    )

    ai_content = generate_resume_content(
        name=name,
        job_role=job_role,
        education=education,
        experience=experience_text_for_ai,
    )

    summary = ai_content["summary"]
    generated_experience = ai_content["experience"]


    # =====================================================
    # LOAD TEMPLATE
    # =====================================================

    env = Environment(
        loader=FileSystemLoader("templates")
    )

    template = env.get_template(
        "resume_template.html"
    )


    # =====================================================
    # RENDER TEMPLATE
    # =====================================================

    html_content = template.render(
        name=name,
        email=email,
        phone=phone,
        linkedin=linkedin,
        github=github,
        job_role=job_role,
        education=education_items,
        skills=skills,
        projects=projects,
        summary=summary,
        experience=experiences,
        generated_experience=generated_experience,
        achievements=achievements,
    )


    # =====================================================
    # PREVIEW
    # =====================================================

    st.subheader("Resume Preview")

    st.components.v1.html(
        html_content,
        height=1100,
        scrolling=True,
    )


    # =====================================================
    # PDF CONFIGURATION
    # =====================================================

    config = pdfkit.configuration(
        wkhtmltopdf=(
            r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        )
    )


    # =====================================================
    # GENERATE PDF
    # =====================================================

    pdfkit.from_string(
        html_content,
        "resume.pdf",
        configuration=config,
    )


    # =====================================================
    # DOWNLOAD
    # =====================================================

    with open("resume.pdf", "rb") as file:

        st.download_button(
            label="Download Resume PDF",
            data=file,
            file_name="resume.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


    # =====================================================
    # SUCCESS
    # =====================================================

    st.success(
        "Resume generated successfully!"
    )