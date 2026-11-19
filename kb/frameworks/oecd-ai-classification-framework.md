---
title: OECD Framework for the Classification of AI Systems
date: 2026-11-19
updated: 2026-11-19
tags: [framework, oecd, risk-assessment, inventory, ai-register]
aliases: [OECD classification framework, OECD five dimensions, classifying AI systems, AI inventory template]
type: framework
authority: official-guidance
jurisdiction: international
as_of: 2026-11-19
sources: [OECD Digital Economy Papers No. 323 (2022), IAPP AIGP training M1]
---

# OECD Framework for the Classification of AI Systems

**In one sentence:** an [OECD](../orgs/oecd.md) tool for describing an AI system in its real-world context along five dimensions, each with concrete criteria, so organizations and policymakers can compare systems, build inventories and see where risks and policy issues sit.

## Key points
- **Five dimensions**, with People & Planet at the centre. Each dimension has a set of criteria phrased as questions. [Report p. 18, Table 2](../../_library/text/oecd-classification-framework/01-overview.md#Page%2018)
  1. **People & Planet:** user competency; who is impacted (consumers, workers, agencies); whether people can opt out or challenge the output; impact on human rights, well-being and the environment; potential to displace human work. [§ People & Planet](../../_library/text/oecd-classification-framework/02-people-and-planet.md)
  2. **Economic Context:** sector; business function; for-profit, non-profit or public service; whether it supports critical functions or essential services; breadth of deployment (pilot to widespread); technical maturity. [§ Economic Context](../../_library/text/oecd-classification-framework/03-economic-context.md)
  3. **Data & Input:** collected by humans or sensors; provenance (expert, provided, observed, synthetic, derived); static or dynamic; proprietary, public or personal; anonymised or pseudonymised; structure, format, scale; quality and representativeness. [§ Data & Input](../../_library/text/oecd-classification-framework/04-data-and-input.md)
  4. **AI Model:** how much is known about the model; symbolic, statistical or hybrid; open-source or proprietary, own or third-party; generative or discriminative; one model or several; how it learns (rules, supervised, reinforcement); whether it keeps evolving in the field; central or federated training; deterministic or probabilistic use; transparency and explainability. [§ AI Model](../../_library/text/oecd-classification-framework/05-ai-model.md)
  5. **Task & Output:** what tasks it performs (recognition, event detection, forecasting…); whether it combines tasks into composite systems; **action autonomy** and the role humans play; core application area (language, vision, optimisation, robotics); whether evaluation methods exist. [§ Task & Output](../../_library/text/oecd-classification-framework/06-task-and-output.md)
- **Context matters:** the same model is classified differently "in the lab" and "in the field", so the framework describes an applied system in a specific deployment. [Report p. 22](../../_library/text/oecd-classification-framework/01-overview.md#Page%2022)
- Every dimension is tied to the OECD AI Principles it affects (e.g. user competency → accountability, transparency, safety). [Report p. 26](../../_library/text/oecd-classification-framework/02-people-and-planet.md#Page%2026)
- The report includes sample checklists for impact on human rights and on well-being (Tables 3–4) and four worked examples. [pp. 27–28](../../_library/text/oecd-classification-framework/02-people-and-planet.md#Page%2027) · [Examples](../../_library/text/oecd-classification-framework/07-applying-the-framework.md)

## In practice
- **AI inventory or register:** use the criteria from Table 2 as the columns, so every system is described the same way, and add owner, vendor and legal classification.
- **Risk triage:** People & Planet and Economic Context show who could be harmed and how much is at stake; Data & Input and AI Model show where technical and data-protection risks sit; Task & Output shows autonomy and human oversight.
- **Impact assessments:** the human rights and well-being checklists (Tables 3–4) are a good starting set of questions for a fundamental rights impact assessment.
- It describes systems; it does not decide legal obligations. Pair it with the legal classification under the applicable law.

## Connected
- [What counts as an "AI system"](../concepts/what-is-an-ai-system.md): confirm it is an AI system before classifying it.
- EU AI Act [Annex III](../../_library/text/eu-ai-act/annex-03-high-risk-ai-systems-referred-to-in-article-6-2.md): legal list of high-risk use areas. Sector and impacted-stakeholder answers point straight to it.
- EU AI Act [Art. 27 fundamental rights impact assessment](../../_library/text/eu-ai-act/art-027-fundamental-rights-impact-assessment-for-high-risk-ai-system.md): the human rights checklist (Table 3) feeds directly into it.
- EU AI Act [Art. 14 human oversight](../../_library/text/eu-ai-act/art-014-human-oversight.md): the action-autonomy criterion maps to it.
- Personal data and identifiability criteria → GDPR obligations (note to come in `kb/laws/`).
- [NIST AI RMF](../orgs/nist.md): its Map function covers the same context-setting work.

## Sources
- OECD (2022), *OECD Framework for the Classification of AI Systems*, OECD Digital Economy Papers No. 323: [reading copy](../../_library/text/oecd-classification-framework/00-index.md) · [PDF](../../_library/originals/oecd-framework.pdf) · [doi.org/10.1787/cb6d9eca-en](https://doi.org/10.1787/cb6d9eca-en) · [two-page overview](https://wp.oecd.ai/app/uploads/2022/02/Classification-2-pager-1.pdf)
- IAPP AIGP training, Module 1 › Core concepts of AI (training material)

Related: [OECD](../orgs/oecd.md), [source card](../sources/oecd-classification-framework.md)
