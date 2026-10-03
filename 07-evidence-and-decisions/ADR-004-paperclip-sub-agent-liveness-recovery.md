---
status: proposed
builds-on: [ADR-001]
---

# Paperclip-owned sub-agent liveness and recovery

## Decision

Treat issue status and execution liveness as separate state. An `in_progress` issue is actionable only while it has a current run lease owned by a specific issue/run/agent tuple. The control plane, not the LLM, owns lease expiry and recovery scheduling.

## Lease protocol

At run start, atomically create or renew a lease containing `issue_id`, `run_id`, `agent_id`, `generation`, `started_at`, `last_heartbeat_at`, `expires_at`, and `attempt`. The run renews it at a fixed interval (recommended 30 s) with a bounded expiry (recommended 2 min; make these configuration, not constants). Heartbeat writes are conditional on the same generation, so a late old run cannot revive a replacement run. Run completion and lease release are idempotent on `(issue_id, generation)`.

The scheduler must distinguish:

* `live`: lease unexpired and run adapter reports the run as active or waiting on a supported continuation path;
* `grace`: lease expired, but within one expiry interval, with no recovery launch yet;
* `stale`: lease expired beyond grace or the adapter reports terminal/lost execution;
* `finalizing`: a recovery/finalization attempt owns the generation transition.

An issue may remain `in_progress` during `live` and `grace`; it must not remain indefinitely `in_progress` once `stale`.

## Detection and escalation

Run a watchdog at least once per lease interval. On expiry, re-read the lease and adapter state transactionally (or with compare-and-swap); do not infer liveness from comments, artifacts, process existence, or issue status alone.

After grace expires, mark the lease stale and enqueue exactly one recovery action keyed by `issue_id + generation + recovery_kind`. Recovery first attempts idempotent finalization: inspect the worktree/control-plane state, apply the required handoff/status update if the deliverable is complete, and record the observed run as lost. If finalization cannot determine disposition, create one CEO escalation/recovery run with the same issue and a new generation. The CEO run must receive the stale run metadata, last heartbeat, recent control-plane events, changed files, and any failed write responses.

Use bounded retries: at most two automatic finalization attempts and one CEO/recovery launch per stale generation, with exponential delays (for example 30 s and 2 min). A retry must be safe after timeout because all writes use idempotency keys and conditional generation checks. A new heartbeat from the old generation is rejected and audited rather than changing state.

## Audit and safeguards

Persist lease transitions and recovery attempts as append-only events: acquisition, renewal, expiry, takeover, finalization result, retry, escalation, and suppression reason. Include actor/run/generation, timestamps, idempotency key, and outcome. Metrics should expose expired leases, recovery latency, duplicate suppression, rejected late heartbeats, and unresolved stale issues.

Do not auto-close or mark work complete solely because a lease expired. Recovery may apply only the normal handoff/status operation, and otherwise must escalate to CEO. Suppress recovery when the issue is paused/cancelled/closed, when a newer generation is live, or when an explicit human review path is pending. Clock skew should use server timestamps. Watchdog outages must be visible and must not mass-expire leases; require two consecutive observations or a healthy scheduler epoch before takeover.

## Acceptance criteria

1. A test can create an `in_progress` issue with an expired lease and show that it is classified stale independently of issue status.
2. A late heartbeat or completion from an old generation cannot alter the newer generation; both outcomes are audited.
3. Duplicate watchdog ticks and request timeouts produce at most one finalization and one escalation per stale generation.
4. Finalization can be replayed safely and leaves the issue in a clear terminal or review state, with the normal handoff comment/status recorded once.
5. Adapter-reported active and supported waiting runs do not trigger recovery, while adapter-reported lost runs do not wait for the full lease timeout.
6. Pause/cancel/close and pending human-review safeguards suppress automatic takeover, and watchdog health is observable.

## Follow-up implementation slices

* Add lease and audit-event persistence plus conditional heartbeat/finalization endpoints.
* Add the watchdog classifier, scheduler-health guard, retry budget, and deduplication key.
* Add adapter integration for active/waiting/lost run states and a CEO recovery-run payload.
* Add fault-injection tests for process death, network timeout after commit, duplicate ticks, stale heartbeats, scheduler outage, and pause/cancel races.

This proposal is a control-plane design based on the LAB-21 failure mode; it is not hardware validation and does not claim implementation exists yet.
