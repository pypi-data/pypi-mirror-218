import typing as t

__all__ = [
    "JSONSerialization",
    "FlattenJSONSerialization",
    "GeneralJSONSerialization",
]

JSONRecipientDict = t.TypedDict("JSONRecipientDict", {
    "header": t.Dict[str, any],
    "encrypted_key": str,
}, total=False)

GeneralJSONSerialization = t.TypedDict("GeneralJSONSerialization", {
    "protected": str,
    "unprotected": t.Dict[str, any],
    "iv": str,
    "aad": str,
    "ciphertext": str,
    "tag": str,
    "recipients": t.List[JSONRecipientDict],
}, total=False)

FlattenJSONSerialization = t.TypedDict("FlattenJSONSerialization", {
    "protected": str,
    "unprotected": t.Dict[str, any],
    "header": t.Dict[str, any],
    "encrypted_key": str,
    "iv": str,
    "aad": str,
    "ciphertext": str,
    "tag": str,
}, total=False)

JSONSerialization = t.Union[GeneralJSONSerialization, FlattenJSONSerialization]
