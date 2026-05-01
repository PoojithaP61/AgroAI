import pytest
from backend.ml.agro_intelligence import assess_disease_intelligence

def test_assess_disease_intelligence_late_stage():
    # High confidence > 0.9 and high cam coverage > 0.6
    stage, action, yield_loss = assess_disease_intelligence(0.95, 0.7)
    assert stage == "Late"
    assert action == "Immediate Treatment"
    assert yield_loss == "35–60%"

def test_assess_disease_intelligence_mid_stage():
    # Confidence > 0.75 but cam coverage not high enough or confidence just > 0.75
    stage, action, yield_loss = assess_disease_intelligence(0.85, 0.5)
    assert stage == "Mid"
    assert action == "Curative Treatment"
    assert yield_loss == "15–30%"

def test_assess_disease_intelligence_early_stage():
    # Low confidence < 0.75
    stage, action, yield_loss = assess_disease_intelligence(0.60, 0.7)
    assert stage == "Early"
    assert action == "Preventive Monitoring"
    assert yield_loss == "5–10%"

def test_assess_disease_intelligence_edge_cases():
    # Exactly on boundary 0.9 confidence and 0.6 coverage
    stage, action, yield_loss = assess_disease_intelligence(0.9, 0.6)
    assert stage == "Mid"  # Because condition is > 0.9
    
    stage, action, yield_loss = assess_disease_intelligence(0.75, 0.8)
    assert stage == "Early" # Because condition is > 0.75
