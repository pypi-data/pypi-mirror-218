# mypy: disable-error-code="override"
from typing import List, Optional

import aiohttp
from aiohttp import ClientResponseError

from klu.action.models import PromptResponse
from klu.common.client import KluClientBase
from klu.common.errors import (
    InvalidUpdateParamsError,
    UnknownKluAPIError,
    UnknownKluError,
)
from klu.common.models import PromptInput
from klu.experiment.constants import EXPERIMENT_ENDPOINT, PROMPT_EXPERIMENT_ENDPOINT
from klu.experiment.errors import ExperimentNotFoundError
from klu.experiment.models import Experiment
from klu.utils.dict_helpers import dict_no_empty


class ExperimentClient(KluClientBase):
    def __init__(self, api_key: str):
        super().__init__(api_key, EXPERIMENT_ENDPOINT, Experiment)

    async def create(
        self,
        name: str,
        app_guid: str,
        action_primary_guid: str,
        action_secondary_guid: str,
    ) -> Experiment:
        """
        Creates an experiment based on the data provided.

        Args:
            name (str): Name of the experiment
            app_guid (str): Guid of the app object this experiment is attached to.
            action_primary_guid (str): Guid of the primary action object this experiment is attached to.
            action_secondary_guid (str): Guid of the secondary action object this experiment is attached to.

        Returns:
            A newly created Experiment object.
        """
        return await super().create(
            name=name,
            app_guid=app_guid,
            action_primary_guid=action_primary_guid,
            action_secondary_guid=action_secondary_guid,
        )

    async def get(self, guid: str) -> Experiment:
        """
        Retrieves experiment information based on the unique Experiment guid, created during the Experiment creation.

        Args:
            guid (str): GUID of an experiment to fetch. The one that was used during the experiment creation

        Returns:
            Experiment object
        """
        return await super().get(guid)

    async def update(
        self,
        guid: str,
        name: Optional[str] = None,
        action_primary_guid: Optional[str] = None,
        action_secondary_guid: Optional[str] = None,
    ) -> Experiment:
        """
        Update experiment data. At least one of the params has to be provided

        Args:
            guid (str): GUID of an application to fetch. The one that was used during the app creation
            name: Optional[str]. New experiment name
            action_primary_guid: Optional[str]. New experiment primary action guid
            action_secondary_guid: Optional[str]. New experiment secondary action guid

        Returns:
            Updated experiment instance
        """

        if not name and not action_primary_guid and not action_secondary_guid:
            raise InvalidUpdateParamsError()

        return await super().update(
            **{
                "guid": guid,
                **dict_no_empty(
                    {
                        "name": name,
                        "action_primary_guid": action_primary_guid,
                        "action_secondary_guid": action_secondary_guid,
                    }
                ),
            }
        )

    async def delete(self, guid: str) -> Experiment:
        """
        Delete experiment based on the id.

        Args:
            guid (str): Unique Guid of an experiment to delete.

        Returns:
            Deleted experiment object
        """
        return await super().delete(guid)

    async def run_experiment_prompt(
        self,
        experiment_guid: str,
        input: PromptInput,
        filter: Optional[str] = None,
        force_action: Optional[str] = None,
        streaming: Optional[bool] = False,
        async_mode: Optional[bool] = False,
        session_guid: Optional[str] = None,
        indices: Optional[List[int]] = None,
        metadata_filter: Optional[dict] = None,
    ) -> PromptResponse:
        """
        Run a prompt with an agent, optionally using streaming.

        Args:
            experiment_guid (str): The GUID of the experiment to run the prompt with.
            input (PromptInput): The experiment prompt input. Can be string or a key-value dict.
            filter (Optional[str]): The filter to use when running the prompt.
            force_action (Optional[str]): The action guid to enforce when running experiment prompt.
            session_guid (Optional[str]): The GUID of the session to run the prompt with.
            indices (Optional[List[int]]): An array of indices to be used when running the prompt.
            metadata_filter (Optional[dict]): The filter over the metadata to be applied during prompting
            streaming (Optional[bool]): Flag that defines whether to use streaming or not.
            async_mode (Optional[bool]): Boolean that identifies whether the async mode should be used. Defaults to False.

        Returns:
            An object result of running the prompt with the message and a feedback_url for providing feedback.
        """
        async with aiohttp.ClientSession() as session:
            client = self._get_api_client(session)

            try:
                response = await client.post(
                    PROMPT_EXPERIMENT_ENDPOINT.format(id=experiment_guid),
                    {
                        "input": input,
                        "filter": filter,
                        "indices": indices,
                        "streaming": streaming,
                        "session": session_guid,
                        "async_mode": async_mode,
                        "force_action": force_action,
                        "metadata_filter": metadata_filter,
                    },
                )
                return PromptResponse(**response)
            except ClientResponseError as e:
                if e.status == 404:
                    raise ExperimentNotFoundError(experiment_guid)

                raise UnknownKluAPIError(e.status, e.message)
            except Exception:
                raise UnknownKluError()
