# 🎓 Karen MCP Server: Learn MCP 101 While Laughing! 🚀

**Your Fun Introduction to the Model Context Protocol**

Welcome to the most entertaining way to learn MCP basics! This project teaches you how to build, deploy, and use MCP servers by creating hilarious "Karen Product Manager" tools that every developer will recognize. You'll learn real MCP concepts while generating over-the-top PM demands, impossible deadlines, and feature requests that ignore all technical reality.

## 🎯 What You'll Learn

By building and using this server, you'll understand:

- **What is MCP?** - The Model Context Protocol that connects AI assistants to tools and data
- **Server Architecture** - How MCP servers expose tools that AI assistants can use
- **Tool Creation** - Building functions that AI can invoke with parameters
- **Docker Deployment** - Packaging and running MCP servers in containers
- **AI Integration** - Using OpenAI API to generate dynamic responses
- **Fallback Systems** - Building resilient tools that work even when APIs fail
- **Real-World Skills** - Everything you learn here applies to building serious MCP servers!

## 🎭 Why "Karen PM"?

Every developer has experienced impossible feature requests, arbitrary deadline changes, and "it's just a button" moments. This server turns those frustrations into comedy while teaching you MCP fundamentals. You'll laugh, you'll cry, you'll build a real MCP server!

## 🌟 Perfect For

- **MCP Beginners** - Your first MCP server with clear examples
- **Visual Learners** - See immediate, hilarious results from your code
- **Developers** - Finally, a tool that understands your pain
- **Students** - Learn by doing (and laughing)
- **Anyone Curious** - About MCP, AI tools, or developer humor

## 🎪 Karen PM Tools (Your Learning Playground!)

Each tool demonstrates key MCP concepts while generating hilariously accurate PM behavior:

### � Karen PM Tools (The Developer's Nightmare!)

These tools capture every developer's worst PM experiences:

1. **`demand_feature_immediately`** - 🎯 **START HERE!**
   - "This should be a simple 5-minute change, right? Just add a button!"
   - *Reality: Complex 3-sprint feature with dependencies*
   - *Teaching: Optional parameters and default values*

2. **`override_engineering_estimate`** 
   - "Three sprints?! I need it by FRIDAY! Just use AI to build it!"
   - *Reality: Ignoring all technical complexity and sprint planning*
   - *Teaching: Multiple parameter handling*

3. **`change_requirements_post_deployment`** 
   - "Actually, what I MEANT was... Why didn't you build what I was THINKING?!"
   - *Reality: Major spec changes after production deployment*
   - *Teaching: Conditional logic in tool responses*

4. **`invoke_competitor_feature`** 
   - "But [Competitor] has this! Can't you just copy it? How hard can it be?"
   - *Reality: Different architectures, user bases, and technical constraints*
   - *Teaching: External data integration concepts*

5. **`escalate_to_ceo_over_ui_color`** 
   - "This button color is BLOCKING the ENTIRE ROADMAP! I need the CEO!"
   - *Reality: Trivial UI decision escalated to executive level*
   - *Teaching: Parameter validation and response formatting*

6. **`schedule_unnecessary_meeting`** 
   - "Let's get EVERYONE in a room for 2 hours to discuss this footer text!"
   - *Reality: Converting 5-minute decisions into multi-hour committees*
   - *Teaching: Time/duration parameter handling*

7. **`request_daily_status_updates`** 
   - "Can you give me HOURLY updates? I need screenshots of your screen!"
   - *Reality: Micromanagement that treats coding like factory work*
   - *Teaching: Frequency/repetition concepts*

8. **`create_urgent_non_urgent_task`** 
   - "Updating the copyright year is URGENT and BLOCKING EVERYTHING!"
   - *Reality: Fake urgency to bypass prioritization*
   - *Teaching: Priority/metadata handling*

9. **`bypass_development_process`** 
   - "We don't have time for testing! Let's skip code review and push it live!"
   - *Reality: Treating security and quality as optional paperwork*
   - *Teaching: Boolean flags and conditional responses*

10. **`demand_impossible_integration`** 
    - "Just make our COBOL mainframe talk to this AI chatbot! They're both computers!"
    - *Reality: Incompatible systems from different decades*
    - *Teaching: Complex parameter relationships*

11. **`generate_sarcastic_status_update`** 
    - "Everything is going EXACTLY as planned... if your plan was chaos!"
    - *Reality: Pretending disasters are 'minor bumps in the road'*
    - *Teaching: Dynamic content generation with sarcasm*

12. **`random_feature_request`** 
    - "Change ALL fonts to Comic Sans! Add blockchain to the login page!"
    - *Reality: Completely absurd ideas disguised as innovation*
    - *Teaching: Random generation and creative AI responses*

13. **`generate_pm_meme`** 🎨 **NEW!**
    - "Drake meme: Reject 'Testing' ❌, Accept 'Ship broken code' ✅"
    - *Reality: Capture PM behavior in perfect meme format using Imgflip API*
    - *Teaching: External API integration and image generation*

## 🚀 Quick Start (Your MCP Learning Journey!)

### What You Need (Prerequisites)

- **Docker Desktop** with MCP Toolkit enabled ([get it here](https://www.docker.com/products/docker-desktop))
- **Claude Desktop** ([download](https://claude.ai/download))
- **OpenAI API key** (optional - server works without it using fallback responses)
  - Get one at [platform.openai.com](https://platform.openai.com)
  - Free tier is fine for learning!

### 🎓 Step-by-Step Installation (Learn While You Build!)

#### Step 1: Build Your First MCP Server! 🏗️

**Using Makefile (Recommended - Docker-First Workflow)**
```bash
cd karen-mcp-server

# See all available commands
make help

# Build the Docker image
make build

# Run tests to verify everything works
make test

# Run all validation checks
make all
```

**Manual Docker Build (Alternative)**
```bash
cd karen-mcp-server
docker build -t karen-mcp-server:latest .
docker run --rm karen-mcp-server:latest python test_karen_server.py
```

**💡 What's Happening Here?**
- Docker packages your MCP server into a portable container
- The `Dockerfile` defines the environment (Python 3.11) and dependencies
- Tests run inside Docker to ensure everything works
- This creates an image called `karen-mcp-server:latest`
- **MCP Concept**: Servers can run anywhere Docker runs!

**📝 Local Development Note:**
- This project requires Python 3.11+ (for FastMCP compatibility)
- If you have Python 3.9 or older, use Docker (recommended)
- The Makefile now uses Docker for all operations (build, test, run, validate)
- No local Python setup needed - Docker handles everything!

#### Step 2: Set Up AI Integration (Optional) 🤖

**Option A: Using .env File (Best for Testing & Learning)**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use any text editor

# Your .env should look like:
# OPENAI_API_KEY=sk-your-key-here
# OPENAI_MODEL=gpt-4o-mini
# IMGFLIP_USERNAME=your-username
# IMGFLIP_PASSWORD=your-password

# Test with real APIs - automatically loads .env
make test

# Run server with .env - automatically loaded
make run
```

**Option B: Using Docker Secrets (Best for Production)**
```bash
# Store your OpenAI API key securely
docker mcp secret set OPENAI_API_KEY="sk-your-api-key-here"

# Choose your AI model (optional)
docker mcp secret set OPENAI_MODEL="gpt-4"

# Verify secrets are stored
docker mcp secret list
```

**💡 What's Happening Here?**
- `.env` files are perfect for local testing and development
- Docker secrets are stored securely (never in your code!)
- The server uses OpenAI to generate creative Karen responses
- Without an API key, it uses pre-written fallback responses
- **MCP Concept**: Servers can integrate with external APIs!
- **Best Practice**: Use `.env` locally, Docker secrets in production

#### Step 3: Register Your Server 📋

Create or edit `~/.docker/mcp/catalogs/custom.yaml`:

```bash
mkdir -p ~/.docker/mcp/catalogs
nano ~/.docker/mcp/catalogs/custom.yaml
```

Add this configuration:

```yaml
version: 2
name: custom
displayName: MCP Learning - Custom Servers
registry:
  karen:
    description: "Learn MCP basics with humorous PM behavior tools"
    title: "Karen PM Server (MCP 101)"
    type: server
    dateAdded: "2025-11-07T00:00:00Z"
    image: karen-mcp-server:latest
    tools:
      # Karen PM Tools (Developer Edition!)
      - name: demand_feature_immediately
      - name: override_engineering_estimate
      - name: change_requirements_post_deployment
      - name: invoke_competitor_feature
      - name: escalate_to_ceo_over_ui_color
      - name: schedule_unnecessary_meeting
      - name: request_daily_status_updates
      - name: create_urgent_non_urgent_task
      - name: bypass_development_process
      - name: demand_impossible_integration
      - name: generate_sarcastic_status_update
      - name: random_feature_request
      - name: generate_pm_meme
    
    secrets:
      - name: OPENAI_API_KEY
        env: OPENAI_API_KEY
        example: sk-...
      - name: OPENAI_MODEL
        env: OPENAI_MODEL
        example: gpt-3.5-turbo
    
    metadata:
      category: education
      tags:
        - learning
        - mcp-101
        - tutorial
        - humor
        - product-management
        - development
      license: MIT
```

**💡 What's Happening Here?**
- The catalog is like an app store for MCP servers
- It tells Claude Desktop what tools your server provides
- The `tools` list defines what AI can invoke
- **MCP Concept**: Catalogs make servers discoverable!

#### Step 4: Update Registry 📝

Edit `~/.docker/mcp/registry.yaml`:

```bash
nano ~/.docker/mcp/registry.yaml
```

Add under the existing `registry:` key:

```yaml
registry:
  # ... existing servers ...
  karen:
    ref: ""
```

**⚠️ IMPORTANT**: Must be under `registry:`, not at root level!

**💡 What's Happening Here?**
- Registry maps server names to their configurations
- This connects your catalog entry to the MCP gateway
- **MCP Concept**: Gateway routes requests to correct servers!

#### Step 5: Connect to Claude Desktop 🔌

Find your config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Edit and add your custom catalog:

```json
{
  "mcpServers": {
    "mcp-toolkit-gateway": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v", "/var/run/docker.sock:/var/run/docker.sock",
        "-v", "/Users/your_username/.docker/mcp:/mcp",
        "docker/mcp-gateway",
        "--catalog=/mcp/catalogs/docker-mcp.yaml",
        "--catalog=/mcp/catalogs/custom.yaml",
        "--config=/mcp/config.yaml",
        "--registry=/mcp/registry.yaml",
        "--tools-config=/mcp/tools.yaml",
        "--transport=stdio"
      ]
    }
  }
}
```

**💡 What's Happening Here?**
- Claude Desktop communicates with MCP servers via stdio
- The gateway manages multiple MCP servers
- Multiple catalogs can be loaded (default + custom)
- **MCP Concept**: AI and tools communicate through JSON-RPC!

#### Step 6: Launch and Test! 🎉

1. **Quit Claude Desktop completely** (Command+Q on Mac)
2. **Restart Claude Desktop**
3. **Test your first MCP tool!**

Try asking Claude:
> "I need a feature built by tomorrow, but engineering says it'll take 3 sprints. Use the demand_feature_immediately tool!"

**💡 What's Happening Here?**
- Claude sees your tools and knows when to use them
- When you mention a tool, Claude invokes it
- The server processes the request and returns a response
- **MCP Concept**: AI assistants orchestrate tool usage!

## 🎮 Try It Out! (Discover the Responses Yourself!)

### 🎯 Karen PM Scenarios (Start Here!)

**Ready to see some hilarious PM behavior?** Fire up Claude and try these:

**Scenario 1: The Classic "Just Add a Button"**
```
"The client wants a real-time collaborative editing feature with conflict resolution. 
Engineering says it's 3 sprints. Use demand_feature_immediately to respond."
```
💡 **What You'll Learn**: How AI invokes tools with parameters
😂 **What You'll See**: ...run it to find out!

**Scenario 2: Deadline Override**
```
"The database migration team estimated 2 weeks. We need it by Friday. 
Use override_engineering_estimate."
```
💡 **What You'll Learn**: Multiple parameters, response formatting
🔥 **What You'll See**: Trust me, you'll laugh

**Scenario 3: Post-Launch Surprise**
```
"The login screen is live, but now I need OAuth, SSO, biometric auth, 
and magic links. Use change_requirements_post_deployment."
```
💡 **What You'll Learn**: Context-aware responses
🎭 **What You'll See**: Classic PM gaslighting in action

**Scenario 4: Competitor Envy**
```
"Our competitor has blockchain AI in the cloud. We need this too! 
Use invoke_competitor_feature."
```
💡 **What You'll Learn**: How tools reference external context
🤦 **What You'll See**: Zero understanding of technical feasibility

**Scenario 5: The Great Button Color Debate**
```
"The login button needs to be #2E86AB instead of #2E86AC. 
Use escalate_to_ceo_over_ui_color."
```

**Scenario 6: Fake Status Report**
```
"The project is 3 weeks behind, over budget, and half the team quit. 
Use generate_sarcastic_status_update to report to stakeholders."
```

**Scenario 7: Random Chaos Generator**
```
"We need a new feature idea. Use random_feature_request to generate something."
```

**Scenario 8: PM Meme Creation** 🎨
```
"Create a meme about demanding features with impossible deadlines using generate_pm_meme."
```

### 🎭 More Scenarios to Try

**PM Greatest Hits**:
- Schedule a 2-hour meeting about footer text
- Request hourly updates on a database migration
- Mark copyright year update as URGENT
- Skip testing because "we don't have time for process"
- Integrate a COBOL mainframe with an AI chatbot
- Generate a status update pretending the disaster is fine
- Get a random absurd feature suggestion
- Create PM behavior memes (deadline chaos, competitor envy, process bypass)

### 🎓 Your Learning Journey

1. **🌱 Start**: Try 3-5 tools, see what happens
2. **🚀 Explore**: Experiment with different parameters
3. **🎨 Create**: Combine tools to build funny scenarios
4. **🔬 Understand**: Read the code to see how it works
5. **🏆 Master**: Build your own tools!

**💡 Pro Tip**: The responses are even funnier than you imagine. Go try them!

## 📚 Understanding MCP Through Karen

### The MCP Stack (Simplified!)

```
┌─────────────────────────────────────┐
│  YOU (via Claude Desktop)           │  ← User requests something
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  CLAUDE (AI Assistant)               │  ← Decides which tool to use
│  - Understands your request          │
│  - Chooses appropriate tool          │
│  - Passes parameters                 │
└──────────────┬──────────────────────┘
               │  MCP Protocol (JSON-RPC)
               ▼
┌─────────────────────────────────────┐
│  MCP GATEWAY (Docker)                │  ← Routes to correct server
│  - Manages multiple servers          │
│  - Handles authentication            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  KAREN SERVER (Your Code!)           │  ← Executes the tool
│  - Receives tool invocation          │
│  - Processes parameters              │
│  - Returns formatted response        │
└──────────────┬──────────────────────┘
               │  (Optional)
               ▼
┌─────────────────────────────────────┐
│  OPENAI API                          │  ← Generates creative content
│  - Creates dynamic responses         │
│  - Adds variety and humor            │
└─────────────────────────────────────┘
```

### Key MCP Concepts You're Learning

1. **Tools** = Functions AI can call
   - Example: `demand_feature_immediately()` is a tool
   
2. **Parameters** = Inputs to tools
   - Example: `feature="user authentication"`, `deadline="tomorrow"`
   
3. **Server** = Collection of related tools
   - Example: Karen PM server has 13 PM behavior tools
   
4. **Protocol** = How AI and server communicate
   - MCP uses JSON-RPC over stdio
   
5. **Transport** = How messages are sent
   - stdin/stdout for local, HTTP for remote
   
6. **Catalog** = Directory of available servers
   - Your custom.yaml is a catalog
   
7. **Registry** = Maps servers to their locations
   - Tells gateway where to find servers

## 🛠️ Development & Learning

### 🔍 Explore the Code

The server code is heavily commented to teach MCP concepts:

```python
# karen_server.py - Check out these learning sections:

1. Tool Definition
   @mcp.tool()  # ← This decorator makes a function an MCP tool
   async def demand_feature_immediately(feature: str = "", deadline: str = "") -> str:
       """Single-line description that AI sees"""  # ← AI reads this!

2. Parameter Handling
   - Default values make parameters optional
   - Type hints help AI understand what to send
   
3. Response Formatting
   - Returns formatted strings
   - Emojis make output fun and readable
   
4. External API Integration
   - Shows how to call OpenAI
   - Demonstrates fallback patterns
   
5. Error Handling
   - Try-catch blocks for reliability
   - Graceful degradation when APIs fail
```

### 🧪 Test Locally

**Using Makefile (Easy Mode!)**
```bash
# Install dependencies
make install

# Run all tests
make test

# Validate Python syntax
make validate

# Build and run everything
make all
```

**Testing with Real API Keys** 🔑
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys:
# OPENAI_API_KEY=sk-your-key-here
# IMGFLIP_USERNAME=your-username
# IMGFLIP_PASSWORD=your-password

# Run tests - automatically loads .env file
make test

# The Makefile detects .env and mounts it to Docker
# You'll see real OpenAI and Imgflip API calls!
```

**Manual Testing (Advanced)**
```bash
# Test without Claude (great for learning!)
export OPENAI_API_KEY="your-key"

# Run the test suite
python3 test_karen_server.py

# Send MCP protocol messages directly
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  docker run -i --rm karen-mcp-server:latest

# Test a specific tool with your .env file
echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"demand_feature_immediately","arguments":{"feature":"blockchain AI","deadline":"tomorrow"}},"id":2}' | \
  docker run -i --rm --env-file .env karen-mcp-server:latest
```

**💡 What You're Learning**:
- MCP uses JSON-RPC 2.0 protocol
- Tools are listed with `tools/list`
- Tools are called with `tools/call`
- Parameters go in the `arguments` object
- Environment variables keep API keys secure
- Automated testing catches issues early!
- `.env` files work seamlessly with Docker!

### 🎨 Create Your Own Tool!

Try adding this to `karen_server.py`:

```python
@mcp.tool()
async def demand_documentation(feature: str = "") -> str:
    """Demand that devs write docs after shipping to production."""
    
    if not feature.strip():
        feature = "the new feature"
    
    system_prompt = """You are Karen PM demanding documentation be written 
    AFTER the feature is in production. Act like docs are just paperwork 
    that can be done anytime."""
    
    prompt = f"Demand documentation for '{feature}' that's already live"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"📝❌ RETROACTIVE DOCS DEMAND ❌📝\n\n{ai_response}\n\n📚 *Treating documentation as optional paperwork*"
    else:
        return f"📝❌ RETROACTIVE DOCS DEMAND ❌📝\n\nThe feature is LIVE! Can't you just write the docs now? It's just typing! How long could it take?!\n\n📚 *Treating documentation as optional paperwork*"
```

Then:
1. Rebuild: `docker build -t karen-mcp-server .`
2. Add tool name to catalog's `tools:` list
3. Restart Claude Desktop
4. Test your new tool!

**🎓 Congratulations!** You just created an MCP tool!

## ❓ Troubleshooting (Learn from Common Issues!)

### Tools Not Appearing in Claude

**Problem**: Can't see Karen tools in Claude Desktop

**Learning Opportunity**: Understanding the MCP stack!

**Solutions**:
1. Check Docker image exists: `docker images | grep karen`
   - *Learn*: Images must be built before use
2. Verify catalog syntax: `cat ~/.docker/mcp/catalogs/custom.yaml`
   - *Learn*: YAML indentation matters!
3. Check registry entry exists under `registry:` key
   - *Learn*: Registry maps names to servers
4. Restart Claude Desktop **completely** (Quit, not just close)
   - *Learn*: Config is read at startup
5. Check Claude logs for errors
   - *Learn*: Debugging is part of development!

### OpenAI API Errors

**Problem**: "API key invalid" or timeout errors

**Learning Opportunity**: External API integration!

**Solutions**:
1. Verify secret: `docker mcp secret list`
   - *Learn*: Secrets must be set before use
2. Check API key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - *Learn*: API keys can expire or be revoked
3. **No API key?** Server works with fallback responses!
   - *Learn*: Always build fallback systems!

### "Tool Failed" Errors

**Problem**: Tool invocation fails

**Learning Opportunity**: Error handling and debugging!

**Solutions**:
1. Check Docker logs: `docker ps` then `docker logs [container-id]`
   - *Learn*: Logs are your best friend!
2. Test tool locally with JSON-RPC
   - *Learn*: You can test without Claude!
3. Verify parameter types match expectations
   - *Learn*: Type validation prevents errors!

### Responses Too Generic

**Problem**: Karen responses aren't funny enough

**Learning Opportunity**: AI prompt engineering!

**Solutions**:
1. Increase temperature in code (currently 0.8)
   - *Learn*: Temperature controls creativity
2. Enhance system prompts with more specific instructions
   - *Learn*: Better prompts = better results
3. Switch to GPT-4: `docker mcp secret set OPENAI_MODEL="gpt-4"`
   - *Learn*: Different models, different results!

## 📖 Learn More About MCP

### Official Resources
- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

### What to Build Next
- **Personal MCP Server**: Tools for your daily workflow
- **Data Access**: Connect AI to your databases
- **API Integrations**: GitHub, Jira, Slack, etc.
- **Custom AI Agents**: Build specialized assistants
- **Internal Tools**: Company-specific integrations

### MCP Best Practices (Learned Here!)
✅ Clear tool descriptions (AI needs to understand them)
✅ Optional parameters with defaults (more flexible)
✅ Formatted responses (emojis, structure, readability)
✅ Error handling (graceful failures)
✅ Fallback systems (work without external APIs)
✅ Security (secrets in environment, not code)
✅ Documentation (help others learn!)

## 🎉 What You've Accomplished!

By completing this tutorial, you now understand:

- ✅ What MCP is and why it matters
- ✅ How MCP servers expose tools to AI
- ✅ How to build tools with parameters
- ✅ How to deploy servers with Docker
- ✅ How to integrate external APIs (OpenAI)
- ✅ How to build fallback systems
- ✅ How Claude Desktop connects to MCP servers
- ✅ How the MCP protocol works (JSON-RPC)
- ✅ How to debug and troubleshoot MCP servers
- ✅ How to create your own tools!

**🎓 You're now ready to build production MCP servers!**

## 🎭 Why This Matters (The Serious Stuff)

This humorous server teaches real MCP skills you'll use for serious projects:

### Real-World Applications

**What You Learned** → **Where You'll Use It**

- Tool creation → Building business automation
- Parameter handling → User input processing  
- External APIs → Database connections, web services
- Fallback systems → Resilient production code
- Docker deployment → Modern cloud infrastructure
- Error handling → Professional software development
- AI integration → Next-generation applications

### Every Developer's Experience

The Karen PM tools aren't just funny—they're based on real experiences:

- "Just add a button" = Underestimating complexity
- Estimate overrides = Ignoring expertise
- Post-launch changes = Scope creep
- Competitor copying = Misunderstanding architecture
- Unnecessary meetings = Communication overhead
- Process bypassing = Technical debt creation

**Learning with humor makes concepts stick!**

## 🤝 Contributing

Want to add more Karen behaviors or improve the learning experience?

1. Fork the repository
2. Create a feature branch
3. Add your hilarious tool
4. Update documentation
5. Submit a pull request!

**Ideas for contributions**:
- More Karen PM tools
- Better educational comments
- Video tutorials
- Translation to other languages
- Additional learning exercises

## 📄 License

MIT License - Learn freely, build amazing things!

## 🙏 Acknowledgments

- **Every developer** who's experienced these PM moments
- **MCP community** for building this amazing protocol
- **FastMCP** for making server creation simple
- **You** for learning and building!

---

## 🚀 Ready to Build Something Real?

Now that you understand MCP basics, try building:

1. **Personal Assistant**: Tools for your daily tasks
2. **Code Helper**: Integrate with GitHub, run tests, deploy
3. **Data Explorer**: Query databases, visualize data
4. **Team Tools**: Company-specific workflows
5. **Creative Tools**: Generate content, images, music

**The MCP protocol is your playground—go build something awesome! 🎉**

---

### 💬 Questions or Stuck?

- Check the troubleshooting section above
- Review the code comments in `karen_server.py`
- Read the official [MCP docs](https://modelcontextprotocol.io)
- Experiment and have fun!

**Remember**: Every expert was once a beginner. You've got this! 💪