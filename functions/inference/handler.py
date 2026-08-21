"""Application-level inference request handling.

Expected responsibilities: validate a live-feature request, map it to the serving
contract, call the model-serving client, and return a structured response.
Heavy feature engineering does not belong here.
"""
