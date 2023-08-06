# SPDX-License-Identifier: MIT
# Copyright (c) 2022 MBition GmbH
from ..encodestate import EncodeState
from .parameterwithdop import ParameterWithDOP


class LengthKeyParameter(ParameterWithDOP):
    """Length Keys specify the bit (!) length of another parameter.

    The other parameter references the length key parameter using a ParamLengthInfoType as .diag_coded_type.

    LengthKeyParameters are decoded the same as ValueParameters.
    The main difference to ValueParameters is that a LengthKeyParameter has an `.odx_id` attribute
    and its DOP must be a simple DOP with PHYSICAL-TYPE/BASE-DATA-TYPE="A_UINT32".
    """

    def __init__(self, *, odx_id, **kwargs):
        super().__init__(parameter_type="LENGTH-KEY", **kwargs)
        self.odx_id = odx_id

    def is_required(self):
        return False

    def is_optional(self):
        return True

    def encode_into_pdu(self, encode_state: EncodeState) -> bytearray:
        physical_value = encode_state.parameter_values.get(self.short_name,)

        if physical_value is None:
            raise TypeError(f"A value for the length key '{self.short_name}'"
                            f" must be specified.")

        # Set the value of the length key in the length key dict.
        encode_state.length_keys[self.odx_id] = physical_value

        return super(ParameterWithDOP, self).encode_into_pdu(encode_state)
