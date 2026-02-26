import os
import re
from typing import Any

from ink_maze import InkMaze

def enable_langsmith(project_name: str) -> None:
    if not os.getenv("LANGSMITH_API_KEY"):
        return

    os.environ.setdefault("LANGSMITH_TRACING", "true")
    os.environ.setdefault("LANGSMITH_PROJECT", project_name)

    # Optional, but helpful in short scripts:
    # os.environ.setdefault("LANGSMITH_TRACING_BACKGROUND", "false")


def _create_chat_model(provider: str, model_name: str, temperature: float) -> Any:
    """Create a model for the selected provider.

    NOTE: For Hugging Face we use *text-generation* (HuggingFaceEndpoint) because
    HF routed providers may not support chat-completions for many models.
    """
    provider = provider.lower()

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=model_name, temperature=temperature)

    if provider == "huggingface":
        from langchain_huggingface import HuggingFaceEndpoint

        # IMPORTANT:
        # - task='text-generation' forces text-generation rather than chat-completions.
        # - provider='hf-inference' uses Hugging Face serverless inference.
        # - Most instruct models work here via text-generation.
        return HuggingFaceEndpoint(
            repo_id=model_name,
            task="text-generation",
            temperature=temperature,
            max_new_tokens=512,
            provider="hf-inference",
        )

    if provider == "transformers":
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=96,
            temperature=temperature,
        )

        class _LocalTransformersLLM:
            def __init__(self, text_generator: Any):
                self._text_generator = text_generator

            def invoke(self, prompt_text: str) -> str:
                outputs = self._text_generator(prompt_text)
                if not outputs:
                    return ""
                generated = outputs[0].get("generated_text", "")
                if generated.startswith(prompt_text):
                    generated = generated[len(prompt_text):]
                return generated.strip()

        return _LocalTransformersLLM(generator)

    raise ValueError(
        f"Unsupported provider: {provider}. Use 'openai', 'huggingface', or 'transformers'."
    )

def build_agent(maze: InkMaze, model_name: str, temperature: float, provider: str) -> Any:
    """Create a tool-calling LangChain agent over maze tools."""
    from langchain_core.tools import tool
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

    @tool
    def read_current_room() -> str:
        """Inspect the current room text and the three available doors."""
        return maze.read_room()

    @tool
    def pick_door(door_index: int) -> str:
        """Choose one of the three doors by passing door_index=1, 2, or 3."""
        return maze.choose_door(door_index)

    @tool
    def maze_status() -> str:
        """Return the current knot name and whether the maze is finished."""
        return f"knot={maze.state.current_knot}, finished={maze.state.finished}"

    llm = _create_chat_model(provider=provider, model_name=model_name, temperature=temperature)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a careful maze navigator. "
                "Always call read_current_room first, then select one door with pick_door. "
                "Stop when maze_status indicates finished=True. "
                "Briefly justify each door choice.",
            ),
            ("human", "Navigate the maze to completion."),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    tools = [read_current_room, pick_door, maze_status]

        # Hugging Face text-generation models do not implement tool-calling (no bind_tools),
    # so we run a small local controller loop instead of LangChain tool-calling agents.
    if provider.lower() in {"huggingface", "transformers"}:
        try:
            from langsmith import traceable
        except ModuleNotFoundError:
            def traceable(*_args: Any, **_kwargs: Any):
                def _decorator(func: Any) -> Any:
                    return func

                return _decorator

        class _HFRunner:
            def __init__(self, llm_model: Any):
                self._llm = llm_model

            @traceable(run_type="tool", name="maze_pick_door")
            def _pick(self, room_text: str) -> int:
                # Force a tiny, machine-readable output.
                prompt_text = (
                    "You are navigating a maze. You must choose exactly one door number: 1, 2, or 3.\n"
                    "Reply with ONLY the digit 1, 2, or 3 on a single line.\n\n"
                    f"ROOM:\n{room_text}\n"
                )
                raw = self._llm.invoke(prompt_text)
                text = raw if isinstance(raw, str) else getattr(raw, "content", str(raw))
                m = re.search(r"\b([123])\b", text)
                if not m:
                    raise ValueError(f"Model did not return a door index. Got: {text!r}")
                return int(m.group(1))

            @traceable(run_type="tool", name="maze_navigation_run")
            def invoke(self, _: dict[str, Any]) -> dict[str, Any]:
                steps: list[tuple[Any, Any]] = []
                for _i in range(20):
                    room = maze.read_room()
                    if maze.state.finished:
                        break
                    door = self._pick(room)
                    obs = maze.choose_door(door)
                    # Store a lightweight history compatible with your printing loop.
                    steps.append((type("Action", (), {"tool": "pick_door", "tool_input": {"door_index": door}})(), obs))
                    if maze.state.finished:
                        break
                return {
                    "output": f"knot={maze.state.current_knot}, finished={maze.state.finished}",
                    "intermediate_steps": steps,
                }

        return _HFRunner(llm)

    # OpenAI (and other chat tool-calling models) can use LangChain's agent factory.
    from langchain.agents import create_agent

    system_prompt = (
        "You are a careful maze navigator. "
        "Always call read_current_room first, then select one door with pick_door. "
        "Stop when maze_status indicates finished=True. "
        "Briefly justify each door choice."
    )

    agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt)

    class _AgentRunner:
        def __init__(self, wrapped_agent: Any):
            self._agent = wrapped_agent

        def invoke(self, _: dict[str, Any]) -> dict[str, Any]:
            response = self._agent.invoke(
                {"messages": [{"role": "user", "content": "Navigate the maze to completion."}]}
            )
            messages = response.get("messages", []) if isinstance(response, dict) else []
            output = ""
            for message in reversed(messages):
                content = getattr(message, "content", None)
                if isinstance(content, str) and content.strip():
                    output = content
                    break

            if not output and isinstance(response, dict):
                output = str(response)

            return {"output": output, "intermediate_steps": []}

    return _AgentRunner(agent)
