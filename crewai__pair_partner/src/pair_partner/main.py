#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from pair_partner.crew import PairPartner, mcp_server_adapter

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'file_with_feature': '/home/jorge/code/code-pair-partner/new_feature.py',
        'write_tests_in_path': '/home/jorge/code/code-pair-partner/test_new_feature.py',
    }
    
    try:
        PairPartner().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}") from e
    finally:
        mcp_server_adapter.stop()



if __name__ == '__main__':
    run()