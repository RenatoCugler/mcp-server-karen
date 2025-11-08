# 🎮 Interactive Examples: Learn MCP with Karen PM!

This guide provides hands-on scenarios to help you understand MCP concepts through hilarious Karen PM interactions.

## 📚 Table of Contents

- [Beginner Examples](#-beginner-examples-your-first-tools)
- [Intermediate Examples](#-intermediate-examples-complex-scenarios)
- [Advanced Examples](#-advanced-examples-combining-tools)
- [Real Development Scenarios](#-real-development-scenarios)
- [Creative Challenges](#-creative-challenges)

---

## 🌱 Beginner Examples (Your First Tools)

### Example 1: The "Just Add a Button" Request

**Scenario**: Client wants a feature, engineering says it's complex, PM thinks it's trivial.

**Try This in Claude**:
```
"I need a real-time collaborative document editing feature with conflict resolution, 
operational transforms, and presence indicators. Engineering says it's a 3-sprint project. 
Use demand_feature_immediately to respond as a PM."
```

**Expected Output**:
```
💼🔥 PM KAREN DEMANDS 🔥💼

This should be a SIMPLE 5-minute change, right?! Can't you just ADD A BUTTON 
for collaboration?! I promised the client this would be ready by TOMORROW! 
Why is engineering always making excuses?! Just copy the code from Google Docs! 
How hard can it be?!

⚡ *Completely ignoring technical reality and sprint planning*
```

**🎓 What You're Learning**:
- ✅ Tools receive parameters (`feature` and `deadline`)
- ✅ Tools return formatted text responses
- ✅ AI chooses the right tool based on context
- ✅ Parameters can be extracted from natural language

**💡 Try Variations**:
- Change the feature to "blockchain integration"
- Change the deadline to "by end of day"
- Ask for multiple features at once

---

### Example 2: Overriding Engineering Estimates

**Scenario**: Engineers give realistic estimates, PM has "better" ideas.

**Try This**:
```
"The backend team estimated the database migration will take 2 weeks with proper 
testing and rollback procedures. We need it done by Friday. Use override_engineering_estimate."
```

**Expected Output**:
```
📊❌ ESTIMATE OVERRIDE ACTIVATED ❌📊

Two WEEKS?! That sounds like PADDING to me! This is definitely a ONE-DAY task! 
Just export the data and import it! Why can't we just use AI to migrate it?! 
I'm OVERRIDING that estimate - this will be done by Friday!

🎯 *Completely disrespecting engineering expertise and technical complexity*
```

**🎓 What You're Learning**:
- ✅ Tools can have multiple parameters (task, original_estimate, new_deadline)
- ✅ Default values make parameters optional
- ✅ Tools can reference all parameters in responses
- ✅ AI extracts structured data from conversational input

**💡 Try Variations**:
- Different tasks: "security audit", "performance optimization"
- Different estimates: "3 months", "6 sprints", "Q4"
- Different deadlines: "tomorrow", "next week", "by lunch"

---

### Example 3: Post-Deployment Requirements Change

**Scenario**: Feature is live, PM suddenly remembers what they "actually" wanted.

**Try This**:
```
"We just launched the login system with email/password authentication. 
Now I need it to support OAuth, SSO, biometric authentication, passwordless 
magic links, and 2FA. Use change_requirements_post_deployment."
```

**Expected Output**:
```
📝🔄 REQUIREMENTS CHANGE GASLIGHTING 🔄📝

Actually, what I MEANT was OAuth, SSO, and biometric auth! This was ALWAYS 
part of the original scope! It's just ONE small addition! Why didn't you 
BUILD what I was thinking?! The client just clarified this was needed! 
This should be a MINOR change!

🧠 *Rewriting history and blaming engineers for not reading minds*
```

**🎓 What You're Learning**:
- ✅ Tools can handle complex, multi-part inputs
- ✅ Responses can include context from parameters
- ✅ AI understands the humor/sarcasm pattern
- ✅ One tool invocation can process lots of information

---

## 🚀 Intermediate Examples (Complex Scenarios)

### Example 4: The Competitor Copy Request

**Scenario**: PM sees a screenshot of a competitor's feature, wants exact copy.

**Try This**:
```
"I saw that FancyApp has this amazing AI-powered dashboard with predictive analytics. 
Our architecture is completely different, but we need this exact feature. 
Use invoke_competitor_feature to demand it."
```

**Expected Output**:
```
📱👀 COMPETITOR COMPARISON DEMAND 👀📱

But FancyApp has this amazing feature! Can't we just COPY it?! How hard can it be? 
They built it! Just make it look EXACTLY like their screenshot! I don't understand 
why you're making excuses about "different architectures"! It's all SOFTWARE!

🎯 *Ignoring all technical and business context while demanding feature copies*
```

**🎓 What You're Learning**:
- ✅ Tools can reference external entities (competitors)
- ✅ Context matters in tool responses
- ✅ Parameters can be company/product names
- ✅ Tools maintain personality across different inputs

**💡 Real Development Insight**:
This happens because PMs often don't understand:
- Different tech stacks require different implementations
- UI similarity ≠ code similarity
- Features may be loss-leaders or rely on proprietary tech
- User bases and use cases differ

---

### Example 5: Trivial Escalation

**Scenario**: Minor UI decision escalated to executive level.

**Try This**:
```
"The design team can't decide if the submit button should be #2E86AB or #2E86AC 
blue. This is holding up the release! Use escalate_to_ceo_over_ui_color."
```

**Expected Output**:
```
🚨💼 CEO ESCALATION PROTOCOL 💼🚨

This button color issue is BLOCKING the ENTIRE ROADMAP! I need to escalate 
this to the CEO IMMEDIATELY! This is a CRITICAL business decision that requires 
executive attention! I'm calling an EMERGENCY meeting with the C-suite about #2E86AB!

📧 *CCing entire executive team on trivial UI decisions*
```

**🎓 What You're Learning**:
- ✅ Tools can dramatize low-stakes situations
- ✅ Parameters can be very specific (hex colors)
- ✅ Tools maintain humor through exaggeration
- ✅ AI understands the absurdity being requested

---

### Example 6: Meeting Overload

**Scenario**: Something that could be a Slack message becomes a 2-hour meeting.

**Try This**:
```
"We need to discuss whether to use 'Login' or 'Sign In' as the button text. 
Use schedule_unnecessary_meeting to set this up."
```

**Expected Output**:
```
📅💤 MEETING OVERLOAD ACTIVATED 💤📅

Let's circle back on this! I think we need to ALIGN on the button text! 
I'm scheduling a 2-HOUR meeting with the ENTIRE engineering team, design, 
product, and stakeholders to discuss 'Login' vs 'Sign In'! This deserves 
its own meeting! Let's get everyone in a room!

⏰ *Converting 5-minute decisions into multi-hour committee discussions*
```

**🎓 What You're Learning**:
- ✅ Tools can handle time/duration parameters
- ✅ Responses can suggest specific meeting lengths
- ✅ Humor comes from disproportionate responses
- ✅ Tools reflect real workplace pain points

---

## 🎯 Advanced Examples (Combining Tools)

### Example 7: The Full PM Experience

**Try This Conversation** (multiple tool invocations):

```
You: "We need a feature that shows real-time analytics with live charts."

Claude: [Might ask for clarification or use demand_feature_immediately]

You: "Engineering says it's 4 weeks. Use override_engineering_estimate to respond."

Claude: [Uses override_engineering_estimate]

You: "Now we've launched it, but I forgot to mention it needs to support 
mobile, export to PDF, and email reports. Use change_requirements_post_deployment."

Claude: [Uses change_requirements_post_deployment]

You: "Our competitor has this feature with AI predictions. Use invoke_competitor_feature."

Claude: [Uses invoke_competitor_feature]

You: "The chart colors are wrong. This needs CEO attention. 
Use escalate_to_ceo_over_ui_color."

Claude: [Uses escalate_to_ceo_over_ui_color]
```

**🎓 What You're Learning**:
- ✅ Multiple tools can be used in sequence
- ✅ Each tool maintains its own personality
- ✅ Tools build on previous context
- ✅ Realistic PM behavior patterns emerge
- ✅ You're experiencing a day in the life of a developer!

---

## 💼 Real Development Scenarios

### Scenario A: Sprint Planning Gone Wrong

**The Situation**:
```
Your backlog has:
1. Database migration (2 weeks)
2. Security audit (1 week)
3. Performance optimization (3 weeks)
4. New feature X (4 weeks)

PM wants everything done in 1 sprint (2 weeks).
```

**Try These**:
```
"Override all these estimates and say they're all 2-day tasks. 
Use override_engineering_estimate."

"Mark the copyright year update as more urgent than the security audit. 
Use create_urgent_non_urgent_task."

"Suggest we skip testing and code review to save time. 
Use bypass_development_process."
```

**💡 Learning Point**: Time management and prioritization are constant battles. 
Tools help you laugh about it while understanding the MCP tool invocation pattern.

---

### Scenario B: The Integration Nightmare

**The Situation**:
```
Legacy System: COBOL mainframe from 1985
New System: React/Node.js microservices with GraphQL
PM Request: Make them work together seamlessly by Friday
```

**Try This**:
```
"Demand integration between our COBOL mainframe and the new React app with 
real-time syncing. Timeline is Friday. Use demand_impossible_integration."
```

**Expected Output**:
```
🔌💥 IMPOSSIBLE INTEGRATION DEMAND 💥🔌

Can't they just TALK to each other?! It's all software, right?! Just make 
our COBOL mainframe and React app work together! How hard can integration be?! 
They're both COMPUTERS! Just sync the data in real-time by FRIDAY!

🧩 *Treating incompatible systems like plug-and-play toys*
```

**💡 Learning Point**: This demonstrates how tools can handle multiple complex 
parameters and generate responses that reference technical concepts.

---

### Scenario C: Micromanagement Mode

**Try This**:
```
"Ask engineering for hourly updates on the database refactoring project, 
including line-by-line code changes. Use request_daily_status_updates."
```

**Expected Output**:
```
📊🔍 MICROMANAGEMENT MODE ENGAGED 🔍📊

Can you give me HOURLY updates on the database refactoring?! I need to see 
progress DAILY! What EXACTLY are you working on right NOW?! Send me screenshots 
of every code change! I need granular details on every line! How else can I 
report progress to leadership?!

⏱️ *Treating complex development like factory production with hourly quotas*
```

**💡 Learning Point**: Tools can be specific about frequency, detail level, and 
reporting requirements while maintaining humor.

---

## 🎨 Creative Challenges

### Challenge 1: Build a Complete PM Conversation

**Goal**: Use 5 different tools to create a realistic (and hilarious) PM interaction.

**Starter Prompts**:
1. Start with a feature request
2. Override the estimate
3. Skip some development process
4. Compare to a competitor
5. Escalate something trivial

**🎓 What You're Learning**: How multiple tool calls create complex interactions.

---

### Challenge 2: Find the Breaking Point

**Goal**: Give extreme inputs to see how tools handle edge cases.

**Try These**:
```
- Demand a feature "yesterday" (deadline in the past)
- Override estimate from "5 years" to "5 minutes"
- Request integration between "pen and paper" and "quantum computer"
- Escalate "comma placement" to "UN Security Council"
```

**🎓 What You're Learning**: 
- How tools handle unusual inputs
- Default behavior for edge cases
- Error handling and graceful degradation

---

### Challenge 3: Real Quotes

**Goal**: Use actual PM quotes you've heard and see the Karen response.

**Example**:
```
Real Quote: "Can't we just parallelize it to make it go faster?"
Tool: override_engineering_estimate

Real Quote: "The client just needs to see something working, we'll fix bugs later"
Tool: bypass_development_process
```

**🎓 What You're Learning**: The tools reflect real patterns, making them 
educational about actual workplace dynamics.

---

## 🎪 Bonus: Easter Eggs and Fun Discoveries

### Hidden Behaviors to Find

Try these and see what happens:

1. **Empty Parameters**: What happens if you call a tool with no inputs?
   ```
   "Use demand_feature_immediately with no feature or deadline"
   ```

2. **Contradictions**: Give contradictory information
   ```
   "Demand an enterprise feature on a free product using demand_feature_immediately"
   ```

3. **Meta Requests**: Ask Karen PM about Karen PMs
   ```
   "Use escalate_to_ceo_over_ui_color to complain about a PM who always escalates UI colors"
   ```

4. **Tool Chaining**: Use output from one tool as input to another
   ```
   "Take the feature from demand_feature_immediately and use it in 
   change_requirements_post_deployment"
   ```

---

## 📊 Learning Progress Checklist

Track what you've mastered:

- [ ] Called a tool with parameters
- [ ] Called a tool without parameters (using defaults)
- [ ] Used multiple tools in one conversation
- [ ] Experimented with different parameter values
- [ ] Found edge cases and unusual behaviors
- [ ] Understood how AI chooses which tool to use
- [ ] Read the server code to see how tools work
- [ ] Modified a tool's behavior
- [ ] Created your own custom tool
- [ ] Explained MCP to someone else using Karen examples

---

## 🚀 Next Steps

1. **Read the Code**: Open `karen_server.py` and trace how tools work
2. **Modify Behavior**: Change system prompts to alter responses
3. **Create New Tools**: Add your own Karen PM behaviors
4. **Build Something Real**: Use what you learned for a serious MCP server

**Remember**: Every tool call you make is teaching you MCP fundamentals that 
apply to real-world applications!

---

## 💬 Share Your Favorites!

Found a hilarious tool combination? Created an amazing scenario? 

The best way to learn is to teach others—share your creative Karen PM 
interactions and help others learn!

**Happy Learning! 🎉**
