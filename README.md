# pyfarm-config

Centralized settings management for the pyfarm ecosystem.

Services read configuration via `get_settings()`, which returns a cached
`PyfarmSettings` populated from `PYFARM_`-prefixed environment variables
(optionally a `.env` file) with development defaults.
