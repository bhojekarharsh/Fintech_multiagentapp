from dataclasses import dataclass

from agents.base_agent import AgentResult


@dataclass
class CommitteeDecision:
	decision: str
	rationale: str
	conditions: list[str]
	priority_risks: list[str]

	def to_dict(self) -> dict:
		return {
			"decision": self.decision,
			"rationale": self.rationale,
			"conditions": self.conditions,
			"priority_risks": self.priority_risks,
		}


class CommitteeAgent:
	def decide(self, results: list[AgentResult]) -> CommitteeDecision:
		high_risk = [result for result in results if result.risk_level == "high"]
		concerns = [concern for result in results for concern in result.concerns]
		priority = concerns[:6]
		if len(high_risk) >= 3:
			return CommitteeDecision("REJECT", "Multiple specialist reviews identified material unmitigated risks.", [], priority)
		if high_risk or len(concerns) >= 5:
			return CommitteeDecision("CONDITIONAL APPROVAL", "The proposal is potentially viable, subject to closing the identified evidence gaps.", concerns[:5], priority)
		return CommitteeDecision("APPROVE", "Specialist reviews found no material blockers in the supplied evidence.", [], priority)
