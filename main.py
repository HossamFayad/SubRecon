import subprocess
import dns.resolver
import argparse
import os
import shutil
import sys
import json


def load_fingerprints():

    with open("fingerprints.json", "r") as file:

        return json.load(file)


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


def check_cname(
    subdomain,
    line,
    domain,
    resolver,
    fingerprints
):

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

            for fp in fingerprints:

                if any(
                    cname_item in cname.lower()
                    for cname_item in fp["cname"]
                ):

                    print(
                        "[Service]",
                        fp["service"]
                    )

                    if (
                        fp["fingerprint"]
                        .lower()
                        in line.lower()
                    ):

                        print(
                            "[Fingerprint Match]"
                        )

                        print(
                            "[Status]",
                            fp["status"]
                        )

    except dns.resolver.NoAnswer:

        print("[No CNAME]")

    except dns.resolver.LifetimeTimeout:

        print("[DNS Timeout]")

    except Exception as e:

        print(e)


def analyze_results(
    lines,
    domain,
    resolver,
    fingerprints
):

    for line in lines:

        for fp in fingerprints:

            if (
                fp["fingerprint"]
                .lower()
                in line.lower()
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
                    line,
                    domain,
                    resolver,
                    fingerprints
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

    fingerprints = load_fingerprints()

    resolver = dns.resolver.Resolver()

    resolver.timeout = 2
    resolver.lifetime = 2

    check_tools()

    run_subfinder(domain, filename)

    lines = run_httpx(filename)

    analyze_results(
        lines,
        domain,
        resolver,
        fingerprints
    )

    cleanup(filename)


main()
