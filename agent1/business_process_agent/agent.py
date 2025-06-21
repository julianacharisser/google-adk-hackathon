from google.adk.agents import SequentialAgent

from .subagents.document_ingestion_agent import document_ingestion_agent
from .subagents.process_mining_agent import process_mining_agent
from .subagents.pattern_detection_agent import pattern_detection_agent
from .subagents.benchmarking_agent import benchmarking_agent
from .subagents.roi_estimation_agent import roi_estimation_agent

# Create the sequential agent with minimal callback
root_agent = SequentialAgent(
    name="BusinessProcessPipeline",
    sub_agents=[document_ingestion_agent, process_mining_agent, pattern_detection_agent,benchmarking_agent, roi_estimation_agent],
    description="Coordinates end-to-end business process analysis for Singapore SMEs.",
)
