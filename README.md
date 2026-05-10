# SubRecon

A simple subdomain reconnaissance and takeover fingerprinting tool written in Python.

---

## Features

* Subdomain enumeration using subfinder
* HTTP probing using httpx
* Status code filtering
* Fingerprint detection
* CNAME analysis
* Provider detection
* Internal / external CNAME classification
* JSON-based fingerprint database
* Detection of possible takeover patterns
* Automated recon workflow

---

## Requirements

* Python 3
* subfinder
* httpx

Make sure subfinder and httpx are installed and accessible from your PATH.

---

## Install Python Requirements

```bash
pip install -r requirements.txt
```

---

## Install subfinder

```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

---

## Install httpx

```bash
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
```

---

## Usage

```bash
python main.py -d example.com
```

---

## Example Output

```text
[Interesting]
https://invite.example.com [] [Fastly error: unknown domain]

[CNAME] example.herokudns.com.

[External Provider]

[Service] Heroku

[Fingerprint Match]

[Status] Edge case
```

---

## Fingerprint Database

SubRecon uses a JSON-based fingerprint database
to detect possible takeover patterns and
misconfigured services.

---

## Supported Services

* Heroku
* GitHub Pages
* Vercel
* Netlify
* Fastly
* AWS S3
* Azure
* Shopify
* WordPress
* Pantheon
* ReadTheDocs
* Surge
* Wix
* Ngrok
* Help Scout
* Tumblr
* Intercom
* وغيرها...

---

## Project Structure

```text
SubRecon/
│
├── main.py
├── fingerprints.json
├── requirements.txt
└── README.md
```

---

## Disclaimer

This project is intended for educational and authorized security testing purposes only.

Do not use this tool against systems without permission.
