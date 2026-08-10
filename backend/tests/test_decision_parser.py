from app.services.decision_parser import extract_decisions


def test_extracts_decision_with_responsible_party_and_amount():
    text = (
        "در جلسه‌ی امروز موارد زیر بررسی شد. "
        "مقرر شد که تغییر طراحی نما توسط مهندس احمدی پیگیری شود. "
        "هزینه‌ی اضافی ۵۰,۰۰۰,۰۰۰ ریال برآورد شد."
    )
    parsed = extract_decisions(text)
    assert len(parsed.decisions) >= 1
    first = parsed.decisions[0]
    assert "مهندس احمدی" in (first.responsible_party or "")
