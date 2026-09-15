from pathlib import Path


WORKFLOWS_DIR = Path(__file__).parents[2] / "workflows"

EXTERNAL_PR_GUARD = (
    "if: github.event_name != 'pull_request' || "
    "(github.actor != 'dependabot[bot]' && "
    "github.event.pull_request.head.repo.full_name == github.repository)"
)


def _workflow(name: str) -> str:
    return (WORKFLOWS_DIR / name).read_text()


def test_cloud_tests_skip_aws_backed_jobs_for_untrusted_pull_requests() -> None:
    workflow = _workflow("cloud-tests.yml")

    assert EXTERNAL_PR_GUARD in workflow
    assert "aws-actions/configure-aws-credentials" in workflow


def test_conformance_discovery_skips_untrusted_pull_requests() -> None:
    workflow = _workflow("conformance-tests.yml")

    assert EXTERNAL_PR_GUARD in workflow
    assert "aws-actions/configure-aws-credentials" in workflow


def test_opentelemetry_conformance_skips_untrusted_pull_requests() -> None:
    workflow = _workflow("opentelemetry-conformance-tests.yml")

    assert EXTERNAL_PR_GUARD in workflow
    assert "CONFORMANCE_TEST_ROLE_ARN: ${{ secrets.TEST_ROLE_ARN }}" in workflow
