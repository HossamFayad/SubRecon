# SubRecon

A simple subdomain reconnaissance and takeover fingerprinting tool written in Python.

## Features

- Subdomain enumeration using subfinder
- HTTP probing using httpx
- Status code filtering
- Fingerprint detection
- CNAME analysis
- Provider detection
- Internal / external CNAME classification

---

## Requirements

- Python 3
- subfinder
- httpx

Make sure subfinder and httpx are installed and accessible from your PATH.
---

## Install Python Requirements

```bash
pip install -r requirements.txt
Install subfinder
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
Install httpx
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
Usage
python main.py -d example.com
Example Output
[Interesting]
https://invite.example.com [] [Fastly error: unknown domain]

[CNAME] example.herokudns.com.

[External Provider]

[Possible Provider] heroku
Fingerprints

Current fingerprints include:

Fastly error
No such app
unknown domain
GitHub Pages errors
Providers

Current provider detection includes:

Heroku
GitHub
Vercel
AWS
Azure
Disclaimer

This project is intended for educational and authorized security testing purposes only.

Do not use this tool against systems without permission.
