"""Type atn.outside.temp.regr.coeffs, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from gridworks.errors import SchemaError
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator


class AtnOutsideTempRegrCoeffs(BaseModel):
    """.

        Coefficients for a linear regression of avg power leaving a building as a function of weather:

    PowerOut = Alpha + Beta * OutsideTempF

        These are an example of Slowly Varying State variables maintained for a thermal storage heating Terminal Asset by
        its AtomicTNode and Scada.
        [More info](https://gridworks-atn.readthedocs.io/en/latest/data-categories.html#slowly-varying-state-variables).
    """

    Alpha: int = Field(
        title="Alpha (units: W)",
        default=200,
    )
    Beta: float = Field(
        title="Beta (units: W / deg F)  ",
        default=-1.5,
    )
    TypeName: Literal["atn.outside.temp.regr.coeffs"] = "atn.outside.temp.regr.coeffs"
    Version: str = "000"

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))  # noqa


class AtnOutsideTempRegrCoeffs_Maker:
    type_name = "atn.outside.temp.regr.coeffs"
    version = "000"

    def __init__(self, alpha: int, beta: float):
        self.tuple = AtnOutsideTempRegrCoeffs(
            Alpha=alpha,
            Beta=beta,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: AtnOutsideTempRegrCoeffs) -> str:
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> AtnOutsideTempRegrCoeffs:
        """
        Given a serialized JSON type object, returns the Python class object
        """
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> AtnOutsideTempRegrCoeffs:
        d2 = dict(d)
        if "Alpha" not in d2.keys():
            raise SchemaError(f"dict {d2} missing Alpha")
        if "Beta" not in d2.keys():
            raise SchemaError(f"dict {d2} missing Beta")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return AtnOutsideTempRegrCoeffs(
            Alpha=d2["Alpha"],
            Beta=d2["Beta"],
            TypeName=d2["TypeName"],
            Version="000",
        )
