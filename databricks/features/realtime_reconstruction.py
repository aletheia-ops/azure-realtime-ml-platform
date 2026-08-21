"""Offline reconstruction of real-time feature semantics.

This module is the Databricks-side implementation of features calculated live by
Azure Stream Analytics. Implementations must follow the shared feature contracts
and preserve event-time/window semantics for training-serving parity.
"""
