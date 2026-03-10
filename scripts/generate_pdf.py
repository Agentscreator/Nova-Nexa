from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

OUTPUT_PATH = "outputs/QuantumCart_Investor_Briefing.pdf"

company_name = "QuantumCart"

cover_title = "QuantumCart — Investor Briefing"
cover_subtitle = "AI-Powered Ecommerce Analytics"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleCenter', parent=styles['Title'], alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Heading', parent=styles['Heading2'], spaceAfter=6))
styles.add(ParagraphStyle(name='Body', parent=styles['BodyText'], spaceAfter=8, leading=14))

# Content sections
sections = []

sections.append(("Table of Contents", "1. Company Overview\n2. Business Model Breakdown\n3. Competitor Landscape\n4. Onboarding Email Draft\n5. Sales Briefing\n6. Investor Memo (one-page)") )

sections.append(("Company Overview",
"QuantumCart provides AI-driven analytics and decisioning for ecommerce merchants, enabling automated merchandising, personalized lifecycle orchestration, and actionable intelligence across the customer journey. Our platform ingests sales, product, and behavioral data; applies proprietary causal and counterfactual models; and surfaces prioritized actions that increase conversion, AOV, and customer lifetime value. Founded in 2024, QuantumCart targets mid-market and enterprise retailers that require automated analytics which translate directly into executionable merchandising and marketing programs."))

sections.append(("Business Model Breakdown",
"""Product: Software-as-a-Service (SaaS) platform delivered via multi-tenant cloud. Core modules include: 1) Insights & Diagnostics — automated anomaly detection and causal attribution; 2) Optimization Engine — price, promotion and assortment recommendations; 3) Activation Suite — integrations into ad channels, email platforms and on-site experiences for automated execution; 4) Data Connectors & ETL.

Pricing: Tiered subscription model with three primary tiers — Growth (SMB), Scale (mid-market), and Enterprise — priced on ARR with usage-based add-ons for API calls and activation volume. Typical contract lengths: 12-36 months with discounts for multi-year commitments.

Revenue Streams: Recurring subscription ARR, professional services (data integration, model customization), performance fees (share of incremental revenue where clients opt-in), and marketplace integrations.

Customer Acquisition: GTM combines direct sales for enterprise, channel partnerships (systems integrators), and product-led growth for SMBs with a freemium diagnostics offering.

Key Metrics & KPIs: ARR growth rate, Net Revenue Retention (target >120% for enterprise cohort), Gross Margin (SaaS target 70%+), CAC payback (target <12 months), LTV:CAC (>3x).
"""))

sections.append(("Competitor Landscape",
"""Direct competitors include established analytics vendors and CDPs with ecommerce plug-ins (e.g., Segment/Twilio Segment, Amplitude), commerce analytics specialists (e.g., Glew, Littledata), and optimization engines (e.g., Dynamic Yield). Indirect competition includes full-stack commerce platforms offering analytics (e.g., Shopify Plus analytics ecosystem) and consulting firms.

Differentiation: QuantumCart differentiates on causal modeling and automated activation: instead of static dashboards, our product delivers prioritized, testable actions and closes the loop by pushing changes to ads, email and storefront. We emphasize ROI-first metrics, transparent uplift estimates, and guardrails for safe automation. Our integration fabric focuses on low-friction connectors to major storefronts (Shopify, BigCommerce), CDPs, and ad platforms.

Market Opportunity: Global ecommerce analytics market is growing with a CAGR in the high single digits. Targeting the mid-market and enterprise merchants addresses a high-value segment where data complexity and integration needs justify enterprise pricing, estimated TAM (addressable within target segments) of $2–4B annually for analytics and activation services.
"""))

sections.append(("Onboarding Email Draft",
"""Subject: Welcome to QuantumCart — Getting Started with Your AI Analytics

Dear [Client Name],

Welcome to QuantumCart. We're excited to partner with you to unlock the next wave of growth through AI-driven analytics and automated activation. Over the next 30 days we will: 1) complete data onboarding and verification, 2) configure core insights and KPI dashboards, 3) run baseline uplift tests and recommend prioritized actions for Q1.

Action items for you: provide storefront API credentials (Shopify/BigCommerce), share product catalog access, and nominate a technical contact for integration. Our team will schedule a kickoff workshop to align success metrics and deployment milestones.

If you have any questions, reply to this email or reach out to your customer success manager at cs@quantumcart.ai.

Best regards,
QuantumCart Onboarding Team
"""))

sections.append(("Sales Briefing",
"""Purpose: Provide the sales team with a concise narrative they can use in discovery and demos.

Elevator Pitch: QuantumCart turns analytics into action — our causal AI not only identifies what moved the needle, it recommends and automates the exact marketing and merchandising changes to reliably reproduce that uplift.

Discovery Questions:
- What are your top 3 ecommerce KPIs this year?
- How do you currently prioritize merchandising or promotion decisions?
- What systems do you use for storefront, email, and advertising?

Demo Focus: Show live example of demand-signal detection, a prioritized action list with projected uplift, and the activation workflow to push recommended updates to an ad campaign or price feed. Emphasize typical time-to-value: initial insights in 48–72 hours, measurable uplift within 6–12 weeks.

Objections & Responses:
- "We have an analytics team" → QuantumCart augments human analysts by surfacing causal tests and automating repeatable activation, reducing time-to-insight and operational overhead.
- "We’re concerned about automation risk" → We provide safety gates: staging, programmable guardrails, and human-in-the-loop approval for first N activations.

Win Criteria: A pilot showing statistically significant uplift, seamless integrations, and an agreed roadmap for scaling.
"""))
sections.append(("Investor Memo — One Page",
"""Executive Summary: QuantumCart is an enterprise-grade SaaS platform delivering causal AI and automated activation to ecommerce merchants. By shifting from descriptive dashboards to closed-loop decisioning, QuantumCart captures measurable uplift and converts analytics into revenue. The product targets mid-market and enterprise merchants and integrates with storefronts, CDPs, and ad platforms to execute prioritized recommendations.

Traction: Early pilots with pilot merchants showed 8–15% incremental revenue lift in targeted cohorts; initial ARR from early customers and pilot engagements is $750k with signs of strong expansion potential.

Business Model: Subscription-based ARR with professional services and optional performance fees. Gross margins target 70%+, with scalable activation integrations driving incremental revenue.

Team: Founders include a former director of data science at a major ecommerce platform and a CTO with distributed systems and ML infrastructure experience. The team includes product managers with domain experience in retail analytics.

Funding Ask: Seeking $4M in Seed round to accelerate product development (activate real-time connectors, expand marketing automation integrations), hire sales and customer success for enterprise GTM, and scale infrastructure. Use of funds: 45% product & engineering, 30% sales & GTM, 15% operations & hiring, 10% runway and legal. Runway target: 18–24 months.

Key Metrics Sought by Investors: ARR growth rate, NRR >120% for enterprise cohort, CAC payback <12 months, LTV:CAC >3x, and contribution margin trends.

Investor Opportunity: Large and growing market with clear monetizable outcomes; differentiated IP in causal uplift modeling and closed-loop activation. Seed round positions QuantumCart to scale enterprise sales and productize key automations for rapid adoption.
"""))

def create_pdf(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=LETTER,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=72)
    story = []

    # Cover will be drawn via onFirstPage
    story.append(Paragraph(cover_title, styles['TitleCenter']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(cover_subtitle, styles['TitleCenter']))
    story.append(Spacer(1, 36))
    story.append(Paragraph("Prepared for: Investors & Strategic Partners", styles['Body']))
    story.append(Paragraph("Date: 2026-03-09", styles['Body']))
    story.append(PageBreak())

    # Add sections
    for title, text in sections:
        story.append(Paragraph(title, styles['Heading']))
        # Split paragraphs by double newlines
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        for p in paragraphs:
            # Replace single newlines with spaces for safe wrapping
            p = p.replace('\n', ' ')
            story.append(Paragraph(p, styles['Body']))
        story.append(PageBreak())

    def on_first_page(canvas_obj, doc_obj):
        canvas_obj.saveState()
        # draw placeholder logo (rectangle)
        canvas_obj.setStrokeGray(0.4)
        canvas_obj.setFillGray(0.9)
        canvas_obj.rect(inch, 10*inch, 1.2*inch, 1.2*inch, fill=1)
        canvas_obj.setFillGray(0)
        canvas_obj.setFont('Helvetica-Bold', 24)
        canvas_obj.drawCentredString(4.25*inch, 10.9*inch, company_name)
        canvas_obj.restoreState()

    def on_later_pages(canvas_obj, doc_obj):
        canvas_obj.saveState()
        canvas_obj.setFont('Helvetica', 9)
        canvas_obj.drawString(inch, 0.75*inch, f"QuantumCart — Investor Briefing")
        canvas_obj.drawRightString(7.5*inch, 0.75*inch, "Page %d" % (doc_obj.page))
        canvas_obj.restoreState()

    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)

if __name__ == '__main__':
    import os
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    create_pdf(OUTPUT_PATH)
    print(f"Wrote PDF to {OUTPUT_PATH}")
