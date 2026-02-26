"""LangChain agent that navigates a three-door Ink maze with LangSmith tracing.

Usage:
  # OpenAI provider (default)
  export OPENAI_API_KEY=...
  export LANGSMITH_API_KEY=...
  python moon_phase_maze/langchain_ink_maze_agent.py \
      --provider openai \
      --model gpt-4o-mini \
      --ink-file moon_phase_maze/lunar_phase_maze.ink \
      --start-knot beginning_room

  # Hugging Face provider
  export HUGGINGFACEHUB_API_TOKEN=...
  export LANGSMITH_API_KEY=...
  python moon_phase_maze/langchain_ink_maze_agent.py \
      --provider huggingface \
      --model meta-llama/Meta-Llama-3-8B-Instruct \
      --ink-file moon_phase_maze/lunar_phase_maze.ink \
      --start-knot beginning_room

  # Local Transformers provider (runs on your own machine)
  export LANGSMITH_API_KEY=...
  python moon_phase_maze/langchain_ink_maze_agent.py \
      --provider transformers \
      --model google/gemma-2-2b-it \
      --ink-file moon_phase_maze/lunar_phase_maze.ink \
      --start-knot beginning_room

  # Or pass an inklecate-compiled JSON file directly:
  python moon_phase_maze/langchain_ink_maze_agent.py \
      --ink-file path/to/story.json \
      --start-knot beginning_room

The script will:
  1) Parse the Ink file into a simple knot graph.
  2) Expose tools for inspecting state and choosing one of three doors.
  3) Run a LangChain agent that chooses doors until DONE/END.
  4) Print intermediate steps so agent behavior can be inspected locally,
     while LangSmith receives full traces when configured.
"""

from __future__ import annotations

import argparse
from langsmith import Client

from agent_langchain_utils import enable_langsmith, build_agent
from ink_maze import InkMaze

from dotenv import load_dotenv
load_dotenv()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ink-file", default="moon_phase_maze/lunar_phase_maze.ink")
    parser.add_argument("--start-knot", default="beginning_room")
    parser.add_argument(
        "--provider",
        choices=["openai", "huggingface", "transformers"],
        default="openai",
    )
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--langsmith-project", default="ink-maze-langchain-agent")
    args = parser.parse_args()

    enable_langsmith(args.langsmith_project)

    maze = InkMaze.from_file(args.ink_file, start_knot=args.start_knot)
    
    ls_client = Client()

    try:
        maze = InkMaze.from_file(args.ink_file, start_knot=args.start_knot)
        executor = build_agent(maze, model_name=args.model, temperature=args.temperature, provider=args.provider)
        result = executor.invoke({})
    finally:
        # CRITICAL: upload buffered traces even if an exception is thrown
        ls_client.flush()

    print("\n=== Final output ===")
    print(result["output"])

    print("\n=== Intermediate steps (local history) ===")
    for idx, (action, observation) in enumerate(result.get("intermediate_steps", []), start=1):
        print(f"Step {idx}: tool={action.tool}, tool_input={action.tool_input}")
        print(f"Observation: {observation}\n")


if __name__ == "__main__":
    main()
