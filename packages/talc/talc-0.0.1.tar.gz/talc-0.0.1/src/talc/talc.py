import os
from datetime import datetime
from supabase import create_client, Client
import logging
import openai


class _SupabaseClient:
    def __init__(self):
        url: str = os.environ.get(
            "INSTANCE_URL", default="https://qdgodxkfxzzmzwfliahh.supabase.co"
        )
        key: str = os.environ.get(
            "INSTANCE_SERVICE_KEY",
            default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFkZ29keGtmeHp6bXp3ZmxpYWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODg0OTc0NzcsImV4cCI6MjAwNDA3MzQ3N30.4bgCdg77wwOJ9w1hOtCD-z0gBVGv8X_kIxBCr5KDCuA",
        )
        self.__organization: str = os.environ.get("TALC_API_KEY", default="")
        if self.__organization == "":
            logging.warning(
                "TALC_API_KEY environment variable not set. Logging disabled."
            )
        self.supabase: Client = create_client(url, key)

    def createSession(self):
        response = (
            self.supabase.table("sessions")
            .insert(
                {
                    "organization": self.__organization,
                }
            )
            .execute()
        )
        return response.data[0]["id"]

    def __createInput(self, sessionId, generationId, role, content, index):
        response = (
            self.supabase.table("inputs")
            .insert(
                {
                    "session": sessionId,
                    "generation": generationId,
                    "role": role,
                    "content": content,
                    "index": index,
                }
            )
            .execute()
        )
        return response.data[0]["id"]

    def __createGeneration(self, sessionId, content, agent, generated_at):
        response = (
            self.supabase.table("generations")
            .insert(
                {
                    "session": sessionId,
                    "content": content,
                    "agent": agent,
                    "generated_at": generated_at,
                }
            )
            .execute()
        )
        print(response.data[0])
        return response.data[0]["id"]

    def __historyArrayToInputs(self, history, generationId, sessionId):
        for index, chat in enumerate(history):
            self.__createInput(
                sessionId,
                generationId,
                chat["role"],
                chat["content"],
                # Index is reversed because we want the most recent message to have the lowest index
                len(history) - index,
            )

    def log(self, sessionId, history, generationContent, agent):
        generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        generationId = self.__createGeneration(
            sessionId, generationContent, agent, generated_at
        )
        self.__historyArrayToInputs(history, generationId, sessionId)


client = _SupabaseClient()


def createSession():
    response = client.createSession()
    return response


def init():
    global client
    client = _SupabaseClient()


class __alternateCompletion(openai.ChatCompletion):
    @classmethod
    def create(cls, *args, **kwargs):
        # Pop arguments that are not supported by the original create method
        agent = kwargs.pop("agent", None)
        session = kwargs.pop("session", None)

        result = super().create(*args, **kwargs)

        try:
            if session and agent:
                client.log(
                    session,
                    kwargs["messages"],
                    cls.__getContent(result.choices),
                    agent,
                )
        except Exception as e:
            print("Error logging to talc: ", e)

        return result

    @classmethod
    async def acreate(cls, *args, **kwargs):
        # Pop arguments that are not supported by the original create method
        agent = kwargs.pop("agent", None)
        session = kwargs.pop("session", None)

        result = await super().acreate(*args, **kwargs)

        try:
            if session and agent:
                client.log(
                    session,
                    kwargs["messages"],
                    cls.__getContent(result.choices),
                    agent,
                )
        except Exception as e:
            print("Error logging to talc: ", e)

        return result

    @classmethod
    def __getContent(cls, choices):
        if len(choices) == 0:
            return ""
        elif "function_call" in choices[0].message:
            return choices[0].message.function_call
        return choices[0].message.content


openai.ChatCompletion = __alternateCompletion
