import subprocess
import dns.resolver
import argparse
import os
import shutil
import sys


interesting = ["[404]", "[403]", "[500]", "[503]", "[525]"]

fingerprints = [
    "Fastly error",
    "No such app",
    "unknown domain",
    "There isn't a GitHub Pages site here"
]

providers = [
    "heroku",
    "github",
    "vercel",
    "amazonaws",
    "azure"
]


def check_tools():

    if not shutil.which("subfinder"):

        print("[!] subfinder not found")
        sys.exit()

    if not shutil.which("httpx"):

        print("[!] httpx not found")
        sys.exit()


def run_subfinder(domain, filename):

    print("[*] Running subfinder...")

    cmd = (
        f"subfinder "
        f"-d {domain} "
        f"-silent "
        f"-o {filename}"
    )

    subprocess.getoutput(cmd)


def run_httpx(filename):

    print("[*] Running httpx...")

    cmd = (
        f"httpx "
        f"-l {filename} "
        f"-sc "
        f"-title "
        f"-silent"
    )

    result = subprocess.getoutput(cmd)

    return result.splitlines()


def check_cname(subdomain, domain, resolver):

    try:

        answers = resolver.resolve(
            subdomain,
            "CNAME"
        )

        for rdata in answers:

            cname = str(rdata.target)

            print("[CNAME]", cname)

            if domain.lower() in cname.lower():

                print("[Internal CNAME]")

            else:

                print("[External Provider]")

            for provider in providers:

                if provider in cname.lower():

                    print(
                        "[Possible Provider]",
                        provider
                    )

    except dns.resolver.NoAnswer:

        print("[No CNAME]")

    except dns.resolver.LifetimeTimeout:

        print("[DNS Timeout]")

    except Exception as e:

        print(e)


def analyze_results(lines, domain, resolver):

    for line in lines:

        if (
            any(code in line for code in interesting)
            or
            any(
                fp.lower() in line.lower()
                for fp in fingerprints
            )
        ):

            print("\n[Interesting]")
            print(line)

            subdomain = (
                line.split(" ")[0]
                .replace("https://", "")
                .replace("http://", "")
            )

            check_cname(
                subdomain,
                domain,
                resolver
            )


def cleanup(filename):

    if os.path.exists(filename):

        os.remove(filename)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d",
        required=True,
        help="target domain"
    )

    args = parser.parse_args()

    domain = args.d

    filename = f"{domain}_subs.txt"

    resolver = dns.resolver.Resolver()

    resolver.timeout = 2
    resolver.lifetime = 2

    check_tools()

    run_subfinder(domain, filename)

    lines = run_httpx(filename)

    analyze_results(
        lines,
        domain,
        resolver
    )

    cleanup(filename)


main()
