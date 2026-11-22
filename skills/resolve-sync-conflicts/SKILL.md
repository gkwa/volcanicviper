---
name: resolve-sync-conflicts
description: "Find and resolve the Syncthing conflict files in the Obsidian vault: explain what each conflict was, restore the correct version of each note, commit it, and delete the conflict copies. Use when asked to resolve, fix, check or clean up sync conflicts, syncing conflicts, conflict files, or conflicts in the vault. Dictation often garbles the product name, so also use when the request says sync thing, sink thing, sinking, sink conflicts, or any similar phrase next to the word conflict."
---

## Resolving sync conflicts

Syncthing leaves a conflict copy beside a note when two devices each changed it without having seen the other's change.

It keeps the version with the newer modification time as the live note and renames the other to a name containing `sync-conflict`.

The work here is to make sure the live note holds everything worth keeping, and then to delete the copies.

The vault is /Users/mtm/Documents/Obsidian Vault.

## Finding the conflicts

The vault .gitignore excludes conflict copies, so `git status` never shows them.

Find them directly:

```sh
find "/Users/mtm/Documents/Obsidian Vault" -name "*sync-conflict*" -not -path "*/.git/*"
```

Group the conflict copies by the note they belong to, which is the filename with the `.sync-conflict-<date>-<time>-<device>` part removed.

If there are none, say so in one line and stop.

## Trivial conflicts first

Clear the trivial conflicts without asking and without a long explanation.

A conflict copy is trivial when it is empty, when it is byte-identical to the live note, or when it differs from the live note only in trailing whitespace.

A conflict copy is also trivial when every line in it is already present in the live note.

Delete each trivial conflict copy, and report them as a count grouped by note.

The reverse case is not trivial.

If the live note is empty, or is missing lines that the conflict copy has, treat it as a real conflict.

## Understanding a real conflict

Diff every conflict copy against the live note, against the other conflict copies of the same note, and against the versions in git history.

`git hash-object` on a conflict copy, compared with the blob IDs in `git log` for the note, shows at once whether the copy is a version git already holds.

Use the file modification times and the git log for the note to work out when each version was written.

The device suffix in the conflict filename is the first block of a Syncthing device ID, and it names the device whose incoming change displaced the local version.

Look it up in /Users/mtm/Library/Application Support/Syncthing/config.xml to get the device name.

Explain each conflict in plain terms: which devices edited the note, at what times, and exactly which lines differ.

## Choosing the current version

If one version is a strict superset of the others, that version wins.

If each side has content the other lacks, merge them so that nothing is lost.

If the conflict is a plugin state file under .obsidian, do not merge it.

Report it, and propose an .stignore line instead, which every device needs by hand because .stignore does not sync.

## Judgment calls are multiple choice

If the right merge is a judgment call, do not ask about it mid-way.

Collect those cases and resolve the clear ones first.

Ask the collected questions as multiple choice, using the question dialog, with one question per conflicted note.

Each question names the note and states the disagreement in one sentence, so it stands on its own without scrolling back.

Each option is a complete resolution that can be picked as is, such as keep the Mac version, keep the Pixel version, or keep both with the Mac lines first.

Show the differing lines in the option preview, so each choice shows what it keeps and what it drops.

Put the recommended option first and mark it as recommended.

The dialog holds 4 questions at a time, so if there are more, ask them in rounds of 4 until none remain.

Never ask the user to retype or paste note content as an answer.

## Restoring and committing

Before restoring anything, recheck the live note and the git log.

Background processes commit to the vault, and one may have committed the wrong version since the first look, in which case `git checkout -- <note>` restores nothing and the right version has to be named by commit.

Write the winning content into the live note and commit it with a message that explains why.

Delete a conflict copy only after its note is restored and committed, and only once every line in the copy is present in the restored note or in git.

Deleting a conflict copy produces nothing to commit, since the copies are ignored by git.

After all conflicts are handled, commit every tracked file that changed in the process, so the working tree is clean apart from the Obsidian workspace files.

## Finishing

Run the find again to confirm that no conflict files remain.

Report which notes were resolved, which version won for each, and anything left for the user to decide.

Warn the user if a device may still hold a stale copy of a resolved note open, since saving it would recreate the conflict.
