# MonaX Open Workflow

**Pick up yesterday’s work in a fresh chat.** MonaX gives your assistant a place in the project to look up decisions you’ve already made, work you’ve finished, and questions that still need your judgment.

Try whichever example feels familiar.

- You agreed on a reading list’s sort order yesterday. Open a new chat and ask how search and an unread filter should work together. See whether the assistant finds and preserves that decision. [Continue a project](../examples/general/README.md)
- A player taps the reward button twice. Follow the click to the code that grants the reward, check which setting it reads, and run the example to see the balance. [Trace a game reward](../examples/game/README.md)
- A paper boat leaves someone’s hand in the first shot. Give the next shot a starting point so it picks up the drifting boat at the right moment. [Connect two video shots](../examples/ai-video/README.md)

The examples and detailed guides are in Chinese. You can read them first, or try the local setup below with Python 3.10 or later.

## Try without a plugin

From the package root, create a disposable project and run:

```sh
mkdir demo-project
python3 -B plugins/monax-open-workflow/scripts/project.py init --project-root ./demo-project
python3 -B plugins/monax-open-workflow/scripts/project.py init --project-root ./demo-project --apply
python3 -B plugins/monax-open-workflow/scripts/project.py check --project-root ./demo-project
```

On Windows use `python`. Python 3.10+ and its standard library are sufficient. Initialization is dry-run by default and refuses existing destination files. `NeedsProjectFacts` is expected until you supply verified project facts. No command installs a plugin or uploads data.

Open the new project in a file-capable assistant and ask it to read AGENTS.md, verify the project facts and follow only the relevant workflow. Static mode depends on your host loading those instructions. Optional Codex installation is described in the [main README](../README.md).

## Explore

- [Task router](../plugins/monax-open-workflow/rules/context.md)
- [Game workflow](../plugins/monax-open-workflow/rules/game-development.md)
- [AI video workflow](../plugins/monax-open-workflow/rules/ai-video.md)
- [Fictional examples](../examples/README.md)
- [Validation and limitations](../VALIDATION.md)
- [Distribution boundaries](DISTRIBUTION.md)

The package does not include generation services, private business data, personal preferences, machine configuration or source Git history. Readiness checks are structural; they do not establish runtime correctness, media quality, user acceptance or guaranteed model compliance.
