from negmas import ResponseType

from ..agent import OneShotAgent

__all__ = ["OneshotDoNothingAgent"]


class OneshotDoNothingAgent(OneShotAgent):
    """An agent that does nothing.

    Remarks:

        Note that this agent will lose money whenever it is at the edges (i.e.
        it is an input or an output agent trading in raw material or final
        product).
    """

    def propose(self, negotiator_id, state):
        return None

    def respond(self, negotiator_id, state):
        return ResponseType.END_NEGOTIATION
