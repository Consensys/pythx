import json
import logging
from typing import Dict, List

from pythx.models.request.base import BaseRequest
from pythx.models.util import dict_delete_none_fields, resolve_schema

LOGGER = logging.getLogger(__name__)


class AnalysisSubmissionRequest(BaseRequest):
    """

    """
    with open(resolve_schema(__file__, "analysis-submission.json")) as sf:
        schema = json.load(sf)

    def __init__(
        self,
        contract_name: str = None,
        bytecode: str = None,
        source_map: str = None,
        deployed_bytecode: str = None,
        deployed_source_map: str = None,
        sources: Dict[str, Dict[str, str]] = None,
        source_list: List[str] = None,
        solc_version: str = None,
        analysis_mode: str = "quick",
    ):
        self.contract_name = contract_name
        self.bytecode = bytecode
        self.source_map = source_map
        self.deployed_bytecode = deployed_bytecode
        self.deployed_source_map = deployed_source_map
        self.sources = sources
        self.source_list = source_list
        self.solc_version = solc_version
        self.analysis_mode = analysis_mode

    @property
    def endpoint(self):
        """

        :return:
        """
        return "v1/analyses"

    @property
    def method(self):
        """

        :return:
        """
        return "POST"

    @property
    def parameters(self):
        """

        :return:
        """
        return {}

    @property
    def headers(self):
        """

        :return:
        """
        return {}

    @property
    def payload(self):
        """

        :return:
        """
        return {"data": self.to_dict()}

    @classmethod
    def from_dict(cls, d: Dict):
        """

        :param d:
        :return:
        """
        cls.validate(d)
        return cls(
            contract_name=d.get("contractName"),
            bytecode=d.get("bytecode"),
            source_map=d.get("sourceMap"),
            deployed_bytecode=d.get("deployedBytecode"),
            deployed_source_map=d.get("deployedSourceMap"),
            sources=d.get("sources"),
            source_list=d.get("sourceList"),
            solc_version=d.get("version"),
            analysis_mode=d.get("analysisMode"),
        )

    def to_dict(self):
        """

        :return:
        """
        base_dict = dict_delete_none_fields(
            {
                "contractName": self.contract_name,
                "bytecode": self.bytecode,
                "sourceMap": self.source_map,
                "deployedBytecode": self.deployed_bytecode,
                "deployedSourceMap": self.deployed_source_map,
                "sources": self.sources if self.sources else None,
                "sourceList": self.source_list if self.source_list else None,
                "version": self.solc_version,
                "analysisMode": self.analysis_mode,
            }
        )
        self.validate(base_dict)
        return base_dict
