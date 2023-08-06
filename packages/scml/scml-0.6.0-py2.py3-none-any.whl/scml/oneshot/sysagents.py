"""
Implements the one shot version of SCML
"""
from typing import Any, Dict, List, Optional

from negmas import (
    Adapter,
    Breach,
    Contract,
    Issue,
    MechanismState,
    Negotiator,
    NegotiatorMechanismInterface,
    RenegotiationRequest,
)
from negmas.sao import ControlledSAONegotiator

from scml.scml2019.common import QUANTITY

from .agent import OneShotAgent
from .awi import OneShotAWI
from .helper import AWIHelper
from .mixins import OneShotUFunCreatorMixin

__all__ = ["DefaultOneShotAdapter", "_SystemAgent"]


class DefaultOneShotAdapter(Adapter, OneShotUFunCreatorMixin):
    """
    The base class of all agents running in OneShot based on OneShotAgent.

    Remarks:

        - It inherits from `Adapter` allowing it to just pass any calls not
          defined explicity in it to the internal `_obj` object representing
          the SCML2020OneShotAgent.
    """

    def make_ufun(self, add_exogenous: bool):
        return super().make_ufun(add_exogenous, in_adapter=False)

    def on_negotiation_failure(self, partners, annotation, mechanism, state):
        return self._obj.on_negotiation_failure(partners, annotation, mechanism, state)

    def on_negotiation_success(self, contract: Contract, mechanism):
        if contract.annotation["buyer"] == self.id:
            self.awi._register_supply(
                contract.annotation["seller"], contract.agreement["quantity"]
            )
        elif contract.annotation["seller"] == self.id:
            self.awi._register_sale(
                contract.annotation["buyer"], contract.agreement["quantity"]
            )
        else:
            raise ValueError(
                f"{self.id} received a  contract for which it is not a buyer nor a seller: {contract=}"
            )
        return self._obj.on_negotiation_success(contract, mechanism)

    def on_contract_executed(self, contract: Contract) -> None:
        pass

    def on_contract_breached(
        self, contract: Contract, breaches: List[Breach], resolution: Optional[Contract]
    ) -> None:
        pass

    def init_(self):
        if isinstance(self._obj, OneShotAgent):
            if not self.ufun:
                self.make_ufun(add_exogenous=True)
        super().init_()

    def init(self):
        if isinstance(self._obj, OneShotAgent):
            self._obj.connect_to_oneshot_adapter(self)
        else:
            self._obj._awi = AWIHelper(self)
        super().init()

    def reset(self):
        if hasattr(self._obj, "reset"):
            self._obj.reset()

    def before_step(self):
        self.awi._reset_sales_and_supplies()
        if hasattr(self._obj, "before_step"):
            self._obj.before_step()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type_name,
            "level": self.awi.my_input_product if self.awi else None,
            "levels": [self.awi.my_input_product] if self.awi else None,
        }

    def _respond_to_negotiation_request(
        self,
        initiator: str,
        partners: List[str],
        issues: List[Issue],
        annotation: Dict[str, Any],
        mechanism: NegotiatorMechanismInterface,
        role: Optional[str],
        req_id: Optional[str],
    ) -> Optional[Negotiator]:
        partner = [_ for _ in partners if _ != self.id][0]
        if not self._obj:
            return None
        neg = self._obj.create_negotiator(
            ControlledSAONegotiator, name=partner, id=partner
        )
        return neg

    def set_renegotiation_agenda(
        self, contract: Contract, breaches: List[Breach]
    ) -> Optional[RenegotiationRequest]:
        return None

    def respond_to_renegotiation_request(
        self, contract: Contract, breaches: List[Breach], agenda: RenegotiationRequest
    ) -> Optional[Negotiator]:
        return None

    def on_neg_request_rejected(self, req_id: str, by: Optional[List[str]]):
        pass

    def on_neg_request_accepted(
        self, req_id: str, mechanism: NegotiatorMechanismInterface
    ):
        pass

    @property
    def awi(self) -> OneShotAWI:
        return self._awi  # type: ignore

    @awi.setter
    def awi(self, awi: OneShotAWI):
        """Sets the Agent-world interface. Should only be called by the world."""
        self._awi = awi


class _SystemAgent(DefaultOneShotAdapter):
    """Implements an agent for handling system operations"""

    def __init__(self, *args, role, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = role
        self.name = role
        self.profile = None

    @property
    def type_name(self):
        return "System"

    @property
    def short_type_name(self):
        return "System"

    def respond_to_negotiation_request(
        self,
        initiator: str,
        issues: List[Issue],
        annotation: Dict[str, Any],
        mechanism: NegotiatorMechanismInterface,
    ) -> Optional[Negotiator]:
        pass

    def before_step(self):
        pass

    def step(self):
        pass

    def init(self):
        pass

    def on_negotiation_failure(
        self,
        partners: List[str],
        annotation: Dict[str, Any],
        mechanism: NegotiatorMechanismInterface,
        state: MechanismState,
    ) -> None:
        pass

    def on_negotiation_success(
        self, contract: Contract, mechanism: NegotiatorMechanismInterface
    ) -> None:
        pass

    def sign_all_contracts(self, contracts: List[Contract]) -> List[Optional[str]]:
        """Signs all contracts"""
        return [self.id] * len(contracts)
