"""Streamlit UI and programmatic entry point for proposal review."""

import argparse
import json
from pathlib import Path

from services.orchestrator import ProposalOrchestrator
from services.report_generator import build_report


def review_proposal(source, filename: str = "proposal") -> dict:
	return ProposalOrchestrator().review(source, filename)


def main() -> None:
	parser = argparse.ArgumentParser(description="Review a business proposal with specialist agents.")
	parser.add_argument("proposal", nargs="?", help="Path to a PDF or text proposal")
	parser.add_argument("--report", default="risk_assessment.pdf")
	args = parser.parse_args()
	if args.proposal:
		result = review_proposal(args.proposal, Path(args.proposal).name)
		Path(args.report).write_bytes(build_report(Path(args.proposal).name, result["agents"], result["decision"]))
		print(json.dumps(result["decision"], indent=2))
		return
	try:
		import streamlit as st
	except ImportError as exc:
		raise SystemExit("Install requirements.txt or provide a proposal path on the command line.") from exc
	st.set_page_config(page_title="Proposal Review Committee", page_icon="P", layout="wide")
	st.title("Business Proposal Review Committee")
	st.caption("Upload a proposal to run market, finance, legal, technology, HR, GTM, ESG, and risk reviews.")
	uploaded = st.file_uploader("Business proposal PDF or text file", type=["pdf", "txt", "md"])
	if uploaded and st.button("Run review", type="primary"):
		with st.spinner("Agents are reviewing the proposal..."):
			result = review_proposal(uploaded.getvalue(), uploaded.name)
		decision = result["decision"]
		st.subheader(decision["decision"])
		st.write(decision["rationale"])
		cols = st.columns(4)
		for index, item in enumerate(result["agents"]):
			with cols[index % 4]:
				st.metric(item["agent"], item["risk_level"].upper())
		with st.expander("Conditions and priority risks"):
			st.write(decision["conditions"] or decision["priority_risks"])
		pdf = build_report(uploaded.name, result["agents"], decision)
		st.download_button("Download PDF risk assessment", pdf, "risk_assessment.pdf", "application/pdf")


if __name__ == "__main__":
	main()
