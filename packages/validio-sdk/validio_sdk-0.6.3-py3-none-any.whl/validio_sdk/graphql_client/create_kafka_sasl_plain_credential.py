from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialCreation


class CreateKafkaSaslPlainCredential(BaseModel):
    kafka_sasl_plain_credential_create: "CreateKafkaSaslPlainCredentialKafkaSaslPlainCredentialCreate" = Field(
        alias="kafkaSaslPlainCredentialCreate"
    )


class CreateKafkaSaslPlainCredentialKafkaSaslPlainCredentialCreate(CredentialCreation):
    pass


CreateKafkaSaslPlainCredential.update_forward_refs()
CreateKafkaSaslPlainCredentialKafkaSaslPlainCredentialCreate.update_forward_refs()
