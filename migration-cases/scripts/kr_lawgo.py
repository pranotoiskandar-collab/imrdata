"""Collect Korean migration cases from the law.go.kr Open API.

Reads court precedents (target=prec) and Constitutional Court decisions
(target=detc) for each Korean term in ../keywords.json and appends the
hits to ../tables/candidates.csv.

Needs the OC value from open.law.go.kr (API인증키관리), passed as
--oc or the LAWGO_OC environment variable. Waits 3 seconds between calls.

    python3 kr_lawgo.py --oc YOUR_ID
"""
import argparse, csv, json, os, sys, time, datetime
import urllib.parse, urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://www.law.go.kr/DRF/lawSearch.do"
TARGETS = {"prec": "판례", "detc": "헌재결정례"}
DELAY = 3


def search(oc, target, query, page):
    params = {"OC": oc, "target": target, "type": "XML",
              "query": query, "display": 100, "page": page}
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "imrdata-research-crawler"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return ET.fromstring(r.read())


def rows(root, target):
    tag = "prec" if target == "prec" else "Detc"
    for item in root.iter():
        if item.tag.lower() != tag.lower():
            continue
        get = lambda *names: next((item.findtext(n) for n in names if item.findtext(n)), "")
        if target == "prec":
            yield {"court": get("법원명"), "case_no": get("사건번호"),
                   "date": get("선고일자"), "title": get("사건명"),
                   "id": get("판례일련번호"), "link": get("판례상세링크")}
        else:
            yield {"court": "헌법재판소", "case_no": get("사건번호"),
                   "date": get("종국일자"), "title": get("사건명"),
                   "id": get("헌재결정례일련번호"), "link": get("헌재결정례상세링크")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--oc", default=os.environ.get("LAWGO_OC"))
    ap.add_argument("--out", default=os.path.join(HERE, "..", "tables", "candidates.csv"))
    a = ap.parse_args()
    if not a.oc:
        sys.exit("Give the OC value with --oc or LAWGO_OC.")
    kw = json.load(open(os.path.join(HERE, "..", "keywords.json"), encoding="utf-8"))["KR"]
    found = {}
    for target in TARGETS:
        for term in kw["migration"]:
            page = 1
            while True:
                root = search(a.oc, target, term, page)
                batch = list(rows(root, target))
                for r in batch:
                    key = (target, r["id"] or r["case_no"])
                    found.setdefault(key, dict(r, target=target, terms=set()))["terms"].add(term)
                print(f"{TARGETS[target]} {term} p{page}: {len(batch)}", file=sys.stderr)
                time.sleep(DELAY)
                if len(batch) < 100:
                    break
                page += 1
    today = datetime.date.today().isoformat()
    farm = kw["farm"]
    with open(a.out, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for r in found.values():
            link = r["link"]
            if link.startswith("/"):
                link = "https://www.law.go.kr" + link
            w.writerow(["KR", "law.go.kr Open API", r["court"], r["case_no"], r["date"],
                        r["title"], link, "ko", ";".join(sorted(r["terms"])),
                        ";".join(t for t in farm if t in r["title"]), today])
    print(f"{len(found)} cases written to {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
