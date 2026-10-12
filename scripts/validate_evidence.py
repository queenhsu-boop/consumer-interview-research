#!/usr/bin/env python3
"""Validate exact quote provenance against a supplied, versioned source snapshot."""
import argparse
import hashlib
import json
import sys
from pathlib import Path


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def validate(source_bytes, ledger_bytes):
    source = json.loads(source_bytes.decode("utf-8"), object_pairs_hook=unique_object)
    ledger = json.loads(ledger_bytes.decode("utf-8"), object_pairs_hook=unique_object)
    require(isinstance(source, dict) and isinstance(ledger, dict), "expected JSON objects")
    turns = source.get("turns")
    quotes = ledger.get("quotes")
    require(isinstance(turns, list) and bool(turns), "turns must be a nonempty list")
    require(isinstance(quotes, list) and bool(quotes), "quotes must be a nonempty list")
    digest = ledger.get("source_sha256")
    require(isinstance(digest, str) and len(digest) == 64
            and all(c in "0123456789abcdef" for c in digest), "invalid source_sha256")
    by_id = {}
    for turn in turns:
        require(isinstance(turn, dict), "turn must be an object")
        for field in ("id", "participant_id", "locator"):
            require(nonempty(turn.get(field)), "turn missing " + field)
        require(turn.get("speaker") in ("participant", "interviewer", "observer", "other"),
                "invalid speaker")
        require(type(turn.get("verbatim")) is bool, "verbatim must be a boolean")
        require(isinstance(turn.get("text"), str), "turn text must be a string")
        require(turn["id"] not in by_id, "duplicate turn id")
        by_id[turn["id"]] = turn

    errors = []
    if hashlib.sha256(source_bytes).hexdigest() != digest:
        errors.append({"id": "source", "errors": ["source_hash_mismatch"]})
    seen = set()
    for quote in quotes:
        require(isinstance(quote, dict), "quote must be an object")
        for field in ("id", "participant_id", "turn_id", "quote"):
            require(nonempty(quote.get(field)), "quote missing " + field)
        require(quote["id"] not in seen, "duplicate quote id")
        seen.add(quote["id"])
        require(type(quote.get("start")) is int and type(quote.get("end")) is int,
                "quote offsets must be integers")
        issues = []
        turn = by_id.get(quote["turn_id"])
        if turn is None:
            issues.append("unknown_turn")
        else:
            if turn["participant_id"] != quote["participant_id"]:
                issues.append("participant_mismatch")
            if turn["speaker"] != "participant":
                issues.append("not_participant_speech")
            if not turn["verbatim"]:
                issues.append("source_not_verbatim")
            start, end = quote["start"], quote["end"]
            if not 0 <= start < end <= len(turn["text"]):
                issues.append("invalid_range")
            elif turn["text"][start:end] != quote["quote"]:
                issues.append("exact_text_mismatch")
        if issues:
            errors.append({"id": quote["id"], "errors": issues})
    return {
        "status": "failed" if errors else "matched",
        "checked_quotes": len(quotes),
        "errors": errors,
        "scope": "Text provenance only; not source authenticity, context, claim support or report completeness.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.source.read_bytes(), args.evidence.read_bytes())
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"status": "invalid_input", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())

