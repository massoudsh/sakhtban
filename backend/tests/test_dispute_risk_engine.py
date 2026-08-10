from app.models.decision import AmbiguityType, Decision, DecisionStatus
from app.services.dispute_risk_engine import evaluate_decision


def test_flags_missing_financial_impact():
    decision = Decision(
        statement="مقرر شد که محدوده‌ی کار افزایش یابد.",
        status=DecisionStatus.APPROVED,
        responsible_party="مهندس رضایی",
        financial_impact=None,
    )
    flags = evaluate_decision(decision)
    types = {f.ambiguity_type for f in flags}
    assert AmbiguityType.MISSING_FINANCIAL_IMPACT in types


def test_flags_missing_responsible_party():
    decision = Decision(statement="جلسه برگزار شد.", status=DecisionStatus.APPROVED, responsible_party=None)
    flags = evaluate_decision(decision)
    types = {f.ambiguity_type for f in flags}
    assert AmbiguityType.MISSING_RESPONSIBLE_PARTY in types


def test_no_flags_for_clean_decision():
    decision = Decision(
        statement="کار تمام شد.",
        status=DecisionStatus.APPROVED,
        responsible_party="مهندس رضایی",
        financial_impact=0,
    )
    assert evaluate_decision(decision) == []
