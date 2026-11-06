# MonaX Open Workflow

**MonaX gives your AI assistant a way to carry project decisions into the next task and show you what it actually checked before handing work back.**

Say you agreed yesterday that search matches titles only and the newest entries come first. Today you can ask for an “unread” button. The project’s Markdown notes give the assistant both decisions to work from, and a teammate can read the same notes to see why the list behaves that way. [Try the reading list example](../examples/general/README.md)

## What you can use it for

| When you want to… | What you get |
| --- | --- |
| Resume work or hand it to a teammate | A project record of the decisions in force, where work stopped, and what still needs checking. [Project memory](../plugins/monax-open-workflow/rules/memory.md) |
| Change an existing application | A workflow for finding code worth reusing, agreeing on the scope, and handing back the change with the checks run and questions still open. [Development workflow](../plugins/monax-open-workflow/rules/development.md) |
| Find out why a game behaves a certain way | A trace from a player action to the code and configuration that control it. Run the reward example to see the first claim earn three tokens and a second click earn zero. [Run the example](../examples/game/README.md) |
| Hand a video script to a production partner | A shot-by-shot plan with separate still, storyboard and motion prompts, plus a record of which inputs and reviews are still needed. [Read the two-shot prompt pack](../examples/ai-video/shots.md) · [See its production record](../examples/ai-video/ledger.md) |

The examples and detailed guides are in Chinese. To try the workflow locally, you’ll need a file-capable assistant and Python 3.10 or later.

[Get a local copy](#get-a-local-copy) · [Use your own project](#bring-it-to-your-own-project) · [中文首页](../README.md)

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
