"""Public agent registry."""
from .search_agent import search_agent_ag
from .citation_graph_agent import citation_graph_agent_ag
from .trend_analysis_agent import trend_analysis_agent_ag

from .parser_agent import parser_agent_ag
from .matrix_agent import matrix_agent_ag
from .contradiction_agent import contradiction_agent_ag
from .swot_agent import swot_agent_ag

from .gap_agent import gap_agent_ag
from .idea_agent import idea_agent_ag
from .cross_domain_agent import cross_domain_agent_ag

from .dataset_agent import dataset_agent_ag
from .experiment_agent import experiment_agent_ag
from .evaluation_agent import evaluation_agent_ag

from .abstract_writer import abstract_writer_ag
from .method_writer import method_writer_ag
from .results_writer import results_writer_ag
from .citation_validator import citation_validator_ag

__all__ = [
    "search_agent_ag",
    "citation_graph_agent_ag",
    "trend_analysis_agent_ag",
    "parser_agent_ag",
    "matrix_agent_ag",
    "contradiction_agent_ag",
    "swot_agent_ag",
    "gap_agent_ag",
    "idea_agent_ag",
    "cross_domain_agent_ag",
    "dataset_agent_ag",
    "experiment_agent_ag",
    "evaluation_agent_ag",
    "abstract_writer_ag",
    "method_writer_ag",
    "results_writer_ag",
    "citation_validator_ag",
]
