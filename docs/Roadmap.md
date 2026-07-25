# Project Roadmap

## V0.1 - Foundation
Purpose: establish the application shell, architecture, and development standards.

Features:
- Project initialization
- Backend skeleton
- Frontend shell
- Database foundation
- Configuration management
- Logging
- Testing setup
- Documentation baseline

Deliverables:
- runnable local app skeleton
- initial docs and project structure
- CI-ready testing baseline

Dependencies:
- repository setup
- core environment configuration

Testing:
- unit tests for configuration and health endpoints

## V0.2 - Expense Engine
Purpose: support basic expense tracking and analysis.

Features:
- CSV import
- Excel import
- transaction storage
- categorization
- charts and monthly summaries
- category breakdowns
- budget tracking
- budget-aware dashboard insights

Deliverables:
- polished expense dashboard
- import and categorization services
- budget monitoring workflow

Dependencies:
- database schema for transactions, categories, and budgets

Testing:
- import correctness tests
- analytics validation tests
- budget workflow tests

## V0.3 - Advanced Expense Analysis
Purpose: deepen financial insight.

Features:
- PDF statement parsing
- duplicate detection
- income detection
- AI insights
- monthly comparison
- prediction capabilities

Deliverables:
- richer financial analytics
- improved AI recommendations

Dependencies:
- v0.2 expense engine

Testing:
- parser and inference tests
- regression tests for historical reports

## V0.4 - Inventory
Purpose: provide grocery inventory management.

Features:
- Excel inventory import
- stock tracking
- low-stock detection
- consumption tracking
- weekly updates

Deliverables:
- inventory module
- stock dashboard

Dependencies:
- database inventory schema

Testing:
- import and stock-change tests

## V0.5 - Shopping Intelligence
Purpose: support smart shopping planning.

Features:
- shopping list generation
- price comparison
- ratings comparison
- recommended products
- promotion awareness

Deliverables:
- shopping recommendation engine

Dependencies:
- inventory data and product catalog

Testing:
- ranking and recommendation tests

## V0.6 - Shopping Automation
Purpose: enable safe browser-based cart preparation.

Features:
- Playwright automation
- browser login support
- add-to-cart workflows
- user approval gates

Deliverables:
- safe automation workflow

Dependencies:
- shopping intelligence module

Testing:
- workflow simulations and approval tests

## V0.7 - AI Brain
Purpose: turn the platform into an intelligent household assistant.

Features:
- LangGraph orchestration
- memory layer
- expense assistant
- inventory assistant
- shopping assistant
- reminder assistant
- coordinator agent

Deliverables:
- conversational AI layer
- multi-agent orchestration

Dependencies:
- all domain modules

Testing:
- agent reasoning and tool-calling tests

## V0.8 - Reports
Purpose: provide executive and household reporting.

Features:
- weekly reports
- monthly reports
- Excel export
- PDF export
- charts and summaries

Deliverables:
- reporting module and export flows

Dependencies:
- expense and inventory modules

Testing:
- report generation and export tests

## V0.9 - Optimization
Purpose: improve reliability, performance, and polish.

Features:
- performance tuning
- resilience improvements
- usability refinements
- security hardening
- operational monitoring

Deliverables:
- release-ready experience

Dependencies:
- all prior versions

Testing:
- load and resilience testing

## V1.0 - Production Release
Purpose: deliver a polished, documented, production-ready release.

Features:
- final bug fixes
- full testing coverage
- Docker packaging
- installer readiness
- full documentation

Deliverables:
- production release bundle
- release notes and migration documentation

Dependencies:
- all prior versions

Testing:
- full suite integration and deployment validation
