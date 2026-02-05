"""
PDF Generator Module
Generates formatted PDF resumes matching the exact formatting style
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from typing import Dict
import os


class PDFGenerator:
    """Generate formatted PDF resumes with exact styling"""

    # Margin specifications (in inches)
    TOP_MARGIN = 0.5 * inch
    BOTTOM_MARGIN = 0.5 * inch
    LEFT_MARGIN = 0.7 * inch
    RIGHT_MARGIN = 0.7 * inch

    # Font specifications
    FONT_NAME = "Times-Roman"
    FONT_BOLD = "Times-Bold"
    FONT_SIZE = 10.5
    NAME_FONT_SIZE = 14

    def __init__(self):
        """Initialize PDF generator"""
        self.page_width = letter[0] - self.LEFT_MARGIN - self.RIGHT_MARGIN

    def create_styles(self):
        """Create custom paragraph styles matching the sample resume"""
        styles = {}

        # Name style (14pt, bold, left-aligned)
        styles['Name'] = ParagraphStyle(
            'Name',
            fontName=self.FONT_BOLD,
            fontSize=self.NAME_FONT_SIZE,
            alignment=TA_LEFT,
            spaceAfter=2,
            textColor=colors.black,
            leading=16
        )

        # Contact line style (10.5pt, normal)
        styles['Contact'] = ParagraphStyle(
            'Contact',
            fontName=self.FONT_NAME,
            fontSize=self.FONT_SIZE,
            alignment=TA_LEFT,
            spaceAfter=2,
            textColor=colors.black,
            leading=13
        )

        # Contact right style (for email/links)
        styles['ContactRight'] = ParagraphStyle(
            'ContactRight',
            fontName=self.FONT_NAME,
            fontSize=self.FONT_SIZE,
            alignment=TA_RIGHT,
            spaceAfter=2,
            textColor=colors.HexColor('#0000EE'),  # Blue for links
            leading=13
        )

        # Section heading style (10.5pt, bold, uppercase, underlined)
        styles['SectionHeading'] = ParagraphStyle(
            'SectionHeading',
            fontName=self.FONT_BOLD,
            fontSize=self.FONT_SIZE,
            alignment=TA_LEFT,
            spaceAfter=8,
            spaceBefore=10,
            textColor=colors.black,
            leading=13
        )

        # Job title style (10.5pt, bold, left-aligned)
        styles['JobTitle'] = ParagraphStyle(
            'JobTitle',
            fontName=self.FONT_BOLD,
            fontSize=self.FONT_SIZE,
            alignment=TA_LEFT,
            spaceAfter=2,
            textColor=colors.black,
            leading=13
        )

        # Date style (10.5pt, bold, right-aligned)
        styles['Date'] = ParagraphStyle(
            'Date',
            fontName=self.FONT_BOLD,
            fontSize=self.FONT_SIZE,
            alignment=TA_RIGHT,
            spaceAfter=2,
            textColor=colors.black,
            leading=13
        )

        # Company/Location style (10.5pt, normal)
        styles['Company'] = ParagraphStyle(
            'Company',
            fontName=self.FONT_NAME,
            fontSize=self.FONT_SIZE,
            alignment=TA_LEFT,
            spaceAfter=4,
            textColor=colors.black,
            leading=13
        )

        # Bullet point style (10.5pt, normal, with proper indentation)
        styles['Bullet'] = ParagraphStyle(
            'Bullet',
            fontName=self.FONT_NAME,
            fontSize=self.FONT_SIZE,
            alignment=TA_JUSTIFY,
            spaceAfter=4,
            leftIndent=0,
            bulletIndent=0,
            textColor=colors.black,
            leading=14
        )

        # Skills category style (bold inline)
        styles['SkillCategory'] = ParagraphStyle(
            'SkillCategory',
            fontName=self.FONT_NAME,
            fontSize=self.FONT_SIZE,
            alignment=TA_LEFT,
            spaceAfter=4,
            textColor=colors.black,
            leading=14
        )

        return styles

    def generate_pdf(self, resume_data: Dict, output_path: str) -> bool:
        """
        Generate PDF resume from optimized data

        Args:
            resume_data: Dictionary containing resume sections
            output_path: Path to save generated PDF

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create PDF document with specified margins
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                topMargin=self.TOP_MARGIN,
                bottomMargin=self.BOTTOM_MARGIN,
                leftMargin=self.LEFT_MARGIN,
                rightMargin=self.RIGHT_MARGIN
            )

            # Create custom styles
            styles = self.create_styles()

            # Build content
            story = []

            # ===== HEADER SECTION =====
            name = resume_data.get('name', '')
            contact = resume_data.get('contact', {})

            # Name (left-aligned, bold, 14pt)
            story.append(Paragraph(f"<b>{name}</b>", styles['Name']))

            # Contact information in table format (2 rows x 2 columns)
            contact_data = [
                [
                    Paragraph(f"{contact.get('location', '')}", styles['Contact']),
                    Paragraph(f"<link href='mailto:{contact.get('email', '')}'>{contact.get('email', '')}</link>", styles['ContactRight'])
                ],
                [
                    Paragraph(f"{contact.get('phone', '')}", styles['Contact']),
                    Paragraph(f"<link href='{contact.get('github', '')}'>{contact.get('github', '')}</link>", styles['ContactRight'])
                ]
            ]

            contact_table = Table(contact_data, colWidths=[self.page_width * 0.5, self.page_width * 0.5])
            contact_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))
            story.append(contact_table)

            # Horizontal line after contact
            story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=10))

            # ===== PROFESSIONAL SUMMARY =====
            if 'professional_summary' in resume_data and resume_data['professional_summary']:
                story.append(Paragraph("<b>PROFESSIONAL SUMMARY</b>", styles['SectionHeading']))
                story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=8))

                for point in resume_data['professional_summary']:
                    story.append(Paragraph(f"• {point}", styles['Bullet']))

            # ===== PROFESSIONAL EXPERIENCE =====
            if 'professional_experience' in resume_data and resume_data['professional_experience']:
                story.append(Spacer(1, 0.05 * inch))
                story.append(Paragraph("<b>PROFESSIONAL EXPERIENCE</b>", styles['SectionHeading']))
                story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=8))

                for exp in resume_data['professional_experience']:
                    # Job title and dates in a table (left and right aligned)
                    job_title = exp.get('job_title', '')
                    dates = exp.get('dates', '')

                    title_data = [[
                        Paragraph(f"<b>{job_title}</b>", styles['JobTitle']),
                        Paragraph(f"<b>{dates}</b>", styles['Date'])
                    ]]

                    title_table = Table(title_data, colWidths=[self.page_width * 0.7, self.page_width * 0.3])
                    title_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                        ('TOPPADDING', (0, 0), (-1, -1), 0),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ]))
                    story.append(title_table)

                    # Company and location
                    company = exp.get('company', '')
                    location = exp.get('location', '')

                    company_data = [[
                        Paragraph(f"<b>{company}</b>", styles['Company']),
                        Paragraph(f"<b>{location}</b>", styles['Date'])
                    ]]

                    company_table = Table(company_data, colWidths=[self.page_width * 0.7, self.page_width * 0.3])
                    company_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                        ('TOPPADDING', (0, 0), (-1, -1), 0),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ]))
                    story.append(company_table)

                    # Achievements
                    for achievement in exp.get('achievements', []):
                        story.append(Paragraph(f"• {achievement}", styles['Bullet']))

                    story.append(Spacer(1, 0.05 * inch))

            # ===== EDUCATION =====
            if 'education' in resume_data and resume_data['education']:
                story.append(Paragraph("<b>EDUCATION</b>", styles['SectionHeading']))
                story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=8))

                for edu in resume_data['education']:
                    # Institution and location
                    institution = edu.get('institution', '')
                    location = edu.get('location', '')

                    edu_data = [[
                        Paragraph(f"<b>{institution}</b>", styles['JobTitle']),
                        Paragraph(f"<b>{location}</b>", styles['Date'])
                    ]]

                    edu_table = Table(edu_data, colWidths=[self.page_width * 0.7, self.page_width * 0.3])
                    edu_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                        ('TOPPADDING', (0, 0), (-1, -1), 0),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ]))
                    story.append(edu_table)

                    # Degree
                    degree = edu.get('degree', '')
                    story.append(Paragraph(degree, styles['Company']))

                    # Additional details
                    for detail in edu.get('details', []):
                        story.append(Paragraph(f"• {detail}", styles['Bullet']))

                    story.append(Spacer(1, 0.05 * inch))

            # ===== SKILLS =====
            if 'skills' in resume_data:
                story.append(Paragraph("<b>SKILLS</b>", styles['SectionHeading']))
                story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=8))

                skills = resume_data['skills']

                # Format: • Category: skill1, skill2, skill3
                if isinstance(skills, dict):
                    for category, skill_list in skills.items():
                        if skill_list:
                            category_name = category.replace('_', ' ').title()
                            skills_text = ', '.join(skill_list) if isinstance(skill_list, list) else skill_list
                            story.append(Paragraph(f"• <b>{category_name}:</b> {skills_text}", styles['Bullet']))
                else:
                    # If skills is a string or list
                    skills_text = ', '.join(skills) if isinstance(skills, list) else skills
                    story.append(Paragraph(f"• {skills_text}", styles['Bullet']))

            # ===== CERTIFICATIONS =====
            if 'certifications' in resume_data and resume_data['certifications']:
                story.append(Spacer(1, 0.05 * inch))
                story.append(Paragraph("<b>CERTIFICATIONS</b>", styles['SectionHeading']))
                story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=8))

                # Format certifications as a single line separated by commas
                cert_text = ', '.join(resume_data['certifications'])
                story.append(Paragraph(cert_text, styles['Bullet']))

            # Build PDF
            doc.build(story)
            return True

        except Exception as e:
            print(f"Error generating PDF: {e}")
            import traceback
            traceback.print_exc()
            return False
