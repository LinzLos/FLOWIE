# Expected finding — Case 005

FLOWIE should surface a **count-parity violation** between the sidebar and the
content:

> The sidebar lists **6** entries but the page contains **5** sections. The
> **"Webhooks"** link targets `#webhooks`, which does not exist — clicking it
> silently does nothing (or scrolls nowhere). The number of entries on the
> control side must match the number of reachable targets. A reader who clicks
> "Webhooks" either assumes the docs are broken or wrongly concludes the API has
> no webhooks documentation. Either restore the Webhooks section or remove the
> sidebar entry.

## Must include (to score "caught")

- States the count mismatch (6 nav entries vs 5 sections) **and** identifies
  "Webhooks" as the specific dangling entry with no target.
- States the user-facing consequence (silent no-op click; content assumed
  missing or broken).

## Score "partial" if

- It notices the dead `#webhooks` anchor but doesn't frame it as control/target
  count parity — or says "verify all anchors resolve" generically without
  naming which one doesn't.

## Score "missed" if

- It reviews the page without ever matching sidebar entries against the
  sections that exist.

## Invariant this case defends

```
count-parity: entries on the control side === reachable targets; 6 nav items ⇒ 6 sections
```

Designed trap (not a field miss): the input is code; the missing section is
never mentioned — it must be found by counting both sides of the coupling.
