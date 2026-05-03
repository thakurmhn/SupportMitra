# SupportMitra Development Plan

## 1. Architecture Blueprint

### Core Layers

1. Customer Portal (React + Tailwind)
   - Public landing, service catalog, pricing, case opening flow
   - Authenticated dashboard for customers
   - Payment checkout with Razorpay / PayU integration
   - Case status view and knowledge base
   - File attachment upload for ticket evidence

2. API Backend (Python + Django Rest Framework)
   - Ticket creation, assignment, updates
   - Customer, freelancer, payment, and SLA management
   - OAuth2 + MFA
   - Integration adapter for osTicket/Zammad
   - Celery + Redis for async tasks (SLA alerts, notifications, payouts)

3. Database Layer (PostgreSQL)
   - Central transactional data store
   - Customer profiles, tickets, payments, SLAs, freelancer logs

4. Ticketing Platform
   - Phase 1: Integrate open-source osTicket or Zammad
   - Phase 2: Connector to ServiceNow / Jira

5. Payment Gateway
   - Razorpay / PayU integration for:
     - initial consulting fee
     - resolution fee capture
     - refunds and payouts
   - GST invoice generation (mandatory for Indian billing)

6. Freelancer Operations
   - Admin dashboard for assignment
   - SLA compliance engine
   - Payout management and audit logs
   - Notifications via email / Slack / WhatsApp
   - Escalation matrix for SLA breaches

7. Hosting / Infrastructure
   - Low-cost VPS on DigitalOcean / Linode
   - Docker Compose or lightweight Kubernetes (k3s) later
   - CDN for frontend assets
   - SSL via Let's Encrypt
   - Object storage (DigitalOcean Spaces / S3) for ticket attachments and backups

8. Notification Services
   - Email: SendGrid or AWS SES for transactional mail
   - WhatsApp Business API: Gupshup or Twilio (India-first)
   - In-app: Django Channels or polling-based notification feed

9. Remote Support Tooling
   - AnyDesk or Zoho Assist for remote desktop sessions during ticket resolution
   - Session links attached to ticket record for audit trail

### Layered ASCII Diagram

```
+---------------------------+
|  Customer Portal (React)  |
+-------------+-------------+
              |
              v
+---------------------------+
|   API Backend (Django)    |
| - Auth/OAuth2/MFA         |
| - Ticketing Adapter       |
| - Payments Service        |
| - SLA Engine              |
| - Celery Worker (async)   |
+------+------+------+------+
       |      |      |
       |      |      v
       |      |  +----------------+
       |      |  | Redis          |
       |      |  | (sessions/     |
       |      |  |  task queue)   |
       |      |  +----------------+
       |      |
       |      v
       |  +----------------+
       |  | Payment Gateway|
       |  | Razorpay/PayU  |
       |  +----------------+
       |
       v
+---------------------------+
|      PostgreSQL DB        |
| - customers               |
| - tickets                 |
| - payments                |
| - freelancers             |
| - sla_logs                |
| - audit_logs              |
+---------------------------+
       |
       v
+---------------------------+
| Ticketing Tool (osTicket) |
| / Zammad / ServiceNow     |
+---------------------------+
       |
       v
+---------------------------+
| Object Storage (Spaces/S3)|
| - ticket attachments      |
| - DB backups              |
+---------------------------+
```

---

## 2. Phased Development Plan (Month 1–6)

### Month 1: MVP Planning & Foundation

- Goals:
  - Validate product-market fit for SMB IT support and SAP Basis lite
  - Build a lowest-cost viable system
- Deliverables:
  - Requirements for support services, pricing, and case workflow
  - Hosting setup on DigitalOcean / Linode droplet
  - Django project skeleton and React shell
  - PostgreSQL provisioning
  - Basic user auth and customer signup
  - Secrets management via `.env` files (never hardcoded)
  - Domain registration and SSL (Let's Encrypt)
  - Freelancer agreement template (NDA + contract)
  - Legal: Terms of Service, Privacy Policy, Refund Policy pages drafted
- Checklist:
  - [ ] Define service packages and fee model (consulting + resolution fee split)
  - [ ] Define freelancer payout percentage and schedule
  - [ ] Create MVP wireframes
  - [ ] Set up repository and branch strategy
  - [ ] Configure VPS and firewall (UFW, disable root SSH)
  - [ ] Deploy initial landing page
  - [ ] Register domain and configure SSL
  - [ ] Set up `.env` based secret management; remove hardcoded credentials from docker-compose
  - [ ] Draft freelancer contract / NDA template
  - [ ] Draft Terms of Service and Privacy Policy (DPDP Act 2023 compliant)
  - [ ] Register business (sole proprietor or Pvt Ltd) and obtain GST number if applicable

### Month 2: MVP Development

- Goals:
  - Launch customer-facing support portal
  - Enable ticket opening and payments
- Deliverables:
  - Customer registration and login
  - Ticket creation workflow with severity and file attachment
  - Razorpay / PayU checkout for ₹299 consulting fee
  - Basic backend ticket API with full schema (severity, ticket_number, notes, resolved_at)
  - Frontend dashboard with ticket history
  - GST-compliant invoice generation on payment
  - JWT token refresh and password-reset endpoints
- Checklist:
  - [ ] Implement OAuth2 login (Google/GitHub)
  - [ ] Build payment integration with Razorpay / PayU
  - [ ] Add GST invoice generation (PDF)
  - [ ] Implement JWT refresh and password-reset flows
  - [ ] Create ticket model and API (full schema including severity, ticket_number)
  - [ ] Add file attachment support (object storage integration)
  - [ ] Add service catalog UI with pricing cards
  - [ ] Deploy staging environment
  - [ ] Set up transactional email provider (SendGrid / AWS SES)

### Month 3: Pilot Launch + Freelance Backend

- Goals:
  - Start pilot with first SMB customers and freelance admins
  - Introduce admin assignment flow
- Deliverables:
  - Freelancer registration, vetting workflow, and profile management
  - Admin dashboard for ticket assignment and monitoring
  - SLA monitoring for response/resolution times
  - Payment record capture and invoice generation
  - Escalation matrix for SLA breach handling
  - Celery + Redis for async notifications and SLA cron checks
- Checklist:
  - [ ] Build freelancer portal (registration, skill tagging, availability)
  - [ ] Define and document freelancer vetting / onboarding process
  - [ ] Set up Celery + Redis for async tasks
  - [ ] Implement SLA breach alerts via email / WhatsApp
  - [ ] Implement case assignment workflows (manual + basic skill match)
  - [ ] Add SLA log tracking (sla_logs model + API)
  - [ ] Define escalation matrix (L1 → L2 → admin escalation rules)
  - [ ] Run pilot with 5–10 customers
  - [ ] Collect feedback and adjust pricing
  - [ ] Set up WhatsApp Business API provider (Gupshup / Twilio)

### Month 4: Expand Ticketing & Support Ops

- Goals:
  - Integrate open-source ticketing tool
  - Improve operations and transparency
- Deliverables:
  - osTicket / Zammad sync
  - Notifications for customers and admins (email + WhatsApp)
  - Freelancer activity logs and payout dashboard
  - Basic reporting for cases opened and SLA breaches
  - Remote session link attachment to tickets (AnyDesk / Zoho Assist)
  - CSAT (Customer Satisfaction Score) survey after ticket closure
- Checklist:
  - [ ] Install and configure osTicket / Zammad
  - [ ] Build connector for ticket sync (bi-directional status + comments)
  - [ ] Add email and WhatsApp notifications (templates for open/assign/resolve/breach events)
  - [ ] Add payout tracking dashboard
  - [ ] Integrate AnyDesk / Zoho Assist session links in tickets
  - [ ] Add CSAT survey trigger on ticket close
  - [ ] Harden infrastructure (dependency scans, OS patching schedule)
  - [ ] Add audit_logs model and populate for all key actions

### Month 5: Scale & Improve UX

- Goals:
  - Stabilize platform and scale to 20+ customers
  - Improve customer experience and security
- Deliverables:
  - Performance tuning
  - MFA and RBAC
  - Enhanced case tracking and comments
  - Self-service FAQ and knowledge base
  - In-app notification feed
  - Subscription / retainer package billing
- Checklist:
  - [ ] Add React/Tailwind UI polish and mobile responsiveness
  - [ ] Implement MFA (TOTP) for admin and freelancer accounts
  - [ ] Optimize database queries (add indexes, query analysis)
  - [ ] Add Redis caching for sessions and rate limiting
  - [ ] Add service-level views and filters (by severity, SLA status, service type)
  - [ ] Deploy production-ready monitoring (Prometheus + Grafana or Sentry)
  - [ ] Build knowledge base / FAQ module with search
  - [ ] Add subscription billing model (monthly retainer tiers)
  - [ ] Conduct user testing (UAT) with 3+ pilot customers

### Month 6: Enterprise Readiness & Roadmap

- Goals:
  - Prepare for larger SAP shops and enterprise integrations
  - Launch analytics and subscription model
- Deliverables:
  - Subscription / retainer support packages
  - Enterprise SLA dashboards
  - Jira / ServiceNow roadmap design
  - Backup and disaster recovery plan
  - NPS tracking and customer health metrics
  - SEO-optimized public pages and case study content
- Checklist:
  - [ ] Design subscription pricing tiers (Silver / Gold / Platinum)
  - [ ] Build analytics dashboard (ticket volume, CSAT, revenue by service, freelancer utilization)
  - [ ] Plan connector for ServiceNow / Jira
  - [ ] Document SOPs for support workflows and security incidents
  - [ ] Validate backup and failover (quarterly restore test)
  - [ ] Add NPS survey trigger (30 days post-signup)
  - [ ] Publish 2–3 SEO-targeted landing pages (e.g., "SAP Basis support for SMBs")
  - [ ] Plan RMM (Remote Monitoring & Management) tool evaluation for proactive support

---

## 3. Database Schema

### customers
- id UUID PK
- name varchar
- email varchar unique
- phone varchar
- company varchar
- address text
- plan varchar (free, silver, gold, platinum)
- gstin varchar (GST number for B2B billing)
- created_at, updated_at
- oauth_provider varchar
- oauth_id varchar
- mfa_enabled boolean default false

### tickets
- id UUID PK
- customer_id FK -> customers
- ticket_number varchar unique (human-readable, e.g. TKT-00042)
- title varchar
- description text
- service_type enum [desktop, linux, windows, patching, security, vmware, sap]
- severity enum [low, medium, high, critical]
- status enum [open, assigned, in_progress, resolved, closed]
- assigned_to FK -> freelancers nullable
- created_at, updated_at, resolved_at
- external_ticket_id varchar
- remote_session_url varchar
- notes text

### ticket_comments
- id UUID PK
- ticket_id FK -> tickets
- author_id UUID
- author_type enum [customer, freelancer, admin]
- body text
- created_at

### ticket_attachments
- id UUID PK
- ticket_id FK -> tickets
- file_name varchar
- storage_url varchar
- uploaded_by UUID
- uploaded_at

### payments
- id UUID PK
- customer_id FK -> customers
- ticket_id FK -> tickets nullable
- amount numeric
- currency varchar default 'INR'
- gst_amount numeric
- invoice_number varchar unique
- payment_type enum [consulting_fee, resolution_fee, subscription, refund]
- gateway enum [razorpay, payu]
- gateway_payment_id varchar
- status enum [pending, completed, failed, refunded]
- created_at, updated_at

### freelancers
- id UUID PK
- name varchar
- email varchar unique
- phone varchar
- skills text (comma-separated or JSON tags)
- availability enum [full_time, part_time, ad_hoc]
- rating numeric (0.0–5.0, avg of CSAT scores)
- active boolean default true
- payout_mode enum [bank_transfer, upi]
- payout_details jsonb (encrypted)
- contract_signed boolean default false
- onboarding_status enum [pending, approved, suspended]
- created_at, updated_at

### sla_policies
- id UUID PK
- service_type varchar
- severity enum [low, medium, high, critical]
- first_response_seconds int
- resolution_seconds int
- plan varchar

### sla_logs
- id UUID PK
- ticket_id FK -> tickets
- event enum [created, assigned, first_response, resolved, breach]
- timestamp
- target_seconds int
- actual_seconds int
- status enum [met, missed]
- notes text

### freelancer_logs
- id UUID PK
- freelancer_id FK -> freelancers
- ticket_id FK -> tickets
- action varchar
- details text
- timestamp

### audit_logs
- id UUID PK
- user_id UUID
- user_type enum [customer, freelancer, admin]
- entity varchar
- entity_id UUID
- action varchar
- metadata jsonb
- ip_address inet
- created_at

### csat_surveys
- id UUID PK
- ticket_id FK -> tickets
- customer_id FK -> customers
- score int (1–5)
- comment text
- submitted_at

### subscriptions
- id UUID PK
- customer_id FK -> customers
- plan varchar (silver, gold, platinum)
- billing_cycle enum [monthly, annual]
- status enum [active, cancelled, expired]
- started_at, expires_at
- payment_id FK -> payments nullable

---

## 4. API Design

### Authentication
- POST /api/auth/signup
- POST /api/auth/login
- POST /api/auth/logout
- POST /api/auth/token/refresh
- POST /api/auth/password-reset
- POST /api/auth/password-reset/confirm
- POST /api/auth/oauth/callback
- POST /api/auth/mfa/setup
- POST /api/auth/mfa/verify

### Customer Profile
- GET  /api/customers/me
- PATCH /api/customers/me
- GET  /api/customers/me/subscriptions

### Customer Ticket Flow
- GET  /api/services
- POST /api/tickets
- GET  /api/tickets
- GET  /api/tickets/{ticket_id}
- PATCH /api/tickets/{ticket_id}
- POST /api/tickets/{ticket_id}/comments
- GET  /api/tickets/{ticket_id}/comments
- POST /api/tickets/{ticket_id}/attachments
- GET  /api/tickets/{ticket_id}/attachments
- POST /api/tickets/{ticket_id}/csat

### Payment Flow
- POST /api/payments/checkout
- POST /api/payments/webhook
- GET  /api/payments/{payment_id}
- GET  /api/payments/{payment_id}/invoice
- GET  /api/customers/{customer_id}/payments

### Subscription Management
- GET  /api/subscriptions/plans
- POST /api/subscriptions
- PATCH /api/subscriptions/{subscription_id}
- DELETE /api/subscriptions/{subscription_id}

### Freelancer / Admin Operations
- GET  /api/admin/tickets
- POST /api/admin/tickets/{ticket_id}/assign
- PATCH /api/admin/tickets/{ticket_id}/status
- GET  /api/admin/freelancers
- POST /api/admin/freelancers
- PATCH /api/admin/freelancers/{freelancer_id}
- GET  /api/admin/sla
- GET  /api/admin/payouts
- POST /api/admin/payouts/{freelancer_id}
- GET  /api/admin/csat

### Notifications
- GET  /api/notifications
- PATCH /api/notifications/{notification_id}/read
- POST /api/notifications/preferences (email, whatsapp toggles)

### Ticketing Integration
- POST /api/integrations/osticket/sync
- POST /api/integrations/zammad/sync
- POST /api/integrations/jira/prepare
- POST /api/integrations/servicenow/prepare

### Dashboard / Analytics
- GET /api/dashboard/summary
- GET /api/dashboard/sla
- GET /api/dashboard/revenue
- GET /api/dashboard/csat
- GET /api/dashboard/freelancer-utilization

---

## 5. DevOps Plan

### Secrets Management
- All secrets in `.env` files; never committed to git
- `.env.example` with placeholder values committed instead
- Production secrets in DigitalOcean environment variables or Vault
- Docker Compose credentials read from environment variables, not hardcoded

### CI/CD Pipeline
- Use GitHub Actions or GitLab CI
- Pipeline stages:
  - lint (Python + JavaScript)
  - test (unit + integration)
  - security scan (Bandit for Python, npm audit for JS)
  - build frontend
  - build backend
  - deploy to staging
  - deploy to production on main release
- Deployment:
  - Docker Compose on DigitalOcean / Linode
  - Optionally use dokku or Caprover for lower ops overhead
- Branch strategy:
  - `main` for production
  - `develop` for integration
  - `feature/<name>` for each epic

### Async Task Infrastructure
- Celery with Redis as broker
- Task queues:
  - `notifications` — email, WhatsApp delivery
  - `sla` — periodic SLA breach checks (celerybeat every 5 min)
  - `payouts` — freelancer payout batch processing
  - `integrations` — osTicket/Zammad sync jobs

### Monitoring
- Application: Sentry (free tier) or open-source Prometheus + Grafana
- Logs: centralized Loki + Grafana or ELK stack
- Health check endpoints:
  - GET /health
  - GET /readiness
  - GET /liveness
- Alerts:
  - SLA breaches
  - payment failures
  - high error rate
  - Celery worker down
  - disk space > 80%

### Logging
- Structured JSON logs
- Separate logs for:
  - API requests
  - payment events
  - freelancer actions
  - Celery tasks
- Retain 30 days in low-cost object storage

### Backup Strategy
- Daily PostgreSQL dump with point-in-time retention
- Weekly snapshot of VPS volume
- Store backups offsite in DigitalOcean Spaces or S3
- Restore test quarterly
- Backup checklist:
  - [ ] Automated DB backups (pg_dump via cron)
  - [ ] Encrypted storage (gpg or storage-level encryption)
  - [ ] Recovery playbook documented
  - [ ] Periodic restore validation

---

## 6. Security Plan

### Authentication & Authorization
- OAuth2 for primary login (Google / GitHub)
- MFA via TOTP for all admin and freelancer accounts
- Role-based access control:
  - customer
  - freelancer
  - admin
- Principle of least privilege for all API endpoints
- JWT with short access token TTL (15 min) + refresh token rotation

### Data Protection
- Encrypt data in transit with TLS 1.2+
- Encrypt sensitive fields at rest (payout_details, personal data)
- Store only minimal PCI-sensitive info; use gateway tokenization
- Comply with India's DPDP Act 2023:
  - explicit user consent at signup
  - data retention and deletion policy
  - data principal rights (access, correction, erasure requests)
  - data breach notification obligation

### Infrastructure Security
- Harden server OS; install only required packages
- Use UFW firewall rules
- Disable root SSH login; use SSH key authentication only
- Regular OS and dependency patching schedule
- Container isolation for backend, frontend, and ticketing app
- Secrets never in environment variables in Dockerfiles; use `.env` files or secrets manager

### Application Security
- Input validation and sanitization on all endpoints
- CSRF protection (Django built-in)
- Rate limiting on login (max 5 attempts), payment, and OTP endpoints
- Content Security Policy headers for frontend
- Payment webhook signature validation (Razorpay/PayU HMAC)
- File upload validation (MIME type, size limit, virus scan for attachments)
- Regular dependency vulnerability scans (Dependabot / Snyk)
- Security checklist:
  - [ ] MFA enabled for admins and freelancers
  - [ ] RBAC implemented and tested
  - [ ] Payment webhooks HMAC-validated
  - [ ] File upload sanitization in place
  - [ ] DPDP Act compliance checklist completed
  - [ ] Periodic security reviews (quarterly)
  - [ ] Penetration test before enterprise launch

---

## 7. Business & Legal

### Freelancer Agreements
- Signed NDA before platform access
- Service agreement covering:
  - scope of work and prohibited actions
  - payout terms and schedule
  - IP ownership of work delivered
  - termination and dispute resolution clause
- Store signed documents in object storage linked to freelancer profile

### Customer Agreements
- Terms of Service with SLA commitments
- Refund Policy (e.g., full refund if ticket not accepted within 2 hrs)
- Privacy Policy (DPDP Act 2023 compliant)
- Acceptable Use Policy

### Financial Compliance (India)
- GST registration (if turnover > ₹20L or providing digital services)
- GST invoice generated on every payment (GSTIN of both parties)
- TDS tracking on freelancer payouts (Section 194C if applicable)
- Annual financial audit readiness

### Dispute Resolution
- Customer dispute flow: raise dispute within 7 days of ticket closure
- Admin mediates; refund issued if resolution deemed inadequate
- Freelancer dispute: flagged, reviewed, payout held pending investigation

---

## 8. Scalability Roadmap

### Phase 1 → Phase 2
- Move from single VPS to multi-node setup
- Add Redis cache for sessions and rate limiting
- Use load balancer with two app instances
- Separate DB server from app server
- Dedicated Celery worker nodes

### Future Integrations
- ServiceNow / Jira connector:
  - map internal tickets to external cases
  - bi-directional sync for status and comments
  - phased as enterprise integration feature
- Add osTicket → Zammad migration path
- RMM (Remote Monitoring & Management) tool integration:
  - proactive alerting to create tickets automatically
  - candidates: Atera, NinjaRMM (evaluate at scale)

### Product Evolution
- Subscription and retainer models:
  - monthly support bundles (Silver / Gold / Platinum)
  - SLA tiers per plan (e.g., Gold = 1 hr response, 8 hr resolution)
- Analytics dashboard:
  - ticket volume trends
  - CSAT and NPS tracking
  - freelancer utilization and performance
  - revenue by service and plan tier
- Auto-assignment engine:
  - skill tag matching
  - availability-based routing
  - load balancing across active freelancers
- Customer self-service:
  - searchable knowledge base
  - automated diagnostics (common issues)
  - chatbot for pre-sales and common queries (Phase 3)

### Customer Acquisition
- SEO-optimized landing pages per service vertical (e.g., "SAP Basis support India")
- Case studies and testimonials from pilot customers
- Partner with SMB IT consultants for referrals
- Google Ads for high-intent search terms ("server support outsourcing India")

---

## 9. Tech Stack Summary

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite + Tailwind CSS |
| Backend | Python 3.11 + Django 4.x + DRF |
| Database | PostgreSQL 15 |
| Cache / Queue broker | Redis |
| Async tasks | Celery + Celery Beat |
| Auth | Django SimpleJWT + OAuth2 (allauth) |
| Payments | Razorpay / PayU |
| Email | SendGrid or AWS SES |
| WhatsApp | Gupshup or Twilio WhatsApp Business API |
| Object Storage | DigitalOcean Spaces (S3-compatible) |
| Remote Support | AnyDesk or Zoho Assist |
| Ticketing | osTicket or Zammad (Phase 1) |
| Monitoring | Sentry + Prometheus/Grafana |
| CI/CD | GitHub Actions |
| Hosting | DigitalOcean / Linode VPS |
| Containers | Docker Compose (k3s later) |
| CDN | Cloudflare (free tier) |

---

## Executive Summary

- Use an open-source, low-cost stack: React + Tailwind, Django, PostgreSQL, osTicket/Zammad.
- Start with a strong MVP: customer portal, paid ticket creation, and freelancer assignment.
- Host on DigitalOcean / Linode for cost control and simplicity.
- Secure the platform with OAuth2, MFA, RBAC, and DPDP Act compliance from day one.
- Never hardcode credentials — use `.env` files and environment variables throughout.
- Add Celery + Redis from Month 3 to power async notifications and SLA breach detection.
- Build operational dashboards and payment transparency to drive trust.
- Establish freelancer contracts, GST invoicing, and customer agreements before going live.
- Roadmap into enterprise-ready ServiceNow/Jira integration, RMM tooling, and subscription offerings.
