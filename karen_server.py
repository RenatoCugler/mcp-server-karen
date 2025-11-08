#!/usr/bin/env python3
"""
🎓 Karen MCP Server - Learn MCP Through Humor!

This server demonstrates Model Context Protocol (MCP) fundamentals by providing
hilarious "Karen PM" behavior tools. Every part of this code teaches MCP concepts!

LEARNING OBJECTIVES:
- Understand MCP server structure
- Learn how to create tools with @mcp.tool()
- Handle parameters with defaults
- Integrate external APIs (OpenAI)
- Build fallback systems
- Format user-friendly responses
- Deploy servers with Docker

Read the comments to understand what each section does and why!
"""

# ============================================================================
# IMPORTS - What We Need
# ============================================================================
import os          # Access environment variables (API keys, config)
import sys         # System operations (exit codes, stderr)
import logging     # Track what's happening (debugging, monitoring)
import json        # Parse/create JSON (MCP uses JSON-RPC)
import random      # Pick random fallback responses (variety!)
from datetime import datetime  # Timestamps for responses

import httpx       # HTTP client for OpenAI API (async-capable)
from mcp.server.fastmcp import FastMCP  # The MCP magic! 🎉

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("karen-server")

# 💡 LEARNING: Logging is crucial for debugging MCP servers!
#    - stdout is for MCP protocol messages (JSON-RPC)
#    - stderr is for your debugging output
#    - Never mix them or MCP protocol breaks!

# Initialize MCP server
mcp = FastMCP("karen")

# 💡 LEARNING: This single line creates an MCP server!
#    FastMCP handles all the protocol details for you:
#    - JSON-RPC message parsing
#    - Tool registration and discovery
#    - Request routing
#    - Response formatting
#    You just focus on building tools!

# ============================================================================
# CONFIGURATION - Settings from Environment
# ============================================================================
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")  # API key from Docker secrets
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")  # Which AI model to use
API_TIMEOUT = 30  # Don't wait forever for OpenAI

# Imgflip API credentials (optional - works without auth but has rate limits)
IMGFLIP_USERNAME = os.environ.get("IMGFLIP_USERNAME", "")
IMGFLIP_PASSWORD = os.environ.get("IMGFLIP_PASSWORD", "")

# Popular meme templates perfect for PM Karen behavior
PM_MEME_TEMPLATES = {
    "distracted_boyfriend": "112126428",  # PM looking at competitor features
    "drake": "181913649",  # Rejecting proper process, preferring shortcuts
    "two_buttons": "87743020",  # Follow process vs ship broken feature
    "is_this": "100947",  # Is this a simple 5-minute change?
    "disaster_girl": "97984",  # PM watching codebase burn
    "change_my_mind": "129242436",  # This is a simple feature
    "this_is_fine": "55311130",  # Everything is on track (it's not)
    "one_does_not_simply": "61579",  # One does not simply skip testing
    "ancient_aliens": "101470",  # What if we just used AI?
    "expanding_brain": "93895088",  # Evolution of terrible PM ideas
}

# 💡 LEARNING: NEVER hardcode secrets in your code!
#    - Use environment variables (os.environ.get)
#    - Docker MCP secrets become environment variables
#    - Default to empty string if not set (enables fallbacks)

# Pre-defined Karen PM responses for fallback
FALLBACK_RESPONSES = {
    "demand_feature_immediately": [
        "This should be a SIMPLE 5-minute change, right?! Can't you just ADD A BUTTON for that?! I promised the client this would be ready by TOMORROW!",
        "Why is this taking so long?! Just copy the code from that other feature! This is BLOCKING everything!",
        "I don't understand why this is complicated! Just make it work! I'm escalating this to the C-suite!"
    ],
    "override_engineering_estimate": [
        "Three sprints?! I need it by FRIDAY! Why can't we just use AI to build it?! This is just making excuses!",
        "That estimate sounds like padding to me! Just copy the code from somewhere else! How hard can it be?!",
        "I'm overriding that estimate! This is definitely a one-day task! Stop being so negative!"
    ],
    "change_requirements_post_deployment": [
        "Actually, what I MEANT was... This is just ONE small thing! Why didn't you BUILD what I was thinking?!",
        "The client just clarified... (they never said that!) This should be a MINOR change! Why is this so hard?!",
        "It's already built, just TWEAK it a little! This was OBVIOUSLY what I wanted from the beginning!"
    ],
    "schedule_unnecessary_meeting": [
        "Let's circle back on this! I think we need to align! Let's get EVERYONE in a room for 2 hours to discuss this button!",
        "This deserves its own meeting! We need to sync up! I'm scheduling a follow-up meeting to discuss the follow-up!",
        "Let's take this offline! I'm booking the conference room for the whole afternoon to discuss this footer text!"
    ],
    "request_daily_status_updates": [
        "Can you give me HOURLY updates?! I need to see progress DAILY! What EXACTLY are you working on right NOW?!",
        "Why isn't this moving faster?! The client is asking for updates! Send me screenshots of your screen!",
        "I need granular details on every line of code! How can I report progress to leadership without knowing EVERYTHING?!"
    ],
    "create_urgent_non_urgent_task": [
        "This is URGENT! Drop everything and update this footer text! This should have been done YESTERDAY!",
        "The client is expecting this TODAY! This is TOP PRIORITY! I promised this would be ready this morning!",
        "This is blocking EVERYTHING! Why didn't anyone tell me updating one word would take so long?!"
    ],
    "bypass_development_process": [
        "We don't have time for process! Can't we just push it live?! Testing is optional for this feature!",
        "Let's skip the review and deploy! The client won't notice if there are bugs! We'll fix them later!",
        "Process is slowing us down! Just make it work! Security review is just paperwork anyway!"
    ],
    "demand_impossible_integration": [
        "Can't they just talk to each other?! It's all software, right?! Just make our COBOL mainframe work with this AI chatbot!",
        "How hard can integration be?! They're both computers! Just sync the data between 1970s and 2025 systems!",
        "Make it seamless! I don't understand why connecting incompatible architectures is complicated!"
    ],
    "generate_sarcastic_status_update": [
        "Everything is going EXACTLY as planned... if your plan was chaos and missed deadlines!",
        "We're definitely shipping Friday! According to the timeline that exists only in my dreams!",
        "Progress is AMAZING! If we measure success by meetings held instead of features shipped!"
    ],
    "random_feature_request": [
        "Change ALL fonts to Comic Sans! The client will LOVE it! It's professional!",
        "Rebrand the entire project as 'Project Karen 2.0'! We need a FRESH start!",
        "Add a dancing paperclip assistant! It worked for Microsoft in the 90s!"
    ],
    "generate_pm_meme": [
        "🎨 Meme generation failed, but imagine a Drake meme: Top panel 'Following sprint planning' ❌, Bottom panel 'Demanding features by tomorrow' ✅",
        "🎨 Picture this meme: Distracted Boyfriend looking at 'Competitor's Feature' while ignoring 'Technical Debt'",
        "🎨 Imagine the 'This is Fine' meme but it's a PM saying 'Everything is on track' while the roadmap burns"
    ]
}

# Company policies (made up)
FAKE_POLICIES = [
    "According to Section 4.7 of the Customer Service Charter, all complaints must be escalated within 2 minutes.",
    "Corporate Policy 12-B clearly states that customers are entitled to speak with senior management upon request.",
    "The Customer Rights Act of 2019 mandates immediate supervisor involvement for service issues.",
    "Company Protocol 7.3 requires management approval for any customer interaction lasting more than 30 seconds."
]

# === UTILITY FUNCTIONS ===

async def call_openai(prompt: str, system_prompt: str = "") -> str:
    """Make a request to OpenAI API."""
    if not OPENAI_API_KEY:
        logger.warning("No OpenAI API key provided, using fallback responses")
        return ""
    
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": OPENAI_MODEL,
                    "messages": messages,
                    "max_tokens": 300,
                    "temperature": 0.8
                },
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
    
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return ""

def get_fallback_response(tool_type: str) -> str:
    """Get a random fallback response for the given tool type."""
    responses = FALLBACK_RESPONSES.get(tool_type, ["This is UNACCEPTABLE!"])
    return random.choice(responses)

# === MCP TOOLS - PM EDITION ===

@mcp.tool()
async def demand_feature_immediately(feature: str = "", deadline: str = "") -> str:
    """Demand a complex feature be built immediately with zero understanding of technical complexity."""
    logger.info(f"Executing demand_feature_immediately for: {feature}")
    
    if not feature.strip():
        feature = "a new feature"
    
    if not deadline.strip():
        deadline = "by tomorrow"
    
    system_prompt = """You are Karen as a Product Manager who has zero technical understanding but maximum entitlement.
    You think every feature is "just adding a button", ignore all technical debt and dependencies, and promise impossible deadlines.
    You use phrases like "This should be a simple 5-minute change, right?", "Can't you just add a button?", "Just copy the code from that other feature",
    "Why can't we just use AI to build it?", "I promised the client...", and "This is blocking everything!" You completely dismiss sprint planning,
    technical complexity, and engineering estimates. You threaten to escalate to C-suite over minor features."""
    
    prompt = f"Demand that engineers build '{feature}' {deadline} and act like it's a trivial task"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"💼🔥 PM KAREN DEMANDS 🔥💼\n\n{ai_response}\n\n⚡ *Completely ignoring technical reality and sprint planning*"
    else:
        fallback = get_fallback_response("demand_feature_immediately")
        return f"💼🔥 PM KAREN DEMANDS 🔥💼\n\n{fallback}\n\n⚡ *Completely ignoring technical reality and sprint planning*"

@mcp.tool()
async def override_engineering_estimate(task: str = "", original_estimate: str = "", new_deadline: str = "") -> str:
    """Confidently override engineering estimates with zero technical knowledge."""
    logger.info(f"Executing override_engineering_estimate for: {task}")
    
    if not task.strip():
        task = "complex backend refactor"
    
    if not original_estimate.strip():
        original_estimate = "3 sprints"
    
    if not new_deadline.strip():
        new_deadline = "by Friday"
    
    system_prompt = """You are Karen as a PM who thinks engineers are just making excuses and padding estimates. 
    You have zero technical knowledge but maximum confidence in telling engineers how long code takes to write.
    Use phrases like "That sounds like padding", "Just copy the code from somewhere else", "Why can't we just use AI?",
    "This is definitely a one-day task", "Stop being so negative", "That estimate is ridiculous", and "I'm overriding that estimate".
    You treat complex technical work like simple copy-paste operations."""
    
    prompt = f"Override the engineering estimate of '{original_estimate}' for '{task}' and demand it be done '{new_deadline}'"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"📊❌ ESTIMATE OVERRIDE ACTIVATED ❌📊\n\n{ai_response}\n\n🎯 *Completely disrespecting engineering expertise and technical complexity*"
    else:
        fallback = get_fallback_response("override_engineering_estimate")
        return f"📊❌ ESTIMATE OVERRIDE ACTIVATED ❌📊\n\n{fallback}\n\n🎯 *Completely disrespecting engineering expertise and technical complexity*"

@mcp.tool()
async def change_requirements_post_deployment(original_feature: str = "", new_requirement: str = "") -> str:
    """Wait until after deployment to mention completely different requirements."""
    logger.info(f"Executing change_requirements_post_deployment for: {original_feature}")
    
    if not original_feature.strip():
        original_feature = "the login feature"
    
    if not new_requirement.strip():
        new_requirement = "completely different functionality"
    
    system_prompt = """You are Karen as a PM who waits until features are in production to reveal what you actually wanted.
    You treat major specification changes like minor typos and act like engineers should have read your mind.
    Use phrases like "Actually, what I meant was...", "This was always part of the original scope", "It's just a small addition",
    "The client just clarified..." (client never said that), "This should be a minor change", "Why didn't you build what I was thinking?",
    and "This was OBVIOUSLY what I wanted from the beginning!" You gaslight engineers about the original requirements."""
    
    prompt = f"Act like '{new_requirement}' was always part of the requirements for '{original_feature}' even though you never mentioned it before"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"📝🔄 REQUIREMENTS CHANGE GASLIGHTING 🔄📝\n\n{ai_response}\n\n🧠 *Rewriting history and blaming engineers for not reading minds*"
    else:
        fallback = get_fallback_response("change_requirements_post_deployment")
        return f"📝🔄 REQUIREMENTS CHANGE GASLIGHTING 🔄📝\n\n{fallback}\n\n🧠 *Rewriting history and blaming engineers for not reading minds*"

@mcp.tool()
async def invoke_competitor_feature(competitor: str = "", feature: str = "") -> str:
    """Demand features based on competitor screenshots with zero understanding of different architectures."""
    logger.info(f"Executing invoke_competitor_feature: {competitor} has {feature}")
    
    if not competitor.strip():
        competitor = "our main competitor"
    
    if not feature.strip():
        feature = "this amazing feature"
    
    system_prompt = """You are Karen as a PM who thinks all software is the same and features can be copied like LEGO blocks.
    You have zero understanding of different architectures, user bases, technical debt, or business models.
    Use phrases like "But [Competitor] has this feature!", "Can we just make it look like this?", "How hard can it be? They built it!",
    "Just copy their design", "Our users want EXACTLY this", "Why can't we just do what they do?", and "They made it look so simple!"
    You send random screenshots and expect identical functionality regardless of technical feasibility."""
    
    prompt = f"Demand that we copy '{feature}' from '{competitor}' and act like it should be trivial to implement"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"📱👀 COMPETITOR COMPARISON DEMAND 👀📱\n\n{ai_response}\n\n🎯 *Ignoring all technical and business context while demanding feature copies*"
    else:
        return f"📱👀 COMPETITOR COMPARISON DEMAND 👀📱\n\nBut {competitor} has {feature}! How hard can it be? They built it! Can we just make it look like this? I'm sending you a screenshot - just copy their design exactly!\n\n🎯 *Ignoring all technical and business context while demanding feature copies*"

@mcp.tool()
async def escalate_to_ceo_over_ui_color(ui_element: str = "", preferred_color: str = "") -> str:
    """Escalate trivial UI decisions to executive leadership as if they're critical business issues."""
    logger.info(f"Executing escalate_to_ceo_over_ui_color for: {ui_element}")
    
    if not ui_element.strip():
        ui_element = "button color"
    
    if not preferred_color.strip():
        preferred_color = "blue instead of green"
    
    system_prompt = """You are Karen as a PM who escalates the most trivial design decisions to the highest levels of management.
    You treat minor UI tweaks like critical business blockers and involve the entire C-suite in discussions about button colors.
    Use phrases like "This is blocking the entire roadmap!", "I need to escalate this to the CEO", "This is a critical business issue",
    "The entire success of the product depends on this", "I'm calling an emergency meeting", and "This requires executive attention".
    You CC entire leadership chains on messages about trivial design decisions."""
    
    prompt = f"Escalate the '{ui_element}' decision (wanting '{preferred_color}') to CEO level as if it's a critical business emergency"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"🚨💼 CEO ESCALATION PROTOCOL 💼🚨\n\n{ai_response}\n\n📧 *CCing entire executive team on trivial UI decisions*"
    else:
        return f"🚨💼 CEO ESCALATION PROTOCOL 💼🚨\n\nThis {ui_element} issue is BLOCKING the entire roadmap! I need to escalate this to the CEO immediately! This is a critical business decision that requires executive attention! I'm calling an EMERGENCY meeting about {preferred_color}!\n\n📧 *CCing entire executive team on trivial UI decisions*"

@mcp.tool()
async def schedule_unnecessary_meeting(topic: str = "", duration: str = "") -> str:
    """Schedule pointless meetings that could have been a Slack message."""
    logger.info(f"Executing schedule_unnecessary_meeting about: {topic}")
    
    if not topic.strip():
        topic = "button alignment"
    
    if not duration.strip():
        duration = "2 hours"
    
    system_prompt = """You are Karen as a PM who loves meetings more than actual progress. You schedule meetings to discuss 
    things that could be resolved in a single message, invite way too many people, and make engineers sit through discussions 
    about trivial topics. Use phrases like "Let's circle back on this", "I think we need to align", "Let's get everyone in a room", 
    "This deserves its own meeting", "We need to sync up", "Let's take this offline", and "I'm scheduling a follow-up meeting". 
    You treat every minor decision like it needs a committee."""
    
    prompt = f"Schedule an unnecessary '{duration}' meeting to discuss '{topic}' and invite way too many people"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"📅💤 MEETING OVERLOAD ACTIVATED 💤📅\n\n{ai_response}\n\n⏰ *Converting 5-minute decisions into multi-hour committee discussions*"
    else:
        fallback = get_fallback_response("schedule_unnecessary_meeting")
        return f"📅💤 MEETING OVERLOAD ACTIVATED 💤📅\n\n{fallback}\n\n⏰ *Converting 5-minute decisions into multi-hour committee discussions*"

@mcp.tool()
async def request_daily_status_updates(project: str = "", detail_level: str = "") -> str:
    """Demand hourly progress reports on tasks that take weeks to complete."""
    logger.info(f"Executing request_daily_status_updates for: {project}")
    
    if not project.strip():
        project = "the backend refactor"
    
    if not detail_level.strip():
        detail_level = "line-by-line code changes"
    
    system_prompt = """You are Karen as a PM who thinks micromanagement equals productivity. You demand constant updates 
    on complex technical work as if watching it will make it go faster. Use phrases like "Can you give me hourly updates?", 
    "I need to see progress daily", "What exactly are you working on right now?", "Can you send me screenshots?", 
    "I need granular details", "Why isn't this moving faster?", and "The client is asking for updates". You treat 
    software development like assembly line work that should have visible progress every hour."""
    
    prompt = f"Demand excessive status updates on '{project}' including '{detail_level}' and act like this helps productivity"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"📊🔍 MICROMANAGEMENT MODE ENGAGED 🔍📊\n\n{ai_response}\n\n⏱️ *Treating complex development like factory production with hourly quotas*"
    else:
        fallback = get_fallback_response("request_daily_status_updates")
        return f"📊🔍 MICROMANAGEMENT MODE ENGAGED 🔍📊\n\n{fallback}\n\n⏱️ *Treating complex development like factory production with hourly quotas*"

@mcp.tool()
async def create_urgent_non_urgent_task(task: str = "", fake_deadline: str = "") -> str:
    """Mark everything as urgent to bypass normal prioritization processes."""
    logger.info(f"Executing create_urgent_non_urgent_task: {task}")
    
    if not task.strip():
        task = "updating the footer text"
    
    if not fake_deadline.strip():
        fake_deadline = "EOD today"
    
    system_prompt = """You are Karen as a PM who uses "urgent" as the default priority for everything, even trivial tasks. 
    You create artificial urgency to jump queues and bypass proper planning. Use phrases like "This is URGENT!", 
    "The client is expecting this today!", "This should have been done yesterday!", "Drop everything and do this!", 
    "This is TOP PRIORITY!", "I promised this would be ready!", and "This is blocking everything!" You treat updating 
    text on a webpage like it's a server outage."""
    
    prompt = f"Make '{task}' sound incredibly urgent with deadline '{fake_deadline}' even though it's completely non-critical"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"🚨⚡ FAKE URGENCY GENERATOR ⚡🚨\n\n{ai_response}\n\n🎭 *Converting routine tasks into imaginary emergencies*"
    else:
        fallback = get_fallback_response("create_urgent_non_urgent_task")
        return f"🚨⚡ FAKE URGENCY GENERATOR ⚡🚨\n\n{fallback}\n\n🎭 *Converting routine tasks into imaginary emergencies*"

@mcp.tool()
async def bypass_development_process(feature: str = "", process_step: str = "") -> str:
    """Skip essential development practices because 'we don't have time for process'."""
    logger.info(f"Executing bypass_development_process for: {feature}")
    
    if not feature.strip():
        feature = "payment processing feature"
    
    if not process_step.strip():
        process_step = "security review"
    
    system_prompt = """You are Karen as a PM who thinks development processes are unnecessary bureaucracy that slows down delivery. 
    You encourage skipping testing, code reviews, security checks, and documentation because "we can do that later". 
    Use phrases like "We don't have time for process!", "Can't we just push it live?", "Testing is optional for this", 
    "Let's skip the review and deploy", "Process is slowing us down!", "The client won't notice", and "We'll fix bugs later". 
    You treat essential safeguards like optional paperwork."""
    
    prompt = f"Convince engineers to skip '{process_step}' for '{feature}' and act like it's unnecessary overhead"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"⚠️🚀 PROCESS BYPASS PROTOCOL 🚀⚠️\n\n{ai_response}\n\n🎲 *Rolling dice with product quality and security*"
    else:
        fallback = get_fallback_response("bypass_development_process")
        return f"⚠️🚀 PROCESS BYPASS PROTOCOL 🚀⚠️\n\n{fallback}\n\n🎲 *Rolling dice with product quality and security*"

@mcp.tool()
async def demand_impossible_integration(service_a: str = "", service_b: str = "", timeframe: str = "") -> str:
    """Request integrations between incompatible systems with zero understanding of technical constraints."""
    logger.info(f"Executing demand_impossible_integration: {service_a} with {service_b}")
    
    if not service_a.strip():
        service_a = "our legacy COBOL mainframe"
    
    if not service_b.strip():
        service_b = "this new AI chatbot"
    
    if not timeframe.strip():
        timeframe = "by next Tuesday"
    
    system_prompt = """You are Karen as a PM who thinks all software systems are LEGO blocks that easily connect together. 
    You have zero understanding of APIs, data formats, authentication, or technical compatibility. Use phrases like 
    "Can't they just talk to each other?", "It's all software, right?", "Just make them work together!", 
    "How hard can integration be?", "They're both computers!", "Just sync the data!", and "Make it seamless!". 
    You request integrations between systems from different decades with completely incompatible architectures."""
    
    prompt = f"Demand integration between '{service_a}' and '{service_b}' {timeframe} and act like technical constraints don't exist"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"🔌💥 IMPOSSIBLE INTEGRATION DEMAND 💥🔌\n\n{ai_response}\n\n🧩 *Treating incompatible systems like plug-and-play toys*"
    else:
        fallback = get_fallback_response("demand_impossible_integration")
        return f"🔌💥 IMPOSSIBLE INTEGRATION DEMAND 💥🔌\n\n{fallback}\n\n🧩 *Treating incompatible systems like plug-and-play toys*"

@mcp.tool()
async def generate_sarcastic_status_update(project: str = "", actual_status: str = "") -> str:
    """Generate fake/sarcastic status reports that say everything is fine when it's clearly not."""
    logger.info(f"Executing generate_sarcastic_status_update for: {project}")
    
    if not project.strip():
        project = "the critical launch project"
    
    if not actual_status.strip():
        actual_status = "complete disaster with missed deadlines"
    
    system_prompt = """You are Karen as a PM writing sarcastic status updates that pretend everything is going perfectly 
    when it's obviously a disaster. Use heavy sarcasm and phrases like "Everything is going exactly as planned...", 
    "if your plan was chaos", "Definitely shipped by Friday", "according to the timeline that exists only in my dreams", 
    "Progress is AMAZING!", "if we measure success by meetings held", "Right on track!", "for the wrong destination", 
    "No blockers at all!", "except for all the blockers", and "Team morale is high!" (when everyone wants to quit). 
    Make it obvious you're being sarcastic about the mess."""
    
    prompt = f"Write a sarcastic status update for '{project}' where the actual situation is '{actual_status}'"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"📊😏 SARCASTIC STATUS UPDATE 😏📊\n\n{ai_response}\n\n🎭 *Reporting complete chaos as 'minor bumps in the road'*"
    else:
        fallback = get_fallback_response("generate_sarcastic_status_update")
        return f"📊😏 SARCASTIC STATUS UPDATE 😏📊\n\n{fallback}\n\n🎭 *Reporting complete chaos as 'minor bumps in the road'*"

@mcp.tool()
async def random_feature_request() -> str:
    """Generate completely absurd and random feature requests that make no sense."""
    logger.info("Executing random_feature_request")
    
    system_prompt = """You are Karen as a PM generating completely random, absurd feature requests that make zero business sense. 
    Think of things like "Change all fonts to Comic Sans", "Rebrand as Project Karen 2.0", "Add a dancing paperclip assistant", 
    "Make the logo spin 360 degrees", "Add blockchain to the login page", "Replace all icons with emoji", 
    "Make every button play a sound effect", "Add a chat feature to the 404 page", "Integrate with MySpace", 
    "Auto-post to Friendster", etc. Be creative and ridiculous. Act like these ideas are brilliant and urgent."""
    
    prompt = "Generate one completely absurd, random feature request that makes no sense but act like it's genius"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"🎲💡 RANDOM FEATURE REQUEST 💡🎲\n\n{ai_response}\n\n🤪 *Generating chaos disguised as 'innovation'*"
    else:
        fallback = get_fallback_response("random_feature_request")
        return f"🎲💡 RANDOM FEATURE REQUEST 💡🎲\n\n{fallback}\n\n🤪 *Generating chaos disguised as 'innovation'*"

@mcp.tool()
async def generate_pm_meme(scenario: str = "", meme_type: str = "") -> str:
    """Generate a Karen PM meme using Imgflip API that captures PM behavior perfectly."""
    logger.info(f"Executing generate_pm_meme for scenario: {scenario}")
    
    if not scenario.strip():
        scenario = "demanding features with impossible deadlines"
    
    # Map scenario keywords to appropriate meme templates and text
    meme_configs = {
        "deadline": {
            "template_id": PM_MEME_TEMPLATES["drake"],
            "text0": "Following realistic sprint planning",
            "text1": "Promising features by tomorrow"
        },
        "competitor": {
            "template_id": PM_MEME_TEMPLATES["distracted_boyfriend"],
            "text0": "Our Technical Roadmap",
            "text1": "PM",
            "text2": "Competitor's Feature Screenshot"
        },
        "process": {
            "template_id": PM_MEME_TEMPLATES["drake"],
            "text0": "Testing and code review",
            "text1": "Shipping untested code immediately"
        },
        "estimate": {
            "template_id": PM_MEME_TEMPLATES["is_this"],
            "text0": "Is this a simple 5-minute change?",
            "text1": "Complex 3-sprint feature"
        },
        "fire": {
            "template_id": PM_MEME_TEMPLATES["this_is_fine"],
            "text0": "Everything is going",
            "text1": "exactly as planned"
        },
        "simple": {
            "template_id": PM_MEME_TEMPLATES["change_my_mind"],
            "text0": "This is just adding a button",
            "text1": "Change my mind"
        },
        "buttons": {
            "template_id": PM_MEME_TEMPLATES["two_buttons"],
            "text0": "Follow development process",
            "text1": "Ship broken feature fast"
        },
        "testing": {
            "template_id": PM_MEME_TEMPLATES["one_does_not_simply"],
            "text0": "One does not simply",
            "text1": "Skip testing in production"
        }
    }
    
    # Choose meme based on scenario or random
    config = None
    for key, template_config in meme_configs.items():
        if key in scenario.lower():
            config = template_config
            break
    
    # Default to random meme if no match
    if not config:
        config = random.choice(list(meme_configs.values()))
    
    try:
        # Generate meme via Imgflip API
        async with httpx.AsyncClient() as client:
            params = {
                "template_id": config["template_id"],
                "username": IMGFLIP_USERNAME or "imgflip_hubot",
                "password": IMGFLIP_PASSWORD or "imgflip_hubot",
            }
            
            # Add text boxes based on template
            for i in range(3):
                text_key = f"text{i}"
                if text_key in config:
                    params[f"boxes[{i}][text]"] = config[text_key]
            
            response = await client.post(
                "https://api.imgflip.com/caption_image",
                data=params,
                timeout=15
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                meme_url = result["data"]["url"]
                page_url = result["data"]["page_url"]
                
                return f"🎨😂 KAREN PM MEME GENERATOR 😂🎨\n\n✨ Meme created for: {scenario}\n\n🔗 View your meme: {meme_url}\n📄 Share page: {page_url}\n\n💡 *Capturing PM behavior in meme form*"
            else:
                error_msg = result.get("error_message", "Unknown error")
                logger.warning(f"Imgflip API returned error: {error_msg}")
                fallback = get_fallback_response("generate_pm_meme")
                return f"🎨😂 KAREN PM MEME GENERATOR 😂🎨\n\n{fallback}\n\n💡 *Meme concept for: {scenario}*"
    
    except Exception as e:
        logger.error(f"Meme generation error: {e}")
        fallback = get_fallback_response("generate_pm_meme")
        return f"🎨😂 KAREN PM MEME GENERATOR 😂🎨\n\n{fallback}\n\n💡 *Meme concept for: {scenario}*"

# === SERVER STARTUP ===
if __name__ == "__main__":
    logger.info("Starting Karen MCP server...")
    
    if not OPENAI_API_KEY:
        logger.warning("No OpenAI API key found. Set OPENAI_API_KEY environment variable for AI-powered responses.")
        logger.info("Using fallback responses for now.")
    else:
        logger.info(f"Using OpenAI model: {OPENAI_MODEL}")
    
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)