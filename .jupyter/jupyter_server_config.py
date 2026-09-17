# Jupyter Server settings for the course chat (Jupyter AI).
#
# Loaded because pixi sets JUPYTER_CONFIG_PATH to this directory (see
# `[activation.env]` in pixi.toml). When JupyterLab is started without pixi,
# pass `--config=.jupyter/jupyter_server_config.py` or set that variable.
import os

from jupyter_ai_persona_manager import PersonaManager

c = get_config()  # noqa: F821

TUTOR_ID = "jupyter-ai-personas::course_tutor_persona::CourseTutorPersona"
# The directory of this file, i.e. the project's `.jupyter/`.
DOTJUPYTER_DIR = os.path.dirname(os.path.abspath(__file__))


class CoursePersonaManager(PersonaManager):
    """
    Offers students only the Course Tutor (`.jupyter/personas/`).

    Jupyter AI has no allow-list for personas, so this skips every persona
    registered through the `jupyter_ai.personas` entry point group: the stock
    Jupyternaut (whose tools can edit and run cells) and the ACP agents such as
    Copilot, Claude Code or Codex, which appear whenever their CLI happens to
    be on PATH.
    """

    def _init_ep_persona_classes(self) -> None:
        PersonaManager._ep_persona_classes = []

    def get_dotjupyter_dir(self) -> str:
        # Jupyter AI looks for `.jupyter/personas/` by walking up from the
        # chat file, never above the server root. That only reaches this
        # directory when the project is the root, as with `pixi run lab`. On
        # RRP the root is /home/jovyan (so students see `openbis`, `results`
        # etc.), the chat lands in /home/jovyan/.chat and the walk stops at
        # the user's own ~/.jupyter, which has no personas - the tutor is then
        # missing. Point Jupyter AI at the project's `.jupyter/` regardless of
        # where the chat file lives.
        return DOTJUPYTER_DIR


c.PersonaManagerExtension.persona_manager_class = CoursePersonaManager
# Pre-selects the tutor in the chat's persona picker. Must be set on the
# subclass: the extension reads `<persona_manager_class name>.default_persona_id`
# to advertise the default to the frontend (`jupyter_ai_default_persona`).
c.CoursePersonaManager.default_persona_id = TUTOR_ID

# Chat model served by the Swiss AI Initiative (OpenAI-compatible API, hence
# the `openai/` LiteLLM prefix). These are merged into each user's Jupyternaut
# config at startup, so students can still pick another model in "AI settings".
# The API key must be provided as OPENAI_API_KEY - in the environment or in a
# `.env` file at the server root - or entered in "AI settings" (which writes
# that `.env`). On RRP the root is /home/jovyan, whose `.env` .binder/start
# links into the project so the key survives a restart.
MODEL_ID = "openai/SwissAI-Research/Qwen/Qwen3.5-27B"
c.JupyternautExtension.initial_language_model = MODEL_ID
c.JupyternautExtension.model_parameters = {
    MODEL_ID: {
        "api_base": "https://api.swissai.svc.cscs.ch/v1",
        # Qwen3.5 is a reasoning model and the endpoint (vLLM with
        # `--reasoning-parser qwen3`) has thinking on by default. Jupyternaut
        # streams the reasoning into the chat as if it were the answer, and
        # the next turn fails with "Unknown part type: reasoning" when that
        # history is sent back. Switch thinking off per request instead.
        "model_kwargs": {
            "extra_body": {"chat_template_kwargs": {"enable_thinking": False}},
        },
    },
}

# Make AnyIO's worker threads daemon threads, so Ctrl-C ends the server.
#
# Several extensions run server-lifetime tasks that block in
# `anyio.to_thread.run_sync`: jupyter-live-content watches the directory of
# every open notebook through `watchfiles`, and jupyter-ai-jupyternaut polls
# `.env` every 2 s through the async contents manager. AnyIO stops a worker
# thread only when the task that first used it finishes, and none of those
# tasks are cancelled on shutdown. The workers are ordinary non-daemon
# threads, so after the event loop has stopped the interpreter waits for them
# forever - the "received signal 2, stopping" lines on every further Ctrl-C.
# A daemon worker cannot hold up exit; by then the loop is stopped and nothing
# is waiting for a result anyway.
from anyio._backends._asyncio import WorkerThread as _AnyIOWorkerThread

_anyio_worker_init = _AnyIOWorkerThread.__init__


def _daemon_worker_init(self, *args, **kwargs):
    _anyio_worker_init(self, *args, **kwargs)
    self.daemon = True


_AnyIOWorkerThread.__init__ = _daemon_worker_init
