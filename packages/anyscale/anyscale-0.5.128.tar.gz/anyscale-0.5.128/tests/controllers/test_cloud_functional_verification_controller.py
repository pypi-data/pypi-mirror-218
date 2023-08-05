from typing import Iterator, List
from unittest.mock import MagicMock, Mock, patch

from click import ClickException
import pytest

from anyscale.client.openapi_client.models.cloud_providers import CloudProviders
from anyscale.controllers.cloud_functional_verification_controller import (
    CloudFunctionalVerificationController,
    CloudFunctionalVerificationType,
)
from anyscale.sdk.anyscale_client.models.compute_template_query import (
    ComputeTemplateQuery,
)


@pytest.fixture(autouse=True)
def mock_auth_api_client(base_mock_anyscale_api_client: Mock) -> Iterator[None]:
    mock_auth_api_client = Mock(
        api_client=Mock(), anyscale_api_client=base_mock_anyscale_api_client,
    )
    with patch.multiple(
        "anyscale.controllers.base_controller",
        get_auth_api_client=Mock(return_value=mock_auth_api_client),
    ):
        yield


@pytest.mark.parametrize("cloud_provider", [CloudProviders.AWS, CloudProviders.GCP])
@pytest.mark.parametrize("compute_config_exists", [True, False])
def test_get_or_create_cluster_compute(
    compute_config_exists: bool, cloud_provider: CloudProviders,
) -> None:
    mock_cloud_id = "mock_cloud_id"
    mock_cluster_compute_id = "mock_cluster_compute_id"
    mock_api_client = Mock()
    mock_api_client.search_compute_templates_api_v2_compute_templates_search_post = Mock(
        return_value=Mock(
            results=[Mock(id=mock_cluster_compute_id)] if compute_config_exists else []
        )
    )
    mock_anyscale_api_client = Mock()
    mock_anyscale_api_client.create_cluster_compute = Mock(
        return_value=Mock(result=Mock(id=mock_cluster_compute_id))
    )

    funciontal_verification_controller = CloudFunctionalVerificationController()
    funciontal_verification_controller.api_client = mock_api_client
    funciontal_verification_controller.anyscale_api_client = mock_anyscale_api_client
    assert (
        funciontal_verification_controller.get_or_create_cluster_compute(
            mock_cloud_id, cloud_provider
        )
        == mock_cluster_compute_id
    )

    mock_api_client.search_compute_templates_api_v2_compute_templates_search_post.assert_called_with(
        ComputeTemplateQuery(
            orgwide=True,
            name={"equals": f"functional_verification_{mock_cloud_id}"},
            include_anonymous=True,
        )
    )

    if compute_config_exists:
        mock_anyscale_api_client.create_cluster_compute.assert_not_called()
    else:
        mock_anyscale_api_client.create_cluster_compute.assert_called_once()


@pytest.mark.parametrize(
    ("prepare_verification_failed", "create_workspace_failed"),
    [
        pytest.param(False, False, id="happy-path"),
        pytest.param(True, False, id="prepare-verification-failed"),
        pytest.param(False, True, id="create-workspace-failed"),
    ],
)
def test_create_workspace(
    prepare_verification_failed: bool, create_workspace_failed: bool
):
    expected_result = not prepare_verification_failed and not create_workspace_failed
    mock_prepare_verification = Mock(return_value=(Mock(), Mock(), Mock()))
    if prepare_verification_failed:
        mock_prepare_verification.side_effect = ClickException("mock error")
    mock_create_workspace = Mock()
    if create_workspace_failed:
        mock_create_workspace.side_effect = ClickException("mock error")
    with patch.multiple(
        "anyscale.controllers.cloud_functional_verification_controller.CloudFunctionalVerificationController",
        _prepare_verification=mock_prepare_verification,
    ):
        controller = CloudFunctionalVerificationController()
        controller.api_client.create_workspace_api_v2_experimental_workspaces_post = (
            mock_create_workspace
        )
        if expected_result:
            controller.create_workspace(Mock(), Mock())
        else:
            with pytest.raises(ClickException):
                controller.create_workspace(Mock(), Mock())


@pytest.mark.parametrize(
    (
        "create_workspace_succeed",
        "poll_until_active_succeed",
        "terminate_workspace_succeed",
        "expected_result",
    ),
    [
        pytest.param(True, True, True, True, id="happy-path",),
        pytest.param(False, False, False, False, id="create-workspace-failed",),
        pytest.param(True, False, False, False, id="poll-until-active-failed",),
        pytest.param(True, True, False, False, id="workspace-termination-failed",),
    ],
)
def test_verify_workspace(
    create_workspace_succeed: bool,
    poll_until_active_succeed: bool,
    terminate_workspace_succeed: bool,
    expected_result: bool,
):
    mock_create_task = MagicMock()

    mock_terminate_workspace = (
        Mock()
        if terminate_workspace_succeed
        else Mock(side_effect=ClickException("mock error"))
    )
    with patch.multiple(
        "anyscale.controllers.cloud_functional_verification_controller.CloudFunctionalVerificationController",
        create_workspace=Mock()
        if create_workspace_succeed
        else Mock(side_effect=ClickException("mock error")),
        poll_until_active=Mock()
        if poll_until_active_succeed
        else Mock(side_effect=ClickException("mock error")),
        _create_task=mock_create_task,
    ):
        controller = CloudFunctionalVerificationController()
        controller.anyscale_api_client.terminate_cluster = mock_terminate_workspace
        assert controller.verify_workspace(Mock(), Mock()) == expected_result
        task_count = 1 + create_workspace_succeed + poll_until_active_succeed
        assert mock_create_task.call_count == task_count


@pytest.mark.parametrize(
    ("get_current_status_error", "status_not_allowed", "expected_result"),
    [
        pytest.param(False, False, True, id="happy-path"),
        pytest.param(True, False, False, id="get-current-status-error"),
        pytest.param(False, True, False, id="status-not-allowed"),
    ],
)
def test_poll_until_active(
    get_current_status_error, status_not_allowed, expected_result
):
    mock_function = Mock()
    mock_function_id = "mock_function_id"
    goal_status = "goal_status"
    mock_get_current_status = Mock(
        return_value="not_allowed" if status_not_allowed else goal_status
    )
    if get_current_status_error:
        mock_get_current_status.side_effect = ClickException("mock error")
    with patch.multiple(
        "anyscale.controllers.cloud_functional_verification_controller.CloudFunctionalVerificationController",
        _update_task_in_step_progress=Mock(),
    ), patch.multiple(
        "anyscale.controllers.cloud_functional_verification_controller",
        POLL_INTERVAL_SECONDS=0,
    ):
        controller = CloudFunctionalVerificationController()
        if expected_result:
            assert (
                controller.poll_until_active(
                    mock_function,
                    mock_function_id,
                    mock_get_current_status,
                    goal_status,
                    set(goal_status),
                    Mock(),
                    1,
                )
                == expected_result
            )
            mock_get_current_status.assert_called_once_with(mock_function_id)
        else:
            with pytest.raises(ClickException) as e:
                controller.poll_until_active(
                    mock_function,
                    mock_function_id,
                    mock_get_current_status,
                    goal_status,
                    set(goal_status),
                    Mock(),
                    1,
                )
                if get_current_status_error:
                    assert e.match("Failed to get")
                if status_not_allowed:
                    assert e.match("is in an unexpected state:")


def test_poll_until_active_timeout():
    mock_function = Mock()
    mock_function_id = "mock_function_id"
    goal_status = "goal_status"
    mock_status = "mock_status"
    allowed_status_set = {goal_status, mock_status}
    mock_get_current_status = Mock(return_value=mock_status)
    with patch.multiple(
        "anyscale.controllers.cloud_functional_verification_controller.CloudFunctionalVerificationController",
        _update_task_in_step_progress=Mock(),
    ), patch.multiple(
        "anyscale.controllers.cloud_functional_verification_controller",
        POLL_INTERVAL_SECONDS=0,
    ), pytest.raises(
        ClickException
    ) as e:
        controller = CloudFunctionalVerificationController()
        assert (
            controller.poll_until_active(
                mock_function,
                mock_function_id,
                mock_get_current_status,
                goal_status,
                allowed_status_set,
                Mock(),
                0,
            )
            is False
        )
        assert e.match("Timed out")


@pytest.mark.parametrize("verification_result", [True, False])
@pytest.mark.parametrize("cloud_provider", [CloudProviders.AWS, CloudProviders.GCP])
@pytest.mark.parametrize(
    "functions_to_verify", [[CloudFunctionalVerificationType.WORKSPACE]]
)
def test_start_verification(
    functions_to_verify: List[CloudFunctionalVerificationType],
    cloud_provider: CloudProviders,
    verification_result: bool,
):
    # TODO (congding): add test case for "service"
    mock_cloud_id = "mock_cloud_id"

    with patch.multiple(
        "anyscale.controllers.cloud_functional_verification_controller.CloudFunctionalVerificationController",
        verify=Mock(return_value=verification_result),
        get_live_console=MagicMock(),
    ):
        funciontal_verification_controller = CloudFunctionalVerificationController()
        assert (
            funciontal_verification_controller.start_verification(
                mock_cloud_id, cloud_provider, functions_to_verify, yes=True
            )
            == verification_result
        )


@pytest.mark.parametrize(
    "functions_to_verify", [[CloudFunctionalVerificationType.WORKSPACE]]
)
def test_get_live_console(functions_to_verify):
    funciontal_verification_controller = CloudFunctionalVerificationController()
    funciontal_verification_controller.get_live_console(functions_to_verify)
    for function in functions_to_verify:
        assert funciontal_verification_controller.step_progress[function] is not None
        assert funciontal_verification_controller.overall_progress[function] is not None
        assert funciontal_verification_controller.task_ids[function] is not None
