# Karen MCP Server - Implementation Guide

## Overview

This MCP server provides humorous "Karen" behavior tools that generate over-the-top customer complaint responses. It integrates with OpenAI's API for dynamic response generation while maintaining fallback functionality for when the API is unavailable.

## Architecture

```
┌─────────────────┐
│ Claude Desktop  │
└────────┬────────┘
         │ MCP Protocol (stdio)
         │
┌────────▼────────┐
│  MCP Gateway    │
└────────┬────────┘
         │ Docker Container
         │
┌────────▼────────┐
│ Karen Server    │
│  (FastMCP)      │
└────────┬────────┘
         │ HTTPS API
         │
┌────────▼────────┐
│  OpenAI API     │
│ (optional)      │
└─────────────────┘
```

## Implementation Details

### Tools Provided

1. **speak_to_manager** - Escalates any issue dramatically
   - Parameters: `issue` (string), `severity` (string)
   - Generates manager escalation demands
   - Uses OpenAI with Karen personality prompt

2. **leave_negative_review** - Creates 1-star reviews
   - Parameters: `business` (string), `experience` (string)
   - Generates overly dramatic review content
   - Includes social media posting threats

3. **demand_refund** - Creates refund demands
   - Parameters: `item` (string), `reason` (string)
   - Generates creative refund justifications
   - Includes legal action threats

4. **correct_pronunciation** - Pedantic pronunciation corrections
   - Parameters: `word` (string)
   - Provides condescending "corrections"
   - Claims false authority

5. **cite_company_policy** - Fake policy citations
   - Parameters: `request` (string)
   - Uses pre-defined fake policies
   - Generates supporting arguments

6. **escalate_complaint** - Major complaint escalation
   - Parameters: `issue` (string), `department` (string)
   - Transforms minor issues into major complaints
   - Threatens corporate involvement

7. **generate_complaint_letter** - Formal complaint letters
   - Parameters: `recipient` (string), `subject` (string)
   - Creates business-style complaint letters
   - Includes dramatic Karen language

8. **random_shout** - Unreasonable meltdowns
   - Parameters: `target` (string), `location` (string)
   - Generates completely unjustified rage
   - Pure Karen entitlement for no reason

9. **record_for_social_media** - Social media threats
   - Parameters: `situation` (string), `platform` (string)
   - Announces recording for social media
   - Threatens to make things "viral" to 47 followers

10. **cite_nonexistent_law** - Fake legal citations
    - Parameters: `issue` (string), `legal_area` (string)
    - Makes up completely fabricated laws
    - Confidently misquotes regulations that don't exist

### Key Design Decisions

#### 1. OpenAI Integration with Fallbacks

All tools attempt to use OpenAI API first, then fall back to pre-written responses:

```python
async def call_openai(prompt: str, system_prompt: str = "") -> str:
    """Make a request to OpenAI API."""
    if not OPENAI_API_KEY:
        logger.warning("No OpenAI API key provided, using fallback responses")
        return ""
    
    # API call implementation
    # Returns empty string on failure for fallback handling
```

#### 2. Personality System Prompts

Each tool uses specific system prompts to maintain Karen personality:

```python
system_prompt = """You are Karen, a stereotypical demanding customer who always escalates everything to management. 
You are dramatic, entitled, and believe every minor inconvenience deserves immediate managerial attention. 
Use phrases like "This is UNACCEPTABLE!", "I demand to speak to your manager!", "Do you know who I am?", 
and "I've been a customer here for YEARS!" Be over-the-top but keep it humorous, not offensive."""
```

#### 3. Consistent Response Formatting

All responses follow a consistent format with emojis and Karen-style messaging:

```python
return f"🔥 KAREN MODE ACTIVATED 🔥\n\n{ai_response}\n\n📞 *Demanding to be transferred to management immediately*"
```

#### 4. Fallback Response System

Pre-defined response arrays for each tool type:

```python
FALLBACK_RESPONSES = {
    "speak_to_manager": [
        "This is ABSOLUTELY UNACCEPTABLE! I demand to speak to your manager RIGHT NOW!",
        "I have been a loyal customer for YEARS and this is how you treat me? GET ME YOUR MANAGER!",
        "Excuse me? Do you know who I am? I need to speak to someone in charge IMMEDIATELY!"
    ],
    # ... more categories
}
```

#### 5. Fake Policy Generation

Randomized fake policies for the `cite_company_policy` tool:

```python
FAKE_POLICIES = [
    "According to Section 4.7 of the Customer Service Charter, all complaints must be escalated within 2 minutes.",
    "Corporate Policy 12-B clearly states that customers are entitled to speak with senior management upon request.",
    # ... more policies
]
```

### OpenAI API Configuration

#### Request Parameters

- **Model**: Configurable via `OPENAI_MODEL` (default: gpt-3.5-turbo)
- **Temperature**: 0.8 (high creativity for varied Karen responses)
- **Max Tokens**: 300 (sufficient for complaint rants)
- **Timeout**: 30 seconds

#### Error Handling

```python
try:
    # API call
    return result["choices"][0]["message"]["content"].strip()
except Exception as e:
    logger.error(f"OpenAI API error: {e}")
    return ""  # Triggers fallback system
```

### Testing Approach

#### Local Testing (with Docker)

```bash
# Test with OpenAI API
docker run -i --rm \
  -e OPENAI_API_KEY="your-key" \
  -e OPENAI_MODEL="gpt-3.5-turbo" \
  karen-mcp-server:latest

# Test without API (fallback mode)
docker run -i --rm karen-mcp-server:latest
```

#### MCP Protocol Testing

```bash
# Full MCP test
(echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}},"id":1}' && \
 echo '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' && \
 echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"speak_to_manager","arguments":{"issue":"slow website","severity":"minor"}},"id":3}') | \
docker run -i --rm -e OPENAI_API_KEY="$OPENAI_API_KEY" karen-mcp-server:latest
```

### Common Issues and Solutions

#### Issue: Boring or repetitive responses
**Solution**: 
- Increase OpenAI temperature
- Add more varied system prompts
- Expand fallback response arrays

#### Issue: OpenAI API timeout
**Solution**:
- Increase `API_TIMEOUT` value
- Implement retry logic
- Fallback system handles gracefully

#### Issue: Responses too long/short
**Solution**:
- Adjust `max_tokens` parameter
- Modify system prompts for desired length
- Add length validation

#### Issue: Responses not "Karen-like" enough
**Solution**:
- Enhance system prompts with more specific instructions
- Add more Karen-specific phrases to fallbacks
- Increase temperature for more dramatic responses

### Best Practices Demonstrated

1. **Graceful Degradation**: Works without OpenAI API
2. **Error Handling**: Comprehensive try-catch blocks
3. **Logging**: Detailed logging for debugging
4. **Security**: API keys via environment variables only
5. **Consistency**: Uniform response formatting
6. **Flexibility**: Configurable OpenAI model
7. **Fallbacks**: Pre-written responses ensure functionality

### Performance Considerations

- **API Latency**: 30-second timeout prevents hanging
- **Token Usage**: 300-token limit controls costs
- **Memory**: Minimal memory footprint
- **Caching**: Could be added for repeated requests
- **Rate Limiting**: Handled by OpenAI SDK

### Security Considerations

- **API Key Storage**: Only in Docker Desktop secrets
- **No Data Persistence**: No user data stored
- **Content Filtering**: OpenAI's built-in content policies
- **Error Logging**: No sensitive data in logs
- **Network Security**: HTTPS only for API calls

### Extending the Server

To add new Karen tools:

```python
@mcp.tool()
async def new_karen_tool(parameter: str = "") -> str:
    """Single-line description of what this Karen tool does."""
    
    system_prompt = """Karen personality instructions specific to this tool..."""
    prompt = f"Karen prompt based on parameter: {parameter}"
    
    ai_response = await call_openai(prompt, system_prompt)
    
    if ai_response:
        return f"🎭 TOOL EMOJI 🎭\n\n{ai_response}\n\n💢 *Karen action description*"
    else:
        fallback = "Pre-written Karen response for this tool"
        return f"🎭 TOOL EMOJI 🎭\n\n{fallback}\n\n💢 *Karen action description*"
```

### Monitoring and Debugging

Check logs:
```bash
# Docker logs
docker logs [container_name]

# Application logs (stderr)
# Look for:
# - "Starting Karen MCP server..."
# - "Using OpenAI model: ..."
# - "No OpenAI API key found..." (fallback mode)
# - "OpenAI API error: ..." (API issues)
```

## Conclusion

The Karen MCP server demonstrates a complete implementation with external API integration, fallback systems, and humorous content generation. It serves as both entertainment and a practical example of building resilient MCP servers with AI integration.