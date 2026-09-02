from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class McpContainerContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dockerfile = (REPO_ROOT / "Dockerfile.mcp").read_text(encoding="utf-8")
        self.entrypoint = (REPO_ROOT / "scripts" / "run_v8std_mcp_image.sh").read_text(
            encoding="utf-8"
        )

    def test_build_always_regenerates_every_mcp_artifact(self):
        for command in (
            "generate_social_cards.py",
            "generate_ai_artifacts.py",
            "generate_search_vectors.py",
        ):
            self.assertIn(command, self.dockerfile)

        for artifact in (
            "docs/ai/pages.jsonl",
            "docs/ai/search-vectors.jsonl",
            "docs/llms.txt",
            "docs/llms-full.txt",
        ):
            self.assertIn(f"test -s /build/{artifact}", self.dockerfile)

        dockerignore = (REPO_ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("docs/ai", dockerignore)
        self.assertIn("docs/llms.txt", dockerignore)
        self.assertIn("docs/llms-full.txt", dockerignore)

    def test_runtime_image_contains_only_mcp_runtime_and_generated_data(self):
        runtime = self.dockerfile.split("FROM python:3.12-slim AS runtime", 1)[1]
        self.assertIn("COPY --from=artifacts /build/docs/ai", runtime)
        self.assertIn("COPY --from=artifacts /build/docs/llms.txt", runtime)
        self.assertIn("COPY --from=artifacts /build/docs/llms-full.txt", runtime)
        self.assertIn('ENTRYPOINT ["/opt/v8std/scripts/run_v8std_mcp_image.sh"]', runtime)
        self.assertIn("chmod -R a+rX /opt/v8std/data", runtime)
        self.assertNotIn("zensical_docs.sh", runtime)
        self.assertNotIn("install_zensical.sh", runtime)

    def test_container_start_never_generates_or_downloads_index(self):
        self.assertNotIn("generate_ai_artifacts.py", self.entrypoint)
        self.assertNotIn("generate_search_vectors.py", self.entrypoint)
        self.assertNotIn("V8STD_MCP_GENERATE_INDEX", self.entrypoint)
        for artifact in ("PAGES_PATH", "VECTORS_PATH", "llms.txt", "llms-full.txt"):
            self.assertIn(artifact, self.entrypoint)

    def test_windows_launcher_defaults_to_local_image_without_compose_or_pull(self):
        launcher = (REPO_ROOT / "run-v8std-mcp.cmd").read_text(encoding="utf-8")
        self.assertIn("docker run", launcher)
        self.assertIn('set "V8STD_MCP_IMAGE=v8std-mcp:latest"', launcher)
        self.assertIn('if not "%~1"=="" set "V8STD_MCP_IMAGE=%~1"', launcher)
        self.assertNotIn("Usage:", launcher)
        self.assertNotIn("shadobaai/", launcher)
        self.assertNotIn("ghcr.io", launcher)
        self.assertNotIn("docker pull", launcher)
        self.assertIn("127.0.0.1:8766:8766", launcher)
        self.assertNotIn("docker compose", launcher)
        self.assertNotIn(" -v ", launcher)
        self.assertGreaterEqual(launcher.casefold().count("pause"), 2)
        self.assertTrue((REPO_ROOT / "docker-compose" / "docker-compose.yml").exists())

    def test_local_builder_rebuilds_without_cache_and_requires_no_arguments(self):
        builder = (REPO_ROOT / "build-v8std-mcp.cmd").read_text(encoding="utf-8")
        self.assertIn("docker build --no-cache", builder)
        self.assertIn("Dockerfile.mcp", builder)
        self.assertIn('set "V8STD_MCP_IMAGE=v8std-mcp:latest"', builder)
        self.assertNotIn("docker push", builder)
        self.assertNotIn("%~1", builder)
        self.assertNotIn("shadobaai/", builder)
        self.assertNotIn("ghcr.io", builder)
        self.assertNotIn("--pull", builder)
        self.assertIn('pushd "%~dp0"', builder)
        self.assertIn(" --tag \"%V8STD_MCP_IMAGE%\" .", builder)
        self.assertNotIn('\"%~dp0\" .', builder)
        self.assertNotIn("buildx", builder)
        self.assertNotIn(".github", builder)
        self.assertGreaterEqual(builder.casefold().count("pause"), 2)


if __name__ == "__main__":
    unittest.main()
