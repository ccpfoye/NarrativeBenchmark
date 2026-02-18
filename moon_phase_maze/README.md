## Moon Phase Maze

A maze where navigating to the end requires following the phases of the moon. This is a simple example meant as a tutorial and a demo with basic gameplay features.

https://en.wikipedia.org/wiki/Lunar_phase
1. New Moon
2. Waxing Crescent
3. First Quarter
4. Waxing Gibbous
5. Full Moon
6. Waning Gibbous
7. Last Quarter
8. Waning Crescent

## Random maze generation

This project now includes `moon_phase_maze/maze_generator.py`, which generates a randomized maze of knots with:

- a `beginning_room`
- an `ending_room`
- a progression path that must follow the moon phases in order
- dead-end rooms for incorrect door choices

Generate (or regenerate) the maze file:

```bash
python moon_phase_maze/maze_generator.py \
  --output moon_phase_maze/lunar_phase_maze.ink \
  --seed 11
```

By default, dead-end rooms are now backtrackable, so a wrong choice sends the player to a side room that can route back to the previous chamber. To restore one-way dead ends, pass `--no-dead-ends-backtrackable`.

### Extending beyond moon phases

The generator is structured around an ordered progression track (`RoomTrack`) so you can later swap moon phases for other room types by passing a different `--stages` sequence.

Example:

```bash
python moon_phase_maze/maze_generator.py \
  --track-name elemental_cycle \
  --stages ember smoke storm rain bloom dusk \
  --seed 23
```

## LangChain + LangSmith maze agent

A ready-to-run LangChain agent is provided at `moon_phase_maze/langchain_ink_maze_agent.py`.
It exposes three tools (`read_current_room`, `pick_door`, and `maze_status`) so the LLM can
choose among three doors in each knot.

To run with LangSmith tracing/history (OpenAI):

```bash
export OPENAI_API_KEY=...
export LANGSMITH_API_KEY=...
python moon_phase_maze/langchain_ink_maze_agent.py \
  --provider openai \
  --model gpt-4o-mini \
  --ink-file moon_phase_maze/lunar_phase_maze.ink \
  --start-knot beginning_room \
  --langsmith-project ink-maze-langchain-agent
```

To run with a Hugging Face-backed agent:

```bash
export HUGGINGFACEHUB_API_TOKEN=...
export LANGSMITH_API_KEY=...
python moon_phase_maze/langchain_ink_maze_agent.py \
  --provider huggingface \
  --model meta-llama/Meta-Llama-3-8B-Instruct \
  --ink-file moon_phase_maze/lunar_phase_maze.ink \
  --start-knot beginning_room \
  --langsmith-project ink-maze-langchain-agent
```

The script enables `LANGSMITH_TRACING`/`LANGCHAIN_TRACING_V2` and prints
`intermediate_steps` locally so you can inspect behavior both in terminal and in LangSmith.

You can provide either the source `.ink` file or an inklecate-compiled `.json` story file
as `--ink-file`. If `inklecate` is available on PATH and you pass `.ink`, the script will
prefer parsing the compiled JSON export (`inklecate -o story.json story.ink`) for better
alignment with Ink's serializable runtime format.
