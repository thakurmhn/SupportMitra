# SupportMitra Development Plan

## 1. Architecture Blueprint

### Core Layers

1. Customer Portal (React + Tailwind)
   - Public landing, service catalog, pricing, case opening flow
   - Authenticated dashboard for customers
   - Payment checkout with Razorpay / PayU integration
   - Case status view and knowledge base

2. API Backend (Python + Django Rest Framework)
   - Ticket creation, assignment, updates
   - Customer, freelancer, payment, and SLA management
   - OAuth2 + MFA
   - Integration adapter for osTicket/Zammad

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

6. Freelancer Operations
   - Admin dashboard for assignment
   - SLA compliance engine
   - Payout management and audit logs
   - Notifications via email / Slack / WhatsApp

7. Hosting / Infrastructure
   - Low-cost VPS on DigitalOcean / Linode
   - Docker Compose or lightweight Kubernetes (k3s) later
   - CDN for frontend assets
   - SSL via Let’s Encrypt

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
+------+------+-------------+
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
| / Zammad / future ServiceNow|
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
- Checklist:
  - [ ] Define service packages and fee model
  - [ ] Create MVP wireframes
  - [ ] Set up repository and branch strategy
  - [ ] Configure VPS and firewall
  - [ ] Deploy initial landing page

### Month 2: MVP Development

- Goals:
  - Launch customer-facing support portal
  - Enable ticket opening and payments
- Deliverables:
  - Customer registration and login
  - Ticket creation workflow
  - Razorpay / PayU checkout for ₹299 consulting fee
  - Basic backend ticket API
  - Frontend dashboard with ticket history
- Checklist:
  - [ ] Implement OAuth2 login
  - [ ] Build payment integration
  - [ ] Create ticket model and API
  - [ ] Add service catalog UI
  - [ ] Deploy staging environment

### Month 3: Pilot Launch + Freelance Backend

- Goals:
  - Start pilot with first SMB customers and freelance admins
  - Introduce admin assignment flow
- Deliverables:
  - Freelancer registration and profile management
  - Admin dashboard for ticket assignment
  - SLA monitoring for response/resolution times
  - Payment record capture and invoice generation
- Checklist:
  - [ ] Build freelancer portal
  - [ ] Implement case assignment workflows
  - [ ] Add SLA log tracking
  - [ ] Run pilot with 5–10 customers
  - [ ] Collect feedback and adjust pricing

### Month 4: Expand Ticketing & Support Ops

- Goals:
  - Integrate open-source ticketing tool
  - Improve operations and transparency
- Deliverables:
  - osTicket / Zammad sync
  - Notifications for customers and admins
  - Freelancer activity logs and payout dashboard
  - Basic reporting for cases opened and SLA breaches
- Checklist:
  - [ ] Install and configure osTicket / Zammad
  - [ ] Build connector for ticket sync
  - [ ] Add email notifications
  - [ ] Add payout tracking
  - [ ] Harden infrastructure

### Month 5: Scale & Improve UX

- Goals:
  - Stabilize platform and scale to 20+ customers
  - Improve customer experience and security
- Deliverables:
  - Performance tuning
  - MFA and RBAC
  - Enhanced case tracking and comments
  - Self-service FAQ and knowledge base
- Checklist:
  - [ ] Add React/Tailwind UI polish
  - [ ] Implement MFA
  - [ ] Optimize database queries
  - [ ] Add service-level views and filters
  - [ ] Deploy production-ready monitoring

### Month 6: Enterprise Readiness & Roadmap

- Goals:
  - Prepare for larger SAP shops and enterprise integrations
  - Launch analytics and subscription model
- Deliverables:
  - Subscription / retainer support packages
  - Enterprise SLA dashboards
  - Jira / ServiceNow roadmap design
  - Backup and disaster recovery plan
- Checklist:
  - [ ] Design subscription pricing
  - [ ] Build analytics dashboard
  - [ ] Plan connector for ServiceNow / Jira
  - [ ] Document SOPs for support and security
  - [ ] Validate backup and failover

---

## 3. Database Schema

### customers
- id UUID PK
- name varchar
- email varchar unique
- phone varchar
- company varchar
- address text
- plan varchar
- created_at, updated_at
- oauth_provider, oauth_id
- mfa_enabled boolean

### tickets
- id UUID PK
- customer_id FK -> customers
- ticket_number varchar unique
- title varchar
- service_type enum [desktop, linux, windows, patching, security, vmware, sap]
- severity enum [low, medium, high, critical]
- status enum [open, assigned, in_progress, resolved, closed]
- assigned_to FK -> freelancers
- created_at, updated_at, resolved_at
- external_ticket_id varchar
- notes text

### payments
- id UUID PK
- customer_id FK -> customers
- ticket_id FK -> tickets nullable
- amount numeric
- currency varchar
- payment_type enum [consulting_fee, resolution_fee, refund]
- gateway enum [razorpay, payu]
- gateway_payment_id varchar
- status enum [pending, completed, failed, refunded]
- created_at, updated_at

### freelancers
- id UUID PK
- name varchar
- email varchar unique
- phone varchar
- skills text
- availability enum [full_time, part_time, ad_hoc]
- rating numeric
- active boolean
- payout_mode enum [bank, upi]
- created_at, updated_at

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
- created_at

---

## 4. API Design

### Authentication
- POST /api/auth/signup
- POST /api/auth/login
- POST /api/auth/oauth/callback
- POST /api/auth/mfa/verify
- POST /api/auth/mfa/setup

### Customer Ticket Flow
- GET /api/services
- POST /api/tickets
- GET /api/tickets
- GET /api/tickets/{ticket_id}
- PATCH /api/tickets/{ticket_id}
- POST /api/tickets/{ticket_id}/comments
- GET /api/tickets/{ticket_id}/comments

### Payment Flow
- POST /api/payments/checkout
- POST /api/payments/webhook
- GET /api/payments/{payment_id}
- GET /api/customers/{customer_id}/payments

### Freelancer / Admin Operations
- GET /api/admin/tickets
- POST /api/admin/tickets/{ticket_id}/assign
- POST /api/admin/tickets/{ticket_id}/status
- GET /api/admin/freelancers
- POST /api/admin/freelancers
- GET /api/admin/sla
- GET /api/admin/payouts
- POST /api/admin/payouts/{freelancer_id}

### Ticketing Integration
- POST /api/integrations/osticket/sync
- POST /api/integrations/zammad/sync
- POST /api/integrations/jira/prepare
- POST /api/integrations/servicenow/prepare

### Dashboard / Analytics
- GET /api/dashboard/summary
- GET /api/dashboard/sla
- GET /api/dashboard/revenue

---

## 5. DevOps Plan

### CI/CD Pipeline
- Use GitHub Actions or GitLab CI
- Pipeline stages:
  - lint (Python + JavaScript)
  - test
  - security scan
  - build frontend
  - build backend
  - deploy to staging
  - deploy to production on main release
- Deployment:
  - Docker Compose on DigitalOcean / Linode
  - Optionally use dokku or caprover for lower ops overhead
- Branch strategy:
  - main for production
  - develop for integration
  - feature branches for each epic

### Monitoring
- Application: Sentry or open-source Prometheus + Grafana
- Logs: centralized ELK stack or Loki + Grafana
- Health checks:
  - /health
  - /readiness
  - /liveness
- Alerts:
  - SLA breaches
  - payment failures
  - high error rate

### Logging
- Structured JSON logs
- Separate logs for:
  - API requests
  - payment events
  - freelancer actions
- Retain 30 days in low-cost storage

### Backup Strategy
- Daily PostgreSQL dump with point-in-time retention
- Weekly snapshot of VPS volume
- Store backups offsite in DigitalOcean Spaces or object storage
- Restore test quarterly
- Backup checklist:
  - [ ] automated DB backups
  - [ ] encrypted storage
  - [ ] recovery playbook
  - [ ] periodic restore validation

---

## 6. Security Plan

### Authentication & Authorization
- OAuth2 for primary login
- MFA via TOTP for all admin and freelancer accounts
- Role-based access control:
  - customer
  - freelancer
  - admin
- Principle of least privilege for APIs

### Data Protection
- Encrypt data in transit with TLS
- Encrypt sensitive fields at rest
- Store only minimal PCI-sensitive info; use gateway tokenization

### Infrastructure Security
- Harden server OS and install only required packages
- Use firewall rules and UFW
- Disable root SSH login
- Use SSH keys only
- Regular patching schedule for application and OS
- Container isolation for backend, frontend, and ticketing app

### Application Security
- Input validation and sanitization
- CSRF protection
- Rate limiting on login and payment endpoints
- Content Security Policy for frontend
- Regular dependency vulnerability scans
- Security checklist:
  - [ ] MFA enabled
  - [ ] RBAC implemented
  - [ ] External ticketing endpoints secured
  - [ ] Payment webhooks validated
  - [ ] Periodic security reviews

---

## 7. Scalability Roadmap

### Phase 1 → Phase 2
- Move from single VPS to multi-node setup
- Add Redis cache for sessions and rate limiting
- Use load balancer with two app instances
- Separate DB server from app

### Future Integrations
- ServiceNow / Jira connector:
  - map internal tickets to external cases
  - bi-directional sync for status and comments
  - phased as enterprise integration feature
- Add osTicket → Zammad migration path
- Build microservice for ticket sync if needed

### Product Evolution
- Add subscription and retainer models
  - monthly support bundles
  - SLA tiers for response and resolution
- Introduce analytics dashboard:
  - ticket volume
  - customer satisfaction
  - freelancer utilization
  - revenue by service
- Add auto-assignment engine:
  - skill match
  - availability
  - load balancing
- Add customer self-service:
  - knowledge base
  - automated diagnostics
  - chatbot for common issues

---

## Executive Summary

- Use an open-source, low-cost stack: React + Tailwind, Django, PostgreSQL, osTicket/Zammad.
- Start with a strong MVP: customer portal, paid ticket creation, and freelancer assignment.
- Host on DigitalOcean / Linode for cost control and simplicity.
- Secure the platform with OAuth2, MFA, and RBAC from day one.
- Build operational dashboards and payment transparency to drive trust.
- Roadmap into enterprise-ready ServiceNow/Jira integration and subscription offerings.
