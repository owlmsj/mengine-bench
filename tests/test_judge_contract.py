"""Judge-input contract: every tool kind of every harness reaches the judge's tool log (#185, #176).

One stream per harness in fixtures/judge_contract, event shapes copied from published transcripts:
- codex: web_search `results[]` rows (type, domain, ref_id, snippet, title, url) and open_page from
  results/2026-11-03_codex_gpt-6.1-sol_low_35d7a1b8/transcripts/web-plan-ranking.jsonl.gz and
  results/2026-11-02_codex_gpt-6-astra_low_43e898d9/transcripts/web-plan-ranking.jsonl.gz; mcp_tool_call
  (node_repl.js, mengine-cu.browser) and file_change from other Codex bundles.
- claude: WebSearch `tool_use_result.results[].content[]` ({title, url}) and WebFetch from
  results/2026-11-03_claude_claude-sonnet-5-5_low_cb2cc05a/transcripts/web-plan-ranking.jsonl.gz (the Opus
  eb72035c web-fact-search transcript holds one Bash call, no WebSearch); mcp__ browser calls from cu-social-cycle.
- opencode: shell, write, edit, webfetch, mengine-cu_browser from published OpenCode bundles. No published OpenCode
  run used websearch: its call has the shape of tests/test_trace_evidence.py (input.query, output text).
- agy: run_command, write_file, edit_file, search_web from results/2026-11-03_agy_gemini-4-argon_low_160eecca;
  search_web carries no results in the stream. capture_browser_screenshot from tests/test_agy_agent.py.
  No published AGY run fetched a page or called an MCP tool, so those kinds are not in its fixture.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from mengine_bench.judge_view import tool_log
from mengine_bench.runner.trace import fetched_urls, tool_trace, url_key

FIXTURES = Path(__file__).parent / "fixtures" / "judge_contract"
FETCH_URL = "https://biblioteca.ibge.gov.br/visualizacao/periodicos/236/inpc_ipca_2014_jul.pdf"
SHOWN = ["Indicadores IBGE (biblioteca.ibge.gov.br)", "sumario planos programas jul2019 (www.bcb.gov.br)",
         "Tabela IPCA (www.idinheiro.com.br)", "ipca e 1994 2012 serie historica (biblioteca.ibge.gov.br)",
         "tabela completa (numerando.com.br)"]
SIXTH = "scielo.br/j/rep"
SEARCH_URLS = ["https://www.bcb.gov.br/content/publicacoes/outras_pub_alfa/sumario_planos_programas-jul2019.pdf",
               "https://www.idinheiro.com.br/tabelas/tabela-ipca/"]
KINDS = {
    "claude": ["shell", "write", "edit", "web_search", "fetch", "mcp_tool_call", "browser", "browser"],
    "codex": ["shell", "edit", "edit", "web_search", "fetch", "mcp_tool_call", "browser"],
    "opencode": ["shell", "write", "edit", "web_search", "fetch", "browser"],
    "agy": ["shell", "write", "edit", "web_search", "browser"],
}
_LINE = re.compile(r"\[step 1\] (\S+) ")


def _stream(harness: str) -> str:
    return (FIXTURES / f"{harness}.jsonl").read_text(encoding="utf-8")


def _search_line(harness: str) -> str:
    return next(line for line in tool_log([_stream(harness)]).split("\n") if line.startswith("[step 1] web_search "))


@pytest.mark.parametrize("harness", sorted(KINDS))
def test_each_call_is_one_line_with_its_kind(harness: str) -> None:
    lines = tool_log([_stream(harness)]).split("\n")
    kinds = [match.group(1) if (match := _LINE.match(line)) else line for line in lines]
    assert kinds == KINDS[harness], f"{harness}: got {kinds}, expected {KINDS[harness]}"


@pytest.mark.parametrize("harness", ["claude", "codex"])
def test_a_structured_search_shows_its_count_and_first_results(harness: str) -> None:
    line = _search_line(harness)
    assert "6 results: " in line, line
    assert all(label in line for label in SHOWN), line
    assert SIXTH not in line, line


def test_a_search_given_as_text_shows_its_text() -> None:
    line = _search_line("opencode")
    assert "Indicadores IBGE" in line and "biblioteca.ibge.gov.br" in line, line


def test_a_search_without_results_in_the_stream_says_so() -> None:
    # The #176 misread: an empty output reads as an empty search.
    assert _search_line("agy").endswith('ok -> "(results not in the harness stream)"')


@pytest.mark.parametrize("harness", ["claude", "codex", "opencode"])
def test_the_fetch_line_names_its_url(harness: str) -> None:
    line = next(line for line in tool_log([_stream(harness)]).split("\n") if line.startswith("[step 1] fetch "))
    assert FETCH_URL in line, line


@pytest.mark.parametrize("harness", ["claude", "codex", "opencode"])
def test_fetch_evidence_is_the_fetch_not_the_search_results(harness: str) -> None:
    # Owner rule (#171): search results are not fetched pages; only the judge sees them.
    fetched = fetched_urls(tool_trace([_stream(harness)]))
    assert url_key(FETCH_URL) in fetched, fetched
    assert not {url_key(url) for url in SEARCH_URLS} & fetched, fetched


@pytest.mark.parametrize("harness", sorted(KINDS))
def test_the_log_does_not_name_the_harness(harness: str) -> None:
    log = tool_log([_stream(harness)])
    for leak in ("claude-opus", "sessionID", "ses_x", "item.completed", "thread", "ab86ef80", "codex/", "srvtoolu"):
        assert leak not in log, (harness, leak)
