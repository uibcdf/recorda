# Declared reference checks

Tracked by uibcdf/recorda#12 and uibcdf/recorda-lab#9. These provisional functions
inspect local availability and bytes; they do not authenticate ownership, certify
scientific identity, validate a complete dependency closure or establish replay.
Runtime capture, ScientificRecord inspection and the journal schema are unchanged.

`uibcdf/recorda#20` adopts ArgDigest for local index/checking configuration. Public
signatures stay closed: no arbitrary keyword or public skip route. Registered
value pipelines validate options under metadata-only SMonitor scopes; native core
guards retain filesystem and byte-check invariants through private unwrapping.
Individual reference data stays outside digestion and retains structured
invalid_reference observations. Scientific manifests stay producer-owned.

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

## Configuration contracts and imports

Roots accept strings and os.PathLike objects, including Path, PurePath and custom
str-returning __fspath__ implementations, using native Path conversion. The index
requires an exact dict with exact Reference keys; locations retain their existing
str/Path forms. Algorithm/index/root shapes are validated before path processing;
absolute or parent-traversing locations are refused before root resolution. A
caller-owned path protocol may still raise its native error. The resolver copies
its index; no new index-size limit or arbitrary value coercion is introduced.

The algorithm is an exact "sha256" string or None. Both checking functions require
resolver None or an exact LocalFileResolver, and max_bytes an exact positive int;
booleans and int subclasses are rejected. check_references additionally requires
an exact ScientificRecord. Paths/bytes are processed only after configuration
validation. Fixed native validation errors remain TypeError/ValueError.

Resolver construction and checking calls load the already-required published
ArgDigest/SMonitor closure lazily. Plain import and independent journal inspection
remain provider-free. Missing providers fail at use, with no silent fallback.
The earlier #19 receipt's provider-free reference-call property is historical.
Recorda's safe first-use diagnostic baseline and existing application/project
policy precedence are shared with [ARGUMENT_CONFIGURATION.md](ARGUMENT_CONFIGURATION.md).
Pipeline-only digestion ignores application digester defaults and uses direct
registered rule callables. Metadata-only diagnostics omit private roots, locations,
index identities, record content, native error text and inherited producer context.

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
Configuration is digested once per report; distinct cached references use the
guarded native checker without another ArgDigest invocation. That private checker
still enforces exact resolver identity and byte limits before filesystem access.

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
A producer-free interpreter can inspect saved journals without scientific packages.
Invoking the current local checker additionally requires Recorda's declared provider
closure. The historical stdlib-only laboratory receipt is
evidence/reference_checks_local.json; its source identities and notebook scope are
not rewritten by this adoption. Current argument-contract evidence is retained in
[evidence/reference_arguments_local.json](evidence/reference_arguments_local.json).
Lab's next receiving environments and exact-pair qualification remain in
`uibcdf/recorda-lab#12`. This is source work after immutable 0.2.0.

The new 50 receiving regressions and all 221 source/installed-wheel tests pass
on Python 3.14.7 with published pytest-receptor 1.1.0 (default lane: 209 passes,
12 explicit recovery skips). [CI 37534456487](https://github.com/uibcdf/recorda/actions/runs/37534456487)
passes all 11 jobs at `c6248686815bd405a08955565e4fdc232bcef906`, including
installed-package Linux Python 3.11–3.14/macOS 3.13–3.14 and four recovery lanes,
inspected with published gh-run-receptor 1.2.0. The resolved analysis is
[archive/reference_arguments.md](archive/reference_arguments.md).
