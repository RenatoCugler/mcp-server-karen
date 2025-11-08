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

# 💡 LEARNING: NEVER hardcode secrets in your code!
#    - Use environment variables (os.environ.get)
#    - Docker MCP secrets become environment variables
#    - Default to empty string if not set (enables fallbacks)

# Pre-defined Karen responses for fallback
FALLBACK_RESPONSES = {
    "speak_to_manager": [
        "This is ABSOLUTELY UNACCEPTABLE! I demand to speak to your manager RIGHT NOW!",
        "I have been a loyal customer for YEARS and this is how you treat me? GET ME YOUR MANAGER!",
        "Excuse me? Do you know who I am? I need to speak to someone in charge IMMEDIATELY!"
    ],
    "negative_review": [
        "⭐ WORST SERVICE EVER! The staff was rude and unprofessional. I will NEVER be back!",
        "⭐ TERRIBLE EXPERIENCE! Everything was wrong and nobody cared. Avoid at all costs!",
        "⭐ COMPLETELY UNACCEPTABLE! This place has gone downhill. Management needs to step up!"
    ],
    "demand_refund": [
        "I demand a FULL REFUND immediately! This is false advertising and I'm calling corporate!",
        "This is a SCAM! I want my money back and compensation for my time and emotional distress!",
        "REFUND NOW! I'm contacting the Better Business Bureau if this isn't resolved today!"
    ],
    "random_shout": [
        "EXCUSE ME?! What is WRONG with you people?! This is RIDICULOUS!",
        "Are you KIDDING me right now?! I can't BELIEVE this is happening!",
        "This is OUTRAGEOUS! I am SO SICK of dealing with incompetent people!",
        "WHAT is your PROBLEM?! I have NEVER been treated so poorly in my LIFE!",
        "Do you have ANY idea who you're talking to?! This is UNACCEPTABLE!"
    ],
    "record_for_social_media": [
        "I'm RECORDING this! This is going STRAIGHT to TikTok and my 47 followers will see EXACTLY how you treat customers!",
        "You're being FILMED! I'm posting this on Facebook, Instagram, AND Twitter! This is going VIRAL!",
        "SMILE for the camera! Everyone's going to see what TERRIBLE service looks like! My followers are going to be OUTRAGED!"
    ],
    "cite_nonexistent_law": [
        "According to Federal Regulation 42-B, I am LEGALLY ENTITLED to immediate service! You are VIOLATING my rights!",
        "The Consumer Protection Act of 2018 CLEARLY states that this behavior is ILLEGAL! I'm calling my lawyer!",
        "State Law 7.3-C says you MUST provide compensation! This is a FEDERAL OFFENSE!"
    ],
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

# === MCP TOOLS ===

@mcp.tool()
async def speak_to_manager(issue: str = "", severity: str = "minor") -> str:
    """Escalate any issue to demand speaking with a manager regardless of severity."""
    logger.info(f"Executing speak_to_manager for issue: {issue}")
    
    if not issue.strip():
        issue = "general service issue"
    
    system_prompt = """You are Karen, a stereotypical demanding customer who always escalates everything to management. 
    You are dramatic, entitled, and believe every minor inconvenience deserves immediate managerial attention. 
    Use phrases like "This is UNACCEPTABLE!", "I demand to speak to your manager!", "Do you know who I am?", 
    and "I've been a customer here for YEARS!" Be over-the-top but keep it humorous, not offensive."""
    
    prompt = f"Someone is having this issue: '{issue}' (severity: {severity}). Respond as Karen demanding to speak to a manager."
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"🔥 KAREN MODE ACTIVATED 🔥\n\n{ai_response}\n\n📞 *Demanding to be transferred to management immediately*"
    else:
        fallback = get_fallback_response("speak_to_manager")
        return f"🔥 KAREN MODE ACTIVATED 🔥\n\n{fallback}\n\n📞 *Demanding to be transferred to management immediately*"

@mcp.tool()
async def leave_negative_review(business: str = "", experience: str = "") -> str:
    """Generate an overly dramatic 1-star review with excessive complaints about minor issues."""
    logger.info(f"Executing leave_negative_review for: {business}")
    
    if not business.strip():
        business = "this establishment"
    
    if not experience.strip():
        experience = "poor service"
    
    system_prompt = """You are Karen writing a scathing 1-star review. You blow minor inconveniences completely out of proportion,
    use ALL CAPS frequently, mention how you'll "never return", threaten to "tell everyone", and act like this was the worst
    experience of your life. Include phrases like "WORST EVER!", "AVOID AT ALL COSTS!", "TERRIBLE SERVICE!", 
    and "I'M NEVER COMING BACK!" Keep it humorous and over-the-top."""
    
    prompt = f"Write a 1-star review for '{business}' about this experience: '{experience}'"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"⭐ ONE STAR REVIEW INCOMING ⭐\n\n{ai_response}\n\n💢 *Posted to Google, Yelp, Facebook, and told all my friends*"
    else:
        fallback = get_fallback_response("negative_review")
        return f"⭐ ONE STAR REVIEW INCOMING ⭐\n\n{fallback}\n\n💢 *Posted to Google, Yelp, Facebook, and told all my friends*"

@mcp.tool()
async def demand_refund(item: str = "", reason: str = "") -> str:
    """Generate refund demands with creative justifications, even for free services."""
    logger.info(f"Executing demand_refund for: {item}")
    
    if not item.strip():
        item = "this service"
    
    if not reason.strip():
        reason = "unsatisfactory experience"
    
    system_prompt = """You are Karen demanding a refund. You find creative and dramatic reasons why you deserve your money back,
    even for free services. You mention "emotional distress", "wasted time", "false advertising", and threaten legal action.
    You always demand MORE than what you paid and want compensation. Use phrases like "FULL REFUND!", "This is FRAUD!",
    "I'm calling corporate!", and "You'll be hearing from my lawyer!" Keep it absurdly dramatic but humorous."""
    
    prompt = f"Demand a refund for '{item}' because of '{reason}'"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"💰 REFUND DEMAND INITIATED 💰\n\n{ai_response}\n\n⚖️ *Threatening legal action and corporate complaints*"
    else:
        fallback = get_fallback_response("demand_refund")
        return f"💰 REFUND DEMAND INITIATED 💰\n\n{fallback}\n\n⚖️ *Threatening legal action and corporate complaints*"

@mcp.tool()
async def correct_pronunciation(word: str = "") -> str:
    """Provide unnecessarily pedantic pronunciation corrections for technical terms."""
    logger.info(f"Executing correct_pronunciation for: {word}")
    
    if not word.strip():
        return "🎭 PRONUNCIATION POLICE 🎭\n\n❌ Excuse me, you need to provide a word for me to correct! This is exactly the kind of carelessness I'm talking about!"
    
    system_prompt = """You are Karen, acting as a self-appointed pronunciation expert who corrects people in the most 
    condescending way possible. You make up elaborate "correct" pronunciations for technical terms, claim you know
    because you "took a class" or "have a degree", and act offended when people say things "wrong". 
    Be unnecessarily pedantic and dramatic about pronunciation. Use phrases like "Actually, it's pronounced...",
    "I can't BELIEVE people say it that way!", and "This is why education is so important!" Keep it humorous."""
    
    prompt = f"Correct the pronunciation of '{word}' in the most pedantic, Karen-like way possible"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"🎭 PRONUNCIATION POLICE 🎭\n\n{ai_response}\n\n📚 *Acting superior about linguistic knowledge*"
    else:
        return f"🎭 PRONUNCIATION POLICE 🎭\n\nActually, it's pronounced '{word.upper()}' - I can't BELIEVE you've been saying it wrong this whole time! I have a degree in Communications, so I KNOW these things!\n\n📚 *Acting superior about linguistic knowledge*"

@mcp.tool()
async def cite_company_policy(request: str = "") -> str:
    """Make up arbitrary company policies to support unreasonable requests."""
    logger.info(f"Executing cite_company_policy for: {request}")
    
    if not request.strip():
        request = "general customer service"
    
    policy = random.choice(FAKE_POLICIES)
    
    system_prompt = """You are Karen citing made-up company policies to support your unreasonable demands. 
    You reference specific sections, acts, and protocols that don't exist. You act like you know all the rules
    and regulations better than the employees. Use phrases like "According to your own policy...", 
    "Section X clearly states...", "I know my rights!", and "Corporate told me..." Be authoritative but absurd."""
    
    prompt = f"Cite a fake company policy to support this request: '{request}'"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"📋 POLICY CITATION ACTIVATED 📋\n\n{policy}\n\n{ai_response}\n\n⚖️ *Quoting regulations with supreme confidence*"
    else:
        return f"📋 POLICY CITATION ACTIVATED 📋\n\n{policy}\n\nI KNOW MY RIGHTS! This is clearly outlined in your employee handbook. I've read ALL the fine print!\n\n⚖️ *Quoting regulations with supreme confidence*"

@mcp.tool()
async def escalate_complaint(issue: str = "", department: str = "") -> str:
    """Transform any minor issue into a major complaint requiring immediate escalation."""
    logger.info(f"Executing escalate_complaint for: {issue}")
    
    if not issue.strip():
        issue = "minor inconvenience"
    
    if not department.strip():
        department = "customer service"
    
    system_prompt = """You are Karen escalating a complaint to absurd levels. You take minor issues and make them sound
    like major catastrophes requiring corporate intervention. You mention contacting the CEO, calling the news,
    posting on social media, and how this has "ruined your day/week/year". Use phrases like "This is OUTRAGEOUS!",
    "I'm taking this to the TOP!", "Someone will PAY for this!", and "This is going VIRAL!" Be dramatically over-the-top."""
    
    prompt = f"Escalate this issue: '{issue}' from the '{department}' department to the highest possible level"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"🚨 COMPLAINT ESCALATION PROTOCOL 🚨\n\n{ai_response}\n\n📢 *Preparing to contact corporate headquarters*"
    else:
        return f"🚨 COMPLAINT ESCALATION PROTOCOL 🚨\n\nThis {issue} is COMPLETELY UNACCEPTABLE! I'm escalating this to the CEO, the board of directors, AND posting about it on every social media platform! This is going VIRAL!\n\n📢 *Preparing to contact corporate headquarters*"

@mcp.tool()
async def generate_complaint_letter(recipient: str = "", subject: str = "") -> str:
    """Generate a formal complaint letter with maximum drama and entitlement."""
    logger.info(f"Executing generate_complaint_letter to: {recipient}")
    
    if not recipient.strip():
        recipient = "Corporate Management"
    
    if not subject.strip():
        subject = "Unacceptable Service Experience"
    
    system_prompt = """You are Karen writing a formal complaint letter. Include dramatic language, threats of legal action,
    mentions of being a "loyal customer for X years", demands for compensation, and threats to take business elsewhere.
    Use business letter format but with Karen's over-the-top dramatic style. Include phrases like "I am APPALLED",
    "IMMEDIATE ACTION REQUIRED", "This is DISCRIMINATION!", and "I expect FULL COMPENSATION!" Keep it humorous but formal."""
    
    prompt = f"Write a complaint letter to '{recipient}' about '{subject}'"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"📝 FORMAL COMPLAINT LETTER 📝\n\nTo: {recipient}\nRe: {subject}\nDate: {datetime.now().strftime('%Y-%m-%d')}\n\n{ai_response}\n\n💌 *Sending copies to Better Business Bureau and local news*"
    else:
        return f"📝 FORMAL COMPLAINT LETTER 📝\n\nTo: {recipient}\nRe: {subject}\nDate: {datetime.now().strftime('%Y-%m-%d')}\n\nDear Sir/Madam,\n\nI am ABSOLUTELY APPALLED by the service I received! As a loyal customer for FIFTEEN YEARS, this treatment is UNACCEPTABLE! I demand IMMEDIATE ACTION and FULL COMPENSATION!\n\nSincerely,\nKaren\n\n💌 *Sending copies to Better Business Bureau and local news*"

@mcp.tool()
async def random_shout(target: str = "", location: str = "") -> str:
    """Shout at someone for absolutely no reason with pure Karen entitlement and rage."""
    logger.info(f"Executing random_shout at: {target}")
    
    if not target.strip():
        target = "you people"
    
    if not location.strip():
        location = "here"
    
    system_prompt = """You are Karen having an absolutely unhinged meltdown for no logical reason whatsoever. 
    You are furious, entitled, and completely unreasonable. You make wild accusations, bring up irrelevant past events,
    threaten to call authorities, mention your "rights", and act like the world revolves around you. Use ALL CAPS frequently,
    multiple exclamation points, and phrases like "HOW DARE YOU!", "I am CALLING THE POLICE!", "This is HARASSMENT!", 
    "I know my RIGHTS!", "I'm posting this EVERYWHERE!", and "You'll be HEARING from my LAWYER!" Make it absurdly dramatic 
    but keep it humorous. Channel pure, unfiltered, unreasonable Karen rage for absolutely no justifiable reason."""
    
    prompt = f"Have a completely unreasonable meltdown and shout at '{target}' in '{location}' for absolutely no good reason"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"🔥💢 KAREN MELTDOWN ACTIVATED 💢🔥\n\n{ai_response}\n\n🚨 *Having an absolutely unhinged public breakdown*"
    else:
        fallback = get_fallback_response("random_shout")
        return f"🔥💢 KAREN MELTDOWN ACTIVATED 💢🔥\n\n{fallback}\n\n🚨 *Having an absolutely unhinged public breakdown*"

@mcp.tool()
async def record_for_social_media(situation: str = "", platform: str = "") -> str:
    """Announce that you're recording everything and threaten to post it to social media for your followers."""
    logger.info(f"Executing record_for_social_media for: {situation}")
    
    if not situation.strip():
        situation = "this terrible service"
    
    if not platform.strip():
        platform = "TikTok, Facebook, Instagram, and Twitter"
    
    system_prompt = """You are Karen dramatically announcing that you're recording everything for social media. 
    You act like you have millions of followers when you actually have like 47. You threaten to make things "go viral",
    mention specific social media platforms, talk about how "everyone needs to see this", and act like filming makes you
    powerful. Use phrases like "I'm RECORDING this!", "This is going on TikTok!", "My followers are going to be OUTRAGED!",
    "You're about to be FAMOUS for all the wrong reasons!", "SMILE for the camera!", and "This is going VIRAL!"
    Be dramatically entitled about your "right" to record and post."""
    
    prompt = f"Announce that you're recording '{situation}' and threatening to post it to '{platform}' to expose bad service"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"📱🎥 RECORDING FOR SOCIAL MEDIA 🎥📱\n\n{ai_response}\n\n📲 *Threatening to make this go viral to my 47 followers*"
    else:
        fallback = get_fallback_response("record_for_social_media")
        return f"📱🎥 RECORDING FOR SOCIAL MEDIA 🎥📱\n\n{fallback}\n\n📲 *Threatening to make this go viral to my 47 followers*"

@mcp.tool()
async def cite_nonexistent_law(issue: str = "", legal_area: str = "") -> str:
    """Make up completely fabricated laws and regulations to support unreasonable demands."""
    logger.info(f"Executing cite_nonexistent_law for: {issue}")
    
    if not issue.strip():
        issue = "poor customer service"
    
    if not legal_area.strip():
        legal_area = "consumer rights"
    
    system_prompt = """You are Karen confidently citing completely made-up laws, regulations, and legal statutes that don't exist.
    You reference specific numbered codes, federal regulations, state laws, and constitutional amendments that are totally fabricated.
    You act like you know the law better than actual lawyers and threaten legal action based on your fake legal knowledge.
    Use phrases like "According to Federal Regulation...", "State Law clearly states...", "The Constitution guarantees...",
    "Supreme Court case XYZ vs ABC ruled...", "This violates Section X of the...", "I know my legal RIGHTS!", 
    and "My lawyer says..." Be supremely confident about your completely wrong legal "facts"."""
    
    prompt = f"Cite fake laws and regulations about '{issue}' in the area of '{legal_area}' to support an unreasonable demand"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"⚖️📚 CITING LEGAL AUTHORITY 📚⚖️\n\n{ai_response}\n\n👩‍⚖️ *Confidently misquoting laws that don't exist*"
    else:
        fallback = get_fallback_response("cite_nonexistent_law")
        return f"⚖️📚 CITING LEGAL AUTHORITY 📚⚖️\n\n{fallback}\n\n👩‍⚖️ *Confidently misquoting laws that don't exist*"

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