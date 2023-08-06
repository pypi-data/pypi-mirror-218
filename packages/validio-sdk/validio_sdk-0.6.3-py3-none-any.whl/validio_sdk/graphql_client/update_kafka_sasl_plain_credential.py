from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialUpdate


class UpdateKafkaSaslPlainCredential(BaseModel):
    kafka_sasl_plain_credential_update: "UpdateKafkaSaslPlainCredentialKafkaSaslPlainCredentialUpdate" = Field(
        alias="kafkaSaslPlainCredentialUpdate"
    )


class UpdateKafkaSaslPlainCredentialKafkaSaslPlainCredentialUpdate(CredentialUpdate):
    pass


UpdateKafkaSaslPlainCredential.update_forward_refs()
UpdateKafkaSaslPlainCredentialKafkaSaslPlainCredentialUpdate.update_forward_refs()
