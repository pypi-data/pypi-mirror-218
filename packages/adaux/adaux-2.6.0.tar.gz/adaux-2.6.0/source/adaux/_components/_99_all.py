# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
from ._03_meta import MetaMixin
from ._04_monotonic_version import MonotonicVersionMixin
from ._05_project import ProjectMixin
from ._06_dependency import DependencyMixin
from ._07_package import PackageMixin
from ._08_pip import PipMixin
from ._09_gitignore import GitIgnoreMixin
from ._10_gitlab import GitlabMixin
from ._11_precommit import PrecommitMixin
from ._12_pylint import PylintMixin
from ._13_executable import ExecutablesMixin
from ._14_mypy import MypyMixin
from ._15_pytest import PytestMixin
from ._16_coverage import CoverageMixin
from ._17_docs import DocsMixin
from ._18_payload import PayloadMixin
from ._19_docker import DockerMixin
from ._20_ci import CiMixin
from ._98_sentinel import SentinelMixin

__all__ = ["AllComponents"]


class AllComponents(  # pylint: disable=too-many-ancestors
    SentinelMixin,
    DocsMixin,
    CiMixin,
    DockerMixin,
    PayloadMixin,
    PackageMixin,
    ExecutablesMixin,
    PylintMixin,
    MypyMixin,
    PrecommitMixin,
    CoverageMixin,
    PytestMixin,
    PipMixin,
    DependencyMixin,
    GitlabMixin,
    GitIgnoreMixin,
    ProjectMixin,
    MonotonicVersionMixin,
    MetaMixin,
):
    pass
