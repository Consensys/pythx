from enum import Enum
import dateutil.parser


class AnalysisStatus(Enum):
    QUEUED = 1
    RUNNING = 2
    ERROR = 3
    FINISHED = 4


class Analysis:
    def __init__(
        self,
        uuid: str,
        api_version: str,
        mythril_version: str,
        maru_version: str,
        queue_time: int,
        run_time: int,
        status: AnalysisStatus,
        submitted_at: str,
        submitted_by: str,
    ):
        self.uuid = uuid
        self.api_version = api_version
        self.mythril_version = mythril_version
        self.maru_version = maru_version
        self.queue_time = queue_time
        self.run_time = run_time
        self.status = status
        self.submitted_at = dateutil.parser.parse(submitted_at)
        self.submitted_by = submitted_by
