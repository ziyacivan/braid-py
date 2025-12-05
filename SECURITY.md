# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of BRAID-DSPy seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please do NOT:

- Open a public GitHub issue
- Discuss the vulnerability in public forums or chat rooms
- Share the vulnerability with others until it has been addressed

### Please DO:

1. **Email us directly** at [INSERT SECURITY EMAIL] with:
   - A description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact of the vulnerability
   - Any suggested fixes or mitigations

2. **Allow us time** to investigate and address the vulnerability before disclosure

### What to Expect

- We will acknowledge receipt of your report within 48 hours
- We will provide an initial assessment within 7 days
- We will keep you informed of our progress
- We will notify you when the vulnerability is fixed

### Disclosure Policy

- We will credit you for the discovery (if desired)
- We will work with you to coordinate public disclosure after a fix is available
- We aim to address critical vulnerabilities within 30 days

## Security Best Practices

When using BRAID-DSPy:

- Keep your dependencies up to date
- Use environment variables for sensitive configuration (API keys, etc.)
- Review and validate GRD outputs before execution
- Be cautious when processing untrusted input
- Follow the principle of least privilege

## Known Security Considerations

- **API Keys**: Never commit API keys or credentials to version control
- **Input Validation**: Always validate user input before processing
- **Dependency Updates**: Regularly update dependencies to receive security patches

## Security Updates

Security updates will be announced in:
- GitHub Security Advisories
- Release notes
- CHANGELOG.md

Thank you for helping keep BRAID-DSPy and its users safe!

