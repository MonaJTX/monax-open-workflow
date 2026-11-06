# MonaX Open Workflow

**Pick up yesterday’s work in a fresh chat.** MonaX gives your assistant a place in the project to look up decisions you’ve already made, work you’ve finished, and questions that still need your judgment.

Try whichever example feels familiar.

- You agreed on a reading list’s sort order yesterday. Open a new chat and ask how search and an unread filter should work together. See whether the assistant finds and preserves that decision. [Continue a project](../examples/general/README.md)
- A player taps the reward button twice. Follow the click to the code that grants the reward, check which setting it reads, and run the example to see the balance. [Trace a game reward](../examples/game/README.md)
- A paper boat leaves someone’s hand in the first shot. Give the next shot a starting point so it picks up the drifting boat at the right moment. [Connect two video shots](../examples/ai-video/README.md)

The examples and detailed guides are in Chinese. You can read them first, or try the local setup below with Python 3.10 or later.

## Get a local copy

Clone the repository and open a terminal in the cloned folder, or use **Code → Download ZIP** on GitHub and open the extracted folder that contains both `README.md` and `plugins`.

```sh
git clone https://github.com/MonaJTX/monax-open-workflow.git
cd monax-open-workflow
python3 --version
```

Use Python 3.10 or later. On Windows use `python` or `py -3` in place of `python3`. Keep the terminal in the workflow folder. Open the **target project folder** in your file-capable assistant.

## Try it with a reading list

```sh
mkdir demo-project
python3 -B plugins/monax-open-workflow/scripts/project.py init --project-root "./demo-project"
python3 -B plugins/monax-open-workflow/scripts/project.py init --project-root "./demo-project" --apply
python3 -B plugins/monax-open-workflow/scripts/project.py check --project-root "./demo-project"
```

Expect `Planned`, `Created`, then `NeedsProjectFacts`. Copy [the fictional brief](../examples/general/project-brief.md) into `demo-project` and open that folder in your assistant. Ask:

> Read AGENTS.md and project-brief.md. Fill in the project identity, phase, constraints and decisions in the files linked from PROJECT_CONTEXT/README.md. Resolve the corresponding placeholders and remove the resolved item from blocking_items in workflow_activation_profile.json after checking the facts.

Run `python3 -B plugins/monax-open-workflow/scripts/project.py check --project-root "./demo-project" --require-ready`. Once it reports `Ready`, start a fresh chat in the same project and ask “How should search and the unread filter work together? Which project file records the decision?” Look for title-only matching, unread items only, and newest additions first.

## Bring it to your own project

From the workflow folder, replace `"../my-project"` with the path to your existing project:

```sh
python3 -B plugins/monax-open-workflow/scripts/project.py init --project-root "../my-project"
```

On `Planned`, review the list and repeat with `--apply`. On `Conflict`, keep your current files and follow the [merge walkthrough](USAGE.md#已有项目合并). For a project already using MonaX, run `check` directly. Open your project in your assistant, ask it to fill the indexed files using your own project facts, and check again with `--require-ready`. The `pending` and `issues` fields identify anything that still needs attention.

## Explore

- [Task router](../plugins/monax-open-workflow/rules/context.md)
- [Game workflow](../plugins/monax-open-workflow/rules/game-development.md)
- [AI video workflow](../plugins/monax-open-workflow/rules/ai-video.md)
- [Fictional examples](../examples/README.md)
- [Validation and limitations](../VALIDATION.md)
- [Distribution boundaries](DISTRIBUTION.md)

The package does not include generation services, private business data, personal preferences, machine configuration or source Git history. Readiness checks are structural; they do not establish runtime correctness, media quality, user acceptance or guaranteed model compliance.
