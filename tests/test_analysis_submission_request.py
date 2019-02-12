import json

import pytest

from pythx.models.exceptions import RequestDecodeError, RequestValidationError
from pythx.models.request import AnalysisSubmissionRequest

CONTRACT_NAME = "PublicStorageArray"
BYTECODE = "60806040526020604051908101604052806000600102815250600090600161002892919061003b565b5034801561003557600080fd5b506100ad565b828054828255906000526020600020908101928215610077579160200282015b8281111561007657825182559160200191906001019061005b565b5b5090506100849190610088565b5090565b6100aa91905b808211156100a657600081600090555060010161008e565b5090565b90565b60dd806100bb6000396000f3fe608060405260043610603f576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063017a9105146044575b600080fd5b348015604f57600080fd5b50607960048036036020811015606457600080fd5b8101908080359060200190929190505050608f565b6040518082815260200191505060405180910390f35b600081815481101515609d57fe5b90600052602060002001600091509050548156fea165627a7a72305820477e0888fcd92cabf059fb331003e0f0bc4dc7d0617752544f0c9a0fc80970aa0029"
SOURCE_MAP = "25:75:0:-;;;59:38;;;;;;;;;94:1;86:10;;59:38;;;;;;;;;;;:::i;:::-;;25:75;8:9:-1;5:2;;;30:1;27;20:12;5:2;25:75:0;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;:::i;:::-;;;:::o;:::-;;;;;;;;;;;;;;;;;;;;;;;;;;;:::o;:::-;;;;;;;"
DEPLOYED_BYTECODE = "608060405260043610603f576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063017a9105146044575b600080fd5b348015604f57600080fd5b50607960048036036020811015606457600080fd5b8101908080359060200190929190505050608f565b6040518082815260200191505060405180910390f35b600081815481101515609d57fe5b90600052602060002001600091509050548156fea165627a7a72305820477e0888fcd92cabf059fb331003e0f0bc4dc7d0617752544f0c9a0fc80970aa0029"
DEPLOYED_SOURCE_MAP = "25:75:0:-;;;;;;;;;;;;;;;;;;;;;;;;59:38;;8:9:-1;5:2;;;30:1;27;20:12;5:2;59:38:0;;;;;;13:2:-1;8:3;5:11;2:2;;;29:1;26;19:12;2:2;59:38:0;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;:::o"
SOURCES = {
    "PublicStorageArray.sol": {
        "source": "pragma solidity ^0.5.0;\n\ncontract PublicStorageArray {\n    bytes32[] public states = [bytes32(0)];\n}",
        "ast": '{"contracts":{"/tmp/test.sol:PublicStorageArray":{}},"sourceList":["/tmp/test.sol"],"sources":{"/tmp/test.sol":{"AST":{"attributes":{"absolutePath":"/tmp/test.sol","exportedSymbols":{"PublicStorageArray":[9]}},"children":[{"attributes":{"literals":["solidity","^","0.5",".0"]},"id":1,"name":"PragmaDirective","src":"0:23:0"},{"attributes":{"baseContracts":[null],"contractDependencies":[null],"contractKind":"contract","documentation":null,"fullyImplemented":true,"linearizedBaseContracts":[9],"name":"PublicStorageArray","scope":10},"children":[{"attributes":{"constant":false,"name":"states","scope":9,"stateVariable":true,"storageLocation":"default","type":"bytes32[]","visibility":"public"},"children":[{"attributes":{"length":null,"type":"bytes32[]"},"children":[{"attributes":{"name":"bytes32","type":"bytes32"},"id":2,"name":"ElementaryTypeName","src":"59:7:0"}],"id":3,"name":"ArrayTypeName","src":"59:9:0"},{"attributes":{"argumentTypes":null,"isConstant":false,"isInlineArray":true,"isLValue":false,"isPure":true,"lValueRequested":false,"type":"bytes32[1] memory"},"children":[{"attributes":{"argumentTypes":null,"isConstant":false,"isLValue":false,"isPure":true,"isStructConstructorCall":false,"lValueRequested":false,"names":[null],"type":"bytes32","type_conversion":true},"children":[{"attributes":{"argumentTypes":[{"typeIdentifier":"t_rational_0_by_1","typeString":"int_const 0"}],"isConstant":false,"isLValue":false,"isPure":true,"lValueRequested":false,"type":"type(bytes32)","value":"bytes32"},"id":4,"name":"ElementaryTypeNameExpression","src":"86:7:0"},{"attributes":{"argumentTypes":null,"hexvalue":"30","isConstant":false,"isLValue":false,"isPure":true,"lValueRequested":false,"subdenomination":null,"token":"number","type":"int_const 0","value":"0"},"id":5,"name":"Literal","src":"94:1:0"}],"id":6,"name":"FunctionCall","src":"86:10:0"}],"id":7,"name":"TupleExpression","src":"85:12:0"}],"id":8,"name":"VariableDeclaration","src":"59:38:0"}],"id":9,"name":"ContractDefinition","src":"25:75:0"}],"id":10,"name":"SourceUnit","src":"0:102:0"}}},"version":"0.5.0+commit.1d4f565a.Linux.g++"}',
    }
}
SOURCE_LIST = ["PublicStorageArray.sol"]
SOLC_VERSION = "0.5.0+commit.1d4f565a.Linux.g++"
ANALYSIS_MODE = "full"


VALID_SUBMISSION = {
    "contractName": CONTRACT_NAME,
    "bytecode": BYTECODE,
    "sourceMap": SOURCE_MAP,
    "deployedBytecode": DEPLOYED_BYTECODE,
    "deployedSourceMap": DEPLOYED_SOURCE_MAP,
    "sources": SOURCES,
    "sourceList": SOURCE_LIST,
    "version": SOLC_VERSION,
    "analysisMode": ANALYSIS_MODE,
}
VALID_SUBMISSION_REQUEST = AnalysisSubmissionRequest(
    contract_name=CONTRACT_NAME,
    bytecode=BYTECODE,
    source_map=SOURCE_MAP,
    deployed_bytecode=DEPLOYED_BYTECODE,
    deployed_source_map=DEPLOYED_SOURCE_MAP,
    sources=SOURCES,
    source_list=SOURCE_LIST,
    solc_version=SOLC_VERSION,
    analysis_mode=ANALYSIS_MODE,
)


def assert_submission_request(req: AnalysisSubmissionRequest):
    assert req.contract_name == CONTRACT_NAME
    assert req.bytecode == BYTECODE
    assert req.source_map == SOURCE_MAP
    assert req.deployed_bytecode == DEPLOYED_BYTECODE
    assert req.deployed_source_map == DEPLOYED_SOURCE_MAP
    assert req.sources == SOURCES
    assert req.solc_version == SOLC_VERSION
    assert req.analysis_mode == ANALYSIS_MODE


def test_analysis_submission_request_from_valid_json():
    req = AnalysisSubmissionRequest.from_json(json.dumps(VALID_SUBMISSION))
    assert_submission_request(req)


def test_analysis_submission_request_from_invalid_json():
    with pytest.raises(RequestDecodeError):
        AnalysisSubmissionRequest.from_json("{}")


def test_analysis_submission_request_from_valid_dict():
    req = AnalysisSubmissionRequest.from_dict(VALID_SUBMISSION)
    assert_submission_request(req)


def test_analysis_submission_request_from_invalid_dict():
    with pytest.raises(RequestDecodeError):
        AnalysisSubmissionRequest.from_dict({})


def test_analysis_submission_request_to_json():
    assert json.loads(VALID_SUBMISSION_REQUEST.to_json()) == VALID_SUBMISSION


def test_analysis_submission_request_to_dict():
    assert VALID_SUBMISSION_REQUEST.to_dict() == VALID_SUBMISSION


def test_analysis_submission_request_bytecode_only():
    req = AnalysisSubmissionRequest(bytecode=BYTECODE)
    assert req.bytecode == BYTECODE
    assert req.analysis_mode == "quick"  # default value
    assert req.to_dict() == {"bytecode": BYTECODE, "analysisMode": "quick"}
    assert json.loads(req.to_json()) == {"bytecode": BYTECODE, "analysisMode": "quick"}


def test_analysis_submission_request_source_only():
    req = AnalysisSubmissionRequest(sources=SOURCES)
    assert req.sources == SOURCES
    assert req.analysis_mode == "quick"  # default value
    assert req.to_dict() == {"sources": SOURCES, "analysisMode": "quick"}
    assert json.loads(req.to_json()) == {"sources": SOURCES, "analysisMode": "quick"}


def test_analysis_submission_request_invalid_mode():
    req = AnalysisSubmissionRequest(bytecode=BYTECODE, analysis_mode="invalid")
    with pytest.raises(RequestValidationError):
        req.validate()


def test_analysis_submission_request_missing_field():
    req = AnalysisSubmissionRequest()
    with pytest.raises(RequestValidationError):
        req.validate()
