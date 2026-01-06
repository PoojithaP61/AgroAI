# 🧭 MASTER ROADMAP – FROM ZERO TO FINAL-YEAR PROJECT

> **STATUS: FROZEN & LOCKED**  
> This roadmap is the definitive guide. All implementations will map back to specific research papers.

---

## 🔹 PHASE 0 – PROJECT FREEZE (VERY IMPORTANT)

### What We Are Building (Final Definition)

**An Open-Set, Continual, AI-Reasoned Few-Shot Plant Disease Diagnosis and Decision Support System**

### Core Abilities

- ✔ Few-shot disease recognition
- ✔ Open-set (unknown disease detection)
- ✔ Continual learning (no retraining from scratch)
- ✔ Disease evolution awareness
- ✔ Visual novelty heat index
- ✔ Confidence calibration
- ✔ Preventive vs curative intelligence
- ✔ Economic AI coupling (yield loss)
- ✔ Visual symptom attribution
- ✔ AI-generated cause, symptoms, treatment, fertilizer
- ✔ Database + login system

**📌 This is now locked.**

---

## 🧩 PHASE 1 – BASE SYSTEM STRUCTURE (NO ML YET)

### What You Will Do

- Create project folders
- Setup virtual environment
- Install dependencies
- Create database structure
- Basic backend skeleton

### Research Papers Used

- ❌ None yet *(this is system engineering, not ML)*

### 📌 Literature Review Note

*"System architecture and deployment are engineering components."*

---

## 🧠 PHASE 2 – FEW-SHOT DISEASE RECOGNITION (CORE ML)

### What We Implement

- Feature encoder
- Few-shot classification using prototypes
- Supervised contrastive learning loss

### Research Papers Used

1. **Mu et al., 2024** – Frontiers in Plant Science  
   📄 *"Few-shot disease recognition algorithm based on supervised contrastive learning"*  
   → We take: Supervised contrastive loss, Few-shot disease learning idea

2. **Khosla et al., 2020** – NeurIPS  
   📄 *"Supervised Contrastive Learning"*  
   → We take: SupCon loss formula, Embedding normalization

3. **Snell et al., 2017** – Prototypical Networks  
   → We take: Prototype computation, Distance-based classification

### 📌 Literature Review Mapping

*Few-shot learning + supervised contrastive representations + prototype inference*

---

## 🚫 PHASE 3 – OPEN-SET DISEASE RECOGNITION (UNKNOWN HANDLING)

### What We Implement

- Similarity threshold
- Reject unknown disease instead of guessing
- Known vs unknown decision

### Research Papers Used

4. **Meng et al., 2023** – Open-Set Recognition for Plant Species  
   → We take: Distance-based rejection idea

5. **Dong et al., 2024** – Open-set anomaly detection in plant disease  
   → We take: Thresholding on embedding similarity

### 📌 Literature Review Mapping

*Open-set recognition prevents forced misclassification of unseen diseases.*

---

## 🔄 PHASE 4 – CONTINUAL LEARNING (NO RETRAINING)

### What We Implement

- Add new disease by adding prototypes
- Freeze encoder
- No catastrophic forgetting

### Research Papers Used

6. **Zhao et al., 2023** – Agronomy  
   📄 *"Multi-Task Continual Learning for Plant Disease"*  
   → We take: Continual learning motivation, Incremental learning concept

7. **Wang et al., 2024** – Frontiers  
   → We take: Incremental disease addition idea

### 📌 Literature Review Mapping

*Prototype-based continual learning avoids retraining and forgetting.*

---

## 📊 PHASE 5 – DISEASE EVOLUTION AWARENESS

### What We Implement

- Early / mid / late stage detection
- Based on affected area and intensity

### Research Inspiration

8. **Explainable phenotyping papers** (Frontiers AI, 2023–2024)  
   → We take: Lesion coverage analysis, Severity estimation idea

### 📌 Literature Review Mapping

*Disease progression analysis enables timely intervention.*

---

## 🔥 PHASE 6 – VISUAL NOVELTY HEAT INDEX (VERY RARE)

### What We Implement

- Novelty score based on distance from prototypes
- How different is this disease visually

### Research Inspiration

9. **OOD / anomaly detection papers** (Nature Sci Reports, 2024)  
   → We take: Distance-based novelty scoring

### 📌 Literature Review Mapping

*Quantifying visual novelty helps identify emerging diseases.*

---

## 🎯 PHASE 7 – CONFIDENCE CALIBRATION

### What We Implement

- Adjust raw confidence scores
- Prevent overconfidence

### Research Papers Used

10. **Confidence calibration literature** (ML safety papers, 2021–2024)  
    → We take: Calibration motivation, Reliability vs confidence mismatch

### 📌 Literature Review Mapping

*Confidence calibration improves trustworthiness.*

---

## 🚦 PHASE 8 – PREVENTIVE VS CURATIVE INTELLIGENCE

### What We Implement

- Decision logic:
  - Preventive
  - Curative
  - Monitoring only

### Research Inspiration

11. **Agricultural decision support system papers** (2023–2024)  
    → We take: Decision-based action planning

### 📌 Literature Review Mapping

*Decision-centric AI reduces chemical misuse.*

---

## 💰 PHASE 9 – ECONOMIC AI COUPLING (YIELD LOSS)

### What We Implement

- Expected yield loss estimation
- Cost vs benefit reasoning

### Research Inspiration

12. **AI-based agricultural economics papers** (2024–2025)  
    → We take: Yield loss modeling concept

### 📌 Literature Review Mapping

*Integrating economic reasoning enhances real-world applicability.*

---

## 👁️ PHASE 10 – VISUAL SYMPTOM ATTRIBUTION ENGINE

### What We Implement

- Map Grad-CAM regions to symptoms
- Explain why disease was predicted

### Research Papers Used

13. **Selvaraju et al., 2017** – Grad-CAM
14. **Explainable AI in agriculture** (Frontiers, 2023–2025)

### 📌 Literature Review Mapping

*Visual explanation improves interpretability and trust.*

---

## 🤖 PHASE 11 – AI REASONING ENGINE (NO JSON FILES)

### What We Implement

- AI-generated:
  - Cause
  - Symptoms
  - Treatment
  - Fertilizer recommendation
- Context-aware reasoning

### Research Inspiration

15. **Explainable & decision-centric AI systems** (IEEE Access, 2024)

### 📌 Literature Review Mapping

*AI reasoning replaces static rule-based systems.*

---

## 🗄️ PHASE 12 – DATABASE + LOGIN SYSTEM

### What We Implement

- User login
- Disease history storage
- Continual learning data storage

### Research Relevance

*System-level contribution (engineering)*

### 📌 Literature Review Note

*Mentioned as deployment & system design*

---

## 📈 PHASE 13 – EVALUATION & RESULTS

### What We Evaluate

- Accuracy
- Open-set rejection
- Novelty score behavior
- Confidence calibration
- Decision correctness

### Research Mapping

**Compare against:**
- Mu et al., 2024
- Few-shot baselines

---

## 📋 IMPLEMENTATION NOTES

- ✅ Every phase maps to specific research papers
- ✅ Literature review will reference each paper appropriately
- ✅ Methodology follows established academic standards
- ✅ Step-by-step verification before proceeding to next phase

---

**Last Updated:** Roadmap Frozen  
**Status:** Ready for Phase 1 Implementation
