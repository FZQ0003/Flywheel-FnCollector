from typing_extensions import ParamSpec, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .protocol import SupportsCrossCollection  # noqa: F401

P = ParamSpec('P')
P1 = ParamSpec('P1')
R = TypeVar('R')
R_co = TypeVar('R_co', covariant=True)
R1_co = TypeVar('R1_co', covariant=True)
T = TypeVar('T')
T_sc = TypeVar('T_sc', bound='SupportsCrossCollection')
