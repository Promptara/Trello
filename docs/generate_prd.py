# -*- coding: utf-8 -*-
"""
PROMPTARA Backend PRD Generator
Generates a comprehensive PRD PDF for the Spring Boot backend.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, ListFlowable, ListItem, Preformatted, HRFlowable, Image
)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

OUTPUT = r"C:\Users\Jikoyuooo\Trello-Promptara-FE\docs\PROMPTARA_Backend_PRD.pdf"

# ─────────────────────────────────────────────────────
# Theme colors (match frontend)
# ─────────────────────────────────────────────────────
BRAND = colors.HexColor("#3EB8B8")
BRAND_DARK = colors.HexColor("#2AA0A0")
INK = colors.HexColor("#17172E")
MUTED = colors.HexColor("#6B6B88")
FAINT = colors.HexColor("#B0AFBF")
SURFACE = colors.HexColor("#F7F6F3")
LINE = colors.HexColor("#E5E4EF")
SUCCESS = colors.HexColor("#22C55E")
WARN = colors.HexColor("#F59E0B")
DANGER = colors.HexColor("#EF4444")
CODE_BG = colors.HexColor("#0F0F1C")
CODE_FG = colors.HexColor("#E8F7F7")

# ─────────────────────────────────────────────────────
# Styles
# ─────────────────────────────────────────────────────
styles = getSampleStyleSheet()

class CallableStyle(ParagraphStyle):
    """ParagraphStyle that is also callable: H2("text") returns Paragraph(text, self)."""
    def __call__(self, text):
        return Paragraph(text, self)

H1 = CallableStyle('H1',
    fontName='Helvetica-Bold', fontSize=22, leading=28,
    textColor=INK, spaceBefore=18, spaceAfter=12)

H2 = CallableStyle('H2',
    fontName='Helvetica-Bold', fontSize=16, leading=22,
    textColor=BRAND_DARK, spaceBefore=16, spaceAfter=8,
    borderPadding=4)

H3 = CallableStyle('H3',
    fontName='Helvetica-Bold', fontSize=13, leading=18,
    textColor=INK, spaceBefore=10, spaceAfter=6)

H4 = CallableStyle('H4',
    fontName='Helvetica-Bold', fontSize=11, leading=15,
    textColor=BRAND_DARK, spaceBefore=8, spaceAfter=4)

BODY = ParagraphStyle('Body', parent=styles['BodyText'],
    fontName='Helvetica', fontSize=10, leading=15,
    textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6)

SMALL = ParagraphStyle('Small', parent=BODY,
    fontSize=9, leading=13, textColor=MUTED)

LABEL = ParagraphStyle('Label', parent=BODY,
    fontName='Helvetica-Bold', fontSize=9, leading=12,
    textColor=MUTED, alignment=TA_LEFT)

CODE = ParagraphStyle('Code', parent=styles['Code'],
    fontName='Courier', fontSize=8.5, leading=11,
    textColor=CODE_FG, backColor=CODE_BG,
    leftIndent=8, rightIndent=8,
    spaceBefore=4, spaceAfter=8,
    borderPadding=8, borderColor=CODE_BG)

INLINE_CODE = ParagraphStyle('InlineCode', parent=BODY,
    fontName='Courier', fontSize=9)

# ─────────────────────────────────────────────────────
# Cover page background
# ─────────────────────────────────────────────────────
def first_page(canv, doc):
    canv.saveState()
    width, height = A4
    canv.setFillColor(colors.HexColor("#0F0F1C"))
    canv.rect(0, 0, width, height, fill=1, stroke=0)
    # accent stripe
    canv.setFillColor(BRAND)
    canv.rect(width - 6, height * 0.55, 6, height * 0.45, fill=1, stroke=0)
    canv.setFillColor(colors.HexColor("#3EB8B8"))
    canv.setFont("Helvetica-Bold", 10)
    canv.drawString(2 * cm, 1.5 * cm, "PROMPTARA — Backend PRD")
    canv.setFillColor(colors.HexColor("#9090AA"))
    canv.drawRightString(width - 2 * cm, 1.5 * cm, "v1.0 · Confidential")
    canv.restoreState()

def later_pages(canv, doc):
    canv.saveState()
    width, height = A4
    # top accent
    canv.setStrokeColor(LINE)
    canv.setLineWidth(0.5)
    canv.line(2 * cm, height - 1.5 * cm, width - 2 * cm, height - 1.5 * cm)
    canv.setFont("Helvetica-Bold", 9)
    canv.setFillColor(INK)
    canv.drawString(2 * cm, height - 1.2 * cm, "PROMPTARA")
    canv.setFont("Helvetica", 9)
    canv.setFillColor(MUTED)
    canv.drawRightString(width - 2 * cm, height - 1.2 * cm, "Backend PRD · v1.0")
    # footer
    canv.setLineWidth(0.5)
    canv.line(2 * cm, 1.5 * cm, width - 2 * cm, 1.5 * cm)
    canv.setFont("Helvetica", 9)
    canv.setFillColor(MUTED)
    canv.drawString(2 * cm, 1.0 * cm, "Spring Boot · MySQL · Flyway · Docker")
    canv.drawRightString(width - 2 * cm, 1.0 * cm, f"Page {doc.page}")
    canv.restoreState()

# ─────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────
def code_block(text):
    # escape angle brackets and ampersand for ReportLab paragraph
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe = safe.replace("\n", "<br/>")
    safe = safe.replace(" ", "&nbsp;")
    return Paragraph(f'<font face="Courier" size="8" color="#E8F7F7">{safe}</font>', CODE)

def kv_table(rows):
    t = Table(rows, colWidths=[3.8 * cm, 12.6 * cm])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), MUTED),
        ('TEXTCOLOR', (1, 0), (1, -1), INK),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, -2), 0.3, LINE),
    ]))
    return t

def data_table(header, rows, col_widths=None):
    data = [header] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BACKGROUND', (0, 0), (-1, 0), INK),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('TEXTCOLOR', (0, 1), (-1, -1), INK),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, LINE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, SURFACE]),
    ]))
    return t

def endpoint_block(method, path, summary, auth="Bearer JWT", role="Authenticated"):
    method_color = {
        "GET": colors.HexColor("#3B82F6"),
        "POST": colors.HexColor("#22C55E"),
        "PATCH": colors.HexColor("#F59E0B"),
        "PUT": colors.HexColor("#F59E0B"),
        "DELETE": colors.HexColor("#EF4444"),
    }.get(method, INK)
    method_para = Paragraph(
        f'<font color="white" face="Helvetica-Bold" size="9">&nbsp;{method}&nbsp;</font>',
        BODY)
    path_para = Paragraph(
        f'<font face="Courier" size="9" color="#17172E"><b>{path}</b></font>',
        BODY)
    summary_para = Paragraph(
        f'<font color="#6B6B88" size="8.5">{summary}</font>',
        SMALL)
    auth_para = Paragraph(
        f'<font color="#6B6B88" size="8"><b>Auth:</b> {auth} &nbsp;·&nbsp; <b>Role:</b> {role}</font>',
        SMALL)
    t = Table([
        [method_para, path_para],
        ['', summary_para],
        ['', auth_para],
    ], colWidths=[2.0 * cm, 14.4 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), method_color),
        ('BACKGROUND', (0, 1), (0, -1), method_color),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('VALIGN', (1, 0), (1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('BOX', (0, 0), (-1, -1), 0.5, LINE),
    ]))
    return KeepTogether([t, Spacer(1, 6)])

def callout(title, body, color=BRAND):
    p = Paragraph(
        f'<font color="{color.hexval()}" face="Helvetica-Bold" size="9">{title}</font><br/>'
        f'<font color="#17172E" size="9">{body}</font>',
        BODY)
    t = Table([[p]], colWidths=[16.4 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FAFAF8")),
        ('LINEBEFORE', (0, 0), (0, 0), 3, color),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return KeepTogether([t, Spacer(1, 6)])

def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(f'<font size="10" color="#17172E">{x}</font>', BODY),
                  leftIndent=14, bulletColor=BRAND) for x in items],
        bulletType='bullet', start='circle', leftIndent=12, bulletFontSize=8
    )

# ─────────────────────────────────────────────────────
# Build the story
# ─────────────────────────────────────────────────────
story = []

# ═════ COVER PAGE ═════
story.append(Spacer(1, 4.5 * cm))
story.append(Paragraph(
    '<para align="left"><font color="#3EB8B8" face="Helvetica-Bold" size="11">'
    'PRODUCT REQUIREMENTS DOCUMENT</font></para>', BODY))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph(
    '<para align="left"><font color="white" face="Helvetica-Bold" size="44">'
    'PROMPTARA</font></para>', BODY))
story.append(Paragraph(
    '<para align="left"><font color="white" face="Helvetica-Bold" size="28">'
    'Backend Service</font></para>', BODY))
story.append(Spacer(1, 0.6 * cm))
story.append(Paragraph(
    '<para align="left"><font color="#9090AA" face="Helvetica" size="11">'
    'Spring Boot &nbsp;·&nbsp; MySQL 8 &nbsp;·&nbsp; Flyway &nbsp;·&nbsp; Docker</font></para>',
    BODY))
story.append(Spacer(1, 3 * cm))
story.append(Paragraph(
    '<para align="left"><font color="#3EB8B8" face="Helvetica-Bold" size="9">'
    'AGENCY WORKSPACE PLATFORM</font></para>', BODY))
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    '<para align="left"><font color="#9090AA" face="Helvetica" size="10">'
    'Kanban &nbsp;·&nbsp; Orders &nbsp;·&nbsp; Finance &nbsp;·&nbsp; Timeline &nbsp;·&nbsp; Team</font></para>',
    BODY))
story.append(Spacer(1, 4 * cm))
story.append(Paragraph(
    '<para align="left"><font color="#9090AA" face="Helvetica" size="9">'
    'Document Version: 1.0<br/>'
    'Status: Draft for Implementation<br/>'
    'Last Updated: 2026-06-06<br/>'
    'Owner: PROMPTARA Engineering</font></para>', BODY))
story.append(PageBreak())

# ═════ TABLE OF CONTENTS ═════
story.append(Paragraph("Table of Contents", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))
story.append(Spacer(1, 0.3 * cm))

toc_rows = [
    ["1.", "Executive Summary", "3"],
    ["2.", "Goals & Non-Goals", "4"],
    ["3.", "Tech Stack & High-Level Architecture", "5"],
    ["4.", "Non-Functional Requirements (NFR)", "7"],
    ["5.", "Domain Model & Entity Relationships", "10"],
    ["6.", "Database Schema (MySQL DDL)", "12"],
    ["7.", "Flyway Migration Strategy", "18"],
    ["8.", "API Specification — Authentication", "20"],
    ["9.", "API Specification — Users & Team", "24"],
    ["10.", "API Specification — Boards & Columns", "26"],
    ["11.", "API Specification — Cards (Kanban Core)", "29"],
    ["12.", "API Specification — Comments & Attachments", "34"],
    ["13.", "API Specification — Notifications", "36"],
    ["14.", "API Specification — Orders & Finance", "38"],
    ["15.", "Concurrency Handling Strategy", "41"],
    ["16.", "Low Latency & Performance Strategy", "45"],
    ["17.", "Security Requirements", "48"],
    ["18.", "Error Handling & Standard Response", "51"],
    ["19.", "Observability — Logging, Metrics, Tracing", "53"],
    ["20.", "Docker, Docker-Compose & Deployment", "55"],
    ["21.", "Spring Boot Project Structure", "58"],
    ["22.", "Implementation Roadmap & Milestones", "60"],
    ["23.", "Appendix — Acceptance Criteria & Test Plan", "62"],
]
toc_table = Table(toc_rows, colWidths=[1.2 * cm, 13.0 * cm, 2.2 * cm])
toc_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('TEXTCOLOR', (0, 0), (0, -1), BRAND_DARK),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (1, 0), (1, -1), INK),
    ('TEXTCOLOR', (2, 0), (2, -1), MUTED),
    ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LINEBELOW', (0, 0), (-1, -2), 0.3, LINE),
]))
story.append(toc_table)
story.append(PageBreak())

# ═════ 1. EXECUTIVE SUMMARY ═════
story.append(Paragraph("1. Executive Summary", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))
story.append(Paragraph(
    "PROMPTARA adalah <b>agency workspace platform</b> yang mengelola seluruh siklus "
    "proyek desain kreatif — mulai dari brief masuk, eksekusi studio, preview klien, "
    "touch-up, hingga deal selesai (Done Deal). Frontend sudah berjalan di React 18 + "
    "Vite dengan state ter-persist di localStorage. Dokumen ini mendefinisikan backend "
    "yang akan menggantikan localStorage tersebut dengan persistensi server, kolaborasi "
    "real-time-ready, dan agregasi finansial untuk seluruh tim agency.", BODY))
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "Backend ini dibangun di atas <b>Spring Boot 3.x (Java 21)</b>, <b>MySQL 8</b>, "
    "<b>Flyway</b> untuk version-controlled migration, dan dikemas dengan <b>Docker + "
    "docker-compose</b>. Sistem ditargetkan untuk traffic <b>multi-tenant per workspace</b>, "
    "dengan p95 latency &lt; 200 ms pada endpoint hot path (board read, card drag-drop) "
    "dan dukungan concurrency control yang aman untuk operasi Kanban yang sering "
    "diedit bersamaan.", BODY))

story.append(H2("Key Modules"))
story.append(data_table(
    ["Module", "Frontend View", "Backend Responsibility"],
    [
        ["Auth", "AuthScreen", "Register, login, JWT issuance, refresh, logout"],
        ["Board", "BoardView (Kanban)", "Board CRUD, column reorder, card drag-drop"],
        ["Card", "CardModal", "Card CRUD, status transitions, financial fields"],
        ["Comments", "CardModal", "Threaded comment per card, real-time fanout"],
        ["Attachments", "CardModal", "File upload (S3-compatible), metadata, signed URL"],
        ["Orders", "OrdersView", "Project history, filtering, CSV export"],
        ["Finance", "FinanceView", "Aggregation, monthly summary, by-type/status"],
        ["Calendar", "CalendarView", "Read-only timeline + month view from cards"],
        ["Team", "TeamView", "Workspace member listing, role management"],
        ["Notifications", "NotifPanel", "Due-soon, comment mention, assignment events"],
    ],
    col_widths=[3.0 * cm, 4.0 * cm, 9.4 * cm]
))

story.append(H2("Why this matters"))
story.append(bullets([
    "<b>Persistence:</b> Data agency (revenue, klien, deadline) tidak boleh hilang saat ganti browser/device.",
    "<b>Kolaborasi:</b> Beberapa anggota tim membuka board yang sama secara bersamaan.",
    "<b>Audit:</b> Riwayat order dan finance perlu sumber data tunggal yang konsisten.",
    "<b>Skalabilitas:</b> Setiap workspace bisa punya 5-30 user, ratusan card aktif.",
    "<b>Keamanan:</b> Data klien & nilai project sensitif — harus per-user authorization.",
]))
story.append(PageBreak())

# ═════ 2. GOALS & NON-GOALS ═════
story.append(Paragraph("2. Goals & Non-Goals", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("2.1 In-Scope (Goals)"))
story.append(bullets([
    "REST API JSON lengkap untuk semua TODO yang ada di frontend (auth, board, card, comment, attachment, notif, orders, finance).",
    "Auth berbasis <b>JWT access token (15 menit)</b> + <b>refresh token (7 hari)</b> dengan rotasi.",
    "<b>Role-based authorization</b>: Owner, Project Manager, Designer, Developer, Lainnya.",
    "<b>Multi-workspace per user</b> (1 user bisa join banyak workspace via membership).",
    "<b>Optimistic locking</b> pada card untuk drag-drop concurrent.",
    "<b>Soft-delete</b> pada entity penting (card, board) untuk audit & undo.",
    "<b>CSV / XLSX export</b> server-side untuk orders dan finance.",
    "<b>File upload</b> ke S3-compatible storage (MinIO untuk dev, AWS S3 untuk prod).",
    "<b>Notifikasi internal</b>: due-soon (cron), assignment (event), comment-mention.",
    "Docker-compose lokal yang menjalankan: API + MySQL + Redis + MinIO + Adminer.",
    "Flyway migration dengan strategi versioning yang aman untuk production.",
    "Observability: structured JSON logs, Prometheus metrics, health/readiness endpoints.",
]))

story.append(H2("2.2 Out-of-Scope (Non-Goals)"))
story.append(bullets([
    "<b>Realtime WebSocket sync</b> — V1 cukup REST polling; WebSocket di V2.",
    "<b>Public API / third-party integration</b> (Slack, Trello sync) — V2.",
    "<b>Billing & subscription</b> (Stripe, Midtrans) — V2.",
    "<b>Mobile native app</b> — frontend web responsive sudah cukup di V1.",
    "<b>AI features</b> (auto-tagging, smart estimates) — terpisah dari core backend.",
    "<b>Multi-region replication</b> — single-region MySQL primary di V1.",
]))

story.append(H2("2.3 Success Metrics"))
story.append(data_table(
    ["Metric", "Target", "Measurement"],
    [
        ["P50 latency (board read)", "< 80 ms", "Prometheus histogram"],
        ["P95 latency (board read)", "< 200 ms", "Prometheus histogram"],
        ["P95 latency (card update)", "< 250 ms", "Prometheus histogram"],
        ["Error rate (5xx)", "< 0.1 %", "Daily aggregate"],
        ["Availability (uptime)", "99.5 % monthly", "Healthcheck monitor"],
        ["Cold start (Docker)", "< 25 s", "Container readiness probe"],
        ["DB pool saturation", "< 70 % steady-state", "HikariCP metrics"],
    ],
    col_widths=[5.5 * cm, 4.5 * cm, 6.4 * cm]
))
story.append(PageBreak())

# ═════ 3. TECH STACK ═════
story.append(Paragraph("3. Tech Stack & High-Level Architecture", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("3.1 Stack Summary"))
story.append(data_table(
    ["Layer", "Technology", "Justification"],
    [
        ["Language", "Java 21 (LTS)", "Virtual threads (Loom) untuk konkurensi murah"],
        ["Framework", "Spring Boot 3.3.x", "Mature, ecosystem matang, Native AOT optional"],
        ["Build", "Maven 3.9 atau Gradle 8", "Pilih salah satu, dokumen pakai Maven"],
        ["Web", "Spring Web MVC", "Stable; Reactive (WebFlux) tidak diperlukan di V1"],
        ["Security", "Spring Security 6 + JJWT", "JWT issuance, BCrypt, method-level auth"],
        ["Persistence", "Spring Data JPA + Hibernate 6", "ORM untuk model relasional kompleks"],
        ["DB Driver", "mysql-connector-j 8.4", "Official MySQL connector"],
        ["Database", "MySQL 8.0 (InnoDB)", "Row-level locking, MVCC, JSON column"],
        ["Migration", "Flyway 10.x", "Version-controlled DDL, repeatable for seeds"],
        ["Cache", "Redis 7 + Spring Data Redis", "Session blacklist, hot-data cache"],
        ["File Storage", "MinIO (dev) / S3 (prod)", "Object storage untuk attachment"],
        ["Validation", "Jakarta Validation (Hibernate Validator)", "@Valid pada DTO"],
        ["JSON", "Jackson 2.17", "Default Spring serializer"],
        ["Mapping", "MapStruct 1.6", "Compile-time DTO ↔ Entity mapper"],
        ["Doc API", "springdoc-openapi 2.x", "Auto-generate OpenAPI 3 / Swagger UI"],
        ["Test", "JUnit 5, Mockito, Testcontainers", "Unit + integration test"],
        ["Container", "Docker, docker-compose v2", "Reproducible local & deployment"],
        ["CI/CD", "GitHub Actions", "Build → Test → Push image → Deploy"],
    ],
    col_widths=[3.0 * cm, 4.5 * cm, 8.9 * cm]
))

story.append(H2("3.2 High-Level Architecture"))
story.append(callout("Architecture style",
    "Classic <b>3-tier monolith</b> (Controller → Service → Repository) di-deploy "
    "sebagai single Spring Boot JAR di dalam Docker. Module-internal split per domain "
    "(<i>auth</i>, <i>board</i>, <i>card</i>, <i>finance</i>, <i>notification</i>). "
    "Tidak perlu microservices di V1 — over-engineering untuk skala saat ini."))

arch_diagram = """
┌────────────────────────────────────────────────────────────────────┐
│                       CLIENT (React + Vite)                        │
│            Bearer JWT  +  fetch()  +  optimistic UI                │
└──────────────────────────────┬─────────────────────────────────────┘
                               │  HTTPS / REST JSON
                               ▼
┌────────────────────────────────────────────────────────────────────┐
│                  REVERSE PROXY (Nginx / Traefik)                   │
│       TLS termination · gzip · rate limit (per IP & per user)      │
└──────────────────────────────┬─────────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────────┐
│             SPRING BOOT API (Java 21, Virtual Threads)             │
│                                                                    │
│  Controller layer   →  Service layer  →  Repository layer (JPA)    │
│  - Bean Validation  →  - @Transactional  →  - Spring Data          │
│  - JWT filter       →  - Caching         →  - Native query for hot │
│  - Rate limiter     →  - Event publisher    paths (finance agg)    │
└──────┬──────────────────────┬────────────────────────┬─────────────┘
       │                      │                        │
       ▼                      ▼                        ▼
┌──────────────┐      ┌───────────────┐       ┌─────────────────────┐
│  MySQL 8     │      │   Redis 7     │       │   MinIO / S3        │
│  InnoDB      │      │  - JWT block  │       │   - card attachment │
│  - WAL       │      │  - hot cache  │       │   - user avatar     │
│  - Flyway    │      │  - rate limit │       │   - signed URL      │
└──────────────┘      └───────────────┘       └─────────────────────┘
"""
story.append(code_block(arch_diagram))

story.append(H2("3.3 Request Lifecycle (typical card update)"))
story.append(bullets([
    "<b>1. Client</b> kirim <font face='Courier' size='9'>PATCH /api/v1/cards/{id}</font> dengan body partial update + header <font face='Courier' size='9'>If-Match: &lt;version&gt;</font>.",
    "<b>2. Nginx</b> apply TLS, gzip, IP rate-limit, forward ke API.",
    "<b>3. JWT filter</b> validasi access token; reject 401 jika invalid/expired.",
    "<b>4. Rate limiter</b> per-user (Redis token bucket); reject 429 jika exceed.",
    "<b>5. Controller</b> validasi DTO (Bean Validation).",
    "<b>6. Service</b> load entity, cek <font face='Courier' size='9'>version</font> match, apply update di transaction.",
    "<b>7. Repository</b> commit; Hibernate auto-increment <font face='Courier' size='9'>version</font> (optimistic locking).",
    "<b>8. Event publisher</b> fire <i>CardUpdatedEvent</i> → notification consumer queue.",
    "<b>9. Response</b> 200 dengan entity baru + version baru, atau 409 jika version mismatch.",
]))
story.append(PageBreak())

# ═════ 4. NFR ═════
story.append(Paragraph("4. Non-Functional Requirements (NFR)", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("4.1 Performance Targets"))
story.append(data_table(
    ["Endpoint Class", "P50 Target", "P95 Target", "P99 Target", "Rationale"],
    [
        ["Auth (login/refresh)", "< 100 ms", "< 250 ms", "< 500 ms", "BCrypt cost 12 dominan"],
        ["Board read (cards list)", "< 80 ms", "< 200 ms", "< 400 ms", "Hot path; aggressive cache"],
        ["Card create/update", "< 100 ms", "< 250 ms", "< 500 ms", "Tx + opt lock + audit"],
        ["Card drag-drop", "< 60 ms", "< 150 ms", "< 300 ms", "Single column update"],
        ["Comment add", "< 80 ms", "< 200 ms", "< 400 ms", "Insert + notif fanout async"],
        ["Finance aggregate", "< 200 ms", "< 500 ms", "< 1 s", "Cached 30s; native query"],
        ["Orders export CSV", "< 1.5 s", "< 3 s", "< 5 s", "Streaming response; not cached"],
        ["File upload (5 MB)", "< 2 s", "< 4 s", "< 8 s", "Direct stream ke S3"],
    ],
    col_widths=[3.5 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm, 6.3 * cm]
))

story.append(H2("4.2 Concurrency Requirements"))
story.append(bullets([
    "Backend harus aman jika <b>≥ 10 user</b> melakukan drag-drop di board yang sama bersamaan tanpa data corrupt.",
    "Operasi <b>reorder column</b> harus atomic (semua atau tidak sama sekali).",
    "<b>Counter</b> (cards.order, notification.unread_count) tidak boleh kehilangan increment.",
    "Komentar yang ditambahkan oleh dua user persis bersamaan harus dua-duanya tersimpan dengan urutan timestamp yang stabil.",
    "Refresh token rotation harus thread-safe — token lama langsung invalid setelah dipakai.",
    "<b>Login concurrent</b> dari device berbeda diperbolehkan; backend tidak invalidate sesi lain by default.",
]))

story.append(H2("4.3 Scalability Targets"))
story.append(data_table(
    ["Dimension", "V1 Target", "V2 Target"],
    [
        ["Concurrent active users", "200", "2,000"],
        ["Total registered users", "5,000", "50,000"],
        ["Boards per workspace", "100", "500"],
        ["Cards per board", "500", "2,000"],
        ["Requests per second (steady)", "100 RPS", "1,000 RPS"],
        ["Peak requests per second", "300 RPS", "3,000 RPS"],
        ["DB pool size (HikariCP)", "20 conn", "50 + read replica"],
        ["Horizontal scaling", "Single node", "≥ 3 nodes behind LB"],
    ],
    col_widths=[5.0 * cm, 5.5 * cm, 5.9 * cm]
))

story.append(H2("4.4 Availability & Reliability"))
story.append(bullets([
    "Uptime <b>≥ 99.5%</b> rolling 30 hari (max 3.6 jam downtime/bulan).",
    "<b>Graceful shutdown</b>: SIGTERM → tolak request baru → drain in-flight 30 detik → close DB pool.",
    "<b>Readiness probe</b> (<font face='Courier' size='9'>/actuator/health/readiness</font>) cek DB + Redis sebelum terima traffic.",
    "<b>Liveness probe</b> (<font face='Courier' size='9'>/actuator/health/liveness</font>) untuk restart jika deadlock.",
    "<b>Daily backup</b> MySQL (mysqldump + binlog) retensi 14 hari.",
    "<b>Point-in-time recovery</b> via binlog untuk insiden data corruption.",
]))

story.append(H2("4.5 Maintainability"))
story.append(bullets([
    "Coverage <b>≥ 70%</b> di service layer (unit + integration).",
    "OpenAPI spec auto-generate dari controller — wajib up-to-date setiap PR.",
    "Migration Flyway <b>never edit</b> file yang sudah merged; selalu file baru.",
    "Naming convention: <font face='Courier' size='9'>snake_case</font> di DB, <font face='Courier' size='9'>camelCase</font> di Java/JSON.",
    "Semua API path versioned: <font face='Courier' size='9'>/api/v1/...</font> — breaking change wajib bump ke <font face='Courier' size='9'>v2</font>.",
]))

story.append(H2("4.6 Compliance & Data"))
story.append(bullets([
    "Password <b>tidak pernah</b> dikembalikan di response apapun.",
    "Field sensitif (<i>password_hash</i>, <i>refresh_token</i>) tidak boleh ter-log.",
    "PII (email, nama) di-mask di structured log non-error level.",
    "Hak <b>delete account</b>: hard-delete user + anonimisasi referensi (replace with 'Deleted User').",
    "<b>Export semua data user</b> (GDPR-like) sebagai endpoint admin.",
]))
story.append(PageBreak())

# ═════ 5. DOMAIN MODEL ═════
story.append(Paragraph("5. Domain Model & Entity Relationships", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(Paragraph(
    "Berikut adalah ringkasan entity utama. Detail kolom & tipe ada di Bab 6 (DDL). "
    "Relasi digambarkan dengan notasi crow's foot sederhana.", BODY))

erd = """
┌─────────────────┐                 ┌──────────────────┐
│   workspaces    │                 │      users       │
│─────────────────│                 │──────────────────│
│ id (UUID) PK    │                 │ id (UUID) PK     │
│ name            │     1     ∞     │ email (UNIQUE)   │
│ slug (UNIQUE)   │◀─────────┐      │ password_hash    │
│ owner_user_id   │          │      │ name             │
│ created_at      │          │      │ role             │
└────────┬────────┘          │      │ initials, color  │
         │ 1                 │      │ created_at       │
         │                   │      │ deleted_at       │
         ▼ ∞                 │      └────────┬─────────┘
┌───────────────────────┐    │               │ 1
│  workspace_members    │    │               │
│───────────────────────│    │               ▼ ∞
│ id PK                 │────┘     ┌──────────────────────┐
│ workspace_id FK       │          │   refresh_tokens     │
│ user_id FK            │──────────│ user_id FK           │
│ role  (Owner/PM/...)  │          │ token_hash (UNIQUE)  │
│ joined_at             │          │ expires_at           │
└───────────────────────┘          │ revoked_at           │
         │                          └──────────────────────┘
         │
         ▼ ∞
┌─────────────────┐  1   ∞  ┌──────────────────┐  1   ∞  ┌──────────────────┐
│     boards      │────────▶│     columns      │────────▶│      cards       │
│─────────────────│         │──────────────────│         │──────────────────│
│ id PK           │         │ id PK            │         │ id PK            │
│ workspace_id FK │         │ board_id FK      │         │ board_id FK      │
│ name            │         │ name             │         │ column_id FK     │
│ color           │         │ color            │         │ title            │
│ archived        │         │ display_order    │         │ description      │
│ created_at      │         │ created_at       │         │ type, priority   │
│ deleted_at      │         └──────────────────┘         │ client_name      │
└─────────────────┘                                      │ value, dp_paid   │
                                                         │ due_date         │
                                                         │ display_order    │
                                                         │ version (OPT-LK) │
                                                         │ created_at       │
                                                         │ deleted_at       │
                                                         └────────┬─────────┘
                                                                  │ 1
                                                          ┌───────┼────────┐
                                                          ▼ ∞     ▼ ∞     ▼ ∞
                                              ┌──────────────┐ ┌──────┐ ┌────────────┐
                                              │ card_        │ │ card │ │ comments   │
                                              │  assignees   │ │_atta │ │            │
                                              │──────────────│ │chmen │ │ id PK      │
                                              │ card_id FK   │ │ts    │ │ card_id FK │
                                              │ user_id FK   │ │      │ │ author_id  │
                                              │ assigned_at  │ │      │ │ body       │
                                              └──────────────┘ │      │ │ created_at │
                                                               └──────┘ └────────────┘

┌──────────────────┐  1   ∞  ┌──────────────────────────────────────────────┐
│      users       │────────▶│              notifications                   │
└──────────────────┘         │──────────────────────────────────────────────│
                             │ id PK · recipient_user_id FK · type          │
                             │ ref_card_id (nullable) · payload (JSON)      │
                             │ read_at · created_at                         │
                             └──────────────────────────────────────────────┘
"""
story.append(code_block(erd))

story.append(H2("5.1 Entity Summary"))
story.append(data_table(
    ["Entity", "PK Type", "Purpose"],
    [
        ["workspaces", "UUID", "Tenant root — agency container"],
        ["users", "UUID", "Akun individu, login identity"],
        ["workspace_members", "BIGINT", "Junction: user ↔ workspace dengan role"],
        ["refresh_tokens", "UUID", "Server-side refresh token store (rotation)"],
        ["boards", "UUID", "Kanban board per workspace (1 project bundle)"],
        ["columns", "UUID", "Stage Kanban (Briefs, Studio, …)"],
        ["cards", "UUID", "Task/project utama, financial + assignment"],
        ["card_assignees", "BIGINT", "Junction: card ↔ user"],
        ["card_attachments", "UUID", "File metadata (object disimpan di S3)"],
        ["comments", "UUID", "Diskusi per card"],
        ["notifications", "UUID", "Event feed per user"],
        ["audit_log", "BIGINT", "Append-only audit untuk perubahan sensitif"],
    ],
    col_widths=[3.5 * cm, 2.0 * cm, 10.9 * cm]
))

story.append(H2("5.2 Identifier Choice — Why UUID v7?"))
story.append(bullets([
    "<b>UUID v7</b> (time-ordered) untuk PK utama: tidak bocorkan urutan ke client, tapi tetap sort-friendly di index B-tree.",
    "Hindari UUID v4 untuk PK karena random — fragmentasi index InnoDB tinggi.",
    "Junction table (assignees, members) tetap pakai <font face='Courier' size='9'>BIGINT AUTO_INCREMENT</font> — tidak diekspos ke client.",
    "Semua FK diberi index eksplisit; tidak mengandalkan implicit.",
]))
story.append(PageBreak())

# ═════ 6. DATABASE SCHEMA ═════
story.append(Paragraph("6. Database Schema (MySQL DDL)", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(Paragraph(
    "Semua tabel pakai <b>InnoDB</b>, charset <b>utf8mb4</b>, collation "
    "<b>utf8mb4_0900_ai_ci</b>. Timestamp pakai <b>DATETIME(3)</b> (millisecond) UTC. "
    "ID pakai <b>CHAR(36)</b> (UUID v7 string form) untuk readability dan compatibility "
    "dengan Hibernate. Setiap tabel punya <i>composite index</i> untuk hot query path.", BODY))

story.append(H2("6.1 users"))
story.append(code_block("""CREATE TABLE users (
  id              CHAR(36)      NOT NULL,
  email           VARCHAR(255)  NOT NULL,
  password_hash   VARCHAR(72)   NOT NULL,          -- BCrypt fixed length
  name            VARCHAR(120)  NOT NULL,
  role            VARCHAR(40)   NOT NULL,          -- Owner|PM|Designer|Developer|Other
  initials        VARCHAR(4)    NOT NULL,
  color           CHAR(7)       NOT NULL,          -- #RRGGBB
  email_verified  TINYINT(1)    NOT NULL DEFAULT 0,
  last_login_at   DATETIME(3)   NULL,
  created_at      DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  updated_at      DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
                              ON UPDATE CURRENT_TIMESTAMP(3),
  deleted_at      DATETIME(3)   NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_email (email),
  KEY idx_users_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"""))

story.append(H2("6.2 workspaces & members"))
story.append(code_block("""CREATE TABLE workspaces (
  id              CHAR(36)      NOT NULL,
  name            VARCHAR(120)  NOT NULL,
  slug            VARCHAR(60)   NOT NULL,
  owner_user_id   CHAR(36)      NOT NULL,
  created_at      DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  deleted_at      DATETIME(3)   NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_workspaces_slug (slug),
  KEY idx_workspaces_owner (owner_user_id),
  CONSTRAINT fk_ws_owner FOREIGN KEY (owner_user_id)
    REFERENCES users(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE workspace_members (
  id            BIGINT        NOT NULL AUTO_INCREMENT,
  workspace_id  CHAR(36)      NOT NULL,
  user_id       CHAR(36)      NOT NULL,
  role          VARCHAR(40)   NOT NULL,    -- Owner|PM|Designer|Developer|Other
  joined_at     DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  UNIQUE KEY uq_member (workspace_id, user_id),
  KEY idx_member_user (user_id),
  CONSTRAINT fk_member_ws  FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_member_usr FOREIGN KEY (user_id)      REFERENCES users(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""))

story.append(H2("6.3 refresh_tokens"))
story.append(code_block("""CREATE TABLE refresh_tokens (
  id            CHAR(36)      NOT NULL,
  user_id       CHAR(36)      NOT NULL,
  token_hash    CHAR(64)      NOT NULL,            -- SHA-256 of refresh JWT
  user_agent    VARCHAR(255)  NULL,
  ip_address    VARCHAR(45)   NULL,
  expires_at    DATETIME(3)   NOT NULL,
  revoked_at    DATETIME(3)   NULL,
  created_at    DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  UNIQUE KEY uq_refresh_hash (token_hash),
  KEY idx_refresh_user (user_id, expires_at),
  CONSTRAINT fk_refresh_user FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""))

story.append(H2("6.4 boards"))
story.append(code_block("""CREATE TABLE boards (
  id            CHAR(36)      NOT NULL,
  workspace_id  CHAR(36)      NOT NULL,
  name          VARCHAR(160)  NOT NULL,
  client_name   VARCHAR(160)  NULL,
  color         CHAR(7)       NOT NULL DEFAULT '#3EB8B8',
  archived      TINYINT(1)    NOT NULL DEFAULT 0,
  created_by    CHAR(36)      NOT NULL,
  created_at    DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  updated_at    DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
                            ON UPDATE CURRENT_TIMESTAMP(3),
  deleted_at    DATETIME(3)   NULL,
  PRIMARY KEY (id),
  KEY idx_board_workspace (workspace_id, deleted_at),
  CONSTRAINT fk_board_ws  FOREIGN KEY (workspace_id) REFERENCES workspaces(id),
  CONSTRAINT fk_board_usr FOREIGN KEY (created_by)   REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""))

story.append(H2("6.5 columns"))
story.append(code_block("""CREATE TABLE board_columns (
  id            CHAR(36)      NOT NULL,
  board_id      CHAR(36)      NOT NULL,
  name          VARCHAR(80)   NOT NULL,
  color         CHAR(7)       NOT NULL,
  display_order INT           NOT NULL,
  created_at    DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  UNIQUE KEY uq_col_order (board_id, display_order),
  KEY idx_col_board (board_id),
  CONSTRAINT fk_col_board FOREIGN KEY (board_id) REFERENCES boards(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""))
story.append(callout("Naming",
    "<font face='Courier' size='9'>columns</font> adalah reserved word di beberapa "
    "tool MySQL; pakai <font face='Courier' size='9'>board_columns</font> untuk aman."))

story.append(H2("6.6 cards"))
story.append(code_block("""CREATE TABLE cards (
  id            CHAR(36)      NOT NULL,
  board_id      CHAR(36)      NOT NULL,
  column_id     CHAR(36)      NOT NULL,
  title         VARCHAR(255)  NOT NULL,
  description   TEXT          NULL,
  type          VARCHAR(30)   NOT NULL DEFAULT 'other',  -- web-design|ui-ux|...
  priority      VARCHAR(10)   NOT NULL DEFAULT 'medium', -- high|medium|low
  client_name   VARCHAR(160)  NULL,
  value_idr     BIGINT        NOT NULL DEFAULT 0,        -- nilai project
  dp_paid_idr   BIGINT        NOT NULL DEFAULT 0,        -- DP diterima
  due_date      DATE          NULL,
  display_order INT           NOT NULL DEFAULT 0,        -- urutan di kolom
  version       BIGINT        NOT NULL DEFAULT 0,        -- @Version (optimistic lock)
  created_by    CHAR(36)      NOT NULL,
  created_at    DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  updated_at    DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
                            ON UPDATE CURRENT_TIMESTAMP(3),
  deleted_at    DATETIME(3)   NULL,
  PRIMARY KEY (id),
  KEY idx_cards_board_col   (board_id, column_id, display_order),
  KEY idx_cards_due         (due_date),
  KEY idx_cards_deleted     (deleted_at),
  KEY idx_cards_created     (created_at),
  CONSTRAINT fk_card_board  FOREIGN KEY (board_id)  REFERENCES boards(id),
  CONSTRAINT fk_card_col    FOREIGN KEY (column_id) REFERENCES board_columns(id),
  CONSTRAINT fk_card_user   FOREIGN KEY (created_by) REFERENCES users(id),
  CONSTRAINT chk_dp CHECK (dp_paid_idr >= 0 AND dp_paid_idr <= value_idr * 1.1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""))

story.append(H2("6.7 card_assignees"))
story.append(code_block("""CREATE TABLE card_assignees (
  id          BIGINT      NOT NULL AUTO_INCREMENT,
  card_id     CHAR(36)    NOT NULL,
  user_id     CHAR(36)    NOT NULL,
  assigned_by CHAR(36)    NOT NULL,
  assigned_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  UNIQUE KEY uq_card_user (card_id, user_id),
  KEY idx_assignee_user (user_id),
  CONSTRAINT fk_assign_card FOREIGN KEY (card_id) REFERENCES cards(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_assign_user FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""))

story.append(H2("6.8 comments"))
story.append(code_block("""CREATE TABLE comments (
  id          CHAR(36)      NOT NULL,
  card_id     CHAR(36)      NOT NULL,
  author_id   CHAR(36)      NOT NULL,
  body        TEXT          NOT NULL,
  created_at  DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  edited_at   DATETIME(3)   NULL,
  deleted_at  DATETIME(3)   NULL,
  PRIMARY KEY (id),
  KEY idx_cmt_card (card_id, created_at),
  CONSTRAINT fk_cmt_card FOREIGN KEY (card_id)   REFERENCES cards(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_cmt_user FOREIGN KEY (author_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""))

story.append(H2("6.9 card_attachments"))
story.append(code_block("""CREATE TABLE card_attachments (
  id              CHAR(36)      NOT NULL,
  card_id         CHAR(36)      NOT NULL,
  uploaded_by     CHAR(36)      NOT NULL,
  filename        VARCHAR(255)  NOT NULL,
  mime_type       VARCHAR(120)  NOT NULL,
  size_bytes      BIGINT        NOT NULL,
  storage_key     VARCHAR(500)  NOT NULL,    -- S3 object key
  checksum_sha256 CHAR(64)      NULL,
  uploaded_at     DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  KEY idx_att_card (card_id, uploaded_at),
  CONSTRAINT fk_att_card FOREIGN KEY (card_id) REFERENCES cards(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_att_user FOREIGN KEY (uploaded_by) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""))

story.append(H2("6.10 notifications"))
story.append(code_block("""CREATE TABLE notifications (
  id                CHAR(36)      NOT NULL,
  recipient_user_id CHAR(36)      NOT NULL,
  type              VARCHAR(40)   NOT NULL,     -- due-soon|comment|assignment|...
  message           VARCHAR(500)  NOT NULL,
  ref_card_id       CHAR(36)      NULL,
  ref_board_id      CHAR(36)      NULL,
  actor_user_id     CHAR(36)      NULL,         -- who triggered it
  payload           JSON          NULL,         -- flexible additional context
  read_at           DATETIME(3)   NULL,
  created_at        DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  KEY idx_notif_user_unread (recipient_user_id, read_at, created_at),
  CONSTRAINT fk_notif_user FOREIGN KEY (recipient_user_id) REFERENCES users(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""))

story.append(H2("6.11 audit_log"))
story.append(code_block("""CREATE TABLE audit_log (
  id           BIGINT        NOT NULL AUTO_INCREMENT,
  actor_user_id CHAR(36)     NULL,
  action       VARCHAR(60)   NOT NULL,        -- CARD_CREATE|CARD_UPDATE|...
  entity_type  VARCHAR(40)   NOT NULL,
  entity_id    CHAR(36)      NOT NULL,
  before_json  JSON          NULL,
  after_json   JSON          NULL,
  ip_address   VARCHAR(45)   NULL,
  created_at   DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  KEY idx_audit_entity (entity_type, entity_id, created_at),
  KEY idx_audit_actor  (actor_user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  PARTITION BY RANGE (TO_DAYS(created_at)) (
    PARTITION p_2026q2 VALUES LESS THAN (TO_DAYS('2026-07-01')),
    PARTITION p_2026q3 VALUES LESS THAN (TO_DAYS('2026-10-01')),
    PARTITION p_max    VALUES LESS THAN MAXVALUE
  );"""))

story.append(H2("6.12 Index Strategy"))
story.append(data_table(
    ["Index", "Why"],
    [
        ["idx_cards_board_col (board, column, display_order)",
         "Hot path: load semua card di satu board, urut per kolom"],
        ["idx_cards_due (due_date)",
         "Cron due-soon scan, calendar view"],
        ["idx_notif_user_unread (user, read_at, created_at)",
         "Sidebar bell — list unread terbaru cepat"],
        ["uq_col_order (board, display_order)",
         "Mencegah dua kolom punya order sama di board sama"],
        ["uq_users_email",
         "Validasi register cepat + enforce uniqueness"],
        ["uq_refresh_hash",
         "Lookup refresh token saat /refresh"],
    ],
    col_widths=[7.5 * cm, 8.9 * cm]
))
story.append(PageBreak())

# ═════ 7. FLYWAY ═════
story.append(Paragraph("7. Flyway Migration Strategy", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("7.1 Directory Layout"))
story.append(code_block("""src/main/resources/db/migration/
├── V1__init_users_and_workspaces.sql
├── V2__init_boards_columns_cards.sql
├── V3__init_comments_attachments.sql
├── V4__init_notifications_and_audit.sql
├── V5__seed_default_columns.sql
├── V6__add_card_priority_index.sql
├── ...
└── R__seed_demo_data.sql          (repeatable, dev/staging only)"""))

story.append(H2("7.2 Naming Convention"))
story.append(bullets([
    "<b>V&lt;n&gt;__</b> = versioned migration — <b>never</b> diubah setelah merged.",
    "<b>R__</b> = repeatable — di-run setiap kali checksum berubah; cocok untuk view, stored proc, seed dev.",
    "<b>U&lt;n&gt;__</b> = undo — <b>tidak dipakai di production</b>; lebih baik buat V baru yang revert.",
    "Nomor versi pakai <b>increment 1</b>, bukan timestamp — lebih mudah review PR.",
]))

story.append(H2("7.3 Configuration (application.yml)"))
story.append(code_block("""spring:
  flyway:
    enabled: true
    baseline-on-migrate: true
    baseline-version: 0
    locations: classpath:db/migration
    out-of-order: false           # strict order in production
    validate-on-migrate: true
    clean-disabled: true          # NEVER allow clean in any env from app
    table: flyway_schema_history
    placeholders:
      db_charset: utf8mb4"""))

story.append(H2("7.4 Migration Rules (Hard)"))
story.append(callout("Aturan wajib", (
    "<b>1.</b> Setelah PR di-merge ke main, file V&lt;n&gt;__ tidak boleh diubah. "
    "Perubahan checksum akan membuat Flyway gagal di production.<br/>"
    "<b>2.</b> Setiap migration harus <b>backward-compatible</b> minimal untuk satu "
    "rilis. Contoh: tambah kolom → boleh; <i>drop</i> kolom → harus dua langkah "
    "(kosongkan dulu di rilis N, drop di rilis N+1).<br/>"
    "<b>3.</b> Untuk perubahan besar (rename kolom, ubah tipe), pakai pola "
    "<i>expand → migrate → contract</i>.<br/>"
    "<b>4.</b> Migration harus <i>idempotent on retry</i> sebisa mungkin: pakai "
    "<font face='Courier' size='9'>CREATE TABLE IF NOT EXISTS</font>, "
    "<font face='Courier' size='9'>ADD INDEX IF NOT EXISTS</font>."
), DANGER))

story.append(H2("7.5 Schema Change Patterns"))
story.append(data_table(
    ["Change", "Pattern", "Notes"],
    [
        ["Add column nullable", "Single V file", "Aman; default NULL"],
        ["Add column NOT NULL", "3-step expand/contract", "Add nullable → backfill → set NOT NULL"],
        ["Rename column", "Add new → dual-write → drop old", "Aplikasi tulis ke dua kolom 1 rilis"],
        ["Drop column", "Stop writing (rilis N) → drop (N+1)", "Hindari window code mismatch"],
        ["Add index large table", "ALGORITHM=INPLACE, LOCK=NONE", "MySQL 8 online DDL"],
        ["Backfill data", "Repeatable migration + batch", "Chunk by PK range untuk hindari long tx"],
    ],
    col_widths=[3.5 * cm, 6.5 * cm, 6.4 * cm]
))

story.append(H2("7.6 Production Deployment Flow"))
story.append(bullets([
    "<b>Pre-deploy:</b> CI run <font face='Courier' size='9'>flyway info</font> dan <font face='Courier' size='9'>flyway validate</font> terhadap staging snapshot.",
    "<b>Deploy:</b> Spring Boot startup → Flyway auto-migrate sebelum bean Hibernate init.",
    "<b>Failure:</b> Container gagal start → readiness probe fail → load balancer tidak route traffic → rilis aman di-rollback.",
    "<b>Rollback:</b> Jangan run <font face='Courier' size='9'>undo</font>; deploy ulang versi container lama (DB tetap forward).",
]))
story.append(PageBreak())

# ═════ 8. AUTH API ═════
story.append(Paragraph("8. API Specification — Authentication", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(Paragraph(
    "Semua endpoint API berada di bawah prefix <font face='Courier' size='9'>"
    "/api/v1</font>. Body request/response menggunakan JSON UTF-8. Token dikirim "
    "lewat header <font face='Courier' size='9'>Authorization: Bearer &lt;jwt&gt;</font>.", BODY))

story.append(H2("8.1 Register"))
story.append(endpoint_block("POST", "/api/v1/auth/register",
    "Buat akun baru. Jika first user di workspace, otomatis Owner.",
    auth="Public", role="—"))
story.append(Paragraph("<b>Request body</b>", H4))
story.append(code_block("""{
  "name": "Andi Pratama",
  "email": "andi@promptara.id",
  "password": "P@ssw0rd123!",
  "role": "Designer"
}"""))
story.append(Paragraph("<b>Validation rules</b>", H4))
story.append(bullets([
    "<font face='Courier' size='9'>name</font>: 2-120 char, trimmed.",
    "<font face='Courier' size='9'>email</font>: format RFC 5322, lowercased server-side, unique.",
    "<font face='Courier' size='9'>password</font>: min 8, harus mengandung huruf + angka. Hash BCrypt cost 12.",
    "<font face='Courier' size='9'>role</font>: enum [Owner, Project Manager, Designer, Developer, Lainnya].",
]))
story.append(Paragraph("<b>Response 201 Created</b>", H4))
story.append(code_block("""{
  "user": {
    "id": "01890d4c-7e0b-7c5e-9b3a-...",
    "name": "Andi Pratama",
    "email": "andi@promptara.id",
    "role": "Designer",
    "initials": "AP",
    "color": "#3EB8B8",
    "createdAt": "2026-06-06T08:11:23.482Z"
  },
  "accessToken":  "eyJhbGciOi...",
  "refreshToken": "eyJhbGciOi...",
  "expiresIn": 900
}"""))
story.append(Paragraph("<b>Error responses</b>", H4))
story.append(data_table(
    ["Code", "When", "Body field"],
    [
        ["409 CONFLICT", "Email sudah terdaftar", "code: EMAIL_TAKEN"],
        ["400 BAD REQUEST", "Validation fail", "fields[]: { name, message }"],
        ["429 TOO MANY", "Rate limit (5/menit per IP)", "retryAfterSeconds"],
    ],
    col_widths=[3.5 * cm, 6.5 * cm, 6.4 * cm]
))

story.append(H2("8.2 Login"))
story.append(endpoint_block("POST", "/api/v1/auth/login",
    "Tukar email+password jadi access+refresh token.",
    auth="Public", role="—"))
story.append(code_block("""// Request
{ "email": "andi@promptara.id", "password": "P@ssw0rd123!" }

// Response 200
{ "user": { ... }, "accessToken": "...", "refreshToken": "...", "expiresIn": 900 }

// Response 401
{ "code": "INVALID_CREDENTIALS", "message": "Email atau password salah." }"""))
story.append(callout("Security hardening",
    "Jangan beri tahu apakah email yang salah atau passwordnya. Pesan generic "
    "<i>'Email atau password salah'</i> mencegah user enumeration. Brute-force "
    "diatasi dengan rate limit + exponential backoff per email "
    "(5 attempt → lock 15 menit, di-track via Redis)."))

story.append(H2("8.3 Refresh Token"))
story.append(endpoint_block("POST", "/api/v1/auth/refresh",
    "Tukar refresh token lama jadi access token + refresh token baru (rotation).",
    auth="Refresh token", role="—"))
story.append(code_block("""// Request
{ "refreshToken": "eyJhbGciOi..." }

// Response 200 — NOTE: refreshToken adalah token BARU; yang lama langsung invalid
{ "accessToken": "...", "refreshToken": "...", "expiresIn": 900 }

// Response 401
{ "code": "REFRESH_TOKEN_REVOKED" }"""))
story.append(Paragraph("<b>Server behavior</b>", H4))
story.append(bullets([
    "Hash refresh token (SHA-256) → lookup di <font face='Courier' size='9'>refresh_tokens</font>.",
    "Jika <font face='Courier' size='9'>revoked_at IS NOT NULL</font> atau <font face='Courier' size='9'>expires_at &lt; now()</font> → 401.",
    "Mark old token <font face='Courier' size='9'>revoked_at = now()</font>, insert new row dengan token baru — <b>atomic dalam 1 transaction</b>.",
    "<b>Reuse detection:</b> Jika token yang sudah revoked dipakai lagi → revoke <i>seluruh chain</i> user tersebut (signal token theft).",
]))

story.append(H2("8.4 Logout"))
story.append(endpoint_block("POST", "/api/v1/auth/logout",
    "Revoke refresh token saat ini + blacklist access token sampai expiry.",
    auth="Bearer JWT"))
story.append(code_block("""// Request
{ "refreshToken": "eyJhbGciOi..." }

// Response 204 No Content"""))
story.append(Paragraph("Access token JTI ditambahkan ke Redis dengan TTL = sisa "
    "lifetime token, sehingga filter JWT akan reject sampai expired natural.", BODY))

story.append(H2("8.5 Me (current user)"))
story.append(endpoint_block("GET", "/api/v1/auth/me",
    "Ambil profile user yang sedang login.", auth="Bearer JWT"))
story.append(code_block("""// Response 200
{
  "id": "01890d4c-...",
  "name": "Andi Pratama",
  "email": "andi@promptara.id",
  "role": "Designer",
  "initials": "AP",
  "color": "#3EB8B8",
  "workspaces": [
    { "id": "...", "name": "PROMPTARA Studio", "role": "Designer" }
  ]
}"""))

story.append(H2("8.6 JWT Structure"))
story.append(code_block("""// Access token (15 menit)
{
  "iss": "promptara-api",
  "sub": "01890d4c-7e0b-7c5e-9b3a-...",  // userId
  "aud": "promptara-web",
  "exp": 1717661283,
  "iat": 1717660383,
  "jti": "9f1b...",                       // for blacklist
  "role": "Designer",
  "ws":   "01890d4d-..."                  // active workspaceId
}

// Refresh token (7 hari) — disimpan hash-nya di DB
{
  "iss": "promptara-api",
  "sub": "01890d4c-...",
  "typ": "refresh",
  "jti": "rt-9f1b...",
  "exp": 1718265183
}"""))
story.append(bullets([
    "Algoritma: <b>HS256</b> dengan secret rotasi setiap 90 hari (env var).",
    "Production siap pindah ke <b>RS256</b> jika perlu issuer/verifier split.",
    "Clock skew toleransi: 60 detik (untuk container time drift).",
]))
story.append(PageBreak())

# ═════ 9. USERS & TEAM ═════
story.append(Paragraph("9. API Specification — Users & Team", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("9.1 List workspace members"))
story.append(endpoint_block("GET", "/api/v1/workspaces/{wsId}/members",
    "Daftar anggota workspace untuk Team view & assignee picker.",
    auth="Bearer JWT", role="Member"))
story.append(code_block("""// Response 200
{
  "items": [
    {
      "id": "01890d4c-...",
      "name": "Andi Pratama",
      "email": "andi@promptara.id",
      "role": "Designer",
      "initials": "AP",
      "color": "#3EB8B8",
      "stats": { "totalAssigned": 12, "activeAssigned": 5 }
    }
  ],
  "total": 8
}"""))

story.append(H2("9.2 Invite member"))
story.append(endpoint_block("POST", "/api/v1/workspaces/{wsId}/members",
    "Undang user existing (by email) ke workspace.",
    auth="Bearer JWT", role="Owner / Project Manager"))
story.append(code_block("""// Request
{ "email": "siti@promptara.id", "role": "Project Manager" }

// Response 201
{ "userId": "...", "role": "Project Manager", "joinedAt": "..." }"""))

story.append(H2("9.3 Update member role"))
story.append(endpoint_block("PATCH", "/api/v1/workspaces/{wsId}/members/{userId}",
    "Ubah role member (hanya Owner).",
    auth="Bearer JWT", role="Owner"))
story.append(code_block("""// Request
{ "role": "Designer" }

// Response 200
{ "userId": "...", "role": "Designer" }"""))

story.append(H2("9.4 Remove member"))
story.append(endpoint_block("DELETE", "/api/v1/workspaces/{wsId}/members/{userId}",
    "Hapus dari workspace; assignment di-unassign cascade.",
    auth="Bearer JWT", role="Owner"))
story.append(callout("Side effect",
    "Saat member di-remove: semua <b>card_assignees</b> entry di-cascade delete. "
    "Card yang jadi <i>unassigned</i> akan generate notifikasi untuk Owner."))

story.append(H2("9.5 Update profile (self)"))
story.append(endpoint_block("PATCH", "/api/v1/users/me",
    "Update nama, color, password sendiri.", auth="Bearer JWT"))
story.append(code_block("""// Request
{
  "name": "Andi P.",
  "color": "#EC4899",
  "currentPassword": "old...",      // required jika ubah password
  "newPassword": "new..."           // optional
}

// Response 200 — user object terbaru"""))

story.append(H2("9.6 Delete account (self)"))
story.append(endpoint_block("DELETE", "/api/v1/users/me",
    "Hard delete account + anonimisasi referensi.", auth="Bearer JWT"))
story.append(bullets([
    "Owner workspace harus transfer kepemilikan dulu — kalau belum, response 409.",
    "Comments & audit log: <font face='Courier' size='9'>author_id</font> dipertahankan, tapi user tampil sebagai <i>'Deleted User'</i> via JOIN check.",
    "Refresh token di-revoke semua.",
]))
story.append(PageBreak())

# ═════ 10. BOARDS & COLUMNS ═════
story.append(Paragraph("10. API Specification — Boards & Columns", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("10.1 List boards"))
story.append(endpoint_block("GET", "/api/v1/workspaces/{wsId}/boards",
    "Sidebar — list board aktif di workspace.", auth="Bearer JWT", role="Member"))
story.append(code_block("""// Response 200
{
  "items": [
    {
      "id": "01890dab-...",
      "name": "Client Garuda Q3",
      "color": "#3EB8B8",
      "cardCount": 24,
      "createdAt": "2026-05-12T...",
      "archived": false
    }
  ],
  "total": 6
}"""))

story.append(H2("10.2 Create board"))
story.append(endpoint_block("POST", "/api/v1/workspaces/{wsId}/boards",
    "Buat board baru. Otomatis spawn 5 default column (Briefs, Studio, Preview, Touch Up, Done Deal).",
    auth="Bearer JWT", role="Owner / Project Manager"))
story.append(code_block("""// Request
{ "name": "Brand X Rebranding", "clientName": "Brand X", "color": "#EC4899" }

// Response 201
{
  "id": "...",
  "name": "Brand X Rebranding",
  "color": "#EC4899",
  "columns": [
    { "id": "...", "name": "Briefs",    "color": "#6366F1", "displayOrder": 0 },
    { "id": "...", "name": "Studio",    "color": "#F59E0B", "displayOrder": 1 },
    { "id": "...", "name": "Preview",   "color": "#3B82F6", "displayOrder": 2 },
    { "id": "...", "name": "Touch Up",  "color": "#EC4899", "displayOrder": 3 },
    { "id": "...", "name": "Done Deal", "color": "#22C55E", "displayOrder": 4 }
  ]
}"""))

story.append(H2("10.3 Get board with columns + cards (hot path)"))
story.append(endpoint_block("GET", "/api/v1/boards/{boardId}",
    "Load satu board lengkap untuk render Kanban view.",
    auth="Bearer JWT", role="Member"))
story.append(callout("Performance critical",
    "Endpoint ini adalah <b>hot path</b> — paling sering dipanggil. Implementasi: "
    "1 query <i>boards</i>, 1 query <i>board_columns</i> (sorted), 1 query <i>cards</i> "
    "dengan <font face='Courier' size='9'>JOIN FETCH</font> ke assignees. Cache di Redis "
    "dengan key <font face='Courier' size='9'>board:{id}:v{updatedAt}</font> TTL 60 detik. "
    "Invalidate via <i>cache-aside</i> saat ada write."))
story.append(code_block("""// Response 200
{
  "id": "...",
  "name": "Brand X Rebranding",
  "color": "#EC4899",
  "columns": [
    {
      "id": "col-1", "name": "Briefs", "color": "#6366F1", "displayOrder": 0,
      "cards": [
        {
          "id": "card-...",
          "title": "Logo exploration round 1",
          "type": "branding",
          "priority": "high",
          "clientName": "Brand X",
          "valueIdr": 15000000,
          "dpPaidIdr": 7500000,
          "dueDate": "2026-06-30",
          "displayOrder": 0,
          "version": 4,
          "assigneeIds": ["user-...", "user-..."],
          "commentCount": 3,
          "attachmentCount": 2,
          "createdAt": "2026-06-01T..."
        }
      ]
    }
  ]
}"""))

story.append(H2("10.4 Update board"))
story.append(endpoint_block("PATCH", "/api/v1/boards/{boardId}",
    "Rename, ubah warna, archive.",
    auth="Bearer JWT", role="Owner / Project Manager"))

story.append(H2("10.5 Delete board (soft)"))
story.append(endpoint_block("DELETE", "/api/v1/boards/{boardId}",
    "Set deleted_at; card & column ikut tertutup. Bisa di-restore 30 hari.",
    auth="Bearer JWT", role="Owner"))

story.append(H2("10.6 Reorder columns"))
story.append(endpoint_block("PUT", "/api/v1/boards/{boardId}/columns/reorder",
    "Atomic: kirim seluruh urutan baru.", auth="Bearer JWT", role="Owner / PM"))
story.append(code_block("""// Request
{
  "order": ["col-3", "col-1", "col-2", "col-4", "col-5"]
}

// Response 200
{ "columns": [ ... ] }"""))
story.append(callout("Concurrency",
    "Operasi reorder dijalankan dalam 1 transaksi dengan "
    "<font face='Courier' size='9'>SELECT ... FOR UPDATE</font> pada semua kolom board "
    "yang bersangkutan. Update <font face='Courier' size='9'>display_order</font> pakai "
    "trick <i>negate-then-flip</i> untuk hindari konflik unique key:<br/>"
    "<font face='Courier' size='9'>UPDATE board_columns SET display_order = -display_order "
    "WHERE board_id=?</font>; kemudian set nilai positif baru."))

story.append(H2("10.7 Create column"))
story.append(endpoint_block("POST", "/api/v1/boards/{boardId}/columns",
    "Tambah stage Kanban kustom.", auth="Bearer JWT", role="Owner / PM"))

story.append(H2("10.8 Rename / recolor column"))
story.append(endpoint_block("PATCH", "/api/v1/columns/{columnId}",
    "Update name dan/atau color.", auth="Bearer JWT", role="Owner / PM"))

story.append(H2("10.9 Delete column"))
story.append(endpoint_block("DELETE", "/api/v1/columns/{columnId}",
    "Tolak jika ada card di dalamnya (force=true → pindah ke kolom pertama).",
    auth="Bearer JWT", role="Owner"))
story.append(PageBreak())

# ═════ 11. CARDS ═════
story.append(Paragraph("11. API Specification — Cards (Kanban Core)", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("11.1 Create card"))
story.append(endpoint_block("POST", "/api/v1/boards/{boardId}/cards",
    "Buat card baru di kolom yang ditentukan.",
    auth="Bearer JWT", role="Member"))
story.append(code_block("""// Request
{
  "columnId": "col-1",
  "title": "Logo exploration round 1",
  "description": "Eksplorasi mark + wordmark, minimal 3 opsi.",
  "type": "branding",
  "priority": "high",
  "clientName": "Brand X",
  "valueIdr": 15000000,
  "dpPaidIdr": 7500000,
  "dueDate": "2026-06-30",
  "assigneeIds": ["user-aa", "user-bb"]
}

// Response 201
{ "id": "card-...", "version": 0, ... }    // full card object"""))
story.append(Paragraph("<b>Server side defaults</b>", H4))
story.append(bullets([
    "<font face='Courier' size='9'>displayOrder</font>: server hitung <font face='Courier' size='9'>MAX(displayOrder)+1024</font> di kolom target (gap stride untuk reorder cepat).",
    "<font face='Courier' size='9'>createdAt</font>, <font face='Courier' size='9'>updatedAt</font>: server time UTC.",
    "<font face='Courier' size='9'>createdBy</font>: dari JWT sub.",
    "Validasi: <font face='Courier' size='9'>dpPaidIdr ≤ valueIdr × 1.1</font> (DB constraint).",
]))

story.append(H2("11.2 Update card (partial)"))
story.append(endpoint_block("PATCH", "/api/v1/cards/{cardId}",
    "Partial update. Semua field optional. Wajib kirim header If-Match.",
    auth="Bearer JWT", role="Member"))
story.append(code_block("""// Headers
If-Match: 4               // current version, dari last GET

// Request (any subset)
{ "title": "Logo round 2", "priority": "medium", "dpPaidIdr": 10000000 }

// Response 200
{ "id": "card-...", "version": 5, ... }

// Response 409 (version conflict)
{
  "code": "VERSION_CONFLICT",
  "message": "Card sudah diubah orang lain. Refresh dulu.",
  "currentVersion": 7
}"""))

story.append(H2("11.3 Move card (drag-drop) — atomic"))
story.append(endpoint_block("POST", "/api/v1/cards/{cardId}/move",
    "Endpoint khusus drag-drop. Lebih efisien dibanding PATCH umum.",
    auth="Bearer JWT", role="Member"))
story.append(code_block("""// Request
{
  "toColumnId": "col-3",
  "toIndex": 2              // 0-based posisi di kolom target
}

// Response 200
{
  "id": "card-...",
  "columnId": "col-3",
  "displayOrder": 2560,     // server hitung di tengah dua tetangga
  "version": 6
}"""))
story.append(callout("Why a dedicated endpoint?",
    "PATCH umum harus baca state penuh; <font face='Courier' size='9'>/move</font> "
    "bisa pakai <b>single UPDATE</b> tanpa load entity penuh. Hemat ±40% latency. "
    "Server menghitung <font face='Courier' size='9'>displayOrder</font> baru sebagai "
    "midpoint antara card di index-1 dan index — tidak perlu reorder ulang seluruh "
    "kolom. Setiap 50 move per board, background job <i>repack</i> spasi order."))

story.append(H2("11.4 Bulk reorder (rare path)"))
story.append(endpoint_block("PUT", "/api/v1/columns/{columnId}/cards/reorder",
    "Set ulang urutan seluruh card di satu kolom (jarang dipakai; backup path).",
    auth="Bearer JWT", role="Member"))
story.append(code_block("""// Request
{ "cardIds": ["card-3", "card-1", "card-2"] }

// Response 200 — semua card dengan displayOrder baru (1024, 2048, 3072, ...)"""))

story.append(H2("11.5 Get card detail"))
story.append(endpoint_block("GET", "/api/v1/cards/{cardId}",
    "Detail penuh + comment + attachment list.",
    auth="Bearer JWT", role="Member"))

story.append(H2("11.6 Delete card (soft)"))
story.append(endpoint_block("DELETE", "/api/v1/cards/{cardId}",
    "Set deleted_at; 30 hari di trash sebelum hard-delete cron.",
    auth="Bearer JWT", role="Owner / PM / Creator"))

story.append(H2("11.7 Restore card"))
story.append(endpoint_block("POST", "/api/v1/cards/{cardId}/restore",
    "Undelete jika masih dalam 30 hari window.",
    auth="Bearer JWT", role="Owner / PM"))

story.append(H2("11.8 List cards with filters (Orders View)"))
story.append(endpoint_block("GET", "/api/v1/workspaces/{wsId}/cards",
    "Filtering + sorting + pagination. Backbone untuk OrdersView.",
    auth="Bearer JWT", role="Member"))
story.append(Paragraph("<b>Query params</b>", H4))
story.append(data_table(
    ["Param", "Type", "Default", "Notes"],
    [
        ["q", "string", "—", "Search title, clientName (LIKE)"],
        ["type", "string", "all", "PROJECT_TYPES key"],
        ["columnId", "uuid", "all", "Filter by stage"],
        ["boardId", "uuid", "all", "Limit ke 1 board"],
        ["priority", "enum", "all", "high|medium|low"],
        ["dueFrom", "date", "—", "YYYY-MM-DD"],
        ["dueTo", "date", "—", "YYYY-MM-DD"],
        ["sort", "string", "createdAt:desc", "createdAt|value|dueDate :asc|desc"],
        ["page", "int", "1", "1-based"],
        ["size", "int", "20", "Max 100"],
    ],
    col_widths=[2.5 * cm, 1.8 * cm, 2.5 * cm, 9.6 * cm]
))
story.append(code_block("""// Example
GET /api/v1/workspaces/ws-1/cards?q=brand&type=branding&page=1&size=20&sort=value:desc

// Response 200
{
  "items": [ { ... card summary ... } ],
  "page": 1, "size": 20, "total": 87, "totalPages": 5
}"""))

story.append(H2("11.9 Card events / activity"))
story.append(endpoint_block("GET", "/api/v1/cards/{cardId}/activity",
    "Riwayat perubahan dari audit_log untuk satu card.",
    auth="Bearer JWT", role="Member"))
story.append(PageBreak())

# ═════ 12. COMMENTS & ATTACHMENTS ═════
story.append(Paragraph("12. API Specification — Comments & Attachments", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("12.1 List comments"))
story.append(endpoint_block("GET", "/api/v1/cards/{cardId}/comments",
    "Daftar komentar paling lama → terbaru. Pagination keyset.",
    auth="Bearer JWT", role="Member"))
story.append(code_block("""// Query
?afterId=cm-12&size=30

// Response 200
{
  "items": [
    {
      "id": "cm-...",
      "author": { "id": "...", "name": "Andi", "initials": "AP", "color": "#..." },
      "body": "Sudah saya cek, looks good!",
      "createdAt": "2026-06-05T11:24:11.482Z",
      "editedAt": null
    }
  ],
  "nextCursor": "cm-42"
}"""))

story.append(H2("12.2 Add comment"))
story.append(endpoint_block("POST", "/api/v1/cards/{cardId}/comments",
    "Buat komentar baru.", auth="Bearer JWT", role="Member"))
story.append(code_block("""// Request
{ "body": "Sudah saya cek, looks good!" }

// Response 201 — comment object lengkap dengan timestamp server"""))
story.append(Paragraph("<b>Side effects</b>", H4))
story.append(bullets([
    "Generate notifikasi tipe <font face='Courier' size='9'>comment</font> untuk semua assignee card kecuali author.",
    "Mention <font face='Courier' size='9'>@nama</font> → notifikasi tambahan ke user yang di-mention.",
    "Update <font face='Courier' size='9'>cards.updated_at</font> agar board cache invalid.",
]))

story.append(H2("12.3 Edit / delete comment"))
story.append(endpoint_block("PATCH", "/api/v1/comments/{commentId}",
    "Author only. Set edited_at.", auth="Bearer JWT", role="Author"))
story.append(endpoint_block("DELETE", "/api/v1/comments/{commentId}",
    "Soft delete; body diganti '[deleted]' di response.",
    auth="Bearer JWT", role="Author / Owner"))

story.append(H2("12.4 Upload attachment — presigned flow"))
story.append(callout("Why presigned?",
    "Upload file lewat backend = bandwidth + memory backend dipakai. Pakai pola "
    "<b>presigned URL</b>: backend cuma menerbitkan URL S3 berbatas waktu, client "
    "upload langsung ke S3. Backend tidak pernah handle byte file."))
story.append(endpoint_block("POST", "/api/v1/cards/{cardId}/attachments/init",
    "Step 1: minta presigned URL untuk upload.",
    auth="Bearer JWT", role="Member"))
story.append(code_block("""// Request
{ "filename": "mockup-v2.fig", "mimeType": "application/octet-stream", "sizeBytes": 8421500 }

// Response 200
{
  "attachmentId": "att-...",
  "uploadUrl": "https://s3.example.com/promptara-attach/...?X-Amz-Signature=...",
  "method": "PUT",
  "expiresIn": 900,
  "headers": { "Content-Type": "application/octet-stream" }
}"""))

story.append(endpoint_block("POST", "/api/v1/attachments/{attachmentId}/complete",
    "Step 2: konfirmasi upload selesai; server verifikasi via HEAD ke S3.",
    auth="Bearer JWT", role="Member"))
story.append(code_block("""// Request
{ "checksumSha256": "9af4..." }   // optional, server verify

// Response 200
{
  "id": "att-...",
  "filename": "mockup-v2.fig",
  "sizeBytes": 8421500,
  "downloadUrl": "https://s3.example.com/...?X-Amz-Signature=...",
  "uploadedAt": "2026-06-06T..."
}"""))

story.append(H2("12.5 Download attachment"))
story.append(endpoint_block("GET", "/api/v1/attachments/{attachmentId}",
    "Get metadata + presigned download URL (TTL 5 menit).",
    auth="Bearer JWT", role="Member"))

story.append(H2("12.6 Delete attachment"))
story.append(endpoint_block("DELETE", "/api/v1/attachments/{attachmentId}",
    "Hard delete row + delete object di S3 (idempotent).",
    auth="Bearer JWT", role="Uploader / Owner / PM"))
story.append(callout("Limits",
    "<b>Max size:</b> 50 MB per file (matches frontend hint).<br/>"
    "<b>Allowed types:</b> image/*, application/pdf, application/figma, application/illustrator, "
    "octet-stream untuk .fig/.ai.<br/>"
    "<b>Total quota:</b> 5 GB per workspace di V1 (configurable per workspace di V2)."))
story.append(PageBreak())

# ═════ 13. NOTIFICATIONS ═════
story.append(Paragraph("13. API Specification — Notifications", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("13.1 List notifications"))
story.append(endpoint_block("GET", "/api/v1/notifications",
    "Sidebar bell — list notifikasi user, terbaru duluan.",
    auth="Bearer JWT"))
story.append(code_block("""// Query
?unreadOnly=true&size=20&beforeId=ntf-42

// Response 200
{
  "items": [
    {
      "id": "ntf-...",
      "type": "due-soon",
      "message": "Logo round 2 akan jatuh tempo besok.",
      "refCardId": "card-...",
      "refBoardId": "board-...",
      "actorUser": null,
      "read": false,
      "createdAt": "2026-06-06T07:00:00.000Z"
    }
  ],
  "unreadCount": 7,
  "nextCursor": "ntf-22"
}"""))

story.append(H2("13.2 Mark one as read"))
story.append(endpoint_block("POST", "/api/v1/notifications/{id}/read",
    "Idempotent.", auth="Bearer JWT"))

story.append(H2("13.3 Mark all as read"))
story.append(endpoint_block("POST", "/api/v1/notifications/read-all",
    "Set read_at = now() untuk semua notif user yang masih unread.",
    auth="Bearer JWT"))

story.append(H2("13.4 Notification types"))
story.append(data_table(
    ["Type", "Trigger", "Recipient"],
    [
        ["due-soon", "Cron daily 07:00 WIB scan card due dalam ≤3 hari", "Semua assignee"],
        ["overdue", "Cron daily; card melewati dueDate dan belum Done", "Semua assignee + Owner"],
        ["assignment", "Card assignees berubah", "User yang baru ditambahkan"],
        ["comment", "Komentar baru di card", "Assignee + author komentar sebelumnya"],
        ["mention", "@nama di body komentar", "User yang di-mention"],
        ["status-changed", "Card pindah ke Done Deal", "Owner workspace"],
        ["dp-received", "dpPaidIdr berubah ke ≥ valueIdr", "Owner workspace"],
    ],
    col_widths=[3.5 * cm, 7.5 * cm, 5.4 * cm]
))

story.append(H2("13.5 Delivery pipeline"))
story.append(code_block("""Service writes card  →  publish DomainEvent (Spring ApplicationEventPublisher)
                     →  @TransactionalEventListener (AFTER_COMMIT)
                     →  NotificationFanoutService
                          ├─ insert notifications rows  (batch insert)
                          ├─ publish ke Redis pub-sub channel "notif:{userId}"
                          └─ (V2) push WebSocket frame ke connected sessions

// V1: client poll GET /notifications setiap 30 detik kalau tab focused"""))
story.append(PageBreak())

# ═════ 14. ORDERS & FINANCE ═════
story.append(Paragraph("14. API Specification — Orders & Finance", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(Paragraph(
    "Orders dan Finance adalah <b>read-side projection</b> dari tabel <i>cards</i>. "
    "Tidak ada tabel terpisah — cukup query agregasi dengan index yang tepat dan cache.",
    BODY))

story.append(H2("14.1 Orders summary (band atas)"))
story.append(endpoint_block("GET", "/api/v1/workspaces/{wsId}/orders/summary",
    "Total nilai, diterima, outstanding, jumlah project.",
    auth="Bearer JWT", role="Member"))
story.append(code_block("""// Response 200 (cached 30 detik)
{
  "totalValueIdr": 142500000,
  "totalReceivedIdr": 87500000,
  "totalOutstandingIdr": 55000000,
  "totalOrders": 38
}"""))

story.append(H2("14.2 Orders list (table view)"))
story.append(Paragraph(
    "Reuses <font face='Courier' size='9'>GET /workspaces/{wsId}/cards</font> "
    "dari Bab 11.8 dengan filter & sort yang sama.", BODY))

story.append(H2("14.3 Export orders to CSV"))
story.append(endpoint_block("GET", "/api/v1/workspaces/{wsId}/orders/export",
    "Streaming CSV (Content-Type: text/csv; charset=utf-8).",
    auth="Bearer JWT", role="Member"))
story.append(code_block("""// Query: sama dengan GET /cards (q, type, columnId, sort, ...)
// Response 200 - streaming, mendukung filter besar tanpa load semua ke memori

Content-Type: text/csv; charset=utf-8
Content-Disposition: attachment; filename="promptara-orders-2026-06-06.csv"

Tanggal Order,Klien,Judul Project,Tipe,Status,Nilai (IDR),DP (IDR),Sisa (IDR),Deadline
"06 Jun 2026","Brand X","Logo round 2","Branding","Studio",15000000,7500000,7500000,"30 Jun 2026"
..."""))
story.append(callout("Streaming",
    "Pakai <font face='Courier' size='9'>StreamingResponseBody</font> + JDBC cursor "
    "untuk fetch per 500 row. Tidak load seluruh result set ke memori. CSV header pakai "
    "BOM (<font face='Courier' size='9'>\\uFEFF</font>) supaya buka di Excel ID langsung "
    "benar."))

story.append(H2("14.4 Finance summary (Finance View)"))
story.append(endpoint_block("GET", "/api/v1/workspaces/{wsId}/finance/summary",
    "Semua agregat finance dalam 1 response.",
    auth="Bearer JWT", role="Member"))
story.append(code_block("""// Response 200 (cached 60 detik di Redis, key per workspaceId)
{
  "totals": {
    "valueIdr": 142500000,
    "receivedIdr": 87500000,
    "outstandingIdr": 55000000,
    "doneRevenueIdr": 62000000
  },
  "monthly": [
    { "month": "2026-01", "label": "Jan 26", "valueIdr": 18000000, "receivedIdr": 12000000, "count": 4 },
    { "month": "2026-02", "label": "Feb 26", "valueIdr": 22500000, "receivedIdr": 22500000, "count": 6 },
    ...
  ],
  "byType": [
    { "type": "branding",   "valueIdr": 45000000, "count": 9 },
    { "type": "web-design", "valueIdr": 38000000, "count": 7 },
    ...
  ],
  "byStatus": [
    { "columnId": "col1", "columnName": "Briefs",  "valueIdr": 12000000, "count": 4 },
    ...
  ],
  "recent": [ { "id": "card-...", "title": "...", "valueIdr": ..., "dpPaidIdr": ..., "columnId": "..." } ]
}"""))
story.append(Paragraph("<b>SQL pattern (native query)</b>", H4))
story.append(code_block("""-- Monthly (driven by index idx_cards_created)
SELECT DATE_FORMAT(created_at, '%Y-%m') AS ym,
       SUM(value_idr)   AS total_value,
       SUM(dp_paid_idr) AS total_received,
       COUNT(*)         AS count
FROM cards
WHERE board_id IN (SELECT id FROM boards WHERE workspace_id = ?)
  AND deleted_at IS NULL
  AND value_idr > 0
  AND created_at >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY ym
ORDER BY ym;

-- By type, by status: similar pattern; satu query masing-masing"""))

story.append(H2("14.5 Export finance"))
story.append(endpoint_block("GET", "/api/v1/workspaces/{wsId}/finance/export",
    "CSV summary bulanan.", auth="Bearer JWT", role="Member"))

story.append(H2("14.6 Finance audit endpoint (Owner only)"))
story.append(endpoint_block("GET", "/api/v1/workspaces/{wsId}/finance/dp-changes",
    "Histori perubahan DP (siapa, kapan, berapa).",
    auth="Bearer JWT", role="Owner"))
story.append(PageBreak())

# ═════ 15. CONCURRENCY ═════
story.append(Paragraph("15. Concurrency Handling Strategy", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(Paragraph(
    "Kanban adalah aplikasi <b>collaborative</b>. Concurrency adalah <i>first-class "
    "concern</i>, bukan afterthought. Dokumen ini menjabarkan strategi per skenario.", BODY))

story.append(H2("15.1 Optimistic Locking (default untuk cards)"))
story.append(Paragraph(
    "Setiap card punya kolom <font face='Courier' size='9'>version BIGINT</font>. "
    "Hibernate <font face='Courier' size='9'>@Version</font> akan otomatis menambahkan "
    "<font face='Courier' size='9'>AND version = ?</font> pada WHERE saat UPDATE. "
    "Jika 0 row affected → throw <font face='Courier' size='9'>OptimisticLockException</font>. "
    "Controller translate ke <b>HTTP 409</b> dengan <font face='Courier' size='9'>"
    "currentVersion</font> agar client bisa merge.", BODY))
story.append(code_block("""@Entity @Table(name = "cards")
public class CardEntity {
    @Id @Column(length = 36) private String id;
    @Version private Long version;
    // ... other fields
}

// In service layer
@Transactional
public CardDto update(String id, CardUpdateRequest req, long ifMatchVersion) {
    CardEntity c = cardRepo.findById(id).orElseThrow(NotFound::new);
    if (c.getVersion() != ifMatchVersion) {
        throw new VersionMismatchException(c.getVersion());
    }
    mapper.applyUpdate(req, c);   // partial copy
    return mapper.toDto(c);       // flush: WHERE id=? AND version=?
}"""))

story.append(H2("15.2 Pessimistic Locking (untuk reorder column / card)"))
story.append(Paragraph(
    "Reorder = banyak row diubah <i>display_order</i>-nya, harus konsisten. Pakai "
    "<font face='Courier' size='9'>SELECT ... FOR UPDATE</font> untuk lock baris yang "
    "akan disentuh, dalam 1 transaksi.", BODY))
story.append(code_block("""@Transactional(isolation = Isolation.READ_COMMITTED)
public void reorderColumns(UUID boardId, List<UUID> orderedIds) {
    // 1. Lock semua row board ini (acquire X lock)
    List<ColumnEntity> cols = columnRepo.lockByBoardId(boardId);
    // 2. Validate ID set match
    if (!sameIdSet(cols, orderedIds))
        throw new BadRequest("ID mismatch");
    // 3. Negate trick — hindari unique key collision sementara
    columnRepo.negateOrders(boardId);
    // 4. Assign nilai baru
    for (int i = 0; i < orderedIds.size(); i++) {
        columnRepo.setOrder(orderedIds.get(i), i);
    }
}

// Repository
@Query(value = "SELECT * FROM board_columns WHERE board_id = :id FOR UPDATE",
       nativeQuery = true)
List<ColumnEntity> lockByBoardId(@Param("id") UUID id);"""))

story.append(H2("15.3 Card Drag-Drop — Sparse Order Strategy"))
story.append(Paragraph(
    "Tradisi: setiap card punya integer order rapat (1,2,3,...). Masalah: drag-drop "
    "bisa men-trigger update banyak row.<br/><br/>"
    "Solusi: <b>sparse / fractional ordering</b>. Saat insert card baru, "
    "<font face='Courier' size='9'>displayOrder = MAX + 1024</font>. Saat move ke tengah, "
    "<font face='Courier' size='9'>displayOrder = (prev + next) / 2</font>. "
    "Update hanya <b>1 row</b>. Tanpa perlu lock semua kolom.", BODY))
story.append(code_block("""// Service untuk /cards/{id}/move
@Transactional
public CardDto move(UUID cardId, UUID toCol, int toIndex) {
    CardEntity c = cardRepo.findByIdForUpdate(cardId)
                           .orElseThrow(NotFound::new);
    List<Long> orders = cardRepo.findOrdersByColumn(toCol);  // already sorted
    long newOrder;
    if (orders.isEmpty()) {
        newOrder = 1024L;
    } else if (toIndex <= 0) {
        newOrder = orders.get(0) - 1024;
    } else if (toIndex >= orders.size()) {
        newOrder = orders.get(orders.size() - 1) + 1024;
    } else {
        newOrder = (orders.get(toIndex - 1) + orders.get(toIndex)) / 2;
    }
    c.setColumnId(toCol);
    c.setDisplayOrder(newOrder);
    return mapper.toDto(c);    // single UPDATE
}

// Periodic compaction (cron weekly): repack jika ada gap < 4
// UPDATE cards SET display_order = ROW_NUMBER() OVER (...) * 1024 WHERE column_id = ?"""))
story.append(callout("Edge case",
    "Jika gap antara dua tetangga = 1 (sangat jarang), insert akan gagal hitung "
    "midpoint. Trigger background <b>repack</b> kolom tersebut secara on-demand, "
    "kemudian retry move sekali."))

story.append(H2("15.4 Comment Append — Insert-Only (Lock-Free)"))
story.append(Paragraph(
    "Comment cuma insert; tidak ada race condition selama "
    "<font face='Courier' size='9'>created_at</font> + <font face='Courier' size='9'>id "
    "(UUID v7)</font> sebagai composite sort. Dua comment di millisecond yang sama "
    "tetap punya UUID v7 berbeda — urutan deterministic.", BODY))

story.append(H2("15.5 Refresh Token Rotation — Atomic Compare-and-Swap"))
story.append(Paragraph(
    "Bisa terjadi: client kirim refresh request 2x bersamaan (network retry). "
    "Strategi:", BODY))
story.append(bullets([
    "Token disimpan sebagai <b>hash</b> di DB (<font face='Courier' size='9'>token_hash UNIQUE</font>).",
    "Refresh op pakai <font face='Courier' size='9'>UPDATE refresh_tokens SET revoked_at = NOW(3) WHERE token_hash = ? AND revoked_at IS NULL</font>.",
    "Cek <font face='Courier' size='9'>rowsAffected == 1</font>. Jika 0 → token sudah revoked → reject 401 + <b>kill seluruh chain user</b> (signal possible theft).",
    "Hanya request yang sukses CAS yang dapat token baru. Yang kalah dapat 401.",
]))

story.append(H2("15.6 Counter — notifications.unreadCount"))
story.append(Paragraph(
    "<b>Tidak</b> di-cache sebagai kolom; hitung selalu via "
    "<font face='Courier' size='9'>COUNT(*) WHERE read_at IS NULL</font> dengan index "
    "<font face='Courier' size='9'>idx_notif_user_unread</font>. Cepat (≤ 5 ms) "
    "selama unread &lt; 10k. Lebih simple dan zero drift.", BODY))

story.append(H2("15.7 Transaction Boundaries"))
story.append(data_table(
    ["Operation", "Isolation", "Why"],
    [
        ["Card create/update", "READ_COMMITTED", "Default; cukup dengan @Version"],
        ["Column reorder", "READ_COMMITTED + FOR UPDATE", "Eksplisit lock subset row"],
        ["Refresh token rotation", "READ_COMMITTED", "CAS lewat UPDATE WHERE"],
        ["Finance summary read", "READ_COMMITTED (read-only)", "Tolerate slight drift"],
        ["Soft delete card", "READ_COMMITTED", "Single UPDATE"],
        ["Workspace owner transfer", "REPEATABLE_READ", "Cek 2 row sebelum swap"],
    ],
    col_widths=[4.5 * cm, 5.0 * cm, 6.9 * cm]
))

story.append(H2("15.8 Deadlock Prevention"))
story.append(bullets([
    "Selalu acquire lock dengan <b>urutan ID konsisten</b> (ascending). "
    "Mis. saat update 2 card → lock card dengan id lebih kecil dulu.",
    "Set timeout: <font face='Courier' size='9'>innodb_lock_wait_timeout = 5</font> "
    "(detik) di MySQL. Bukan default 50 — fail fast lebih baik daripada thread stuck.",
    "Translate <font face='Courier' size='9'>1213 ER_LOCK_DEADLOCK</font> → "
    "automatic retry 1x dengan backoff 50 ms.",
]))
story.append(PageBreak())

# ═════ 16. LOW LATENCY ═════
story.append(Paragraph("16. Low Latency & Performance Strategy", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("16.1 Tomcat / Virtual Threads"))
story.append(code_block("""# application.yml
spring:
  threads:
    virtual:
      enabled: true       # Java 21 virtual threads — cheap per-request
server:
  tomcat:
    threads:
      max: 200            # platform threads pool
      min-spare: 20
    accept-count: 200
    connection-timeout: 5s
    max-connections: 8192
  compression:
    enabled: true
    mime-types: application/json, text/csv, text/plain
    min-response-size: 1024"""))
story.append(callout("Virtual threads win",
    "Workload Spring Boot kita banyak <i>blocking IO</i> (JDBC, S3, Redis). "
    "Dengan virtual threads, kita bisa handle ribuan request concurrent tanpa "
    "kehabisan platform thread. Tidak perlu rewrite ke WebFlux."))

story.append(H2("16.2 Database Connection Pool (HikariCP)"))
story.append(code_block("""spring:
  datasource:
    hikari:
      pool-name: promptara-hikari
      maximum-pool-size: 20          # Java 21 + virtual threads tetap perlu cap koneksi DB
      minimum-idle: 5
      connection-timeout: 3000       # 3 s — fail fast
      idle-timeout: 600000           # 10 min
      max-lifetime: 1800000          # 30 min — rotate sebelum MySQL wait_timeout
      keepalive-time: 300000         # 5 min
      leak-detection-threshold: 30000
      data-source-properties:
        cachePrepStmts: true
        prepStmtCacheSize: 250
        prepStmtCacheSqlLimit: 2048
        useServerPrepStmts: true
        rewriteBatchedStatements: true"""))
story.append(Paragraph(
    "Rumus pool size: <font face='Courier' size='9'>connections = ((core_count × 2) + "
    "effective_spindle_count)</font>. Untuk single VM 4 vCPU + SSD: ~10-20 cukup. "
    "Lebih banyak ≠ lebih cepat; malah memperburuk lock contention di MySQL.", BODY))

story.append(H2("16.3 Caching Layer (Redis)"))
story.append(data_table(
    ["Key Pattern", "TTL", "Invalidation"],
    [
        ["board:{id}:full", "60 s", "Manual on card/column write"],
        ["finance:{wsId}:summary", "30 s", "TTL only — drift acceptable"],
        ["user:{id}:profile", "300 s", "On profile update"],
        ["workspace:{id}:members", "120 s", "On member add/remove"],
        ["jwt:blacklist:{jti}", "= remaining JWT TTL", "Self-expire"],
        ["ratelimit:{userId}:{bucket}", "60 s", "Token bucket refill"],
        ["login:fail:{email}", "900 s (15 min)", "Reset on success"],
    ],
    col_widths=[6.0 * cm, 3.5 * cm, 6.9 * cm]
))
story.append(code_block("""@Cacheable(value = "board", key = "#boardId")
public BoardDto getBoard(UUID boardId) { ... }

@CacheEvict(value = "board", key = "#boardId")
public void updateBoard(UUID boardId, ...) { ... }

// Tipe cache: cache-aside (read), write-through (eviction). Tidak pakai write-back."""))

story.append(H2("16.4 Query-Level Optimizations"))
story.append(bullets([
    "<b>N+1 prevention:</b> JOIN FETCH untuk relasi yang selalu di-load bersama "
    "(card → assignees). Entity Graph untuk yang opsional.",
    "<b>Projection DTO:</b> jangan return entity penuh kalau hanya beberapa kolom yang dipakai. "
    "Pakai <font face='Courier' size='9'>interface projection</font> Spring Data.",
    "<b>Native query</b> untuk finance aggregation (kompleks, perf critical).",
    "<b>Batch fetch:</b> <font face='Courier' size='9'>spring.jpa.properties.hibernate.default_batch_fetch_size: 32</font>.",
    "<b>Statement cache:</b> Hikari + MySQL serverside prepared statement.",
    "<b>Pagination keyset</b> (cursor-based) untuk daftar panjang — hindari OFFSET besar.",
]))

story.append(H2("16.5 Response Size Reduction"))
story.append(bullets([
    "Jackson: <font face='Courier' size='9'>@JsonInclude(NON_NULL)</font> + "
    "<font face='Courier' size='9'>WRITE_DATES_AS_TIMESTAMPS=false</font>.",
    "Field sensitif (passwordHash, refreshToken) di entity → <font face='Courier' size='9'>@JsonIgnore</font>.",
    "Gzip dinyalakan di Spring Boot untuk respons ≥ 1 KB.",
    "Endpoint board read: <i>flattened</i> — assignee cukup ID, full user object di-fetch terpisah dan di-cache.",
]))

story.append(H2("16.6 Async / Background Tasks"))
story.append(code_block("""@Configuration @EnableAsync
public class AsyncConfig {
    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        return Executors.newThreadPerTaskExecutor(
            Thread.ofVirtual().name("promptara-async-", 0).factory()
        );
    }
}

// Use cases:
//  - Notification fanout (sehabis card move → notify assignees)
//  - Email send (async, never block request)
//  - S3 cleanup (delete orphan attachments)
//  - Audit log write (fire-and-forget, but keep order via single queue)"""))

story.append(H2("16.7 CDN & Static Asset"))
story.append(bullets([
    "Frontend di-host terpisah (Vercel / Nginx static); backend cuma serve API.",
    "Attachment download URL adalah <b>presigned S3</b> — langsung dari CloudFront/MinIO, tidak via backend.",
    "Avatar (jika dipakai) di-cache 1 tahun dengan content hash di filename.",
]))
story.append(PageBreak())

# ═════ 17. SECURITY ═════
story.append(Paragraph("17. Security Requirements", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("17.1 Authentication"))
story.append(bullets([
    "<b>Password hashing:</b> BCrypt cost 12 (≈250 ms / hash di 2 vCPU). "
    "Jangan turunkan demi performance — itu yang melindungi DB dump.",
    "<b>JWT signing:</b> HS256 secret 256-bit dari env <font face='Courier' size='9'>JWT_SECRET</font>. "
    "Rotation tiap 90 hari; saat rotasi tetap accept token lama 24 jam.",
    "<b>Token transport:</b> Hanya via header <font face='Courier' size='9'>Authorization</font>. "
    "<b>Tidak</b> di-set sebagai cookie default — CSRF tidak relevan.",
    "<b>Brute force:</b> 5 failed login → lock email 15 menit. IP-level rate limit 20/menit.",
]))

story.append(H2("17.2 Authorization (RBAC + Resource scoping)"))
story.append(code_block("""// Method-level di service
@PreAuthorize("@accessChecker.canEditBoard(#boardId, principal)")
public BoardDto updateBoard(UUID boardId, ...) { ... }

// AccessChecker bean
public boolean canEditBoard(UUID boardId, AuthenticatedUser u) {
    // 1. Board ada di workspace yang user adalah member?
    // 2. Role member ∈ {Owner, Project Manager}?
    return membershipRepo.hasRole(boardId, u.id(), Set.of(OWNER, PM));
}"""))
story.append(Paragraph("<b>Role matrix</b>", H4))
story.append(data_table(
    ["Action", "Owner", "PM", "Designer", "Developer", "Other"],
    [
        ["Create board", "Y", "Y", "N", "N", "N"],
        ["Delete board", "Y", "N", "N", "N", "N"],
        ["Create / update card", "Y", "Y", "Y", "Y", "Y (own)"],
        ["Delete card", "Y", "Y", "Y (own)", "Y (own)", "Y (own)"],
        ["Move card", "Y", "Y", "Y", "Y", "Y"],
        ["Invite member", "Y", "Y", "N", "N", "N"],
        ["Change role", "Y", "N", "N", "N", "N"],
        ["Export finance", "Y", "Y", "N", "N", "N"],
        ["View finance", "Y", "Y", "Y", "Y", "N"],
    ],
    col_widths=[5.0 * cm, 1.8 * cm, 1.8 * cm, 2.4 * cm, 2.4 * cm, 2.0 * cm]
))

story.append(H2("17.3 Input Validation"))
story.append(bullets([
    "Setiap DTO punya <font face='Courier' size='9'>@NotBlank</font>, <font face='Courier' size='9'>@Size</font>, <font face='Courier' size='9'>@Email</font> dll dari Jakarta Validation.",
    "Controller <font face='Courier' size='9'>@Valid</font>; pelanggaran → handler global → 400 dengan field detail.",
    "Path variable UUID di-parse via converter — invalid format → 400 sebelum controller.",
    "Query <font face='Courier' size='9'>size</font> di-clamp max 100 di service.",
]))

story.append(H2("17.4 SQL Injection"))
story.append(bullets([
    "<b>Mandatory:</b> semua query lewat JPA / parameterized native query. Tidak ada string concat.",
    "Search field (LIKE) escape <font face='Courier' size='9'>%</font> dan <font face='Courier' size='9'>_</font> di service.",
    "Sort field whitelist — terima nama logis (<i>value:desc</i>), bukan SQL column mentah.",
]))

story.append(H2("17.5 XSS & Output Encoding"))
story.append(bullets([
    "API return JSON murni — XSS bukan attack-surface langsung.",
    "Komentar disimpan sebagai plain text. Frontend wajib escape saat render (React default).",
    "Filename attachment di-sanitize sebelum disimpan ke S3 (strip path traversal).",
]))

story.append(H2("17.6 CORS"))
story.append(code_block("""@Configuration
public class CorsConfig {
    @Bean public CorsConfigurationSource corsSource() {
        var c = new CorsConfiguration();
        c.setAllowedOrigins(List.of("https://app.promptara.id",
                                    "http://localhost:5173"));   // dev only
        c.setAllowedMethods(List.of("GET","POST","PATCH","PUT","DELETE","OPTIONS"));
        c.setAllowedHeaders(List.of("Authorization", "Content-Type", "If-Match"));
        c.setExposedHeaders(List.of("ETag", "X-Request-Id"));
        c.setAllowCredentials(false);     // pakai bearer header, bukan cookie
        c.setMaxAge(3600L);
        var src = new UrlBasedCorsConfigurationSource();
        src.registerCorsConfiguration("/api/**", c);
        return src;
    }
}"""))

story.append(H2("17.7 Rate Limiting"))
story.append(data_table(
    ["Bucket", "Limit", "Window", "Scope"],
    [
        ["Login / Register", "5", "1 min", "Per IP + per email"],
        ["Default API", "120", "1 min", "Per userId"],
        ["File upload init", "20", "1 min", "Per userId"],
        ["Export endpoint", "10", "1 hour", "Per userId"],
    ],
    col_widths=[4.0 * cm, 2.0 * cm, 3.0 * cm, 7.4 * cm]
))
story.append(Paragraph(
    "Implementasi pakai <b>Redis token bucket</b> (Bucket4j-Redisson) atau script Lua "
    "<font face='Courier' size='9'>INCR + EXPIRE</font> sederhana. Header response include "
    "<font face='Courier' size='9'>X-RateLimit-Remaining</font> dan "
    "<font face='Courier' size='9'>Retry-After</font> saat 429.", BODY))

story.append(H2("17.8 Secrets Management"))
story.append(bullets([
    "Semua secret (DB password, JWT secret, S3 key, Redis password) lewat env var; tidak hardcode.",
    "Local dev pakai <font face='Courier' size='9'>.env</font> yang di-gitignore.",
    "Production: AWS Secrets Manager / Vault → injected sebagai env saat container start.",
    "<b>Tidak pernah</b> log secret. Logback custom converter mask field sensitif.",
]))

story.append(H2("17.9 OWASP Top 10 Checklist"))
story.append(data_table(
    ["Item", "Mitigation"],
    [
        ["A01 Broken Access Control", "RBAC + method-level @PreAuthorize + resource scoping"],
        ["A02 Cryptographic Failures", "BCrypt password, HS256 JWT, TLS at proxy"],
        ["A03 Injection", "JPA parameterized, no string concat, validation"],
        ["A04 Insecure Design", "Threat model dokumen ini; rate limit"],
        ["A05 Security Misconfig", "Spring profiles, no debug in prod, secure headers"],
        ["A06 Vulnerable Components", "Dependabot + monthly mvn versions:display"],
        ["A07 Auth Failures", "BCrypt + brute-force lockout + refresh rotation"],
        ["A08 Data Integrity", "Flyway checksums, signed JWT, optimistic lock"],
        ["A09 Logging Failures", "Structured logs, audit_log, 90 day retention"],
        ["A10 SSRF", "S3 client whitelist endpoint; no user-supplied URL fetch"],
    ],
    col_widths=[5.5 * cm, 10.9 * cm]
))
story.append(PageBreak())

# ═════ 18. ERROR HANDLING ═════
story.append(Paragraph("18. Error Handling & Standard Response", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("18.1 Standard Error Envelope"))
story.append(code_block("""{
  "timestamp": "2026-06-06T08:11:23.482Z",
  "status":    409,
  "code":      "VERSION_CONFLICT",
  "message":   "Card sudah diubah orang lain. Refresh dulu.",
  "path":      "/api/v1/cards/01890d4c-...",
  "requestId": "req-9f1b...",
  "fields": [                                  // hanya untuk validation errors
    { "name": "email", "message": "format tidak valid" }
  ],
  "details": {                                 // optional, context-specific
    "currentVersion": 7
  }
}"""))

story.append(H2("18.2 HTTP Status Mapping"))
story.append(data_table(
    ["Status", "When", "code field examples"],
    [
        ["400 Bad Request", "DTO validation, malformed JSON", "VALIDATION_ERROR, MALFORMED_JSON"],
        ["401 Unauthorized", "Missing/invalid/expired JWT", "INVALID_CREDENTIALS, TOKEN_EXPIRED"],
        ["403 Forbidden", "Auth OK tapi role/scope kurang", "FORBIDDEN, INSUFFICIENT_ROLE"],
        ["404 Not Found", "Resource tidak ada / soft-deleted", "RESOURCE_NOT_FOUND"],
        ["409 Conflict", "Unique violation, version conflict", "EMAIL_TAKEN, VERSION_CONFLICT"],
        ["410 Gone", "Token refresh sudah dipakai", "REFRESH_TOKEN_REUSED"],
        ["413 Payload Too Large", "File > 50 MB", "FILE_TOO_LARGE"],
        ["422 Unprocessable", "Business rule violation", "DP_EXCEEDS_VALUE"],
        ["429 Too Many", "Rate limit", "RATE_LIMITED"],
        ["500 Internal", "Unexpected", "INTERNAL_ERROR"],
        ["503 Service Unavailable", "DB / Redis down", "DEPENDENCY_DOWN"],
    ],
    col_widths=[3.5 * cm, 5.5 * cm, 7.4 * cm]
))

story.append(H2("18.3 Global Exception Handler"))
story.append(code_block("""@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    ResponseEntity<ErrorBody> onValidation(MethodArgumentNotValidException ex) {
        var fields = ex.getBindingResult().getFieldErrors().stream()
            .map(f -> new ErrorField(f.getField(), f.getDefaultMessage()))
            .toList();
        return ResponseEntity.status(400)
            .body(ErrorBody.of(400, "VALIDATION_ERROR", "Periksa input Anda.", fields));
    }

    @ExceptionHandler(OptimisticLockingFailureException.class)
    ResponseEntity<ErrorBody> onOptLock(OptimisticLockingFailureException ex) {
        return ResponseEntity.status(409)
            .body(ErrorBody.of(409, "VERSION_CONFLICT",
                "Data sudah diubah orang lain. Refresh dulu."));
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    ResponseEntity<ErrorBody> onIntegrity(DataIntegrityViolationException ex) {
        // Inspect SQL state — 23000 duplicate, 23503 FK violation, etc
        if (isUniqueViolation(ex)) {
            return ResponseEntity.status(409)
                .body(ErrorBody.of(409, "DUPLICATE", "Resource duplikat."));
        }
        return ResponseEntity.status(422)
            .body(ErrorBody.of(422, "INTEGRITY_ERROR", "Constraint violation."));
    }

    @ExceptionHandler(Exception.class)
    ResponseEntity<ErrorBody> onAny(Exception ex, HttpServletRequest req) {
        log.error("Unhandled at {}", req.getRequestURI(), ex);
        return ResponseEntity.status(500)
            .body(ErrorBody.of(500, "INTERNAL_ERROR",
                "Terjadi kesalahan. Tim sudah diberitahu."));
    }
}"""))

story.append(H2("18.4 Request Tracing"))
story.append(bullets([
    "Filter assign <font face='Courier' size='9'>X-Request-Id</font> (UUID) di awal request.",
    "Di-propagate ke MDC → semua log mencantumkan <font face='Courier' size='9'>requestId</font>.",
    "Header echoed kembali ke client untuk debugging cross-system.",
    "Honor <font face='Courier' size='9'>X-Request-Id</font> dari upstream jika ada (LB).",
]))
story.append(PageBreak())

# ═════ 19. OBSERVABILITY ═════
story.append(Paragraph("19. Observability — Logging, Metrics, Tracing", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("19.1 Structured Logging"))
story.append(code_block("""# logback-spring.xml
<configuration>
  <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="net.logstash.logback.encoder.LogstashEncoder">
      <customFields>{"app":"promptara-api","env":"${SPRING_PROFILES_ACTIVE}"}</customFields>
      <fieldNames>
        <timestamp>ts</timestamp>
        <message>msg</message>
        <level>lvl</level>
        <logger>logger</logger>
      </fieldNames>
    </encoder>
  </appender>
  <root level="INFO">
    <appender-ref ref="JSON"/>
  </root>
</configuration>"""))
story.append(bullets([
    "Format JSON satu baris per event → mudah di-ingest Loki / ELK.",
    "MDC menyertakan: <font face='Courier' size='9'>requestId, userId, workspaceId, path, method</font>.",
    "Level <b>INFO</b> default; <b>DEBUG</b> hanya saat troubleshooting.",
    "Field sensitif (password, token, secret) di-mask via custom converter.",
    "Log retention 30 hari hot, 90 hari cold (S3 Glacier).",
]))

story.append(H2("19.2 Metrics (Prometheus)"))
story.append(code_block("""management:
  endpoints.web.exposure.include: health, info, prometheus, metrics
  endpoint.health.probes.enabled: true
  endpoint.prometheus.enabled: true
  metrics:
    tags:
      app: promptara-api
    distribution:
      percentiles-histogram:
        http.server.requests: true
      slo:
        http.server.requests: 50ms, 100ms, 200ms, 500ms, 1s"""))
story.append(Paragraph("<b>Custom metrics</b>", H4))
story.append(data_table(
    ["Metric", "Type", "Purpose"],
    [
        ["card_move_total", "Counter", "Volume drag-drop"],
        ["card_optimistic_conflict_total", "Counter", "Lock contention warning"],
        ["login_failed_total", "Counter", "Brute force watcher"],
        ["board_cache_hit_ratio", "Gauge", "Tune TTL"],
        ["attachment_upload_bytes", "Summary", "Bandwidth"],
        ["notification_fanout_seconds", "Timer", "Async health"],
        ["db_pool_active", "Gauge (HikariCP)", "Capacity"],
    ],
    col_widths=[5.5 * cm, 2.5 * cm, 8.4 * cm]
))

story.append(H2("19.3 Health Endpoints"))
story.append(code_block("""GET /actuator/health/liveness
  → 200 jika app process alive (always)

GET /actuator/health/readiness
  → 200 jika: DB reachable + Redis reachable + Flyway done
  → 503 jika ada dependency down — load balancer remove dari rotation"""))

story.append(H2("19.4 Distributed Tracing (opsional V1, wajib V2)"))
story.append(bullets([
    "Micrometer Tracing + OTLP exporter → Tempo / Jaeger.",
    "Trace propagation: <font face='Courier' size='9'>traceparent</font> header (W3C).",
    "Sample rate 10% di production, 100% di staging.",
]))
story.append(PageBreak())

# ═════ 20. DOCKER ═════
story.append(Paragraph("20. Docker, Docker-Compose & Deployment", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("20.1 Dockerfile (multi-stage)"))
story.append(code_block("""# syntax=docker/dockerfile:1.7
# ── Stage 1: build
FROM eclipse-temurin:21-jdk-alpine AS build
WORKDIR /workspace
COPY .mvn .mvn
COPY mvnw pom.xml ./
RUN ./mvnw -q dependency:go-offline
COPY src src
RUN ./mvnw -q -DskipTests package && \\
    mkdir -p target/extracted && \\
    java -Djarmode=layertools -jar target/*.jar extract --destination target/extracted

# ── Stage 2: runtime
FROM eclipse-temurin:21-jre-alpine
RUN addgroup -S app && adduser -S app -G app && \\
    apk add --no-cache curl tzdata
ENV TZ=Asia/Jakarta \\
    JAVA_OPTS="-XX:MaxRAMPercentage=70 -XX:+UseG1GC -XX:+ExitOnOutOfMemoryError"
WORKDIR /app
COPY --from=build /workspace/target/extracted/dependencies/ ./
COPY --from=build /workspace/target/extracted/spring-boot-loader/ ./
COPY --from=build /workspace/target/extracted/snapshot-dependencies/ ./
COPY --from=build /workspace/target/extracted/application/ ./
USER app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \\
  CMD curl -fsS http://localhost:8080/actuator/health/liveness || exit 1
ENTRYPOINT ["sh","-c","exec java $JAVA_OPTS org.springframework.boot.loader.launch.JarLauncher"]"""))

story.append(H2("20.2 docker-compose.yml (development)"))
story.append(code_block("""version: "3.9"
services:

  mysql:
    image: mysql:8.0
    container_name: promptara-mysql
    restart: unless-stopped
    command: >
      --default-authentication-plugin=caching_sha2_password
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_0900_ai_ci
      --innodb-buffer-pool-size=512M
      --innodb-lock-wait-timeout=5
      --max-connections=200
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: promptara
      MYSQL_USER: promptara
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    ports: [ "3307:3306" ]
    volumes:
      - mysql-data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost",
             "-u", "promptara", "-p${MYSQL_PASSWORD}"]
      interval: 10s
      timeout: 3s
      retries: 12

  redis:
    image: redis:7-alpine
    container_name: promptara-redis
    restart: unless-stopped
    command: ["redis-server", "--requirepass", "${REDIS_PASSWORD}",
              "--maxmemory", "256mb", "--maxmemory-policy", "allkeys-lru"]
    ports: [ "6380:6379" ]
    volumes: [ "redis-data:/data" ]
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD}", "ping"]
      interval: 10s

  minio:
    image: quay.io/minio/minio:latest
    container_name: promptara-minio
    restart: unless-stopped
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    ports:
      - "9000:9000"     # S3 API
      - "9001:9001"     # Web console
    volumes: [ "minio-data:/data" ]

  adminer:
    image: adminer:4-standalone
    container_name: promptara-adminer
    restart: unless-stopped
    ports: [ "8081:8080" ]
    depends_on: [ mysql ]

  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: promptara-api
    restart: unless-stopped
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_healthy
      minio:
        condition: service_started
    environment:
      SPRING_PROFILES_ACTIVE: docker
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql:3306/promptara?useSSL=false&serverTimezone=UTC
      SPRING_DATASOURCE_USERNAME: promptara
      SPRING_DATASOURCE_PASSWORD: ${MYSQL_PASSWORD}
      SPRING_DATA_REDIS_HOST: redis
      SPRING_DATA_REDIS_PORT: 6379
      SPRING_DATA_REDIS_PASSWORD: ${REDIS_PASSWORD}
      JWT_SECRET: ${JWT_SECRET}
      S3_ENDPOINT: http://minio:9000
      S3_BUCKET: promptara-attach
      S3_ACCESS_KEY: ${MINIO_ROOT_USER}
      S3_SECRET_KEY: ${MINIO_ROOT_PASSWORD}
    ports: [ "8080:8080" ]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/actuator/health/readiness"]
      interval: 15s
      timeout: 3s
      retries: 5
      start_period: 60s

volumes:
  mysql-data:
  redis-data:
  minio-data:"""))

story.append(H2("20.3 .env.example"))
story.append(code_block("""MYSQL_ROOT_PASSWORD=change-me-root
MYSQL_PASSWORD=change-me-app
REDIS_PASSWORD=change-me-redis
MINIO_ROOT_USER=promptara-minio
MINIO_ROOT_PASSWORD=change-me-minio
JWT_SECRET=64-char-random-secret-base64-encoded-please-change-me-now-thanks"""))

story.append(H2("20.4 Local development workflow"))
story.append(code_block("""# clone & setup
cp .env.example .env       # isi nilai secret
docker compose up -d mysql redis minio
./mvnw spring-boot:run -Dspring-boot.run.profiles=local

# or full stack in containers
docker compose up -d
docker compose logs -f api

# down + wipe volumes (CAREFUL — drops DB)
docker compose down -v"""))

story.append(H2("20.5 Production deployment notes"))
story.append(bullets([
    "Production tidak pakai compose; pakai orchestrator (ECS / Kubernetes / Nomad).",
    "MySQL pakai managed service (RDS / CloudSQL); jangan jalankan di container.",
    "Redis pakai managed service (ElastiCache); enable persistence + backup.",
    "Image API di-push ke registry (ECR / GHCR); rolling deploy via blue-green.",
    "Backup: <font face='Courier' size='9'>mysqldump --single-transaction</font> daily + binlog continuous.",
    "Secret injection lewat AWS Secrets Manager / Kubernetes Secret.",
]))
story.append(PageBreak())

# ═════ 21. PROJECT STRUCTURE ═════
story.append(Paragraph("21. Spring Boot Project Structure", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("21.1 Recommended Package Layout"))
story.append(code_block("""src/main/java/id/promptara/api/
├── PromptaraApplication.java                ← main class
├── common/
│   ├── config/                              ← @Configuration beans
│   │   ├── SecurityConfig.java
│   │   ├── CorsConfig.java
│   │   ├── RedisConfig.java
│   │   ├── JpaConfig.java
│   │   ├── OpenApiConfig.java
│   │   ├── AsyncConfig.java
│   │   └── CacheConfig.java
│   ├── exception/
│   │   ├── GlobalExceptionHandler.java
│   │   ├── ErrorBody.java
│   │   ├── NotFoundException.java
│   │   ├── ConflictException.java
│   │   └── ...
│   ├── security/
│   │   ├── JwtFilter.java
│   │   ├── JwtService.java
│   │   ├── AuthenticatedUser.java
│   │   └── AccessChecker.java
│   ├── ratelimit/
│   │   └── RedisRateLimiter.java
│   └── util/
│       ├── UuidV7Generator.java
│       └── ...
│
├── auth/
│   ├── api/AuthController.java
│   ├── api/dto/                ← LoginRequest, RegisterRequest, AuthResponse
│   ├── service/AuthService.java
│   ├── service/RefreshTokenService.java
│   └── persistence/
│       ├── RefreshTokenEntity.java
│       └── RefreshTokenRepository.java
│
├── user/
│   ├── api/...
│   ├── service/UserService.java
│   └── persistence/
│       ├── UserEntity.java
│       └── UserRepository.java
│
├── workspace/
│   └── ...
│
├── board/
│   ├── api/BoardController.java
│   ├── api/ColumnController.java
│   ├── service/...
│   └── persistence/...
│
├── card/
│   ├── api/CardController.java
│   ├── api/dto/...
│   ├── service/
│   │   ├── CardService.java
│   │   ├── CardMoveService.java
│   │   └── CardOrderingStrategy.java
│   └── persistence/
│       ├── CardEntity.java
│       └── CardRepository.java
│
├── comment/...
├── attachment/...
├── notification/
│   ├── api/NotificationController.java
│   ├── service/
│   │   ├── NotificationService.java
│   │   ├── NotificationFanoutListener.java
│   │   └── DueSoonScheduler.java
│   └── persistence/...
│
├── finance/
│   ├── api/FinanceController.java
│   ├── api/OrderController.java
│   └── service/
│       ├── FinanceQueryService.java     ← native query
│       └── OrderExportService.java       ← streaming CSV
│
└── audit/
    ├── service/AuditService.java
    └── persistence/AuditLogEntity.java

src/main/resources/
├── application.yml
├── application-docker.yml
├── application-prod.yml
├── db/migration/V*.sql
└── logback-spring.xml

src/test/java/id/promptara/api/
├── auth/...      (unit)
├── card/...      (unit + integration with Testcontainers)
└── integration/... (full Spring slice tests)"""))

story.append(H2("21.2 Coding Conventions"))
story.append(bullets([
    "Controller <b>tipis</b>: validasi DTO, panggil service, map ke response. Tidak ada business logic.",
    "Service mengandung <b>satu transaction boundary</b> per public method.",
    "Repository <b>satu</b> per aggregate root; tidak return entity ke controller.",
    "DTO request/response <b>terpisah</b> dari entity. Mapper via MapStruct.",
    "Constructor injection (final field); tidak <font face='Courier' size='9'>@Autowired</font> field.",
    "Method publik service punya Javadoc <i>singkat</i>: input, output, side effect.",
]))
story.append(PageBreak())

# ═════ 22. ROADMAP ═════
story.append(Paragraph("22. Implementation Roadmap & Milestones", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("22.1 Milestones (Estimasi 8 minggu, 2 engineer)"))
story.append(data_table(
    ["Sprint", "Week", "Scope", "Deliverable"],
    [
        ["M1: Foundation", "1-2",
         "Project skeleton, Docker stack, Flyway V1-V4, Auth (login/register/refresh), JWT filter, RBAC dasar",
         "/auth/* berjalan + Swagger UI"],
        ["M2: Kanban core", "3-4",
         "Board CRUD, Column CRUD + reorder, Card CRUD, Card move dengan sparse order, optimistic lock",
         "Frontend BoardView bisa swap dari localStorage ke API"],
        ["M3: Collaboration", "5",
         "Comments, attachments (presigned), notifications fanout, audit log",
         "CardModal tabs fully functional"],
        ["M4: Read-side", "6",
         "Orders list dengan filter, Finance aggregation + cache, CSV export streaming",
         "OrdersView + FinanceView dipindah ke API"],
        ["M5: Hardening", "7",
         "Rate limit, structured logging, metrics, healthchecks, integration tests Testcontainers",
         "Coverage ≥ 70% service layer; load test passes"],
        ["M6: Pre-launch", "8",
         "Penetration test fix, performance tuning, runbook, monitoring dashboards",
         "Production go-live"],
    ],
    col_widths=[3.0 * cm, 1.5 * cm, 7.0 * cm, 4.9 * cm]
))

story.append(H2("22.2 Critical Dependencies"))
story.append(bullets([
    "<b>S3-compatible storage</b> (MinIO local, AWS S3 prod) sebelum M3.",
    "<b>SMTP relay</b> (Mailgun / SES) jika email verification dinyalakan — opsional V1.",
    "<b>Reverse proxy</b> (Nginx) untuk TLS sebelum production go-live.",
    "<b>Monitoring stack</b> (Prometheus + Grafana + Loki) sebelum M6.",
]))

story.append(H2("22.3 Risks & Mitigations"))
story.append(data_table(
    ["Risk", "Impact", "Mitigation"],
    [
        ["MySQL lock contention saat drag-drop ramai", "High",
         "Sparse order + load test sejak M2; siapkan repack cron"],
        ["File upload memory pressure", "Medium",
         "Presigned URL — backend tidak handle byte; ditest M3"],
        ["Refresh token theft", "High",
         "Rotation + reuse detection; alert otomatis"],
        ["Flyway migration gagal di prod", "High",
         "CI run terhadap staging snapshot; never edit V file"],
        ["Cache stampede di finance summary", "Medium",
         "TTL jitter + single-flight lock (Redis SETNX) saat refresh"],
        ["Schema drift Entity vs DDL", "Medium",
         "Test ddl-auto=validate di CI"],
    ],
    col_widths=[5.0 * cm, 2.0 * cm, 9.4 * cm]
))
story.append(PageBreak())

# ═════ 23. APPENDIX ═════
story.append(Paragraph("23. Appendix — Acceptance Criteria & Test Plan", H1))
story.append(HRFlowable(width="100%", thickness=1, color=BRAND))

story.append(H2("23.1 Acceptance Criteria (sample for Auth)"))
story.append(bullets([
    "GIVEN email belum terdaftar, WHEN POST /auth/register dengan body valid, THEN 201 + user + accessToken + refreshToken.",
    "GIVEN email sudah terdaftar, WHEN POST /auth/register, THEN 409 dengan code EMAIL_TAKEN.",
    "GIVEN 5 login fail dalam 10 menit, WHEN login ke-6, THEN 429 selama 15 menit walaupun password benar.",
    "GIVEN refresh token valid, WHEN POST /auth/refresh dua kali bersamaan, THEN tepat satu berhasil (200), satu gagal (401).",
    "GIVEN access token valid, WHEN logout, THEN access token langsung ditolak di endpoint selanjutnya.",
]))

story.append(H2("23.2 Acceptance Criteria (Card)"))
story.append(bullets([
    "User A dan B GET card v=3 bersamaan; A PATCH (If-Match: 3) sukses (v→4); B PATCH (If-Match: 3) gagal 409 dengan currentVersion=4.",
    "User A dan B POST /cards/X/move bersamaan ke kolom berbeda; akhir state: card ada di satu kolom saja, version increment 2.",
    "DELETE card → tidak muncul di GET board; restore dalam 30 hari → muncul lagi dengan version yang sama.",
    "POST card dengan dpPaidIdr > valueIdr*1.1 → 422 dengan code DP_EXCEEDS_VALUE.",
]))

story.append(H2("23.3 Test Pyramid"))
story.append(data_table(
    ["Layer", "Tooling", "Coverage Target"],
    [
        ["Unit (service/util)", "JUnit 5 + Mockito", "≥ 80%"],
        ["Integration (slice)", "@DataJpaTest + Testcontainers MySQL", "Repository + JPQL"],
        ["Integration (full)", "@SpringBootTest + Testcontainers (mysql, redis, minio)", "Happy + edge per endpoint"],
        ["Contract", "REST Assured against running container", "All endpoints"],
        ["Load", "k6 / Gatling", "Board GET 500 RPS, p95 < 200ms"],
        ["Security", "OWASP ZAP baseline", "Pass CI gate"],
    ],
    col_widths=[3.5 * cm, 5.5 * cm, 7.4 * cm]
))

story.append(H2("23.4 Load Test Scenarios"))
story.append(bullets([
    "<b>Board read storm:</b> 200 user, 5 board per user, 2 req/s GET board → 60s, target p95 &lt; 200 ms.",
    "<b>Drag-drop storm:</b> 50 user di 1 board, move random card setiap 1-3 detik → tidak boleh ada 409 spike, p95 &lt; 250 ms.",
    "<b>Finance summary:</b> 50 user spam GET finance summary → cache hit ratio &gt; 90%, p95 &lt; 100 ms.",
    "<b>Export CSV:</b> 10 user trigger export ribuan row → memori tidak naik &gt; 200 MB.",
]))

story.append(H2("23.5 Pre-Production Checklist"))
story.append(bullets([
    "All Flyway migration tested terhadap staging restore.",
    "<font face='Courier' size='9'>ddl-auto: validate</font> aktif di production profile.",
    "<font face='Courier' size='9'>flyway.clean-disabled: true</font> di semua environment.",
    "Tidak ada <font face='Courier' size='9'>System.out.println</font> sisa.",
    "<font face='Courier' size='9'>SQL_MODE</font> MySQL: <font face='Courier' size='9'>STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION</font>.",
    "TLS termination di proxy, HSTS header aktif.",
    "Backup MySQL otomatis terverifikasi (test restore minimal sekali).",
    "Runbook untuk: deadlock storm, DB down, Redis down, attachment storage down.",
    "On-call rotation dijadwalkan.",
]))

# ─── Closing ───
story.append(Spacer(1, 1 * cm))
story.append(HRFlowable(width="100%", thickness=1.5, color=BRAND))
story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph(
    '<para align="center"><font color="#17172E" size="11"><b>— END OF DOCUMENT —</b></font></para>',
    BODY))
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    '<para align="center"><font color="#6B6B88" size="9">'
    'PROMPTARA Backend PRD v1.0 · Spring Boot · MySQL · Flyway · Docker<br/>'
    'Dokumen ini hidup; kirim PR untuk koreksi/usulan ke repo backend.</font></para>',
    BODY))

# ─────────────────────────────────────────────────────
# Build
# ─────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2 * cm,
    rightMargin=2 * cm,
    topMargin=2.2 * cm,
    bottomMargin=2.2 * cm,
    title="PROMPTARA Backend PRD",
    author="PROMPTARA Engineering",
    subject="Backend Product Requirements Document",
)

doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
print(f"OK: {OUTPUT}")
