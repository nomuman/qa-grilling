# Example: account profile form review

## Input

```text
Users can edit display name and bio.
Display name is required and limited to 30 characters.
Bio is optional and limited to 160 characters.
Save button writes the profile to the server.
```

## Behavior model

States:

```text
viewing
→ editing
→ saving
→ saved
   or
→ failed
```

Important questions include whether local edits can be lost, whether repeated saves are safe, and whether character-count semantics are consistent across client and server.

## Findings

### P2 — Character-count semantics may differ

**Type:** AMBIGUITY if unspecified

“30 characters” can mean code units, Unicode scalar values, or grapheme clusters. Emoji and combining sequences can expose client/server disagreement.

If the existing product already has a standard counting rule, discover and reuse it rather than grilling the user.

### P2 — Double submit

**Type:** TEST_OBLIGATION if the implementation disables/coalesces duplicate saves; otherwise MISSING_RULE

Rapidly pressing Save must not produce conflicting writes or misleading success feedback.

### P2 — Navigation during save

**Type:** MISSING_RULE

What happens if the user leaves the screen while the save request is pending? The product should avoid a state where the UI implies edits were discarded while the server actually committed them.

### P2 — Server-side validation

**Type:** TEST_OBLIGATION

Client-side limits do not replace server validation.

### P2 — Accessibility of validation errors

**Type:** TEST_OBLIGATION

Errors should be associated with the relevant field, reachable by screen reader/keyboard users, and not communicated by color alone.

## Boundary obligations

For a required max-30 display name, useful representatives include:

- empty;
- 1;
- 29;
- 30;
- 31;
- whitespace-only if relevant;
- Unicode/emoji examples if supported.

Do not ask the user about each boundary. These are test obligations unless a semantic rule is actually missing.
