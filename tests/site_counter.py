"""A minimal task site for the runner tests (#153): POST /hit counts, GET /count reads; run with -m."""

from __future__ import annotations

from mengine_bench.sites.server_base import SiteHandler, serve
from mengine_bench.sites.signed_store import SiteEvent, SiteState


def apply_counter(state: SiteState, event: SiteEvent) -> SiteState:
    if event.get("type") != "hit":
        raise ValueError(f"received event {event!r}; expected type 'hit'")
    return {**state, "hits": int(state.get("hits", 0)) + 1}  # type: ignore[call-overload]


class CounterHandler(SiteHandler):
    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler's name
        if self.path == "/count":
            self.send_json(200, {"hits": self.store.state.get("hits")})
            return
        self.serve_static()

    def do_POST(self) -> None:  # noqa: N802
        state = self.store.record({"type": "hit"})
        self.send_json(200, {"hits": state["hits"]})


if __name__ == "__main__":
    serve(CounterHandler, apply_counter, {"hits": 0})
