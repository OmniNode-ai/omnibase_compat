# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class ProtocolDataSource(Protocol):
    """Protocol for tabular data source adapters.

    Matches the DataSource interface used by omnimarket's data
    verification node. Implementations query table metadata and
    sample rows for post-pipeline data quality checks.
    """

    def get_row_count(self, table_name: str) -> int:
        """Return total row count for the given table."""
        ...

    def get_sample_rows(
        self, table_name: str, sample_size: int
    ) -> list[dict[str, str]]:
        """Return up to sample_size rows from the given table."""
        ...

    def get_columns(self, table_name: str) -> list[str]:
        """Return column names for the given table."""
        ...
