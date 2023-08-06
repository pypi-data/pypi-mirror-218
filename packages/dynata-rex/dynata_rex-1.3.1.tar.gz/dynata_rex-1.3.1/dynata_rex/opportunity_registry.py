"""
Package: src.smor
Filename: api.py
Author(s): Grant W

Description: API interaction for smor
"""
# Python Imports
import json
from typing import List

# Third Party Imports
import pydantic

# Local Imports
import dynata_rex.models as models
from .signer import RexRequest
from .logs import logger
from .exceptions import InvalidShardException


class OpportunityRegistry:
    _BASE_URL = 'https://registry.rex.dynata.com'

    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 base_url: str = _BASE_URL,
                 default_ttl: int = 10,
                 shard_count: int = 1,
                 current_shard: int = 1):
        """
        @access_key: liam access key for REX
        @secret_key: liam secret key for REX

        # Optional
        @base_url  : url of Opportunity Registry
        @shard_count  : number of total shards consuming Opportunity Registry
        @current_shard: curent shard
        @default_ttl: time to live for signature in seconds
        """
        self.default_ttl = default_ttl
        self.make_request = RexRequest(access_key,
                                       secret_key,
                                       default_ttl=default_ttl)
        self.base_url = self._format_base_url(base_url)

        if current_shard > shard_count:
            raise InvalidShardException
        self.shard_count = shard_count
        self.current_shard = current_shard

    def _format_base_url(self, url):
        """Make sure our URL starts with http, and if not add https://
        prefix"""
        if url.startswith('http'):
            return url
        return f"https://{url}"

    def _get_opportunity(self, opportunity_id: int) -> dict:
        """Raw get opportunity"""
        endpoint = f"{self.base_url}/get-opportunity"
        data = {"id": opportunity_id}
        return self.make_request.post(endpoint, data)

    def _list_opportunities(self, limit: int = 10) -> List[dict]:
        """
        [Deprecated - please use _receive_notifications()]
        Raw get opportunities"""
        endpoint = f"{self.base_url}/list-opportunities"
        data = {
            "limit": limit,
            "shards": {
                "count": self.shard_count,
                "current": self.current_shard
            }
        }
        return self.make_request.post(endpoint, data)

    def _receive_notifications(self, limit: int = 10) -> List[dict]:
        """Raw receive notifications"""
        endpoint = f"{self.base_url}/receive-notifications"
        data = {
            "limit": limit,
            "shards": {
                "count": self.shard_count,
                "current": self.current_shard
            }
        }
        return self.make_request.post(endpoint, data)

    def _receive_invites(self, limit: int = 10) -> list[dict]:
        """Raw receive invites"""
        endpoint = f"{self.base_url}/receive_invites"
        data = {
            "limit": limit
        }
        return self.make_request.post(endpoint, data)

    def list_opportunities(self, limit: int = 10) -> List[models.Opportunity]:
        """
        [Deprecated - please use receive_notifications()]
        Get opportunities from Opportunity Registry"""
        opportunities = self._list_opportunities(limit=limit)
        out = []
        for opp in opportunities:
            try:
                out.append(models.Opportunity(**opp))
            except pydantic.error_wrappers.ValidationError:
                opportunity_id = opp['id']
                logger.warning(
                    f"Unable to parse {opportunity_id}, excluding...")
                logger.warning(json.dumps(opp, indent=4))
                # Ack opportunity so we don't see it again
                self.ack_opportunity(opportunity_id)

        return out

    def receive_notifications(self,
                              limit: int = 10) -> List[models.Opportunity]:
        """Get opportunity notifications from Opportunity Registry"""
        opportunities = self._receive_notifications(limit=limit)
        out = []
        for opp in opportunities:
            try:
                out.append(models.Opportunity(**opp))
            except pydantic.error_wrappers.ValidationError:
                opportunity_id = opp['id']
                logger.warning(
                    f"Unable to parse {opportunity_id}, excluding...")
                logger.warning(json.dumps(opp, indent=4))
                # Ack notification so we don't see it again
                self.ack_notification(opportunity_id)

        return out

    def get_opportunity(self, opportunity_id: int) -> models.Opportunity:
        """Get specific opportunity from SMOR
        """
        opportunity = self._get_opportunity(opportunity_id)
        return models.Opportunity(**opportunity)

    def list_project_opportunities(self, project_id: int) -> List[int]:
        """List related opportunities from a project id"""
        endpoint = f"{self.base_url}/list-project-opportunities"
        data = {"project_id": project_id}
        return self.make_request.post(endpoint, data)

    def ack_opportunity(self, opportunity_id: int) -> None:
        """
        [Deprecated - please use ack_notification()]
        Acknowledge a single opportunity"""
        data = [opportunity_id]
        return self.ack_opportunities(data)

    def ack_notification(self, opportunity_id: int) -> None:
        """Acknowledge a single notification"""
        data = [opportunity_id]
        return self.ack_notifications(data)

    def ack_opportunities(self, opportunities: List[int]) -> None:
        """
        [Deprecated - please use ack_notifications()]
        Acknowledge a list of opportunities"""
        endpoint = f"{self.base_url}/ack-opportunities"
        res = self.make_request.post(endpoint, opportunities)
        return res

    def ack_notifications(self, opportunities: List[int]) -> None:
        """Acknowledge a list of notifications"""
        endpoint = f"{self.base_url}/ack-notifications"
        res = self.make_request.post(endpoint, opportunities)
        return res

    def download_collection(self, collection_id: str) -> list:
        """Download targeting from a collection cell"""
        endpoint = f"{self.base_url}/download-collection"
        data = {"id": str(collection_id)}
        res = self.make_request.post(endpoint, data)
        return str(res).split('\n')

    def ack_invites(self, invites: list[int]) -> None:
        """Acknowledge a list of invites"""
        endpoint = f"{self.base_url}/ack-invites"
        res = self.make_request.post(endpoint, invites)
        return res

    def receive_invites(self, limit: int = 10) -> List[models.Invite]:
        """Receive invites from opportunity registry"""
        invites = self._receive_invites(limit=limit)
        out = []
        for inv in invites:
            try:
                out.append(models.Invite(**inv))
            except pydantic.error_wrappers.ValidationError:
                invite_id = inv['id']
                logger.warning(
                    f"Unable to parse {invite_id}, excluding...")
                logger.warning(json.dumps(inv, indent=4))
                # Ack invites so we don't see it again
                self.ack_invites(invite_id)
        return out

    def download_invite_collection(self, invite_id: str) -> list:
        """Download invite collection from opportunity registry"""
        endpoints = f"{self.base_url}/download-invite-collection"
        data = {"id": invite_id}
        res = self.make_request.post(endpoints, data)
        return str(res).split('\n')
