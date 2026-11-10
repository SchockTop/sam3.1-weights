"""Join the *.partNNN files of this repo into the model files and verify them.

    python join.py                  # everything
    python join.py --only <folder>  # one variant folder
    python join.py --delete-parts   # remove the parts of each file once it verified

Works offline, standard library only. The parts must lie where git put them.
"""
import argparse, hashlib, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAN = json.loads((HERE / "manifest.json").read_text())


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="variant folder to join")
    ap.add_argument("--delete-parts", action="store_true")
    a = ap.parse_args()
    bad = 0
    for e in MAN["files"]:
        if a.only and not e["path"].startswith(a.only.strip("/\\") + "/"):
            continue
        dst = HERE / e["path"]
        parts = [HERE / p for p in e["parts"]]
        if dst.exists() and dst.stat().st_size == e["size"] and sha256(dst) == e["sha256"]:
            print("ok (already joined):", e["path"])
        else:
            missing = [p.name for p in parts if not p.exists()]
            if missing:
                print("MISSING PARTS for %s: %s" % (e["path"], ", ".join(missing))); bad += 1
                continue
            tmp = dst.with_name(dst.name + ".joining")
            h = hashlib.sha256()
            with open(tmp, "wb") as out:
                for p in parts:
                    with open(p, "rb") as f:
                        for b in iter(lambda: f.read(1 << 22), b""):
                            out.write(b); h.update(b)
            if h.hexdigest() != e["sha256"]:
                print("SHA256 MISMATCH:", e["path"]); tmp.unlink(); bad += 1
                continue
            tmp.replace(dst)
            print("ok:", e["path"])
        if a.delete_parts:
            for p in parts:
                if p.exists():
                    p.unlink()
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
