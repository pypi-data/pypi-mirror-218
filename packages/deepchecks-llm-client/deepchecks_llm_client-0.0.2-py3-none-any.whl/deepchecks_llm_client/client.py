import typing as t

from deepchecks_llm_client.api import API, EnvType, AnnotationType
from deepchecks_llm_client.openai_instrumentor import OpenAIInstrumentor

__all__ = ["dc_client", "Tags"]


class Tags:
    """
    Namespace for useful tags that deepchecks case use
    You can use `AppContext` to pass user tags to deepchecks

    USER_PROMPT
        Relevant only for auto_collect=True and for cases where there is no clear understanding
        For what is the "user prompt" (like in the case of `openai.Completion`)

    USER_ID
        The external user that used the AI model

    EXT_INTERACTION_ID
        user generated unique id to be used later for reporting annotation results (good/bad) to deepchecks
        if this tag is not set, we will try to get the unique id that was supplied by the AI vendor
        (in the case of OpenAI - it will be response.id)
    """
    USER_PROMPT: str = "user_prompt"
    USER_ID: str = "user_id"
    EXT_INTERACTION_ID: str = "ext_interaction_id"

DEFAULT_APP_NAME = 'DefaultApp'
DEFAULT_VERSION_NAME = '0.0.1'
DEFAULT_ENV_TYPE = EnvType.PROD

class DeepchecksLLMClient:

    def __init__(self):
        self.api = None
        self.instrumentor = None

    def connect(self,
                host: str,
                api_token: str,
                app_name: str = DEFAULT_APP_NAME,
                version_name: str = DEFAULT_VERSION_NAME,
                env_type: EnvType = DEFAULT_ENV_TYPE,
                auto_collect: bool = True
             ):
        """
                Connect to Deepchecks LLM Server

                Parameters
                ----------
                host : str
                    Deepchecks host to communicate with
                api_token : str
                    Deepchecks API Token (can be generated from the UI)
                auto_collect : bool, default=True
                    Auto collect calls to LLM Models
                app_name : str, default='DefaultApp'
                    Application name to connect to, if Application name does not exist SDK will create it
                    automatically
                version_name : str, default='1.0.0'
                    Version name to connect to inside the application,
                    if Version name does not exist SDK will create it automatically,
                env_type : EnvType, default=EnvType.PROD
                    could be EnvType.PROD (for 'Production') or EnvType.EVAL (for 'Evaluation')
                """
        if host is not None and api_token is not None:
            self.api = API.instantiate(host=host, token=api_token)
        else:
            raise ValueError('host/token parameters must be provided')

        self.instrumentor = None
        if auto_collect:
            self.instrumentor = OpenAIInstrumentor(self.api, app_name, version_name, env_type)
            self.instrumentor.perform_patch()

    def set_context(self,
                    app_name: str = DEFAULT_APP_NAME,
                    version_name: str = DEFAULT_VERSION_NAME,
                    env_type: EnvType = DEFAULT_ENV_TYPE):
        if self.instrumentor:
            self.instrumentor.set_context(app_name, version_name, env_type)

    def annotate(self, ext_interaction_id: str, annotation: AnnotationType):
        self.api.annotate(ext_interaction_id, annotation)

    def set_tags(self, tags: t.Dict[str, t.Any]):
        if self.instrumentor:
            self.instrumentor.tags = tags


#
dc_client: DeepchecksLLMClient = DeepchecksLLMClient()


