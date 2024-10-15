from dependency_injector import providers, containers
from app.core.config import BaseAppSettings


class Container(containers.DeclarativeContainer):
    config: BaseAppSettings = providers.Configuration()

    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.api",
            "app.routers",
            "app.core",
            "app.services",
            "app.repositories",
            "app.clients",
            "app.db",
        ]
    )

    # # clients
    # s3_client = providers.Factory(
    #     S3Client,
    #     aws_access_key_id=config.aws_access_key_id,
    #     aws_secret_access_key=config.aws_secret_access_key,
    #     bucket=config.bucket,
    #     aws_region=config.aws_region
    # )

    # # repositories
    # user_repository = providers.Factory(
    #     UserRepository,
    # )

    # # services
    # user_service = providers.Factory(
    #     UserService,
    #     user_repository=user_repository,
    #     key=config.user_key,
    #     iv=config.seed_key,
    # )

    # image_service = providers.Factory(
    #     ImageService,
    #     s3_client=s3_client
    # )
