## Changes made
- Tightened circular-reference section to match actual traversal behavior and recorded tuple semantics.

## Why it was wrong
- `src/docsync/commands/cascade.py::_cascade` records revisits during BFS and stores `(doc, referencing_doc)` tuples; the previous wording over-generalized detection semantics.
