# Live Clario: what is included and what is external

The local scripted demo is the default reproducible experience. The repository also includes the Retell integration; it is not an omitted frontend application.

| In this repository | Hosted / supplied by the service owner |
|---|---|
| Customer UI and live text/voice controls in `web/static/customer.js` | Retell account and API credentials |
| Vendored browser client `web/static/retell-web.js` | Voice/chat agents and their selected models/voices |
| Session endpoints and signed tool adapter `backend/clario_live.py` | Agent instructions, knowledge base and four function definitions |
| Draft confirmation, ranking, case state and status UI | Reachable HTTPS endpoint, approved hostname and any real transfer destination |

## Configure your own environment

1. Install dependencies and run the scripted mode first using [BUILD.md](../BUILD.md).
2. Copy `backend/.env.example` to ignored `backend/.env` if no private settings file exists. Set your own `RETELL_API_KEY`, `RETELL_VOICE_AGENT_ID` and `RETELL_CHAT_AGENT_ID`. Example IDs are not a usable shared service.
3. Expose only the intended endpoint through HTTPS and add its real hostname to `NRY_ALLOWED_HOSTS`. Configure staff authentication for remote staff access. Do not disable signature or hostname checks to get a demo working.
4. Configure Retell's `lookup_customer`, `update_card`, `submit_card` and `correct_card` functions against the signed `/retell/tools/{name}` routes. The agent should read back facts and call submission only after confirmation.
5. Restart after changing settings; existing shell values take precedence over `.env`. Validate your own service with [LIVE_TEST_CHECKLIST.md](../LIVE_TEST_CHECKLIST.md).

The alternative final-card `/webhook/retell` intake uses `NRY_WEBHOOK_SECRET` for remote/protected intake. That secret and the Retell API key are server-side; do not put them in browser code, slides or Git.

## Evidence and limits

The code supports live sessions and signed calls. Automated tests fake the Retell client and do not establish call quality, multilingual correctness or successful telephone transfer. Conversation mappings are in memory and expire on process restart. Configured fictional phone destinations are not real handoffs.

The final deck and video were submitted, but we have not independently established which live channels worked in the recording. A sanitised agent configuration or factual team summary could fill that documentation gap. Do not share keys, private knowledge-base content or real customer data.
