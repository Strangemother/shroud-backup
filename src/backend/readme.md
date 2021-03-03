# App Backend

The Interface runs independently of the main monitoring tool (this backend).
When alive, the UI can request to one or more local backends through mDNS.

# Tooling

Fundamentally this is a local django website hosting a complete backend.

Binding the external components to this _db_, fastAPI with websockets serves the base for all communication.


# Interface

The desktop app content serves through this backend as _html pages_.
