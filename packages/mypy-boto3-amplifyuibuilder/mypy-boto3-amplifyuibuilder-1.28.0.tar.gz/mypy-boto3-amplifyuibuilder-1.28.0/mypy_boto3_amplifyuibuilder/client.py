"""
Type annotations for amplifyuibuilder service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_amplifyuibuilder.client import AmplifyUIBuilderClient

    session = Session()
    client: AmplifyUIBuilderClient = session.client("amplifyuibuilder")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ExportComponentsPaginator,
    ExportFormsPaginator,
    ExportThemesPaginator,
    ListCodegenJobsPaginator,
    ListComponentsPaginator,
    ListFormsPaginator,
    ListThemesPaginator,
)
from .type_defs import (
    CreateComponentDataTypeDef,
    CreateComponentResponseTypeDef,
    CreateFormDataTypeDef,
    CreateFormResponseTypeDef,
    CreateThemeDataTypeDef,
    CreateThemeResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ExchangeCodeForTokenRequestBodyTypeDef,
    ExchangeCodeForTokenResponseTypeDef,
    ExportComponentsResponseTypeDef,
    ExportFormsResponseTypeDef,
    ExportThemesResponseTypeDef,
    GetCodegenJobResponseTypeDef,
    GetComponentResponseTypeDef,
    GetFormResponseTypeDef,
    GetMetadataResponseTypeDef,
    GetThemeResponseTypeDef,
    ListCodegenJobsResponseTypeDef,
    ListComponentsResponseTypeDef,
    ListFormsResponseTypeDef,
    ListThemesResponseTypeDef,
    PutMetadataFlagBodyTypeDef,
    RefreshTokenRequestBodyTypeDef,
    RefreshTokenResponseTypeDef,
    StartCodegenJobDataTypeDef,
    StartCodegenJobResponseTypeDef,
    UpdateComponentDataTypeDef,
    UpdateComponentResponseTypeDef,
    UpdateFormDataTypeDef,
    UpdateFormResponseTypeDef,
    UpdateThemeDataTypeDef,
    UpdateThemeResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AmplifyUIBuilderClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class AmplifyUIBuilderClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AmplifyUIBuilderClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#close)
        """

    def create_component(
        self,
        *,
        appId: str,
        environmentName: str,
        componentToCreate: "CreateComponentDataTypeDef",
        clientToken: str = ...
    ) -> CreateComponentResponseTypeDef:
        """
        Creates a new component for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.create_component)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#create_component)
        """

    def create_form(
        self,
        *,
        appId: str,
        environmentName: str,
        formToCreate: "CreateFormDataTypeDef",
        clientToken: str = ...
    ) -> CreateFormResponseTypeDef:
        """
        Creates a new form for an Amplify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.create_form)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#create_form)
        """

    def create_theme(
        self,
        *,
        appId: str,
        environmentName: str,
        themeToCreate: "CreateThemeDataTypeDef",
        clientToken: str = ...
    ) -> CreateThemeResponseTypeDef:
        """
        Creates a theme to apply to the components in an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.create_theme)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#create_theme)
        """

    def delete_component(
        self, *, appId: str, environmentName: str, id: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a component from an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.delete_component)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#delete_component)
        """

    def delete_form(
        self, *, appId: str, environmentName: str, id: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a form from an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.delete_form)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#delete_form)
        """

    def delete_theme(
        self, *, appId: str, environmentName: str, id: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a theme from an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.delete_theme)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#delete_theme)
        """

    def exchange_code_for_token(
        self, *, provider: Literal["figma"], request: "ExchangeCodeForTokenRequestBodyTypeDef"
    ) -> ExchangeCodeForTokenResponseTypeDef:
        """
        Exchanges an access code for a token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.exchange_code_for_token)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#exchange_code_for_token)
        """

    def export_components(
        self, *, appId: str, environmentName: str, nextToken: str = ...
    ) -> ExportComponentsResponseTypeDef:
        """
        Exports component configurations to code that is ready to integrate into an
        Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.export_components)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#export_components)
        """

    def export_forms(
        self, *, appId: str, environmentName: str, nextToken: str = ...
    ) -> ExportFormsResponseTypeDef:
        """
        Exports form configurations to code that is ready to integrate into an Amplify
        app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.export_forms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#export_forms)
        """

    def export_themes(
        self, *, appId: str, environmentName: str, nextToken: str = ...
    ) -> ExportThemesResponseTypeDef:
        """
        Exports theme configurations to code that is ready to integrate into an Amplify
        app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.export_themes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#export_themes)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#generate_presigned_url)
        """

    def get_codegen_job(
        self, *, appId: str, environmentName: str, id: str
    ) -> GetCodegenJobResponseTypeDef:
        """
        Returns an existing code generation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.get_codegen_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_codegen_job)
        """

    def get_component(
        self, *, appId: str, environmentName: str, id: str
    ) -> GetComponentResponseTypeDef:
        """
        Returns an existing component for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.get_component)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_component)
        """

    def get_form(self, *, appId: str, environmentName: str, id: str) -> GetFormResponseTypeDef:
        """
        Returns an existing form for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.get_form)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_form)
        """

    def get_metadata(self, *, appId: str, environmentName: str) -> GetMetadataResponseTypeDef:
        """
        Returns existing metadata for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.get_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_metadata)
        """

    def get_theme(self, *, appId: str, environmentName: str, id: str) -> GetThemeResponseTypeDef:
        """
        Returns an existing theme for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.get_theme)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_theme)
        """

    def list_codegen_jobs(
        self, *, appId: str, environmentName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListCodegenJobsResponseTypeDef:
        """
        Retrieves a list of code generation jobs for a specified Amplify app and backend
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.list_codegen_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#list_codegen_jobs)
        """

    def list_components(
        self, *, appId: str, environmentName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListComponentsResponseTypeDef:
        """
        Retrieves a list of components for a specified Amplify app and backend
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.list_components)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#list_components)
        """

    def list_forms(
        self, *, appId: str, environmentName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListFormsResponseTypeDef:
        """
        Retrieves a list of forms for a specified Amplify app and backend environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.list_forms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#list_forms)
        """

    def list_themes(
        self, *, appId: str, environmentName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListThemesResponseTypeDef:
        """
        Retrieves a list of themes for a specified Amplify app and backend environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.list_themes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#list_themes)
        """

    def put_metadata_flag(
        self,
        *,
        appId: str,
        environmentName: str,
        featureName: str,
        body: "PutMetadataFlagBodyTypeDef"
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stores the metadata information about a feature on a form.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.put_metadata_flag)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#put_metadata_flag)
        """

    def refresh_token(
        self, *, provider: Literal["figma"], refreshTokenBody: "RefreshTokenRequestBodyTypeDef"
    ) -> RefreshTokenResponseTypeDef:
        """
        Refreshes a previously issued access token that might have expired.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.refresh_token)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#refresh_token)
        """

    def start_codegen_job(
        self,
        *,
        appId: str,
        environmentName: str,
        codegenJobToCreate: "StartCodegenJobDataTypeDef",
        clientToken: str = ...
    ) -> StartCodegenJobResponseTypeDef:
        """
        Starts a code generation job for for a specified Amplify app and backend
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.start_codegen_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#start_codegen_job)
        """

    def update_component(
        self,
        *,
        appId: str,
        environmentName: str,
        id: str,
        updatedComponent: "UpdateComponentDataTypeDef",
        clientToken: str = ...
    ) -> UpdateComponentResponseTypeDef:
        """
        Updates an existing component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.update_component)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#update_component)
        """

    def update_form(
        self,
        *,
        appId: str,
        environmentName: str,
        id: str,
        updatedForm: "UpdateFormDataTypeDef",
        clientToken: str = ...
    ) -> UpdateFormResponseTypeDef:
        """
        Updates an existing form.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.update_form)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#update_form)
        """

    def update_theme(
        self,
        *,
        appId: str,
        environmentName: str,
        id: str,
        updatedTheme: "UpdateThemeDataTypeDef",
        clientToken: str = ...
    ) -> UpdateThemeResponseTypeDef:
        """
        Updates an existing theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.update_theme)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#update_theme)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["export_components"]
    ) -> ExportComponentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["export_forms"]) -> ExportFormsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["export_themes"]) -> ExportThemesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_codegen_jobs"]
    ) -> ListCodegenJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_components"]) -> ListComponentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_forms"]) -> ListFormsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_themes"]) -> ListThemesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_paginator)
        """
