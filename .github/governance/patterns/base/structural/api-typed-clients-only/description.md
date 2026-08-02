# api-typed-clients-only

**Rule ID:** `api-typed-clients-only`
**Severity:** error · **State:** enforced · **Owner:** qe-platform-team

All API step definitions must call typed API client classes
(e.g. `PortfolioClient(context.client).get_holdings(portfolio_id)`).
Raw `requests.get(...)` / `requests.post(...)` / `requests.put(...)` /
`requests.delete(...)` / `requests.patch(...)` calls are not permitted in
API step definitions — those calls belong only inside `clients/` classes,
where authentication, retry, base-URL, and timeout policy live in one
place rather than being copied into every step.

## Why

Step files that call `requests` directly bypass the typed client layer
and re-implement cross-cutting concerns (auth header injection, base-URL
resolution, retry-on-503, request-ID propagation) ad-hoc. Every such
re-implementation is an opportunity for divergence: one step sets the
auth header, another forgets it; one step uses the staging base URL,
another hardcodes prod. When the auth scheme changes from bearer token
to OAuth refresh, the typed client gets updated in one place and every
step keeps working — but every raw `requests` call has to be tracked
down and patched.

Test failures from auth or base-URL drift are the second-most common
kind of test-suite rot (after UI selector drift, the rule
`ui-no-raw-selectors` already addresses). Centralising HTTP semantics in
the client layer is the API-side mirror of the page-object pattern.

## What this rule catches

Any call to `requests.get(...)`, `requests.post(...)`, `requests.put(...)`,
`requests.delete(...)`, or `requests.patch(...)` appearing in a Python
file under `steps/api/`. Inside `clients/`, those same calls are not
just permitted but expected — that is the layer the typed clients are
built on.

## How to comply

Move the HTTP call into a method on the relevant typed client under
`clients/<app>/`. Expose a semantic operation (`get_holdings`,
`submit_order`) and call that from the step definition. Authentication,
retry, base-URL, and timeout handling should be set up once in the
client's `__init__` or the base client class it extends.

```python
# Step file (compliant):
def step_get_holdings(context, portfolio_id):
    holdings = PortfolioClient(context.client).get_holdings(portfolio_id)
    context.last_response = holdings

# Typed client (also compliant — this is where requests lives):
class PortfolioClient(BaseClient):
    def get_holdings(self, portfolio_id):
        return self._get(f"/portfolios/{portfolio_id}/holdings").json()
```

## Override

If a step genuinely needs to exercise a raw HTTP call (e.g. testing the
client layer's own auth-header behaviour from outside it), use an inline
`nosemgrep: api-typed-clients-only` annotation with a reason and expiry,
OR add a path-scoped waiver to `governance/waivers.yaml`. See proposal
§"Override Model."
