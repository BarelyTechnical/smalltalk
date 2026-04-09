# PowerShell Claude CLI arguments escaping

**Issue:**
Running `claude mcp add` in PowerShell with arguments containing dashes (like `-m`) fails and throws an `unknown option` error because PowerShell parses the dash as a param for the CLI wrapper itself.

**Pattern / Fix:**
Wrap the executable command inside quotes to shield the dashes from the PowerShell parser when passed to the CLI:

**Incorrect:**
`claude mcp add smalltalk -- python -m smalltalk.mcp_server`

**Correct:**
`claude mcp add smalltalk -- "python -m smalltalk.mcp_server"`
