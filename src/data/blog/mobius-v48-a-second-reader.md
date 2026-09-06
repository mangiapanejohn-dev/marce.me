---
title: "MØBIUS V48 — A Second Reader Exists, and Its Blind Spots Are Disjoint"
description: "V47 said the runtime has one witness per fact and no second source to contradict it. This version goes looking for one. It is there, it is not the thing you would reach for, and finding it makes the next step less attractive rather than more."
pubDatetime: 2026-09-06T12:58:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
series: "MØBIUS"
---

V47 closed by locating the obstacle to independent evidence: not a missing emitter, but the absence
of a **second source** — another reader with an opinion about the same fact. It named the nearest
real one: `repo` and `filesystem` both see a working tree.

This version goes and measures whether that is true. It is, but not in the shape the sentence
implies.

### The obvious second witness does not exist

The natural move is to compare per-path content digests: the filesystem provider reports
`{path, digest}`, so ask the repository provider for the same thing about the same path.

It does not report one. `PathChange` carries `{path, index, worktree, renamedFrom, conflicted}`.
The repository knows **that** a path changed, never **to what**. The two providers never state the
same fact at the same granularity, so the corroboration you would design on a whiteboard is not
available at any price.

What the repository does carry is two tokens over the whole tree — `diffDigest` over tracked
content, and `changeSetDigest` over which paths are in which state.

### Three witnesses, and the useful part is where they are blind

Running both providers against one git tree and stepping through four states:

| step | fs digest | `diffDigest` | `changeSetDigest` |
|---|---|---|---|
| baseline | `2c8b08…` | `e3b0c4…` | `6be11…` |
| tracked file edited | `27dd8e…` moved | `06d723…` moved | `1ce41…` moved |
| edited again | `f69369…` moved | `3c7ef7…` moved | `1ce41…` **unchanged** |
| untracked file created | — | `3c7ef7…` **unchanged** | `59e80…` moved |

Row two is the corroboration: a filesystem digest and a repository diff digest, different process,
different algorithm — `stat`-and-hash the bytes versus digest `git diff`'s output — agreeing about
one file. That is the first place in this runtime where a claim has two witnesses rather than one
carried forward.

Rows three and four are why the measurement was worth taking. Each blind spot is documented on its
own; what the table adds is that they are **disjoint**. A second edit of an already-modified file
moves the content token and leaves the status token alone. An untracked file does the reverse.
Neither is derivable from the other — and a test that only edited a tracked file once would have
watched all three move together and concluded they were the same measurement three times.

### What it can actually settle

V47 measured the runtime's one open disagreement: at equal `worldRevision`, the receipt's digest
and the verifying observation's digest differ, and V37 reads that as *the world moved* rather than
*one of the two reads is wrong*. Nothing in the runtime can tell those apart.

`diffDigest` can, for a tracked file. If it also moved, the world moved. If it did not, it did not.
That is the first claim in this project a second source can adjudicate.

It is also worth being precise about what this independence is. Both readers read the same bytes
from the same disk through the same kernel. A corrupted file corrupts both digests identically. The
independence is of **implementation**, not of source — it catches a reader error, not a world error
— and that is pinned as a limit so the corroboration is not read as more than it is.

### Why nothing was built on it

Using this means the runtime taking a `repo.status` observation to adjudicate a filesystem verdict:
a cross-provider read inside the verification path. Three things make that its own version.

It **costs a look** — a second gated, budgeted observation on a path V44 and V45 spent two versions
making cheaper. It **only answers for tracked files**, and the case V37 cares most about is a file
the runtime just created, which is exactly where `diffDigest` is blind: the witness is weakest where
the question is loudest. And it **needs both providers in one run**, so it is a composition change
before it is a runtime one — and composition is where V40 was burned reaching into a plane it had
not considered.

So the honest reading of V48 is that H5 moved from *unreachable* to *reachable and possibly not
worth reaching*. That is progress of a kind the earlier versions in this line would have been
tempted to write up as a feature.

### Two notes from the battery

No production code changed, so the three mutations attack the tokens the pins rest on. All died.
The one worth naming is the second: making `changeSetDigest` content-sensitive collapses the two
witnesses into one, and the whole finding is that they are *different*. The mutation that erases the
finding is caught.

A fourth was unbuildable — filtering untracked paths by the porcelain code (`c.index !== '?'`) is a
type error, because `ChangeKind` is a named union (`'untracked'`) rather than the wire codes it is
parsed from. Fifth unbuildable mutation in this line, same cause every time: writing the mutation
against the shape at the **seam** instead of the shape at the **site**. The compile guard reported
it rather than counting the red run as a kill.

And one test was deliberately left out. V43's rule is *derive the list from what the change touches,
and from what recently pinned it* — but V47 pinned the **filesystem** side and touches no repository
code, so running it here would have measured nothing. The rule cuts both ways: a test included for
its provenance rather than its coverage is padding.
