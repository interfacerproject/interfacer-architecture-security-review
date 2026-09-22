> **English edition.** [Italian version](../it/17-team-discussion.md) · Technical terms and commit-pinned evidence are shared across both editions.

# 17 · Technical discussion with the team

## Objective of the meeting

Don't get buy-in to a predefined solution, but agree **what guarantees to offer, who has the authoritative data, and what risk to contain first**. Read first summary, F01–F05 and confidential report in controlled channel.

## Proposed agenda · 90 minutes

| Minutes | Theme | Required outcome |
|---|---|---|
| 0–15 | Commit truly deployed, ingress and consumer | Map fixes, DevOps owner |
| 15–30 | Resource/event/DPP/feedback traces | Agreement on facts and conditions, not on preferences |
| 30–45 | Controller, membership, ambiguous history | Interim rule and migration manager |
| 45–60 | Authority/PEP/revocation/faults | Choose trade-off Q01/Q06/Q11/Q12 |
| 60–75 | DPP sections and Medusa seller | Boundaries between edit, repair, publish, sell |
| 75–90 | Milestones and tests | First scope, acceptance gate and release coordination |

## Cases to be discussed concretely

**Fablab and machine:** Alice creates a machine for a fablab, Bob looks after it, Carla has to use it. Who can correct specifications, authorize an ON command, transfer custody, and sell a derivative kit? Do not use a single "owner" field for four questions.

**Open design and independent seller:** Bob contributes to Alice's design, then sells a legally built product. You can create your own listing, but not change Alice's payout or DPP manufacturer. What claims can you make about the manufacturer?

**Repair:** An external operator attaches a repair event to an exemplar. Do you need to see the customer's contact details? Can you collect a certificate? How do you rectify your own erroneous event without rewriting history?

**Simultaneous Revoke:** Alice revokes Bob while DPP is completing an already authorized change. Does the UI say "revoked" on grant commit or after drain? How much downtime do we accept if Zenflows is unavailable?

**Ambiguous History:** primaryAccountable is one person created by import/email, custodian is another, and contributor claims control. Who decides and what data remains editable during the dispute?

## Roles to involve

Maintainer Zenflows (model and transactions), DPP (workflow/documents/storage), GUI/SDK (compatibility and onboarding), DevOps (deployment/secrets/HA), product manager/legal (privacy, seller, certification), QA/security (negatives and fault injection). Assign real people in the meeting, don't assume availability.

## Decision log to be produced after the discussion

For each ADR: accepted/rejected/deferred outcome, motivation, alternatives considered, owner, review deadline, additional evidence and acceptance test. This document does not automatically update ADRs to ACCEPTED. Plan the work in the repository tracker chosen by the team; This roadmap does not create issues or modify application repositories.

## Reasonable objections and provisional responses

- «An external Authz service is cleaner»: it can be; demonstrate data, consistency and operational costs before imposing it.
- «Everything is public»: public does not authorize writes and does not automatically include emails, drafts or orders.
- «The signature is sufficient»: proves the key, not the right to the object; compare F02/F04.
- «Basta primaryAccountable»: does not cover delegation, org, repair, seller and historical import.
- «Block DPP interrupts work»: maintain reading and a controlled channel; don't call remediation just hide the editor.
- «Immediate revocation is a given»: a precise definition and a concurrency test are needed between different DBs.

## Information to request without secrets

Image/commit digest, ingress and firewall topology, inventory of variables **by name and consumer**, volumes/latency/SLO, summary examples of historical records, current publication policy, organizational flows, Medusa/PSP planning, meaning of wallet points and active physical services. No one should paste credentials, seeds or production dumps into chat/issue.
