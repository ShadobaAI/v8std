"""Run the fork's corpus, retrieval and Docker MCP checks.

The upstream VPS deployment suites exercise its public five-tool runtime and
remain available through unittest discover. CI publication tests are upstream-only too.
"""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
UPSTREAM_DELIVERY_TESTS = {
    "test_mcp_publication",
    "test_v8std_mcp_initial_install",
    "test_v8std_mcp_release",
    "test_v8std_mcp_release_docker",
    "test_v8std_mcp_release_hold",
    "test_v8std_mcp_logging",
    "test_v8std_mcp_logging_docker",
    "test_v8std_mcp_monitoring_retirement",
}


def main():
    modules = ["tests." + path.stem for path in sorted((ROOT / "tests").glob("test_*.py"))
               if path.stem not in UPSTREAM_DELIVERY_TESTS]
    print("Fork Docker MCP checks; upstream VPS/CI suites: " + ", ".join(sorted(UPSTREAM_DELIVERY_TESTS)), flush=True)
    suite = unittest.defaultTestLoader.loadTestsFromNames(modules)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
