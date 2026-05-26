# Project Guidelines for Claude

## Overview

This project follows comprehensive development standards across security, testing, code quality, error handling, and documentation. These guidelines are enforced through workspace-wide skills stored in `~/.config/Code/User/prompts/`.

## Workspace-Wide Skills

The following foundational skills apply to this project and all other projects:

### 1. Security Best Practices
**File**: `security-guidelines.md`

Covers OWASP Top 10 prevention, input validation & sanitization, secrets management, HTTPS enforcement, dependency auditing, rate limiting, and secure error messaging. Always follow these standards—never hardcode secrets or trust user input.

### 2. Testing Standards
**File**: `testing-guidelines.md`

Unit and integration testing patterns, test organization (collocate with code), coverage goals (>80%), TDD approach, and error case testing. Write tests for all features; aim for comprehensive coverage including edge cases and error paths.

### 3. Code Quality & Readability
**File**: `code-quality-guidelines.md`

Naming conventions (descriptive, verb-based for functions), Single Responsibility Principle, DRY principle, comment philosophy (explain "why", not "what"), type hints, and complexity reduction. Focus on code that's easy to understand and maintain.

### 4. Error Handling & Logging
**File**: `error-handling-guidelines.md`

Exception handling patterns, logging levels (debug/info/warn/error/critical), structured logging with context, debug logging dos/don'ts, and user-facing vs. internal error messages. Log meaningfully without leaking secrets or sensitive data.

### 5. Documentation Standards
**File**: `documentation-guidelines.md`

README essentials, inline code comments (explain complex logic), API documentation, Architecture Decision Records (ADRs), type hints as documentation, and keeping docs in sync with code. Docs should live near code and be treated as code.

## Project-Specific Guidance

### Core Principles

#### Security
Follow **security-guidelines.md** strictly. Never commit secrets, always validate input, use environment variables for configuration, and keep dependencies updated.

#### Code Quality
Follow **code-quality-guidelines.md**. Write readable, well-named code. Apply DRY principle, keep functions focused, use meaningful comments, and include type hints.

#### Testing
Follow **testing-guidelines.md**. Write tests alongside code. Aim for >80% coverage. Test error cases, edge cases, and happy paths. Organize tests near the code they test.

#### Error Handling
Follow **error-handling-guidelines.md**. Use specific exception handling, log with context, never log secrets, and provide safe error messages to users.

#### Documentation
Follow **documentation-guidelines.md**. Maintain a quality README, document complex logic, include API documentation, and keep docs current with code.

## Development Workflow
1. Understand requirements thoroughly before implementing
2. Plan complex changes before coding
3. Write tests alongside code or immediately after
4. Keep commits focused and atomic
5. Review code for security and quality before finalization
6. Consult workspace-wide skills before starting new features

## File Organization
- Follow language/framework conventions
- Keep related code together
- Separate concerns (models, services, controllers, etc.)
- Use meaningful directory names
- Tests colocate with the code they test

## Stack-Specific Guidance
*To be added once tech stack is decided.* When you select a framework/language, project-specific patterns and preferences will be documented here.

