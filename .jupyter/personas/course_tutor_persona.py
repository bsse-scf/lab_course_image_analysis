"""
Course Tutor: a Jupyter AI persona for the lab-course chat.

Jupyter AI loads every `*persona*.py` in `.jupyter/personas/` (found by
walking up from the chat file), so this file needs no packaging. It is a thin
subclass of the stock Jupyternaut persona - the same LiteLLM backend, model
picker, settings UI and per-chat conversation memory (in process memory: it
lasts while the chat is open, not across closing it or restarting the server)
- that differs in three ways:

1. Its system prompt is the pedagogical one in `course_tutor_prompt.md`,
   re-read on every message so it can be edited without a restart.
2. Before each reply it fetches the notebook cell the student currently has
   selected (source plus output/error) from the browser and appends it to the
   system prompt, so "why does this fail?" needs no copy-pasting.
3. Its tools are the read-only part of the notebook toolkit only: it can
   look at cells, but cannot add, edit, delete or run them.
"""

import asyncio
import re
from pathlib import Path

from jupyter_ai_jupyternaut.jupyternaut.jupyternaut import JupyternautPersona
from jupyter_ai_persona_manager import PersonaDefaults
from jupyter_ai_tools.toolkits.notebook import (
    get_active_notebook,
    read_cell,
    read_notebook,
)
from jupyter_ai_tools.utils import format_outputs, run_lab_command
from jupyterlab_chat.models import Message
from jupyterlab_commands_toolkit.tools import target_client_id

HERE = Path(__file__).parent
PROMPT_PATH = HERE / "course_tutor_prompt.md"
AVATAR_PATH = HERE / "course_tutor.svg"

# Cell outputs (long tracebacks, printed arrays) are cut at this many
# characters so one cell cannot crowd out the conversation.
MAX_OUTPUT_CHARS = 4000
_ANSI_ESCAPES = re.compile(r"\x1b\[[0-9;]*m")


def _load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8").strip()


class CourseTutorPersona(JupyternautPersona):
    # Context of the student's selected cell, refreshed by `process_message`
    # and consumed by `get_system_prompt` for the same message.
    _cell_context: str | None = None

    @property
    def defaults(self):
        return PersonaDefaults(
            name="Course Tutor",
            description=(
                "Tutor for the image analysis lab course: guides with hints and "
                "questions instead of solutions, and sees the notebook cell you "
                "have selected."
            ),
            avatar_path=str(AVATAR_PATH),
            system_prompt=_load_prompt(),
        )

    async def get_tools(self):
        # Read-only subset of `jupyter_ai_tools`' notebook toolkit. Overriding
        # this drops Jupyternaut's add/edit/delete/run tools, its code-execution
        # toolkit and any MCP servers, so the tutor cannot change the notebook.
        return [get_active_notebook, read_notebook, read_cell]

    async def process_message(self, message: Message) -> None:
        # Route frontend commands - the cell lookup below and any tool call the
        # agent makes - to the browser tab that sent the message, the same way
        # jupyter-server-mcp does for MCP tool calls.
        token = target_client_id.set((message.metadata or {}).get("web_client_id"))
        try:
            self.set_status("is reading your notebook cell...")
            self._cell_context = await self._active_cell_context()
            await super().process_message(message)
        finally:
            target_client_id.reset(token)

    def get_system_prompt(self, model_id: str, message: Message) -> str:
        parts = [_load_prompt(), f"The student's username is '{message.sender}'."]
        parts.append(
            self._cell_context
            or "The student has no notebook cell selected right now (no notebook "
            "is open or the cell could not be read)."
        )
        if attachments := self.process_attachments(message):
            parts.append(f"## Files attached by the student\n\n{attachments}")
        return "\n\n".join(parts)

    async def _active_cell_context(self) -> str | None:
        """
        Returns the student's currently selected cell as a Markdown block, or
        None when there is no active notebook.

        Both commands come from the `jupyterlab-ai-commands` frontend extension
        and read the live (possibly unsaved) notebook model in the browser.
        """
        try:
            notebook, cell = await asyncio.gather(
                run_lab_command("jupyterlab-ai-commands:get-notebook-info"),
                run_lab_command("jupyterlab-ai-commands:get-cell-info"),
            )
        except Exception:
            self.log.warning("Course Tutor could not read the active cell.", exc_info=True)
            return None
        notebook = notebook.get("result") or {}
        cell = cell.get("result") or {}
        if not cell.get("success"):
            return None

        lang = "python" if cell.get("cellType") == "code" else "markdown"
        parts = [
            "## Notebook cell the student currently has selected",
            f"Notebook: `{notebook.get('notebookPath')}`, cell id `{cell.get('cellId')}` "
            f"({cell.get('cellType')} cell)",
            f"### Source\n\n```{lang}\n{cell.get('source', '')}\n```",
        ]
        if cell.get("outputs"):
            output = _ANSI_ESCAPES.sub("", format_outputs(cell["outputs"]))
            if len(output) > MAX_OUTPUT_CHARS:
                output = output[:MAX_OUTPUT_CHARS] + "\n... (output truncated)"
            parts.append(f"### Output\n\n{output}")
        elif cell.get("cellType") == "code":
            parts.append("### Output\n\n(the cell has not been run, or produced no output)")
        return "\n\n".join(parts)

