from datetime import datetime

import dateutil.parser

from pythx.models.request import (
    AnalysisListRequest,
    AnalysisStatusRequest,
    AnalysisSubmissionRequest,
    AuthLoginRequest,
    AuthLogoutRequest,
    AuthRefreshRequest,
    DetectedIssuesRequest,
    OASRequest,
    VersionRequest,
)
from pythx.models.response import (
    Analysis,
    AnalysisListResponse,
    AnalysisStatusResponse,
    AnalysisSubmissionResponse,
    AuthLoginResponse,
    AuthLogoutResponse,
    AuthRefreshResponse,
    DetectedIssuesResponse,
    Issue,
    OASResponse,
    Severity,
    SourceFormat,
    SourceLocation,
    SourceType,
    VersionResponse,
)

# BASE DATA
API_VERSION_1 = "v1.3.0"
API_VERSION_2 = "v1.4.0"
MARU_VERSION_1 = "v0.2.0"
MARU_VERSION_2 = "v0.3.0"
MYTHRIL_VERSION_1 = "0.19.11"
MYTHRIL_VERSION_2 = "0.20.1"
MAESTRO_VERSION_1 = "v1.1.4"
MAESTRO_VERSION_2 = "v1.1.5"
HARVEY_VERSION_1 = "0.0.8"
HARVEY_VERSION_2 = "0.0.9"
HASHED_VERSION_1 = "31337deadbeef"
HASHED_VERSION_2 = "31337cafebabe"

QUEUE_TIME_1 = 1
QUEUE_TIME_2 = 2
RUN_TIME_1 = 300
RUN_TIME_2 = 200

STATUS_1 = "In Progress"
STATUS_2 = "Finished"

SUBMITTED_AT_1 = "2019-01-10T01:29:38.410Z"
SUBMITTED_AT_2 = "2019-01-09T01:29:38.410Z"
SUBMITTED_BY_1 = "000008544b0aa00010a91111"
SUBMITTED_BY_2 = "000008544b0aa00010a91112"

ERROR = "my test error"

UUID_1 = "0680a1e2-b908-4c9a-a15b-636ef9b61486"
UUID_2 = "0680a1e2-b908-4c9a-a15b-636ef9b61487"

ACCESS_TOKEN_1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIzNmQ0OGI2Yi03ZjFiLTQ0NjEtYjI1OS1hM2M5MmQzMGI4NWQiLCJpc3MiOiJNeXRocmlsIEFQSSIsImV4cCI6MTU1MTAyNTg3OS4wMjgsInVzZXJJZCI6IjEyMzQ1Njc4OTAxMjM0NTY3ODkwMTIzNCIsImlhdCI6MTU1MTAyNTI3OX0.M9SGJayVcreihIFis406wmZLtq3kSsbiV5VAbIuCE0U"
ACCESS_TOKEN_2 = "some other access token"
REFRESH_TOKEN_1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyNDY3NzZkZC1iY2FjLTQ0NGItOGYwMy02ZDcyYWY3MjcwYWMiLCJpc3MiOiJNeXRocmlsIEFQSSIsImV4cCI6MTU1MzQ0NDQ3OS4wMjgsImlhdCI6MTU1MTAyNTI3OX0.iPRrfFZgnotvMuqu5shi4aQR9GCZR5kUjyzqTTQhZp8"
REFRESH_TOKEN_2 = "some other refresh token"

OFFSET = 0
DATE_FROM = "2019-02-07T00:40:49.058158"
DATE_TO = "2019-02-08T00:40:49.058158"

SWC_ID = "SWC-103"
SWC_TITLE = "Floating Pragma"
DESCRIPTION_HEAD = "A floating pragma is set."
DESCRIPTION_TAIL = 'It is recommended to make a conscious choice on what version of Solidity is used for compilation. Currently any version equal or greater than \\"0.4.24\\" is allowed.'
SEVERITY = "Low"
SOURCE_MAP = "48:1:0"
SOURCE_TYPE = "raw-bytecode"
SOURCE_FORMAT = "evm-byzantium-bytecode"
SOURCE_LIST = "/test/my-super-safe-contract.sol"

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

GLOBAL_LOGOUT = False
ETH_ADDRESS = "0x0"
PASSWORD = "supersecure1337"
MOCK_API_URL = "mock://test.com/path"


# ISSUE
SOURCE_LOCATION = {
    "sourceMap": SOURCE_MAP,
    "sourceType": SOURCE_TYPE,
    "sourceFormat": SOURCE_FORMAT,
    "sourceList": SOURCE_LIST,
}
ISSUE_DICT = {
    "swcID": SWC_ID,
    "swcTitle": SWC_TITLE,
    "description": {"head": DESCRIPTION_HEAD, "tail": DESCRIPTION_TAIL},
    "severity": SEVERITY,
    "locations": [SOURCE_LOCATION],
    "extra": {},
}
ISSUE_OBJECT = Issue(
    swc_id=SWC_ID,
    swc_title=SWC_TITLE,
    description_short=DESCRIPTION_HEAD,
    description_long=DESCRIPTION_TAIL,
    severity=Severity.LOW,
    locations=[
        SourceLocation(
            source_map=SOURCE_MAP,
            source_type=SourceType.RAW_BYTECODE,
            source_format=SourceFormat.EVM_BYZANTIUM_BYTECODE,
            source_list=SOURCE_LIST,
        )
    ],
    extra={},
)

# ANALYSIS
ANALYSIS_DICT = {
    "apiVersion": API_VERSION_1,
    "maruVersion": MARU_VERSION_1,
    "mythrilVersion": MYTHRIL_VERSION_1,
    "maestroVersion": MAESTRO_VERSION_1,
    "harveyVersion": HARVEY_VERSION_1,
    "queueTime": QUEUE_TIME_1,
    "status": STATUS_1,
    "submittedAt": SUBMITTED_AT_1,
    "submittedBy": SUBMITTED_BY_1,
    "uuid": UUID_1,
    "runTime": 0,
}
ANALYSIS_OBJECT = Analysis(
    uuid=UUID_1,
    api_version=API_VERSION_1,
    maru_version=MARU_VERSION_1,
    mythril_version=MYTHRIL_VERSION_1,
    maestro_version=MAESTRO_VERSION_1,
    harvey_version=HARVEY_VERSION_1,
    queue_time=QUEUE_TIME_1,
    status=STATUS_1,
    submitted_at=SUBMITTED_AT_1,
    submitted_by=SUBMITTED_BY_1,
)

# LOGIN
LOGIN_REQUEST_DICT = {"ethAddress": ETH_ADDRESS, "password": PASSWORD}
LOGIN_REQUEST_OBJECT = AuthLoginRequest(eth_address=ETH_ADDRESS, password=PASSWORD)
LOGIN_RESPONSE_DICT = {"access": ACCESS_TOKEN_1, "refresh": REFRESH_TOKEN_1}
LOGIN_RESPONSE_OBJECT = AuthLoginResponse(
    access_token=ACCESS_TOKEN_1, refresh_token=REFRESH_TOKEN_1
)

# LOGOUT
LOGOUT_REQUEST_DICT = LOGOUT = {"global": GLOBAL_LOGOUT}
LOGOUT_REQUEST_OBJECT = AuthLogoutRequest()
LOGOUT_RESPONSE_DICT = {}
LOGOUT_RESPONSE_OBJECT = AuthLogoutResponse()

# REFRESH
REFRESH_REQUEST_PAYLOAD_DICT = {
    "accessToken": ACCESS_TOKEN_1,
    "refreshToken": REFRESH_TOKEN_1,
}
REFRESH_REQUEST_DICT = LOGIN_RESPONSE_DICT
REFRESH_REQUEST_OBJECT = AuthRefreshRequest(
    access_token=ACCESS_TOKEN_1, refresh_token=REFRESH_TOKEN_1
)
REFRESH_RESPONSE_DICT = LOGIN_RESPONSE_DICT
REFRESH_RESPONSE_OBJECT = AuthRefreshResponse(
    access_token=ACCESS_TOKEN_1, refresh_token=REFRESH_TOKEN_1
)

# OPENAPI
OPENAPI_REQUEST_OBJECT = OASRequest(mode="yaml")
OPENAPI_RESPONSE = "openapi stuff"
OPENAPI_RESPONSE_OBJECT = OASResponse(data=OPENAPI_RESPONSE)

# VERSION
VERSION_REQUEST_OBJECT = VersionRequest()
VERSION_RESPONSE_DICT = {
    "api": API_VERSION_1,
    "maru": MARU_VERSION_1,
    "mythril": MYTHRIL_VERSION_1,
    "maestro": MAESTRO_VERSION_1,
    "harvey": HARVEY_VERSION_1,
    "hash": HASHED_VERSION_1,
}
VERSION_RESPONSE_OBJECT = VersionResponse(
    api_version=API_VERSION_1,
    maru_version=MARU_VERSION_1,
    mythril_version=MYTHRIL_VERSION_1,
    maestro_version=MAESTRO_VERSION_1,
    harvey_version=HARVEY_VERSION_1,
    hashed_version=HASHED_VERSION_1,
)

# ANALYSIS SUBMISSION
ANALYSIS_SUBMISSION_REQUEST_DICT = {
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
ANALYSIS_SUBMISSION_REQUEST_OBJECT = AnalysisSubmissionRequest(
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
ANALYSIS_SUBMISSION_RESPONSE_DICT = {
    "uuid": UUID_1,
    "apiVersion": API_VERSION_1,
    "maruVersion": MARU_VERSION_1,
    "mythrilVersion": MYTHRIL_VERSION_1,
    "maestroVersion": MAESTRO_VERSION_1,
    "harveyVersion": HARVEY_VERSION_1,
    "queueTime": QUEUE_TIME_1,
    "runTime": RUN_TIME_1,
    "status": STATUS_1,
    "submittedAt": SUBMITTED_AT_1,
    "submittedBy": SUBMITTED_BY_1,
}
ANALYSIS_SUBMISSION_RESPONSE_OBJECT = AnalysisSubmissionResponse(
    analysis=Analysis(
        uuid=UUID_1,
        api_version=API_VERSION_1,
        maru_version=MARU_VERSION_1,
        mythril_version=MYTHRIL_VERSION_1,
        maestro_version=MAESTRO_VERSION_1,
        harvey_version=HARVEY_VERSION_1,
        queue_time=QUEUE_TIME_1,
        run_time=RUN_TIME_1,
        status=STATUS_1,
        submitted_at=SUBMITTED_AT_1,
        submitted_by=SUBMITTED_BY_1,
    )
)

# ANALYSIS STATUS
ANALYSIS_STATUS_REQUEST_DICT = {"uuid": UUID_1}
ANALYSIS_STATUS_REQUEST_OBJECT = AnalysisStatusRequest(uuid=UUID_1)
ANALYSIS_STATUS_RESPONSE_DICT = ANALYSIS_SUBMISSION_RESPONSE_DICT
ANALYSIS_STATUS_RESPONSE_OBJECT = AnalysisStatusResponse(
    analysis=Analysis(
        uuid=UUID_1,
        api_version=API_VERSION_1,
        maru_version=MARU_VERSION_1,
        mythril_version=MYTHRIL_VERSION_1,
        maestro_version=MAESTRO_VERSION_1,
        harvey_version=HARVEY_VERSION_1,
        queue_time=QUEUE_TIME_1,
        run_time=RUN_TIME_1,
        status=STATUS_1,
        submitted_at=SUBMITTED_AT_1,
        submitted_by=SUBMITTED_BY_1,
    )
)

# ANALYSIS LIST
ANALYSIS_LIST_REQUEST_DICT = {
    "offset": OFFSET,
    "dateFrom": DATE_FROM,
    "dateTo": DATE_TO,
}
ANALYSIS_LIST_REQUEST_OBJECT = AnalysisListRequest(
    offset=OFFSET,
    date_from=dateutil.parser.parse(DATE_FROM),
    date_to=dateutil.parser.parse(DATE_TO),
)
ANALYSIS_LIST_RESPONSE_DICT = {
    "analyses": [
        {
            "uuid": UUID_1,
            "apiVersion": API_VERSION_1,
            "maruVersion": MARU_VERSION_1,
            "mythrilVersion": MYTHRIL_VERSION_1,
            "maestroVersion": MAESTRO_VERSION_1,
            "harveyVersion": HARVEY_VERSION_1,
            "queueTime": QUEUE_TIME_1,
            "runTime": RUN_TIME_1,
            "status": STATUS_1,
            "submittedAt": SUBMITTED_AT_1,
            "submittedBy": SUBMITTED_BY_1,
        },
        {
            "uuid": UUID_2,
            "apiVersion": API_VERSION_2,
            "maruVersion": MARU_VERSION_2,
            "mythrilVersion": MYTHRIL_VERSION_2,
            "maestroVersion": MAESTRO_VERSION_2,
            "harveyVersion": HARVEY_VERSION_2,
            "queueTime": QUEUE_TIME_2,
            "runTime": RUN_TIME_2,
            "status": STATUS_2,
            "submittedAt": SUBMITTED_AT_2,
            "submittedBy": SUBMITTED_BY_2,
        },
    ],
    "total": 2,
}
ANALYSIS_LIST_RESPONSE_OBJECT = AnalysisListResponse(
    analyses=[
        Analysis(
            uuid=UUID_1,
            api_version=API_VERSION_1,
            maru_version=MARU_VERSION_1,
            mythril_version=MYTHRIL_VERSION_1,
            maestro_version=MAESTRO_VERSION_1,
            harvey_version=HARVEY_VERSION_1,
            queue_time=QUEUE_TIME_1,
            run_time=RUN_TIME_1,
            status=STATUS_1,
            submitted_at=SUBMITTED_AT_1,
            submitted_by=SUBMITTED_BY_1,
        ),
        Analysis(
            uuid=UUID_2,
            api_version=API_VERSION_2,
            maru_version=MARU_VERSION_2,
            mythril_version=MYTHRIL_VERSION_2,
            maestro_version=MAESTRO_VERSION_2,
            harvey_version=HARVEY_VERSION_2,
            queue_time=QUEUE_TIME_2,
            run_time=RUN_TIME_2,
            status=STATUS_2,
            submitted_at=SUBMITTED_AT_2,
            submitted_by=SUBMITTED_BY_2,
        ),
    ],
    total=2,
)

# DETECTED ISSUES
DETECTED_ISSUES_REQUEST_DICT = {"uuid": UUID_1}
DETECTED_ISSUES_REQUEST_OBJECT = DetectedIssuesRequest(uuid=UUID_1)
DETECTED_ISSUES_RESPONSE_DICT = [
    {
        "issues": [
            {
                "swcID": SWC_ID,
                "swcTitle": SWC_TITLE,
                "description": {"head": DESCRIPTION_HEAD, "tail": DESCRIPTION_TAIL},
                "severity": SEVERITY,
                "locations": [
                    {
                        "sourceMap": SOURCE_MAP,
                        "sourceType": SOURCE_TYPE,
                        "sourceFormat": SOURCE_FORMAT,
                        "sourceList": SOURCE_LIST,
                    }
                ],
                "extra": {},
            }
        ],
        "sourceType": SOURCE_TYPE,
        "sourceFormat": SOURCE_FORMAT,
        "sourceList": SOURCE_LIST,
        "meta": {},
    }
]
DETECTED_ISSUES_RESPONSE_OBJECT = DetectedIssuesResponse(
    issues=[ISSUE_OBJECT],
    source_type=SourceType.RAW_BYTECODE,
    source_format=SourceFormat.EVM_BYZANTIUM_BYTECODE,
    source_list=SOURCE_LIST,
    meta_data={},
)
