from pydantic import Field

from .base_model import BaseModel
from .fragments import CredentialSecretChanged


class KafkaSaslPlainCredentialSecretChanged(BaseModel):
    kafka_sasl_plain_credential_secret_changed: "KafkaSaslPlainCredentialSecretChangedKafkaSaslPlainCredentialSecretChanged" = Field(
        alias="kafkaSaslPlainCredentialSecretChanged"
    )


class KafkaSaslPlainCredentialSecretChangedKafkaSaslPlainCredentialSecretChanged(
    CredentialSecretChanged
):
    pass


KafkaSaslPlainCredentialSecretChanged.update_forward_refs()
KafkaSaslPlainCredentialSecretChangedKafkaSaslPlainCredentialSecretChanged.update_forward_refs()
