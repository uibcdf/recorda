# Declared reference checks

Tracked by uibcdf/recorda#12 and uibcdf/recorda-lab#9. These provisional functions
inspect local availability and bytes; they do not authenticate ownership, certify
scientific identity, validate a complete dependency closure or establish replay.
Runtime capture, ScientificRecord inspection and the journal schema are unchanged.

```python
files = recorda.LocalFileResolver(
    "retained/native",
    {input_reference: "input.json", result_reference: "result.json"},
    digest_algorithm="sha256",
)
record = recorda.inspect("analysis.jsonl")
report = recorda.check_references(record, resolver=files)
checked = recorda.check_reference(input_reference, resolver=files)
```

The caller supplies the local root and an exact Reference-to-relative-path index.
Owner, identifier, revision and digest all participate in lookup; journal identities
are never interpreted as paths or URLs. Locations are kept outside the journal and
outside reports. The resolver copies its index and checks resolved containment
on each lookup. It is a trusted local locator, not an adversarial filesystem sandbox.

## Observation states

| Status | Meaning |
| --- | --- |
| matched | Local file bytes match the declared SHA256 digest. |
| mismatched | Readable file bytes differ from the declared digest. |
| missing | The indexed file cannot be found. |
| unresolved | No supplied local index entry matches the complete reference. |
| available_unverified | A regular local file is available, but the reference has no digest. |
| unsupported_digest | The algorithm is undeclared or the digest format is unsupported. |
| too_large | The file exceeds the requested byte-check bound. |
| not_a_file | The location is not a regular file. |
| outside_root | The indexed location resolves outside its declared root. |
| unreadable | The local location cannot be read or resolved. |
| unstable | File metadata changed while its bytes were checked. |
| invalid_reference | The supplied value is not a bounded Reference representation. |

The resolver must explicitly declare digest_algorithm="sha256" for hash checking;
its default None checks availability without assuming an algorithm. The supported
format is 64 hexadecimal characters. No hash is inferred from an identifier prefix
or string length. Other digest algorithms remain future work. A supported hash
match compares the receipt to observed bytes; either may still be unauthenticated.

Hash reads are streamed and bounded by max_bytes (default 64 MiB), with one
additional byte permitted to detect growth beyond the limit. Nonregular files
are rejected and FIFO locations are opened without waiting. An oversized or unsupported
reference is not reported as matching. Reports contain safe declared references,
fixed states, algorithm and bytes_checked, without paths, file contents, computed
content digests or arbitrary I/O error text. No file is changed by checking.

## Record-level scope

check_references accepts an inspected ScientificRecord. It reports declared top-level
input, parameter, output and native exception-reference occurrences with operation
identity and group/field. Repeated references share one byte check within a report;
each new report checks again, so later removal or alteration stays visible.

The report separately exposes explicit value/policy omissions and incomplete operation
ids. Historical failures without exception.reference have reason not_recorded.
Ordinary scalars and unregistered native objects are not searched for hidden references.
Native manifest traversal, object/version binding and scientific validity stay with
the owning library and its domain inspector. A scalar field that happens to look like
a URI is not opened. Omitting a reference does not make it verified or available.

session_status is the original observed execution outcome. A missing output file
can coexist with a succeeded operation; checking does not change the record or
manufacture a successful completion for interrupted work. Report data is independent
of the inspected snapshot. Existing journals remain readable; no authenticity or
power-loss durability guarantee follows from a readable journal prefix.

## Controlled laboratory

The sixth notebook uses an unchanged population-statistics result (mean 2.5,
variance 1.25). It inspects intact files, removes an input, modifies output bytes,
restores both, and distinguishes references without digests, unknown references,
policy omissions and actual process interruption. The SciPy and Sabueso inspectors
reuse the common local checker while keeping their native semantic validations.
A producer-free interpreter can inspect saved journals and the explicit index with
Recorda and stdlib only. See evidence/reference_checks_local.json for actual sources,
commands, notebook execution and scope. This is source work after immutable 0.2.0.
