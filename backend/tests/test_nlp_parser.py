from app.models.report import ReportEntityType
from app.services.nlp_parser import extract_entities


def test_extracts_location_quantity_and_delay():
    text = "امروز در طبقه ۳ بتن‌ریزی سقف انجام شد. ۵۰ متر مکعب بتن مصرف شد. به‌دلیل بارش باران کار بعدازظهر متوقف شد."
    parsed = extract_entities(text)
    types = {e.entity_type for e in parsed.entities}

    assert ReportEntityType.LOCATION in types
    assert ReportEntityType.QUANTITY in types
    assert ReportEntityType.DELAY_REASON in types

    qty_entities = [e for e in parsed.entities if e.entity_type == ReportEntityType.QUANTITY]
    assert any(e.quantity == 50.0 and e.unit and "مکعب" in e.unit for e in qty_entities)
