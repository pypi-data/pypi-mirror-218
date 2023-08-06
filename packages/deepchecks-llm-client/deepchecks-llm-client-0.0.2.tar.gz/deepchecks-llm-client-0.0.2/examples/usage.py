import os
import uuid

import coloredlogs
import dotenv
import openai

from deepchecks_llm_client.api import AnnotationType, EnvType
from deepchecks_llm_client.client import dc_client, Tags


def run():
    coloredlogs.install(level='DEBUG')

    dotenv.load_dotenv()

    deepchecks_api_key = os.environ.get("DEEPCHECKS_LLM_API_KEY")
    # auto_collect=True wraps `openai.ChatCompletion` and `openai.Completion` APIs
    # so any OpenAI invocation will fire an event to deepchecks with the relevant data
    dc_client.connect(host='http://localhost:8000',
                      api_token=deepchecks_api_key,
                      app_name="ShaysApp",
                      version_name="0.0.1-shay",
                      env_type=EnvType.EVAL,
                      auto_collect=True)

    # Adding context to the call, deepchecks will monitor the context together with any OpenAI's request/response
    dc_client.set_tags({Tags.USER_ID: "mycustomer@gmail.com"})

    # Set up your OpenAI API credentials
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", temperature=0.7,
                                                   messages=[{"role": "user", "content": "How much is 2 plus 2?"}])

    # print the chat completion`
    print(chat_completion.choices[0].message.content)

    # Annotating based on openai.id
    dc_client.annotate(chat_completion.openai_id, annotation=AnnotationType.GOOD)


    ### Next Iteration ###
    ######################


    dc_client.set_context(app_name="ShaysApp", version_name="0.0.2-shay", env_type=EnvType.EVAL)

    user_prompt = "how many trees in the garden?"
    external_id = "myGenID1" + str(uuid.uuid4())
    dc_client.set_tags({Tags.USER_ID: "mycustomer2@gmail.com", Tags.USER_PROMPT: user_prompt,
                        Tags.EXT_INTERACTION_ID: external_id})

    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=user_prompt,
      temperature=0.5,
      max_tokens=150,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=["#", ";"]
    )

    print(response)

    # Annotating based on external id
    dc_client.annotate(external_id, annotation=AnnotationType.BAD)


if __name__ == "__main__":
    #asyncio.run(run())
    run()
