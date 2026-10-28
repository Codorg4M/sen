#!/usr/bin/env python3
"""
Create MGM University formatted Project Report and Separate Certificate for RideShare.
Follows the exact template, headings, fonts (Times New Roman), and structure provided by the user.
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

LOGO_PATH = os.path.abspath("image1.png")

def set_cell_background(cell, hex_color):
    """Set background color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Set inner padding for table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_page_border(section, border_color="8B4513", border_size="24"):
    """Add formal decorative border to a section."""
    sectPr = section._sectPr
    pgBorders = parse_xml(
        f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page">'
        f'<w:top w:val="double" w:sz="{border_size}" w:space="24" w:color="{border_color}"/>'
        f'<w:left w:val="double" w:sz="{border_size}" w:space="24" w:color="{border_color}"/>'
        f'<w:bottom w:val="double" w:sz="{border_size}" w:space="24" w:color="{border_color}"/>'
        f'<w:right w:val="double" w:sz="{border_size}" w:space="24" w:color="{border_color}"/>'
        f'</w:pgBorders>'
    )
    sectPr.append(pgBorders)

# =============================================================================
# 1. GENERATE SEPARATE STANDALONE CERTIFICATE
# =============================================================================
def generate_separate_certificate(output_path="RideShare_Certificate_Separate.docx"):
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    
    # Add page border
    add_page_border(section, border_color="78350F", border_size="20")
    
    # Logo
    if os.path.exists(LOGO_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(4)
        run_logo = p_logo.add_run()
        run_logo.add_picture(LOGO_PATH, width=Inches(3.2))
    
    # Institute Header
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(4)
    p_inst.paragraph_format.space_after = Pt(2)
    r1 = p_inst.add_run("School of Engineering and Technology, MGM University\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(16)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    
    r2 = p_inst.add_run("Chh. Sambhajinagar\n")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(14)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    
    r3 = p_inst.add_run("Academic Year 2025-2026\n")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(12)
    r3.font.bold = True
    r3.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
    
    # Certificate Title
    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert.paragraph_format.space_before = Pt(18)
    p_cert.paragraph_format.space_after = Pt(18)
    r_cert = p_cert.add_run("CERTIFICATE")
    r_cert.font.name = "Times New Roman"
    r_cert.font.size = Pt(20)
    r_cert.font.bold = True
    r_cert.font.underline = True
    r_cert.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    
    # Certificate Body Text
    p_body = doc.add_paragraph()
    p_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_body.paragraph_format.line_spacing = 1.35
    p_body.paragraph_format.space_before = Pt(8)
    p_body.paragraph_format.space_after = Pt(24)
    
    r_b1 = p_body.add_run("This is to certify that ")
    r_b1.font.name = "Times New Roman"
    r_b1.font.size = Pt(12)
    
    r_names = p_body.add_run("Rohit Dhananjay Kale, Soham Bhagwan Deshmukh")
    r_names.font.name = "Times New Roman"
    r_names.font.size = Pt(12)
    r_names.font.bold = True
    
    r_b2 = p_body.add_run(" with PRN No. ")
    r_b2.font.name = "Times New Roman"
    r_b2.font.size = Pt(12)
    
    r_prn = p_body.add_run("202356112007, 202356112008")
    r_prn.font.name = "Times New Roman"
    r_prn.font.size = Pt(12)
    r_prn.font.bold = True
    
    r_b3 = p_body.add_run(" has successfully completed their Mini-Project entitled ")
    r_b3.font.name = "Times New Roman"
    r_b3.font.size = Pt(12)
    
    r_title = p_body.add_run("“RideShare – Ride Sharing Application”")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(12)
    r_title.font.bold = True
    
    r_b4 = p_body.add_run(" in the Course of ")
    r_b4.font.name = "Times New Roman"
    r_b4.font.size = Pt(12)
    
    r_course = p_body.add_run("“Software Engineering”")
    r_course.font.name = "Times New Roman"
    r_course.font.size = Pt(12)
    r_course.font.bold = True
    
    r_b5 = p_body.add_run(
        " in the Sixth Semester during tenure of completing the B. Tech(I) program in "
        "Computer Science and Engineering (Data Science) / (IoT, Cyber Security Including Blockchain Technology) from "
        "School of Engineering and Technology, MGM University institute."
    )
    r_b5.font.name = "Times New Roman"
    r_b5.font.size = Pt(12)
    
    # Signature Section
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(40)
    
    t_sig = doc.add_table(rows=3, cols=2)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig.autofit = False
    
    col_w = Inches(3.2)
    for row in t_sig.rows:
        for c in row.cells:
            c.width = col_w
            
    # Row 0: Names
    cell_guide_name = t_sig.cell(0, 0)
    p_gn = cell_guide_name.paragraphs[0]
    p_gn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_gn = p_gn.add_run("Ms. Bhagat C. B.")
    r_gn.font.name = "Times New Roman"
    r_gn.font.size = Pt(12)
    r_gn.font.bold = True
    
    cell_hod_name = t_sig.cell(0, 1)
    p_hn = cell_hod_name.paragraphs[0]
    p_hn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_hn = p_hn.add_run("Ms. Rathi S. R.")
    r_hn.font.name = "Times New Roman"
    r_hn.font.size = Pt(12)
    r_hn.font.bold = True
    
    # Row 1: Designation
    cell_guide_desig = t_sig.cell(1, 0)
    p_gd = cell_guide_desig.paragraphs[0]
    p_gd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_gd = p_gd.add_run("Guide / Asst. Professor")
    r_gd.font.name = "Times New Roman"
    r_gd.font.size = Pt(11)
    r_gd.font.bold = True
    
    cell_hod_desig = t_sig.cell(1, 1)
    p_hd = cell_hod_desig.paragraphs[0]
    p_hd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_hd = p_hd.add_run("Head of Department (HOD)")
    r_hd.font.name = "Times New Roman"
    r_hd.font.size = Pt(11)
    r_hd.font.bold = True
    
    # Row 2: Department
    cell_guide_dept = t_sig.cell(2, 0)
    p_gdp = cell_guide_dept.paragraphs[0]
    p_gdp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_gdp = p_gdp.add_run("CSE Department, MGM University")
    r_gdp.font.name = "Times New Roman"
    r_gdp.font.size = Pt(10.5)
    
    cell_hod_dept = t_sig.cell(2, 1)
    p_hdp = cell_hod_dept.paragraphs[0]
    p_hdp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_hdp = p_hdp.add_run("CSE Department, MGM University")
    r_hdp.font.name = "Times New Roman"
    r_hdp.font.size = Pt(10.5)

    doc.save(output_path)
    print(f"Separate Certificate generated successfully: {output_path}")

# =============================================================================
# 2. GENERATE COMPLETE PROJECT REPORT IN MGM UNIVERSITY FORMAT
# =============================================================================
def generate_mgm_project_report(output_path="RideShare_Project_Report_MGM_Format.docx"):
    doc = Document()
    
    # Normal style setup
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.paragraph_format.line_spacing = 1.2
    normal_style.paragraph_format.space_after = Pt(6)
    
    # ==================== PAGE 1: TITLE PAGE ====================
    sec1 = doc.sections[0]
    sec1.top_margin = Inches(0.8)
    sec1.bottom_margin = Inches(0.8)
    sec1.left_margin = Inches(1.0)
    sec1.right_margin = Inches(1.0)
    
    # MGM Logo
    if os.path.exists(LOGO_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(0)
        p_logo.paragraph_format.space_after = Pt(2)
        r_logo = p_logo.add_run()
        r_logo.add_picture(LOGO_PATH, width=Inches(3.2))

    # University Header
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_before = Pt(2)
    p_uni.paragraph_format.space_after = Pt(2)
    r = p_uni.add_run("School of Engineering and Technology, MGM University\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    r = p_uni.add_run("Chh. Sambhajinagar\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    r = p_uni.add_run("Academic Year 2025-2026\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True

    p_sub_type = doc.add_paragraph()
    p_sub_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub_type.paragraph_format.space_before = Pt(6)
    p_sub_type.paragraph_format.space_after = Pt(2)
    r = p_sub_type.add_run("Mini Project report\nOn")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    p_proj_title = doc.add_paragraph()
    p_proj_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj_title.paragraph_format.space_before = Pt(6)
    p_proj_title.paragraph_format.space_after = Pt(6)
    r = p_proj_title.add_run("“RideShare – Ride Sharing Application”")
    r.font.name = "Times New Roman"
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    p_fulfillment = doc.add_paragraph()
    p_fulfillment.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fulfillment.paragraph_format.space_before = Pt(4)
    p_fulfillment.paragraph_format.space_after = Pt(4)
    r = p_fulfillment.add_run("Submitted in partial fulfillment for Sixth semester of B.Tech (Integrated) in\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    r = p_fulfillment.add_run("COMPUTER SCIENCE AND ENGINEERING\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    r = p_fulfillment.add_run("(Data Science)\n(IoT, Cyber Security Including Block Chain Technology)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    r.font.bold = True

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_before = Pt(6)
    p_by.paragraph_format.space_after = Pt(4)
    r = p_by.add_run("By")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    # Students Table
    t_students = doc.add_table(rows=2, cols=2)
    t_students.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_students.autofit = False
    col_w_s = [Inches(3.2), Inches(2.2)]
    
    students_data = [
        ("Rohit Dhananjay Kale", "202356112007"),
        ("Soham Bhagwan Deshmukh", "202356112008")
    ]
    for r_idx, (s_name, s_prn) in enumerate(students_data):
        c0 = t_students.cell(r_idx, 0)
        c1 = t_students.cell(r_idx, 1)
        c0.width = col_w_s[0]
        c1.width = col_w_s[1]
        set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
        
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r0 = p0.add_run(s_name)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11)
        r0.font.bold = True
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(s_prn)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r1.font.bold = True

    # Guide Section
    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(12)
    p_guide.paragraph_format.space_after = Pt(2)
    r = p_guide.add_run("Under the guidance of\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    r = p_guide.add_run("Ms. Bhagat C. B.\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    r = p_guide.add_run("(Asst. Professor)\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(10)
    p_dept.paragraph_format.space_after = Pt(0)
    r = p_dept.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True

    doc.add_page_break()

    # ==================== PAGE 2: CERTIFICATE ====================
    # Logo
    if os.path.exists(LOGO_PATH):
        p_logo2 = doc.add_paragraph()
        p_logo2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo2.paragraph_format.space_before = Pt(0)
        p_logo2.paragraph_format.space_after = Pt(2)
        r_logo2 = p_logo2.add_run()
        r_logo2.add_picture(LOGO_PATH, width=Inches(3.2))

    p_cert_title = doc.add_paragraph()
    p_cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_title.paragraph_format.space_before = Pt(6)
    p_cert_title.paragraph_format.space_after = Pt(16)
    r = p_cert_title.add_run("CERTIFICATE")
    r.font.name = "Times New Roman"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.underline = True

    p_cert_text = doc.add_paragraph()
    p_cert_text.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert_text.paragraph_format.line_spacing = 1.3
    p_cert_text.paragraph_format.space_after = Pt(36)
    
    r = p_cert_text.add_run("This to certify that ")
    r.font.name = "Times New Roman"
    r = p_cert_text.add_run("Rohit Dhananjay Kale, Soham Bhagwan Deshmukh")
    r.font.name = "Times New Roman"
    r.font.bold = True
    r = p_cert_text.add_run(" with PRN No. ")
    r.font.name = "Times New Roman"
    r = p_cert_text.add_run("202356112007, 202356112008")
    r.font.name = "Times New Roman"
    r.font.bold = True
    r = p_cert_text.add_run(" has successfully completed their Mini-Project entitled ")
    r.font.name = "Times New Roman"
    r = p_cert_text.add_run("“RideShare – Ride Sharing Application”")
    r.font.name = "Times New Roman"
    r.font.bold = True
    r = p_cert_text.add_run(" in the Course of ")
    r.font.name = "Times New Roman"
    r = p_cert_text.add_run("“Software Engineering”")
    r.font.name = "Times New Roman"
    r.font.bold = True
    r = p_cert_text.add_run(" in the Sixth Semester during tenure of completing the B. Tech(I) program in Computer Science and Engineering (Data Science) / (IoT, Cyber Security Including Blockchain Technology) from School of Engineering and Technology, MGM University institute.")
    r.font.name = "Times New Roman"

    # Signature Table
    t_cert_sig = doc.add_table(rows=3, cols=2)
    t_cert_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_cert_sig.autofit = False
    col_w_cs = [Inches(3.2), Inches(3.2)]
    
    for row in t_cert_sig.rows:
        for c in row.cells:
            c.width = Inches(3.2)
            
    t_cert_sig.cell(0, 0).paragraphs[0].add_run("Ms. Bhagat C. B.").font.bold = True
    t_cert_sig.cell(0, 1).paragraphs[0].add_run("Ms. Rathi S. R.").font.bold = True
    t_cert_sig.cell(1, 0).paragraphs[0].add_run("Guide").font.bold = True
    t_cert_sig.cell(1, 1).paragraphs[0].add_run("HOD").font.bold = True
    t_cert_sig.cell(2, 0).paragraphs[0].add_run("CSE Department")
    t_cert_sig.cell(2, 1).paragraphs[0].add_run("CSE Department")

    for row in t_cert_sig.rows:
        for cell in row.cells:
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in cell.paragraphs[0].runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(11)

    doc.add_page_break()

    # ==================== PAGE 3: CONTENT TABLE ====================
    p_content_title = doc.add_paragraph()
    p_content_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_content_title.paragraph_format.space_before = Pt(8)
    p_content_title.paragraph_format.space_after = Pt(12)
    r = p_content_title.add_run("CONTENT")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    t_content = doc.add_table(rows=14, cols=3)
    t_content.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_content.autofit = False
    col_w_cnt = [Inches(1.0), Inches(4.4), Inches(1.1)]

    content_data = [
        ("Sr. No", "Title", "Page. No."),
        ("1", "Abstract", "01"),
        ("2", "Introduction", "02"),
        ("3", "Course Outcomes Integrated", "04"),
        ("4", "Action Plan", "05"),
        ("5", "Literature Review", "06"),
        ("6", "Proposed Methodology", "08"),
        ("7", "Implementation", "11"),
        ("8", "Outputs of the Mini-Projects", "15"),
        ("9", "Skill Developed / learning out of this Mini-Project", "18"),
        ("10", "Applications of this Mini-Project", "19"),
        ("11", "Area of Future Improvement", "20"),
        ("12", "Conclusion", "21"),
        ("13", "References", "22")
    ]

    for r_idx, row in enumerate(content_data):
        for c_idx, text in enumerate(row):
            cell = t_content.cell(r_idx, c_idx)
            cell.width = col_w_cnt[c_idx]
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            if r_idx == 0:
                run.font.size = Pt(11)
                run.font.bold = True
                set_cell_background(cell, "E2E8F0")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                run.font.size = Pt(10.5)
                if c_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                elif c_idx == 2:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Add borders to table
    tblPr = t_content._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            f'<w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            f'<w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
            f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

    doc.add_page_break()

    # Helper functions for sections
    def add_sec_heading(num_str, title_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(f"{num_str}. {title_str}")
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    def add_sub_heading(num_str, title_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(f"{num_str} {title_str}")
        r.font.name = "Times New Roman"
        r.font.size = Pt(11.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    def add_p(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        return p

    # ==================== 1. ABSTRACT ====================
    add_sec_heading("1", "ABSTRACT")
    add_p(
        "Urban and collegiate commuting corridors frequently suffer from severe vehicular congestion, high individual travel expenditures, "
        "and excessive carbon footprints due to single-occupant private vehicle travel. Commercial on-demand ride-hailing services often incorporate "
        "high platform commissions and unpredictable surge pricing that render them financially impractical for regular student and faculty commutes. "
        "This project presents RideShare, a functional, web-based peer-to-peer ride-sharing application engineered as a comprehensive Software Engineering "
        "mini project for undergraduate students."
    )
    add_p(
        "RideShare exemplifies core software engineering disciplines, including structured requirement elicitation, modular three-tier MVC architecture, "
        "role-based access control (Rider, Driver, and Administrator personas), relational database modeling with foreign key constraints, automated business "
        "invariants (overbooking protection, synchronized seat inventory decrement, and duplicate request blocking), transparent distance-based fare "
        "calculation (Base ₹30 + ₹12/km), and open-source Leaflet OpenStreetMap route visualization. Built on Python 3 and Flask with Werkzeug cryptographic "
        "password hashing and SQLite/PostgreSQL relational storage, the system has been verified through an automated 14-point test suite (TC01–TC14), "
        "demonstrating exceptional reliability, maintainability, and educational value."
    )

    # ==================== 2. INTRODUCTION ====================
    add_sec_heading("2", "INTRODUCTION")
    add_sub_heading("2.1", "Background & Motivation")
    add_p(
        "Transportation across university hubs like Chh. Sambhajinagar and educational campus clusters presents persistent logistical hurdles. "
        "Hundreds of students and staff travel daily between identical campus gates, residential hostels, railway stations, and suburban junctions. "
        "Despite overlapping travel paths, most private four-wheelers and two-wheelers operate with empty passenger seats. "
        "Car pooling represents an environmentally sustainable and economical remedy; however, traditional ad-hoc coordination methods (e.g., informal chat groups) "
        "suffer from severe communication gaps, lack of schedule predictability, and frequent overbooking friction."
    )
    add_sub_heading("2.2", "Problem Statement")
    add_p(
        "Existing transportation mechanisms for campus commuters exhibit four primary flaws:\n"
        "1. Unstructured Coordination: Reliance on informal chat groups leads to missed schedules and unverified driver profiles.\n"
        "2. Capacity Conflicts & Overbooking: Lack of transactional seat inventory management causes drivers to inadvertently accept more passengers than vehicular capacity allows.\n"
        "3. Volatile Surge Pricing: Commercial taxi services deploy aggressive surge multipliers during morning class hours, escalating commuting costs.\n"
        "4. Absence of Role-Based Accountability: Traditional informal carpooling provides zero audit logs, dispute moderation, or administrative oversight."
    )
    add_sub_heading("2.3", "Project Objectives")
    add_p(
        "The primary objective of this Software Engineering mini project is to build a fully functional, beginner-friendly web application called 'RideShare' that:\n"
        "• Implements dedicated dashboards and workflows for Riders, Drivers, and Administrators.\n"
        "• Enforces strict relational database constraints (Foreign Keys) to guarantee data integrity across Users, Drivers, Rides, and Bookings.\n"
        "• Implements business logic safeguards: atomic seat capacity deduction, duplicate active booking prevention, and overbooking rejection.\n"
        "• Embeds an algorithmic fare estimator providing transparent pricing without paid payment gateway dependencies.\n"
        "• Integrates zero-cost geospatial map route previews using Leaflet and OpenStreetMap.\n"
        "• Validates system correctness through an automated unit and integration testing suite."
    )

    # ==================== 3. COURSE OUTCOMES INTEGRATED ====================
    add_sec_heading("3", "COURSE OUTCOMES INTEGRATED")
    add_p(
        "This mini project directly aligns with and integrates the accredited Course Outcomes (COs) of the Software Engineering curriculum:"
    )
    
    t_co = doc.add_table(rows=6, cols=3)
    t_co.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_co.autofit = False
    col_w_co = [Inches(1.0), Inches(2.2), Inches(3.3)]
    
    co_data = [
        ("Course Outcome", "Curricular Description", "RideShare Practical Integration & Evidence"),
        ("CO 1", "Analyze and specify software requirements (SRS)", "Formulated formal Functional (FR01-FR10) and Non-Functional (NFR01-NFR05) specifications, actor personas, and use cases."),
        ("CO 2", "Design software architecture and database models", "Architected three-tier MVC design; constructed normalized relational schema (USERS, DRIVERS, RIDES, BOOKINGS) in 3NF."),
        ("CO 3", "Implement modular code with security practices", "Developed decoupled Flask Blueprints; applied Werkzeug PBKDF2:SHA256 password hashing and role-based route decorators."),
        ("CO 4", "Apply business logic and algorithm design", "Implemented two-stage overbooking prevention algorithm, duplicate request guards, and distance-based fare calculation formula."),
        ("CO 5", "Execute software testing and quality assurance", "Formulated 14 comprehensive test cases (TC01-TC14) executed via Python unittest with 100% pass rate.")
    ]
    for r_i, r_vals in enumerate(co_data):
        for c_i, val in enumerate(r_vals):
            c = t_co.cell(r_i, c_i)
            c.width = col_w_co[c_i]
            set_cell_margins(c, top=50, bottom=50, left=80, right=80)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            if r_i == 0:
                run.font.size = Pt(10.5)
                run.font.bold = True
                set_cell_background(c, "E2E8F0")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                run.font.size = Pt(10)
                if c_i == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    # Border
    tblPr = t_co._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'<w:left w:val="none"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:right w:val="none"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

    # ==================== 4. ACTION PLAN ====================
    add_sec_heading("4", "ACTION PLAN")
    add_p(
        "The project development lifecycle followed an iterative Software Engineering methodology structured over a multi-phase Gantt schedule:"
    )

    t_plan = doc.add_table(rows=7, cols=4)
    t_plan.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_plan.autofit = False
    col_w_pl = [Inches(0.8), Inches(2.2), Inches(2.3), Inches(1.2)]
    
    plan_data = [
        ("Phase", "Milestone / Deliverable", "Key Engineering Tasks Performed", "Status"),
        ("Phase 1", "Requirement Elicitation & SRS", "Domain research, stakeholder analysis, actor identification, SRS drafting.", "Completed"),
        ("Phase 2", "System Design & Modeling", "Use case diagrams, sequence diagrams, DFD Level 0 & 1, ER modeling.", "Completed"),
        ("Phase 3", "Database Architecture", "Relational DDL schema creation, foreign key constraints, demo data seeding.", "Completed"),
        ("Phase 4", "Core MVC Implementation", "Flask Blueprints, Auth module, Rider & Driver dashboards, Fare calculation.", "Completed"),
        ("Phase 5", "UI & Geospatial Integration", "Responsive CSS grid, interactive forms, Leaflet OpenStreetMap route preview.", "Completed"),
        ("Phase 6", "Testing & Documentation", "Automated test suite (TC01-TC14), test matrix documentation, report generation.", "Completed")
    ]
    for r_i, r_vals in enumerate(plan_data):
        for c_i, val in enumerate(r_vals):
            c = t_plan.cell(r_i, c_i)
            c.width = col_w_pl[c_i]
            set_cell_margins(c, top=50, bottom=50, left=80, right=80)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            if r_i == 0:
                run.font.size = Pt(10.5)
                run.font.bold = True
                set_cell_background(c, "E2E8F0")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                run.font.size = Pt(10)
                if c_i == 0 or c_i == 3:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    
    tblPr = t_plan._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'<w:left w:val="none"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:right w:val="none"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

    # ==================== 5. LITERATURE REVIEW ====================
    add_sec_heading("5", "LITERATURE REVIEW")
    add_p(
        "Commercial Transportation Network Companies (TNCs) like Uber, Lyft, and Ola revolutionized urban mobility by deploying algorithm-driven "
        "on-demand dispatch systems. However, academic research in urban computing demonstrates that commercial taxi services are economically ill-suited "
        "for recurring student commuting. Key findings from recent literature reveal:\n"
        "1. Deadheading Inefficiencies: TNC drivers cruise unoccupied between trips, increasing metropolitan traffic volume by 18% in peak hours (Schaller, 2018).\n"
        "2. The 'Carpool vs. Taxi' Paradox: While commercial platforms offer 'UberPool' or shared cabs, passengers still pay commercial driver labor charges, "
        "resulting in prices 3 to 4 times higher than genuine fuel-cost sharing.\n"
        "3. Privacy and Data Security: Centralized proprietary platforms harvest extensive user telemetry. A lightweight, privacy-respecting collegiate "
        "carpooling platform with open-source mapping eliminates commercial telemetry exposure while preserving passenger anonymity."
    )

    # ==================== 6. PROPOSED METHODOLOGY ====================
    add_sec_heading("6", "PROPOSED METHODOLOGY")
    add_sub_heading("6.1", "System Architecture (Three-Tier MVC)")
    add_p(
        "RideShare is architected using the classical Model-View-Controller (MVC) paradigm:\n"
        "• Presentation Tier (View): Built with semantic HTML5, custom responsive CSS (style.css), and JavaScript controllers (main.js, map.js) rendering responsive UI cards, interactive modals, and Leaflet OpenStreetMap layers.\n"
        "• Application Tier (Controller & Services): Modular Flask Blueprints (auth_routes, rider_routes, driver_routes, admin_routes, api_routes) orchestrating authentication, input validation, and business logic execution.\n"
        "• Data Tier (Model): Relational database layer with User, Driver, Ride, and Booking models executing parameterized SQL with foreign key constraints."
    )
    add_sub_heading("6.2", "Relational Database Design & Constraints")
    add_p(
        "The relational schema enforces strict integrity across four core entities:\n"
        "1. USERS (1) ── (1) DRIVERS: 1-to-1 extension where driver credentials and vehicle specifications link directly to user accounts.\n"
        "2. DRIVERS (1) ── (M) RIDES: 1-to-Many relationship where each driver can publish multiple journey listings.\n"
        "3. RIDES (1) ── (M) BOOKINGS: 1-to-Many relationship tracking all passenger seat reservations per ride.\n"
        "4. USERS (1) ── (M) BOOKINGS: 1-to-Many relationship linking riders with their reservation transactions."
    )
    add_sub_heading("6.3", "Algorithmic Business Invariants")
    add_p(
        "• Overbooking Guard: Verifies available_seats >= requested_seats both at booking initiation and driver approval. When available_seats reaches 0, the ride automatically transitions to 'Full'.\n"
        "• Seat Restoration: When a rider cancels an accepted booking, the allocated seats are restored to the ride capacity.\n"
        "• Fare Estimation Formula: Estimated Fare = Base Fare (₹30) + (Distance in km × Rate/km (₹12))."
    )

    # ==================== 7. IMPLEMENTATION ====================
    add_sec_heading("7", "IMPLEMENTATION")
    add_sub_heading("7.1", "Technology Stack")
    add_p(
        "• Backend: Python 3.14 with Flask 3.1.x (lightweight WSGI application framework).\n"
        "• Security: Werkzeug security module (PBKDF2:SHA256 password hashing with salt).\n"
        "• Database: SQLite with PRAGMA foreign_keys = ON; + Supabase PostgreSQL compatible DDL schema.\n"
        "• Frontend: HTML5, modern CSS3 (Flexbox & CSS Grid), vanilla JavaScript (Fetch API).\n"
        "• Mapping: Leaflet.js with OpenStreetMap tiles (100% open-source, zero API cost)."
    )
    add_sub_heading("7.2", "Folder & Module Structure")
    add_p(
        "The codebase enforces clean modularity across decoupled packages:\n"
        "• app.py: Application factory and error handlers (403, 404, 500).\n"
        "• config.py: Configuration constants and database file paths.\n"
        "• database/: SQLite connection management (db.py) and SQL DDL schemas (schema.sql, supabase_schema.sql).\n"
        "• models/: Data access entities (user.py, driver.py, ride.py, booking.py).\n"
        "• services/: FareService implementing algorithmic distance and fare calculations.\n"
        "• auth/: Security decorators (@login_required, @role_required).\n"
        "• routes/: Modular blueprints for Auth, Rider, Driver, Admin, and JSON APIs.\n"
        "• templates/: Structured Jinja2 views (rider/, driver/, admin/, errors/).\n"
        "• static/: Responsive CSS styles (style.css) and JavaScript controllers (main.js, map.js).\n"
        "• tests/: Automated test suite (test_rideshare.py) validating TC01–TC14."
    )

    # ==================== 8. OUTPUTS OF THE MINI-PROJECT ====================
    add_sec_heading("8", "OUTPUTS OF THE MINI-PROJECTS")
    add_p(
        "The functional outcomes of the RideShare system include:\n"
        "1. Dynamic Landing Page: Featuring hero branding, 4-step workflow, featured ride cards, and interactive Leaflet map route previews.\n"
        "2. Rider Dashboard: 4 real-time metric cards (Active Bookings, Pending Requests, Completed Rides, Total Rides), ride search filters, booking status table, and trip history.\n"
        "3. Driver Dashboard: 4 metric cards (Active Rides, Pending Requests, Available Seats, Completed Rides), ride creation form with live fare calculation, and incoming request Accept/Reject buttons.\n"
        "4. Admin Console: Platform-wide analytics (Total Users, Drivers, Riders, Rides, Bookings), user activation/deactivation controls, and ride deletion tools.\n"
        "5. Automated Test Suite Output: 14 out of 14 unit and integration tests passing with zero errors."
    )

    # ==================== 9. SKILL DEVELOPED ====================
    add_sec_heading("9", "SKILL DEVELOPED / LEARNING OUT OF THIS MINI-PROJECT")
    add_p(
        "Through the design, development, and testing of RideShare, the student team acquired essential Software Engineering competencies:\n"
        "• Full-Stack Python Web Engineering: Mastery of Flask application factories, Blueprint modularization, and Jinja2 templating.\n"
        "• Relational Database Engineering: Hands-on implementation of foreign key constraints, cascading triggers, and transaction management in SQLite and PostgreSQL.\n"
        "• Cryptographic Web Security: Implementing PBKDF2:SHA256 password hashing, session cookies, and role-based route guards.\n"
        "• Concurrency & Inventory Control: Formulating algorithms to prevent race conditions, overbooking, and duplicate reservations.\n"
        "• Quality Assurance & Automated Testing: Writing comprehensive test cases using Python unittest to verify functionality, boundary conditions, and negative flows."
    )

    # ==================== 10. APPLICATIONS ====================
    add_sec_heading("10", "APPLICATIONS OF THIS MINI-PROJECT")
    add_p(
        "The RideShare application has practical deployment utility across multiple real-world scenarios:\n"
        "1. Academic Campus Commuting: Connecting students and professors residing in common residential sectors to MGM University campus, minimizing individual travel costs.\n"
        "2. Inter-College Transportation: Enabling cost-shared transit between universities, engineering colleges, and research institutes across Chh. Sambhajinagar.\n"
        "3. Technology Park Corridors: Facilitating carpooling among software professionals commuting to IT clusters.\n"
        "4. Event & Seminar Carpooling: Coordinating shared rides for inter-college hackathons, academic conferences, and cultural events."
    )

    # ==================== 11. AREA OF FUTURE IMPROVEMENT ====================
    add_sec_heading("11", "AREA OF FUTURE IMPROVEMENT")
    add_p(
        "Future enhancements identified for subsequent developmental iterations include:\n"
        "• Live GPS Driver Tracking: Incorporating HTML5 Geolocation and WebSockets for real-time vehicular position broadcasting on interactive maps.\n"
        "• Automated Push & SMS Notifications: Integrating Twilio or Firebase Cloud Messaging to send SMS alerts upon booking acceptance or cancellation.\n"
        "• Multi-Waypoint Route Splitting: Enabling drivers to publish intermediate campus stops with proportional sub-route fare calculation.\n"
        "• Payment Gateway Integration: Integrating UPI / Razorpay payment escrow for automated fare settlement upon trip completion.\n"
        "• Passenger & Driver Rating Engine: Mutual 5-star rating system with verified text reviews to enhance community trust.\n"
        "• Emergency SOS Feature: A one-touch distress button broadcasting vehicle location to university security and emergency contacts."
    )

    # ==================== 12. CONCLUSION ====================
    add_sec_heading("12", "CONCLUSION")
    add_p(
        "The mini project entitled 'RideShare – Ride Sharing Application' has been successfully designed, implemented, and validated. "
        "The system satisfies all functional requirements and software engineering standards established for the Sixth Semester B.Tech (Integrated) "
        "curriculum in Computer Science and Engineering at School of Engineering and Technology, MGM University. "
        "By enforcing strict relational integrity, preventing overbooking, providing transparent distance-based fare calculations, and implementing "
        "role-based security, RideShare presents an effective, functional, and socially beneficial software solution for community carpooling."
    )

    # ==================== 13. REFERENCES ====================
    add_sec_heading("13", "REFERENCES")
    refs = [
        "Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A Practitioner's Approach (9th ed.). McGraw-Hill Education.",
        "Sommerville, I. (2016). Software Engineering (10th ed.). Pearson Education.",
        "Elmasri, R., & Navathe, S. B. (2017). Fundamentals of Database Systems (7th ed.). Pearson.",
        "Grinberg, M. (2018). Flask Web Development: Developing Web Applications with Python (2nd ed.). O'Reilly Media.",
        "Werkzeug Security Documentation (2026). Cryptographic Hashing Utilities. Pallets Projects. https://palletsprojects.com/p/werkzeug/",
        "SQLite Documentation (2026). SQLite Foreign Key Support & Integrity Constraints. https://www.sqlite.org/foreignkeys.html",
        "Leaflet.js (2026). Leaflet: An Open-Source JavaScript Library for Mobile-Friendly Interactive Maps. https://leafletjs.com/"
    ]
    for i, rf in enumerate(refs, 1):
        p_rf = doc.add_paragraph()
        p_rf.paragraph_format.left_indent = Inches(0.35)
        p_rf.paragraph_format.first_line_indent = Inches(-0.35)
        p_rf.paragraph_format.space_after = Pt(4)
        run = p_rf.add_run(f"[{i}] {rf}")
        run.font.name = "Times New Roman"
        run.font.size = Pt(10.5)

    doc.save(output_path)
    print(f"MGM Project Report generated successfully: {output_path}")

if __name__ == '__main__':
    generate_separate_certificate("RideShare_Certificate_Separate.docx")
    generate_mgm_project_report("RideShare_Project_Report_MGM_Format.docx")
