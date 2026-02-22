# XSS-ScanBot 🤖

> A security tool for testing websites and finding XSS vulnerabilities automatically.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![BugBounty](https://img.shields.io/badge/Bug-Bounty-red)

## Features
- Tests multiple XSS payloads automatically
- Detects reflected XSS in URL parameters
- Color coded output (Red=Vulnerable, Green=Safe)
- Saves vulnerable results to output file
- 8 built-in XSS payloads

## Installation
```bash
git clone https://github.com/ambuj9004-blip/XSS-ScanBot
cd XSS-ScanBot
pip install requests colorama
