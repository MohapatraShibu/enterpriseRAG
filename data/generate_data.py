# generate all synthetic enterprise datasets
import json, csv, random
from datetime import datetime, timedelta
from fpdf import FPDF, XPos, YPos
from pathlib import Path

DATA = Path("data")

def _clean(text: str) -> str:
    return text.replace("\u2014", "-").replace("\u2013", "-").replace("\u2019", "'").replace("\u2018", "'")

# PDF helper
def make_pdf(filename: str, title: str, sections: list[tuple[str, str]]):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, _clean(title), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(4)
    for heading, body in sections:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, _clean(heading), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(0, 6, _clean(body))
        pdf.ln(2)
    pdf.output(str(DATA / "pdfs" / filename))

# PDFs
make_pdf("hr_policy_2024.pdf", "HR Policy Manual 2024", [
    ("1. Leave Policy",
     "Employees are entitled to 20 days of paid annual leave per year. "
     "Sick leave is capped at 10 days. Maternity/paternity leave is 90 days paid. "
     "Leave requests must be submitted 5 business days in advance via the HR portal."),
    ("2. Code of Conduct",
     "All employees must maintain professional behaviour. Harassment, discrimination, "
     "and conflicts of interest are strictly prohibited. Violations may result in "
     "disciplinary action up to and including termination."),
    ("3. Performance Reviews",
     "Annual performance reviews are conducted every December. Ratings range from 1-5. "
     "Employees rated 4 or above are eligible for a merit bonus of up to 15% of base salary."),
    ("4. Remote Work Policy",
     "Employees may work remotely up to 3 days per week with manager approval. "
     "A stable internet connection and a secure VPN connection are mandatory."),
])

make_pdf("q2_financial_report.pdf", "Q2 2024 Financial Report", [
    ("Executive Summary",
     "Total revenue for Q2 2024 reached $48.7 million, a 12% increase year-over-year. "
     "Operating expenses were $31.2 million. Net profit stood at $17.5 million (36% margin)."),
    ("Revenue Breakdown",
     "Product sales: $28.4M. Service contracts: $14.1M. Licensing fees: $6.2M. "
     "Top performing region: North America at $22.1M followed by EMEA at $15.3M."),
    ("Cost Analysis",
     "R&D spend: $8.1M (16.6% of revenue). Sales & Marketing: $9.4M. "
     "G&A: $5.2M. COGS: $8.5M. Headcount costs increased 8% due to 45 new hires."),
    ("Outlook",
     "Q3 2024 revenue is projected at $51-54M. Key risks include supply chain delays "
     "and increased competition in the APAC region. Board approved $5M share buyback."),
])

make_pdf("compliance_policy.pdf", "Enterprise Compliance Policy", [
    ("Data Protection",
     "All customer PII must be encrypted at rest (AES-256) and in transit (TLS 1.3). "
     "Data retention is 7 years for financial records and 3 years for operational logs. "
     "GDPR and CCPA compliance is mandatory for all customer-facing systems."),
    ("Access Control",
     "Role-based access control (RBAC) is enforced across all systems. "
     "Privileged access requires MFA and is reviewed quarterly. "
     "Shared credentials are strictly prohibited."),
    ("Incident Response",
     "Security incidents must be reported within 1 hour of detection. "
     "The CISO must be notified for any breach affecting >100 records. "
     "Post-incident reviews are mandatory within 5 business days."),
    ("Audit Requirements",
     "All system access is logged and retained for 12 months. "
     "Internal audits are conducted bi-annually. External audits annually."),
])

make_pdf("strategic_roadmap.pdf", "Strategic Roadmap 2024-2026", [
    ("Vision",
     "Become the leading enterprise AI platform in North America by 2026, "
     "targeting $200M ARR with 500+ enterprise customers."),
    ("2024 Priorities",
     "1. Launch AI-powered analytics suite (Q3). "
     "2. Expand EMEA sales team by 20 headcount. "
     "3. Achieve SOC2 Type II certification. "
     "4. Reduce infrastructure costs by 18% via cloud optimisation."),
    ("2025 Initiatives",
     "Acquire two complementary SaaS companies in the data integration space. "
     "Launch partner ecosystem with 50 certified integrators. "
     "Expand to APAC with Singapore office."),
    ("Risk Factors",
     "Talent retention in engineering (mitigation: equity refresh program). "
     "Regulatory changes in EU AI Act. Macroeconomic slowdown impact on enterprise spend."),
])

make_pdf("onboarding_guide.pdf", "Employee Onboarding Guide", [
    ("Welcome",
     "Welcome to the company! This guide covers your first 30 days. "
     "Your manager will schedule a 1:1 on Day 1. IT will provision your accounts within 4 hours."),
    ("IT Setup",
     "Laptop will be pre-configured. Install VPN client from the IT portal. "
     "Enable MFA on all accounts. Report any issues to helpdesk@company.com."),
    ("Key Contacts",
     "HR: hr@company.com | IT Helpdesk: it@company.com | Payroll: payroll@company.com. "
     "Your buddy mentor will be assigned by HR within 48 hours."),
    ("Policies to Review",
     "Please read: Code of Conduct, Data Protection Policy, Remote Work Policy, "
     "and Acceptable Use Policy. Sign acknowledgement forms in the HR portal by Day 3."),
])

make_pdf("it_infrastructure_report.pdf", "IT Infrastructure Report Q2 2024", [
    ("Infrastructure Overview",
     "The company operates 3 data centres (US-East, EU-West, APAC) and uses AWS for cloud workloads. "
     "Total managed servers: 847. Cloud instances: 1,240. Network uptime: 99.97%."),
    ("Security Posture",
     "Vulnerability scans run weekly. 12 critical CVEs patched in Q2. "
     "EDR deployed on 100% of endpoints. Zero-trust network architecture rollout 70% complete."),
    ("Incidents",
     "3 P1 incidents in Q2: DB failover (Apr 12, RTO 14min), DDoS mitigation (May 3, 2hr), "
     "certificate expiry (Jun 18, 45min). All within SLA."),
    ("Capacity Planning",
     "Storage utilisation at 73%. Projected to hit 85% by Q4 — additional NAS approved. "
     "Network bandwidth upgrade scheduled for August."),
])

print("PDFs created.")

# CSV
employees = [
    ["EMP001","Alice Johnson","hr_manager","HR","85000","2019-03-15","New York","Active"],
    ["EMP002","Bob Smith","finance_analyst","Finance","78000","2020-07-01","Chicago","Active"],
    ["EMP003","Carol White","it_admin","IT","92000","2018-11-20","San Francisco","Active"],
    ["EMP004","Dave Brown","executive","Executive","180000","2015-01-10","New York","Active"],
    ["EMP005","Eve Davis","intern","Engineering","35000","2024-06-01","Remote","Active"],
    ["EMP006","Frank Miller","software_engineer","Engineering","110000","2021-04-22","Austin","Active"],
    ["EMP007","Grace Lee","data_scientist","Analytics","105000","2022-02-14","Seattle","Active"],
    ["EMP008","Henry Wilson","sales_manager","Sales","95000","2020-09-30","Boston","Active"],
    ["EMP009","Iris Chen","legal_counsel","Legal","130000","2017-08-05","New York","Active"],
    ["EMP010","Jack Taylor","devops_engineer","IT","98000","2021-12-01","Remote","Active"],
]
with open(DATA / "csv" / "employee_records.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["employee_id","name","role","department","salary","hire_date","location","status"])
    w.writerows(employees)

budget = [
    ["HR","Recruitment","150000","132000","88%"],
    ["HR","Training & Development","80000","71000","89%"],
    ["Finance","Software Licenses","200000","198000","99%"],
    ["Finance","Consulting","120000","95000","79%"],
    ["IT","Cloud Infrastructure","500000","487000","97%"],
    ["IT","Security Tools","180000","176000","98%"],
    ["Engineering","R&D Projects","800000","812000","102%"],
    ["Sales","Marketing Campaigns","300000","278000","93%"],
    ["Operations","Office & Facilities","250000","241000","96%"],
    ["Legal","External Counsel","400000","362000","91%"],
]
with open(DATA / "csv" / "budget_2024.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["department","category","budget_usd","spent_usd","utilisation_pct"])
    w.writerows(budget)

print("CSVs created.")

# JSON logs
base_time = datetime(2024, 6, 1, 8, 0, 0)
audit_logs = []
actions = [
    ("alice",   "LOGIN",  "hr_portal",       "SUCCESS"),
    ("bob",     "LOGIN",  "finance_system",  "SUCCESS"),
    ("carol",   "LOGIN",  "admin_console",   "SUCCESS"),
    ("eve",     "ACCESS", "finance_system",  "DENIED"),
    ("bob",     "EXPORT", "budget_report",   "SUCCESS"),
    ("unknown", "LOGIN",  "admin_console",   "FAILED"),
    ("carol",   "PATCH",  "server_config",   "SUCCESS"),
    ("alice",   "VIEW",   "employee_records","SUCCESS"),
    ("dave",    "VIEW",   "strategic_docs",  "SUCCESS"),
    ("eve",     "ACCESS", "hr_docs",         "DENIED"),
]
for i, (user, action, resource, status) in enumerate(actions):
    audit_logs.append({
        "timestamp": (base_time + timedelta(hours=i*3)).isoformat(),
        "event_id": f"EVT{1000+i}",
        "user": user,
        "action": action,
        "resource": resource,
        "status": status,
        "ip_address": f"10.0.{random.randint(1,5)}.{random.randint(10,200)}",
        "session_id": f"SES{random.randint(10000,99999)}"
    })
with open(DATA / "json_logs" / "system_audit_logs.json", "w") as f:
    json.dump(audit_logs, f, indent=2)

incidents = [
    {
        "incident_id": "INC-2024-001",
        "date": "2024-04-12",
        "severity": "P1",
        "type": "Database Failover",
        "description": "Primary database became unresponsive due to disk I/O saturation. Automatic failover triggered to replica in 8 minutes. Full recovery in 14 minutes. Root cause: runaway analytics query consuming 100% I/O.",
        "affected_systems": ["prod-db-01", "analytics-service"],
        "resolution": "Query optimised, I/O limits enforced on analytics workloads.",
        "status": "Resolved"
    },
    {
        "incident_id": "INC-2024-002",
        "date": "2024-05-03",
        "severity": "P1",
        "type": "DDoS Attack",
        "description": "Volumetric DDoS attack targeting public API gateway. Peak traffic: 2.3 Gbps. AWS Shield Advanced activated. Traffic scrubbing engaged within 12 minutes. Service restored in 2 hours.",
        "affected_systems": ["api-gateway", "load-balancer-01"],
        "resolution": "Rate limiting tightened, additional WAF rules deployed.",
        "status": "Resolved"
    },
    {
        "incident_id": "INC-2024-003",
        "date": "2024-06-18",
        "severity": "P1",
        "type": "Certificate Expiry",
        "description": "TLS certificate for internal service mesh expired causing service-to-service auth failures. 45-minute outage for 3 internal services. Certificate auto-renewal misconfiguration identified.",
        "affected_systems": ["service-mesh", "auth-service", "notification-service"],
        "resolution": "Certificate renewed, auto-renewal pipeline fixed and tested.",
        "status": "Resolved"
    },
]
with open(DATA / "json_logs" / "security_incidents.json", "w") as f:
    json.dump(incidents, f, indent=2)

print("JSON logs created.")
print("\nAll synthetic data generated successfully!")
