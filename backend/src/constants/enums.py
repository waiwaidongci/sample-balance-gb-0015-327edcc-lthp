from enum import StrEnum
class Role(StrEnum):
    ADMIN='admin'
    ANALYST='analyst'
    VIEWER='viewer'
class RunStatus(StrEnum):
    QUEUED='queued'
    RUNNING='running'
    COMPLETED='completed'
    FAILED='failed'
class Dimension(StrEnum):
    ZONE='zone'
    AGE_BAND='age_band'
    MODE='mode'
