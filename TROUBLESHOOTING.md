# 🔧 Troubleshooting Guide: Karen MCP Server

**Learn MCP debugging while fixing common issues!**

---

## 📚 Table of Contents

1. [Quick Diagnostics](#-quick-diagnostics)
2. [Installation Issues](#-installation-issues)
3. [Tool Discovery Problems](#-tool-discovery-problems)
4. [Runtime Errors](#-runtime-errors)
5. [OpenAI API Issues](#-openai-api-issues)
6. [Performance Problems](#-performance-problems)
7. [Advanced Debugging](#-advanced-debugging)

---

## 🎯 Quick Diagnostics

Before diving deep, run these quick checks:

### ✅ Is Docker Running?
```bash
docker ps
```
**Expected**: List of running containers (may be empty)
**Problem**: "Cannot connect to Docker daemon"
**Fix**: Start Docker Desktop

**💡 Learning**: MCP servers often run in Docker for portability

---

### ✅ Is the Image Built?
```bash
docker images | grep karen
```
**Expected**: `karen-mcp-server    latest    [image-id]    [time]`
**Problem**: No output
**Fix**: Build it: `docker build -t karen-mcp-server .`

**💡 Learning**: Images must exist before containers can run

---

### ✅ Can You See MCP Servers?
```bash
docker mcp server list
```
**Expected**: List including "karen" if configured
**Problem**: "karen" not listed
**Fix**: Check catalog and registry files

**💡 Learning**: Catalogs register servers with MCP gateway

---

### ✅ Are Secrets Set? (Optional)
```bash
docker mcp secret list
```
**Expected**: Shows OPENAI_API_KEY if configured
**Problem**: Not listed
**Fix**: `docker mcp secret set OPENAI_API_KEY="sk-..."`

**💡 Learning**: Secrets are environment variables for containers

---

## 🏗️ Installation Issues

### Problem: Docker Build Fails

**Symptoms**:
```
ERROR: failed to solve: failed to fetch ...
```

**Common Causes**:
1. No internet connection
2. PyPI packages unavailable
3. Dockerfile syntax errors

**Diagnostic Steps**:
```bash
# Check internet
ping pypi.org

# Verify Dockerfile exists
ls -la Dockerfile

# Check Dockerfile syntax
cat Dockerfile
```

**Solutions**:
- **No Internet**: Connect to network
- **Package Issues**: Check `requirements.txt` for typos
- **Syntax Error**: Compare with original Dockerfile

**💡 Learning**: Docker builds need network access to download dependencies

---

### Problem: "No Such File or Directory" During Build

**Symptoms**:
```
ERROR: failed to compute cache key: "/karen_server.py" not found
```

**Cause**: You're not in the correct directory

**Solution**:
```bash
# Check current directory
pwd

# List files
ls -la

# Should see: Dockerfile, karen_server.py, requirements.txt
# If not, navigate to correct directory:
cd /path/to/karen-mcp-server
```

**💡 Learning**: Docker builds run from current directory context

---

## 🔍 Tool Discovery Problems

### Problem: Tools Don't Appear in Claude Desktop

**Symptoms**: Ask Claude about Karen tools, it says it doesn't have them

**Diagnostic Checklist**:

#### 1. Check Catalog File Exists
```bash
ls -la ~/.docker/mcp/catalogs/custom.yaml
```
**Fix if missing**: Create the file (see installation guide)

#### 2. Verify Catalog YAML Syntax
```bash
cat ~/.docker/mcp/catalogs/custom.yaml
```

**Common YAML Mistakes**:
```yaml
# ❌ WRONG: Inconsistent indentation
registry:
  karen:
  description: "..."  # Too far left!

# ✅ CORRECT: Consistent 2-space indentation
registry:
  karen:
    description: "..."
    title: "..."
```

**Test YAML validity**:
```bash
# Install yamllint if needed
pip install yamllint

# Check syntax
yamllint ~/.docker/mcp/catalogs/custom.yaml
```

**💡 Learning**: YAML is indent-sensitive! Use spaces, not tabs.

#### 3. Check Registry File
```bash
cat ~/.docker/mcp/registry.yaml
```

**Must have**:
```yaml
registry:
  karen:
    ref: ""
```

**❌ Common mistake**:
```yaml
# Wrong location (at root instead of under registry:)
karen:
  ref: ""
```

**💡 Learning**: Registry maps server names to configurations

#### 4. Verify Claude Desktop Config
```bash
# macOS
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Look for custom.yaml in args array
```

**Must include**: `--catalog=/mcp/catalogs/custom.yaml`

**💡 Learning**: Claude loads catalogs specified in config

#### 5. Restart Claude Desktop Properly

**Wrong**: Just closing the window ❌
**Right**: 
- macOS: Cmd+Q (or Claude → Quit)
- Check Activity Monitor: no "Claude" processes running
- Restart Claude Desktop

**💡 Learning**: Config is read at startup, not dynamically

---

### Problem: "Server Not Found" Error

**Symptoms**: Claude says it can't connect to the Karen server

**Solutions**:

1. **Check Image Name Matches**:
```bash
# In catalog: image: karen-mcp-server:latest
# In Docker: docker images | grep karen-mcp-server
# Names must match exactly!
```

2. **Verify Docker Socket Access**:
```bash
# Claude config must have:
"-v", "/var/run/docker.sock:/var/run/docker.sock"
```

3. **Check Container Starts**:
```bash
# Try running manually
docker run -i --rm karen-mcp-server:latest

# Should wait for input (press Ctrl+C to exit)
```

**💡 Learning**: MCP gateway starts containers on-demand

---

## ⚠️ Runtime Errors

### Problem: "Tool Failed to Execute"

**Symptoms**: Tool invocation fails with generic error

**Debugging Steps**:

#### 1. Check Docker Logs
```bash
# Find running containers
docker ps

# Check logs (replace CONTAINER_ID)
docker logs CONTAINER_ID
```

**Look for**:
- Python exceptions
- Import errors
- Connection failures

#### 2. Test Tool Directly
```bash
# Test with JSON-RPC
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  docker run -i --rm karen-mcp-server:latest
```

**Expected**: JSON response with tool list
**Problem**: Error message or no response

**💡 Learning**: You can test MCP servers without Claude!

#### 3. Check for Missing Dependencies
```bash
# Run interactive shell in container
docker run -it --rm karen-mcp-server:latest /bin/sh

# Inside container, test imports
python3 -c "from mcp.server.fastmcp import FastMCP"
python3 -c "import httpx"
```

**💡 Learning**: Container has its own isolated environment

---

### Problem: "Permission Denied" Errors

**Symptoms**:
```
PermissionError: [Errno 13] Permission denied
```

**Common Causes**:
1. Docker socket permissions
2. File system access issues
3. SELinux/AppArmor restrictions

**Solutions**:

```bash
# Check Docker socket permissions (macOS/Linux)
ls -la /var/run/docker.sock

# Should be accessible to your user
# If not, add user to docker group (Linux):
sudo usermod -aG docker $USER
# Then log out and back in
```

**💡 Learning**: Containers have security restrictions

---

## 🤖 OpenAI API Issues

### Problem: "API Key Invalid"

**Symptoms**: Tools return fallback responses instead of AI-generated ones

**Diagnostic**:
```bash
# Check if secret is set
docker mcp secret list

# Should show OPENAI_API_KEY
```

**Solutions**:

1. **Verify Key is Valid**:
   - Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Check key exists and is active
   - Copy the FULL key (starts with `sk-`)

2. **Set Secret Correctly**:
```bash
# Remove old secret
docker mcp secret rm OPENAI_API_KEY

# Set new secret
docker mcp secret set OPENAI_API_KEY="sk-your-actual-key-here"

# Verify
docker mcp secret list
```

3. **Rebuild Container** (if needed):
```bash
# Stop any running containers
docker stop $(docker ps -q --filter ancestor=karen-mcp-server)

# Let MCP gateway restart them with new secrets
```

**💡 Learning**: Secrets are injected at container start, not runtime

---

### Problem: Rate Limit Errors

**Symptoms**:
```
Error: Rate limit exceeded
```

**Cause**: Too many OpenAI API requests

**Solutions**:
1. **Wait a bit** - Rate limits reset
2. **Use fallback mode** - Remove OPENAI_API_KEY temporarily
3. **Upgrade OpenAI plan** - For higher limits

**💡 Learning**: Free tier OpenAI has request limits

---

### Problem: API Timeout

**Symptoms**: Tools take forever, then fail

**Current timeout**: 30 seconds (in code)

**Solutions**:
1. **Check OpenAI status**: [status.openai.com](https://status.openai.com)
2. **Increase timeout**: Edit `karen_server.py`:
```python
API_TIMEOUT = 60  # Increase from 30 to 60 seconds
```
3. **Try different model**: 
```bash
docker mcp secret set OPENAI_MODEL="gpt-3.5-turbo"
```

**💡 Learning**: External APIs can be slow or unreliable

---

### Problem: Poor Response Quality

**Symptoms**: Karen responses aren't funny or are too generic

**Solutions**:

1. **Try GPT-4** (better quality):
```bash
docker mcp secret set OPENAI_MODEL="gpt-4"
```

2. **Increase Temperature** (more creative):
   - Edit `karen_server.py`
   - Change `"temperature": 0.8` to `0.9` or `1.0`
   - Higher = more creative (but less predictable)

3. **Enhance System Prompts**:
   - Edit specific tool system prompts
   - Add more Karen-specific phrases
   - Be more explicit about desired tone

**💡 Learning**: Prompt engineering affects AI output quality

---

## 🐌 Performance Problems

### Problem: Slow Tool Responses

**Symptoms**: Tools take 5-10+ seconds to respond

**Causes & Solutions**:

1. **OpenAI API Latency** (most common):
   - Solution: Use fallback mode (no API key)
   - Fallback responses are instant!

2. **Container Startup Time**:
   - First call starts container (1-2 seconds)
   - Subsequent calls are faster
   - Solution: This is normal behavior

3. **Network Issues**:
   - Check internet speed
   - Try different network

**💡 Learning**: External API calls add latency

---

### Problem: High Memory Usage

**Symptoms**: Docker eating RAM

**Check memory**:
```bash
docker stats
```

**Solutions**:
1. **Limit container memory**:
```bash
# In Dockerfile, add:
# --memory=512m to docker run args
```

2. **Stop unused containers**:
```bash
docker container prune
```

**💡 Learning**: Containers use system resources

---

## 🔬 Advanced Debugging

### Enable Verbose Logging

Edit `karen_server.py`:
```python
# Change from INFO to DEBUG
logging.basicConfig(
    level=logging.DEBUG,  # More detailed logs
    # ...
)
```

**Rebuild**:
```bash
docker build -t karen-mcp-server .
```

**💡 Learning**: Debug logging shows internal operations

---

### Test MCP Protocol Directly

Send raw MCP messages:

```bash
# Initialize connection
(echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":1}' && \
 echo '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' && \
 echo '{"jsonrpc":"2.0","method":"tools/list","id":2}') | \
  docker run -i --rm karen-mcp-server:latest
```

**💡 Learning**: MCP is just JSON-RPC messages over stdio

---

### Inspect Network Traffic

```bash
# Run container with network debugging
docker run -i --rm --network host karen-mcp-server:latest
```

**💡 Learning**: Understanding how containers communicate

---

### Read Source Code

When all else fails:
```bash
# Read FastMCP source
python3 -c "import mcp; print(mcp.__file__)"

# Read the code to understand internals
```

**💡 Learning**: Best debugging is understanding the code!

---

## 🆘 Still Stuck?

### Check These Resources

1. **MCP Official Docs**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
2. **FastMCP GitHub**: Issues and discussions
3. **Docker Docs**: Container troubleshooting
4. **OpenAI Status**: Check for outages

### Common Gotchas Checklist

- [ ] Docker Desktop is running
- [ ] Image is built (`docker images | grep karen`)
- [ ] YAML files have correct indentation (2 spaces)
- [ ] Registry entry is under `registry:` key
- [ ] Catalog is in Claude config args
- [ ] Claude Desktop fully restarted (Quit, not close)
- [ ] API key starts with `sk-` if using OpenAI
- [ ] Container can start manually
- [ ] No typos in file paths or names

### Debug Like a Pro

1. **Start Simple**: Test without OpenAI API first
2. **Check Logs**: Always check Docker logs
3. **Test Manually**: Use echo/docker commands
4. **One Change**: Fix one thing at a time
5. **Read Errors**: Error messages usually tell you what's wrong!
6. **Compare Working**: Check against original code
7. **Ask for Help**: With logs and specific error messages

---

## 🎓 What You've Learned

Through troubleshooting, you now understand:
- ✅ How Docker containers work
- ✅ How MCP servers communicate (JSON-RPC)
- ✅ How secrets are managed
- ✅ How to debug distributed systems
- ✅ How to read logs effectively
- ✅ How configuration files connect services
- ✅ How to test components in isolation

**Debugging is learning!** Every error teaches you something about how the system works.

---

## 💡 Prevention Tips

**Avoid Future Issues**:
1. Keep backups of working configurations
2. Test changes in isolation
3. Document what you change
4. Use version control (Git)
5. Read error messages carefully
6. Start simple, add complexity gradually

**Remember**: Everyone hits these issues. You're learning valuable debugging skills! 🚀
