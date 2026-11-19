"""Proposal: turn the matching protocol into a ready-to-approve solution for this case.

Only actions on the fixed executable list can ever run, and each one is mocked (it records that it happened).
Anything in the protocol that is not on that list becomes an officer task, shown but never executed.
"""
import re

import mock_data as md

from . import protocols

# The executable whitelist. Kept here so the proposal, the backend and the dashboard agree.
ACTIONS = ("ACTIVATE_SAFEBLOCK", "BLOCK_CARD", "RAISE_DISPUTE", "DRAFT_PAYMENT_RECALL", "DRAFT_PAYMENT_TRACE",
           "DRAFT_SCAM_REPORT", "DRAFT_HARDSHIP_NOTES", "DRAFT_COMPLAINT_RESPONSE", "ORDER_REPLACEMENT_CARD",
           "BOOK_CALLBACK", "SEND_CUSTOMER_UPDATE", "SEND_GUIDE_LINK", "REFER_SPECIALIST_TEAM")
ACTION_TEXT = {
    "ACTIVATE_SAFEBLOCK": "Turn on SafeBlock", "BLOCK_CARD": "Lock the card",
    "RAISE_DISPUTE": "Raise a dispute", "DRAFT_PAYMENT_RECALL": "Draft a payment recall (draft only, no money moved)",
    "DRAFT_PAYMENT_TRACE": "Draft a payment trace (draft only)", "DRAFT_SCAM_REPORT": "Draft a scam report",
    "DRAFT_HARDSHIP_NOTES": "Draft hardship notes for the specialist",
    "DRAFT_COMPLAINT_RESPONSE": "Draft a complaint response", "ORDER_REPLACEMENT_CARD": "Prepare a replacement card",
    "BOOK_CALLBACK": "Book a callback", "SEND_CUSTOMER_UPDATE": "Send the customer an update",
    "SEND_GUIDE_LINK": "Send the customer a how-to link", "REFER_SPECIALIST_TEAM": "Refer to the specialist team",
}
CUSTOMER_CHOSEN_STATE = {"ACTIVATE_SAFEBLOCK": "safeblock_on", "BLOCK_CARD": "card_blocked"}
NEEDS_TX = ("RAISE_DISPUTE", "DRAFT_PAYMENT_RECALL", "DRAFT_PAYMENT_TRACE")
_NAME = re.compile(r"\b([A-Z][A-Z_]{3,}[A-Z])\b")


def parse_ai_may(item):
    """'prepare DRAFT_PAYMENT_RECALL' -> ('DRAFT_PAYMENT_RECALL', note). Returns (None, item) if no action name."""
    m = _NAME.search(item)
    if not m:
        return None, item
    note = item.replace(m.group(1), "").strip(" ()")
    return m.group(1), note


def _nice(day):
    """'2026-11-19' -> '19 Nov 2026'."""
    return md.parse_ts(day + "T00:00:00Z").strftime("%d %b %Y").lstrip("0") if day else None


def _fill(template, values):
    """Fill {placeholders} we know; leave the rest visible as [placeholder] for the officer to complete."""
    missing = []

    def sub(m):
        key = m.group(1)
        if values.get(key):
            return str(values[key])
        missing.append(key)
        return f"[{key}]"

    return re.sub(r"\{(\w+)\}", sub, template), missing


def draft(card, protocol, priority, ev):
    """Build the proposed solution. Deterministic: the same card and protocol give the same proposal."""
    outgoing = [t for t in ev["own"] if t["amount"] < 0]
    card_tx = [t for t in outgoing if t["type"] == "card"]
    reported = {"ACTIVATE_SAFEBLOCK": card.get("safeblock_reported"), "BLOCK_CARD": card.get("card_locked_reported")}
    actions, tasks, already = [], [], []
    for item in protocol.get("ai_may", []):
        name, note = parse_ai_may(item)
        if name not in ACTIONS:
            tasks.append(f"Officer: {item}")
            continue
        customer_chosen = "customer-chosen" in item
        if name in CUSTOMER_CHOSEN_STATE:
            if ev["account"].get(CUSTOMER_CHOSEN_STATE[name]):
                already.append(f"{ACTION_TEXT[name]}: already on for this account")
                continue
            if reported[name]:
                already.append(f"{ACTION_TEXT[name]}: done by the customer during the conversation (reported by "
                               f"Clario)")
                continue
        base = {"action": name, "label": ACTION_TEXT[name], "customer_chosen": customer_chosen, "note": note}
        if name == "DRAFT_PAYMENT_RECALL":
            if not outgoing:
                tasks.append("Officer: identify the payment to recall (no linked outgoing payment on the card)")
            for t in outgoing:  # one recall per linked outgoing payment
                actions.append({**base, "params": {"transaction_id": t["id"]}})
            continue
        if name in ("RAISE_DISPUTE", "DRAFT_PAYMENT_TRACE"):
            pick = (card_tx or outgoing) if name == "RAISE_DISPUTE" else outgoing
            if not pick:
                tasks.append(f"Officer: {ACTION_TEXT[name].lower()} needs a linked transaction")
                continue
            actions.append({**base, "params": {"transaction_id": pick[0]["id"]}})
            continue
        if name == "ORDER_REPLACEMENT_CARD" and card["issue_type"] == "CARD_DELIVERY":
            # protocol step: only replace a card that is past its expected date
            due = md.get_card_delivery_status(card["customer_id"]) or {}
            if due.get("expected") and ev["as_of"] <= md.parse_ts(due["expected"] + "T23:59:59Z"):
                tasks.append(f"Not yet: the card is still due by {_nice(due['expected'])}. Prepare a replacement "
                             f"only once it is past that date")
                continue
        params = {"when": "tomorrow 10:00"} if name == "BOOK_CALLBACK" else {}
        actions.append({**base, "params": params})
    tasks += [f"Officer must: {x}" for x in protocol.get("officer_must", [])]

    srcs = protocols.sources_for(protocol)
    delivery = md.get_card_delivery_status(card["customer_id"]) or {}
    values = {"case_id": card["case_id"], "dispatched": _nice(delivery.get("dispatched")),
              "expected": _nice(delivery.get("expected")),
              "trace_or_recall": "payment trace" if card["issue_type"] == "MONEY_MISSING" else None,
              "steps_link": srcs[0]["url"] if srcs else None, "source_url": srcs[0]["url"] if srcs else None}
    message, missing = _fill(protocol.get("customer_message", ""), values)

    executor = priority["executor"]
    names = ", ".join(a["label"].lower() for a in actions) or "no automatic actions"
    explanation = (f"Following protocol {protocol['issue_type']} v{protocol['version']}: {protocol['title']}. "
                   f"Proposed: {names}.")
    return {
        "explanation": explanation,
        "actions": actions,
        "already_done": already,
        "officer_tasks": tasks,
        "protocol": {"issue_type": protocol["issue_type"], "title": protocol["title"],
                     "version": protocol["version"], "harm_category": protocol["harm_category"],
                     "min_band": protocol.get("min_band"), "sources": srcs,
                     "change_log": protocol.get("change_log", [])},
        "steps": protocol.get("steps", []),
        "required_checks": protocol.get("required_checks", []),
        "protect_first": protocol.get("protect_first"),
        "timeframes": protocol.get("timeframes", []),
        "customer_message": message,
        "customer_message_missing": missing,
        "executor": executor,
        "drafted_by": "Prorio",
    }
