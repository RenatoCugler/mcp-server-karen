# 🎯 MCP Learning Challenges: Test Your Knowledge!

**Fun exercises to master MCP through Karen PM mayhem!**

---

## 📚 How to Use This Guide

Each challenge has:
- 🎯 **Objective**: What you'll learn
- 📝 **Task**: What to do
- 💡 **Hints**: Clues if you're stuck
- ✅ **Solution**: How to complete it
- 🎓 **Learning**: What this teaches

Start with **Level 1** if you're new to MCP!

---

## 🌱 Level 1: Beginner Challenges

### Challenge 1.1: First Tool Call

**Objective**: Successfully invoke your first MCP tool

**Task**:
Open Claude Desktop and make the `speak_to_manager` tool execute.

**Success Criteria**:
- You see a formatted Karen response
- Response includes emojis and dramatic text
- Claude used the tool (didn't just write text itself)

**💡 Hints**:
- Mention the tool by name in your message
- Describe a situation where you'd want a manager
- Let Claude know you want to USE the tool, not just talk about it

**✅ Example Solution**:
```
You: "Someone gave me a small coffee when I ordered medium. 
Use speak_to_manager to escalate this."
```

**🎓 What You're Learning**:
- How to trigger tool invocations
- How AI chooses when to use tools
- Basic MCP request/response flow

---

### Challenge 1.2: Parameter Detective

**Objective**: Understand how parameters work

**Task**:
Call `demand_feature_immediately` with these specific parameters:
- Feature: "time travel capability"
- Deadline: "yesterday"

**Success Criteria**:
- Response mentions "time travel capability"
- Response references "yesterday" as deadline
- You understand how your words became parameters

**💡 Hints**:
- Parameters can be extracted from natural language
- Be explicit about what you want
- Claude is smart about parsing details

**✅ Example Solution**:
```
You: "I need time travel capability added to the app, and I needed 
it yesterday. Use demand_feature_immediately."
```

**🎓 What You're Learning**:
- Parameters pass data to tools
- AI extracts parameters from conversation
- Tools customize responses based on inputs

---

### Challenge 1.3: Fallback Explorer

**Objective**: Experience the fallback system

**Task**:
1. Check if you have OPENAI_API_KEY set
2. Try a tool without the API key
3. Observe the fallback response

**Success Criteria**:
- Tool still works without OpenAI
- Response is coherent and Karen-like
- You understand why fallbacks matter

**💡 Hints**:
```bash
# Check secrets
docker mcp secret list

# Remove API key temporarily
docker mcp secret rm OPENAI_API_KEY

# Try a tool in Claude
# Then restore: docker mcp secret set OPENAI_API_KEY="sk-..."
```

**🎓 What You're Learning**:
- Resilient tool design
- Fallback systems prevent total failure
- External dependencies should be optional

---

## 🚀 Level 2: Intermediate Challenges

### Challenge 2.1: Tool Chain Reaction

**Objective**: Use multiple tools in sequence

**Task**:
Create a conversation that uses at least 3 different Karen PM tools, telling a coherent story.

**Example Scenario**:
1. Demand a feature
2. Override the estimate
3. Escalate the button color

**Success Criteria**:
- At least 3 tools invoked
- Story makes sense (even if absurd!)
- You see how tools build on context

**💡 Hints**:
- Start with a feature request
- Build complexity with each tool
- Let the scenario escalate naturally

**✅ Example Solution**:
```
You: "I need a blockchain AI feature. Use demand_feature_immediately."
[Wait for response]

You: "Engineering says 6 months. Override that to 2 days using 
override_engineering_estimate."
[Wait for response]

You: "Now the login button color is wrong. Escalate to CEO with 
escalate_to_ceo_over_ui_color."
```

**🎓 What You're Learning**:
- Tool composition and sequencing
- Context maintenance across invocations
- Building complex interactions

---

### Challenge 2.2: Edge Case Explorer

**Objective**: Test tool boundaries

**Task**:
Find what happens when you:
1. Call a tool with empty/missing parameters
2. Provide contradictory information
3. Use extreme values

**Examples to Try**:
```
- "Use demand_feature_immediately but don't specify a feature"
- "Override estimate from 1 year to 30 seconds"
- "Integrate a typewriter with quantum computer"
```

**Success Criteria**:
- Tools handle weird inputs gracefully
- You understand default parameter behavior
- You see error handling in action

**🎓 What You're Learning**:
- Input validation strategies
- Default parameter values
- Graceful degradation

---

### Challenge 2.3: Response Pattern Analysis

**Objective**: Understand response formatting

**Task**:
1. Call 3 different tools
2. Note the common response patterns
3. Identify what makes them user-friendly

**Look For**:
- Emoji usage
- Text structure (sections, spacing)
- Consistency across tools
- Action descriptions

**Success Criteria**:
- List 5+ response patterns you found
- Explain why they improve user experience
- Apply these patterns to your own tools

**🎓 What You're Learning**:
- UX design for tool responses
- Consistency in output formatting
- Making technical outputs human-friendly

---

## 🎨 Level 3: Creative Challenges

### Challenge 3.1: New Tool Creator

**Objective**: Build your own Karen PM tool

**Task**:
Add a new tool to `karen_server.py`:

**Tool Name**: `demand_documentation_later`

**Behavior**: PM wants docs written AFTER shipping to production

**Requirements**:
- Accept a `feature` parameter
- Generate a Karen-style response
- Follow existing tool patterns
- Include emojis and formatting

**💡 Hints**:
```python
@mcp.tool()
async def demand_documentation_later(feature: str = "") -> str:
    """Demand that devs write docs after shipping to production."""
    # Your code here!
```

**Steps**:
1. Add function to `karen_server.py`
2. Rebuild: `docker build -t karen-mcp-server .`
3. Add tool name to catalog's tools list
4. Restart Claude Desktop
5. Test it!

**✅ Solution Structure**:
```python
@mcp.tool()
async def demand_documentation_later(feature: str = "") -> str:
    """Demand that devs write docs after shipping to production."""
    if not feature.strip():
        feature = "the new feature"
    
    system_prompt = """You are Karen PM who thinks documentation 
    is optional paperwork that can be done anytime..."""
    
    prompt = f"Demand documentation for '{feature}' that's already live"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"📝❌ DOCS CAN WAIT ❌📝\n\n{ai_response}\n\n📚 *Treating documentation as optional*"
    else:
        return f"📝❌ DOCS CAN WAIT ❌📝\n\nThe feature is LIVE! Just write the docs later! It's just typing!\n\n📚 *Treating documentation as optional*"
```

**🎓 What You're Learning**:
- Complete tool creation workflow
- @mcp.tool() decorator usage
- Tool registration and discovery
- End-to-end MCP server development

---

### Challenge 3.2: System Prompt Engineer

**Objective**: Improve AI response quality

**Task**:
Pick any tool and enhance its system prompt to generate better/funnier responses.

**Method**:
1. Read current system prompt
2. Identify what could be better
3. Add more specific instructions
4. Test and iterate

**Example Enhancement**:
```python
# Before (generic)
system_prompt = """You are Karen PM who is unreasonable."""

# After (specific)
system_prompt = """You are Karen PM who:
- Uses LOTS of ALL CAPS
- Mentions your "15 years of experience"
- Threatens to escalate to C-suite
- Compares everything to competitors
- Claims it's "just a simple change"
- Ignores all technical constraints
- Makes unrealistic deadline demands
Be dramatic, entitled, and hilariously wrong about technical complexity!"""
```

**Success Criteria**:
- Responses are noticeably better
- More consistent Karen personality
- Funnier/more dramatic outputs

**🎓 What You're Learning**:
- Prompt engineering fundamentals
- AI instruction optimization
- Iterative improvement process

---

### Challenge 3.3: Real PM Quote Collection

**Objective**: Connect tools to reality

**Task**:
1. Collect 10 real PM quotes you've heard
2. Map each to a Karen tool
3. Test if tools capture the essence
4. Share your findings!

**Example**:
```
Real Quote: "Can't we just parallelize it to make it faster?"
Tool: override_engineering_estimate
Test: "Override estimate by suggesting we parallelize it..."
```

**Success Criteria**:
- 10 real quotes collected
- Matched to appropriate tools
- Tested in Claude
- Documented your results

**🎓 What You're Learning**:
- Real-world pattern recognition
- Tool-to-problem mapping
- Understanding developer pain points
- Why humor aids learning

---

## 🔬 Level 4: Advanced Challenges

### Challenge 4.1: Protocol Inspector

**Objective**: Understand MCP protocol details

**Task**:
Send raw MCP messages and analyze responses.

**Steps**:
```bash
# 1. List tools
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  docker run -i --rm karen-mcp-server:latest

# 2. Analyze the JSON response
# 3. Document the structure
# 4. Call a specific tool
# 5. Compare request/response formats
```

**Success Criteria**:
- Understand JSON-RPC structure
- Can manually craft tool invocations
- Know what fields are required
- Documented request/response schemas

**🎓 What You're Learning**:
- MCP protocol internals
- JSON-RPC 2.0 specification
- Request/response message structure
- Low-level debugging skills

---

### Challenge 4.2: Performance Optimizer

**Objective**: Make tools faster

**Task**:
1. Measure tool response time
2. Identify bottlenecks
3. Implement optimizations
4. Measure improvements

**Ideas to Try**:
- Cache OpenAI responses
- Reduce timeout for faster failure
- Optimize string operations
- Use faster JSON parsing

**💡 Benchmark Code**:
```python
import time
start = time.time()
# tool execution
end = time.time()
logger.info(f"Tool took {end-start:.2f} seconds")
```

**Success Criteria**:
- Measured baseline performance
- Identified slowest operations
- Implemented at least 2 optimizations
- Documented speed improvements

**🎓 What You're Learning**:
- Performance profiling
- Optimization techniques
- Tradeoffs between speed and features
- Production considerations

---

### Challenge 4.3: Error Simulator

**Objective**: Build robust error handling

**Task**:
Intentionally break things and handle errors gracefully.

**Scenarios to Test**:
1. OpenAI API returns error
2. Network timeout
3. Invalid parameters
4. Malformed JSON
5. Container resource limits

**Requirements**:
- Tools never crash the server
- Error messages are helpful
- Logs show what went wrong
- Fallbacks activate appropriately

**💡 Test Method**:
```python
# Simulate API failure
async def call_openai_with_failure(prompt: str) -> str:
    import random
    if random.random() < 0.5:
        raise Exception("Simulated API failure!")
    # normal code...
```

**🎓 What You're Learning**:
- Defensive programming
- Error handling strategies
- Graceful degradation
- Production reliability

---

## 🏆 Level 5: Expert Challenges

### Challenge 5.1: Multi-Server Architecture

**Objective**: Build a second MCP server that works with Karen

**Task**:
Create a "Reasonable PM" server with opposite behaviors:
- Accepts estimates
- Respects development process
- Understands technical complexity
- Schedules reasonable meetings

**Requirements**:
- Separate server (different name)
- 5+ tools
- Works alongside Karen server
- Both accessible in Claude

**🎓 What You're Learning**:
- Multi-server MCP architecture
- Server isolation and independence
- Tool namespace management
- Complex MCP deployments

---

### Challenge 5.2: Database Integration

**Objective**: Add persistent state

**Task**:
Modify Karen server to remember:
- How many times each tool was called
- Common feature requests
- Most overridden estimates
- Escalation history

**Requirements**:
- SQLite database in container
- Track tool usage
- Query statistics
- Display fun metrics

**💡 Hints**:
```python
import sqlite3

# Create table
conn = sqlite3.connect('karen_stats.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tool_calls
             (tool_name TEXT, timestamp TEXT)''')

# Track call
c.execute("INSERT INTO tool_calls VALUES (?, ?)", 
          (tool_name, datetime.now()))
conn.commit()
```

**🎓 What You're Learning**:
- Stateful MCP servers
- Database integration
- Data persistence
- Analytics and metrics

---

### Challenge 5.3: Custom MCP Server from Scratch

**Objective**: Build a production-quality MCP server

**Task**:
Create a completely new MCP server for something YOU need:
- Personal productivity tools
- Work automation
- API integrations
- Data processing

**Requirements**:
- At least 5 tools
- Proper error handling
- Documentation
- Tests
- Docker deployment
- Real usefulness!

**Success Criteria**:
- Solves a real problem
- Professional code quality
- Deployed and working
- Others can use it

**🎓 What You're Learning**:
- Complete MCP development cycle
- Production best practices
- Real-world problem solving
- Open source contribution potential

---

## 🎓 Learning Progress Tracker

Mark off as you complete:

**Level 1: Beginner** 🌱
- [ ] First Tool Call
- [ ] Parameter Detective
- [ ] Fallback Explorer

**Level 2: Intermediate** 🚀
- [ ] Tool Chain Reaction
- [ ] Edge Case Explorer
- [ ] Response Pattern Analysis

**Level 3: Creative** 🎨
- [ ] New Tool Creator
- [ ] System Prompt Engineer
- [ ] Real PM Quote Collection

**Level 4: Advanced** 🔬
- [ ] Protocol Inspector
- [ ] Performance Optimizer
- [ ] Error Simulator

**Level 5: Expert** 🏆
- [ ] Multi-Server Architecture
- [ ] Database Integration
- [ ] Custom MCP Server from Scratch

---

## 🎉 Completion Rewards

### Beginner Badge 🌱
Completed Level 1? You understand MCP basics!
**Next**: Build on this foundation with intermediate challenges

### Intermediate Badge 🚀
Completed Level 2? You can use MCP effectively!
**Next**: Get creative with tool development

### Creative Badge 🎨
Completed Level 3? You can modify and create tools!
**Next**: Deep dive into internals

### Advanced Badge 🔬
Completed Level 4? You understand MCP deeply!
**Next**: Build production systems

### Expert Badge 🏆
Completed Level 5? You're an MCP master!
**Next**: Contribute to the ecosystem, teach others!

---

## 💡 Challenge Creation Guidelines

Want to add your own challenges?

**Good Challenges**:
- ✅ Have clear objectives
- ✅ Build on previous knowledge
- ✅ Include hints and solutions
- ✅ Teach specific concepts
- ✅ Are achievable but not trivial

**Challenge Template**:
```markdown
### Challenge X.X: [Name]

**Objective**: [What you'll learn]

**Task**: [What to do]

**Success Criteria**:
- [How to know you succeeded]

**💡 Hints**:
- [Helpful clues]

**✅ Solution**:
[How to complete it]

**🎓 What You're Learning**:
- [Key concepts]
```

---

## 🎯 Your Learning Journey

Remember:
- 🐌 **Go at your own pace** - Learning takes time
- 🔄 **Repeat challenges** - Practice makes perfect
- 💡 **Experiment freely** - Breaking things teaches you
- 🤝 **Ask for help** - Everyone was a beginner once
- 🎉 **Celebrate progress** - Every challenge completed is growth!

**The goal isn't just completing challenges—it's understanding MCP deeply enough to build amazing things!**

---

## 🚀 Beyond the Challenges

Once you've mastered these:
1. **Build real tools** for your workflow
2. **Contribute to open source** MCP projects
3. **Share your knowledge** - teach others
4. **Create challenges** for the community
5. **Push MCP boundaries** - innovate!

**You started with Karen PM jokes. You're ending as an MCP developer. That's amazing! 🎊**

---

*Happy Learning and Building! May your features ship on time and your estimates never be overridden! 😄*
