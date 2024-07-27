import sys
from src.configuration.gcloud import GCloud
from src.constants import *
from src.entity.artifact_entity import ModelEvaluationArtifacts, ModelPusherArtifacts
from src.entity.config_entity import ModelPusherConfig
from src.exception import NerException
from src.logger import logging


class ModelPusher:
    def __init__(
        self,
        model_evaluation_artifact: ModelEvaluationArtifacts,
        model_pusher_config: ModelPusherConfig,
    ) -> None:
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.gcloud = GCloud()


    def initiate_model_pusher(self) -> ModelPusherArtifacts:
        try:
            logging.info("Enetred the initiate_model_pusher method of Model pusher class")
            if self.model_evaluation_artifact.is_model_accepted == True:

                # Uploading the model to google container registry
                self.gcloud.sync_folder_to_gcloud(
                    gcp_bucket_url=self.model_pusher_config.bucket_name,
                    filepath=self.model_pusher_config.upload_model_path,
                    filename=GCP_MODEL_NAME,
                )

                logging.info("Model pushed to google conatiner registry")

            model_pusher_artifacts = ModelPusherArtifacts(
                bucket_name=self.model_pusher_config.bucket_name,
                trained_model_path=self.model_pusher_config.upload_model_path,
            )

            logging.info(
                "Exited the initiate_model_pusher method of Model pusher class"
            )
            return model_pusher_artifacts

        except Exception as e:
            raise NerException(e, sys) from e
