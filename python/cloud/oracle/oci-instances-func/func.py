import base64
import os

from oci.core import compute_client
from oci import pagination


try:
    import pytest

    def test_list_instances():
        test_config, test_compartment_id = create_signer()
        oci_compute = compute_client.ComputeClient(test_config)
        result = pagination.list_call_get_all_results(
            oci_compute.list_instances,
            test_compartment_id
        )
        assert len(result.data) >= 0

except ImportError:
    pass


def ensure_env_var(key):
    val = os.environ.get(key)
    if not val:
        raise Exception(f"{val} is not set")

    return val


def create_signer():
    compartment_id = ensure_env_var("OCI_COMPARTMENT")

    config = {
        "key_content": base64.b64decode(
            ensure_env_var("OCI_PRIVATE_KEY_BASE64")),
        "pass_phrase": os.environ.get("OCI_PRIVATE_KEY_PASS", ""),
        "user": ensure_env_var("OCI_USER"),
        "tenancy": ensure_env_var("OCI_TENANCY"),
        "fingerprint": ensure_env_var("OCI_FINGERPRINT"),
        "region": ensure_env_var("OCI_REGION"),
    }

    return config, compartment_id


def handler(ctx, data=None):
    config, compartment_id = create_signer()
    oci_compute = compute_client.ComputeClient(config)
    result = pagination.list_call_get_all_results(
        oci_compute.list_instances,
        compartment_id
    )

    return f"I have {len(result.data)} instances."