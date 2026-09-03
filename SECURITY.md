# Security

This repo is the public copy of a live SSH-based guest-agent experiment.

## Guest threat model

A paid guest is untrusted. The guest can control prompts and can ask the Cursor Agent to use its shell, file read, file write, edit, delete, glob, grep, and search capabilities.

Prompt instructions, `AGENTS.md`, and Cursor permission lists are not security boundaries. The security boundary must be the operating-system mount namespace created by bubblewrap.

A guest must not be able to:

- read or list the host user's home directory;
- read another guest's session directory;
- write outside the current session workspace;
- obtain host SSH, cloud, deployment, or model credentials.

## Current isolation

The canonical SSH launcher is `run-agent.sh` at the repository root. It starts the Cursor Agent itself as the child of `bwrap`; shell commands and higher-level file operations therefore use the same mount namespace.

The launcher currently:

- mounts the host root read-only;
- masks `/home/ubuntu` with a private tmpfs;
- recreates only the required `development` and `development/guest-sessions` directories;
- bind-mounts the current session directory;
- bind-mounts Cursor state to the private `${REAL_HOME}/.cursor` location;
- sets `HOME` to the masked home directory;
- makes the session workspace the process working directory.

Consequently, writes outside the bound session directory should fail at the kernel mount level, while writes inside the session workspace should succeed. Sibling guest sessions are not mounted into the guest namespace.

`scripts/run-agent.sh` is an older duplicate and is not the canonical launcher. Deployment configuration must continue to invoke the root `run-agent.sh`; changes to the duplicate do not harden the live path.

## Residual credential risk

The canonical launcher currently read-only mounts:

```bash
--ro-bind "${REAL_HOME}/.config/cursor" "${REAL_HOME}/.config/cursor"
```

This keeps the model client usable but means files under the host Cursor configuration directory may be readable by the guest agent. Cursor authentication must therefore be treated as exposed to a sufficiently capable guest until this is changed.

The preferred follow-up is a host-side model broker: keep the credential file outside the guest mount namespace and let the guest agent communicate with a narrowly scoped Unix socket service that performs model requests without returning the credential. Do not solve this by prompt rules or by mounting `auth.json` read-only.

Until that broker exists, operators should use a dedicated least-privilege model credential and should not place unrelated credentials in the mounted Cursor directory.

## Regression test

Run:

```bash
tests/guest-isolation.sh
```

The CI test is intentionally static. A production bwrap integration test requires the live host paths, bubblewrap privileges, the installed Cursor Agent, and a disposable session. The static test fails if the canonical launcher loses the required namespace flags or if the older broad `.config` mount is copied into it.

## Reporting

Do not publish working exploits, credential dumps, prompts, payment links, or personal information. Report suspected host-credential or cross-guest access privately to the maintainers, including reproduction details without secrets.

Fixes belong in this repository. Proof-of-concept testing against the live service must use placeholders and must not access another guest's data.
