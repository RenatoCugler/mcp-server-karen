# Karen MCP Server - Implementation Guide

## Overview

This MCP server provides humorous "Karen PM" behavior tools that generate over-the-top Product Manager responses. It integrates with OpenAI's API for dynamic response generation while maintaining fallback functionality for when the API is unavailable.

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

### PM Tools Provided

1. **demand_feature_immediately** - Demand features with impossible deadlines
   - Parameters: `feature` (string), `deadline` (string)
   - Generates urgent feature demands
   - Ignores technical complexity

2. **override_engineering_estimate** - Dismiss technical estimates
   - Parameters: `task` (string), `estimate` (string), `actual_time` (string)
   - Rewrites realistic estimates with wishful thinking
   - Claims "it should be simple"

3. **change_requirements_post_deployment** - Change scope after release
   - Parameters: `original_requirement` (string), `new_requirement` (string)
   - Demands changes to deployed features
   - Acts surprised about consequences

4. **invoke_competitor_feature** - Reference competitor features
   - Parameters: `competitor` (string), `feature` (string)
   - Uses "but competitor X has this" argument
   - Ignores different contexts

5. **escalate_to_ceo_over_ui_color** - Escalate trivial issues
   - Parameters: `ui_element` (string), `color_complaint` (string)
   - Treats minor UI issues as critical
   - Threatens executive involvement

6. **schedule_unnecessary_meeting** - Create pointless meetings
   - Parameters: `topic` (string), `attendees` (string)
   - Schedules meetings that could be emails
   - Requires all developers present

7. **request_daily_status_updates** - Demand excessive reporting
   - Parameters: `project` (string), `update_frequency` (string)
   - Requires constant status updates
   - Interrupts actual work

8. **create_urgent_non_urgent_task** - False urgency creation
   - Parameters: `task` (string), `fake_urgency_reason` (string)
   - Marks everything as urgent
   - Cries wolf constantly

9. **bypass_development_process** - Skip necessary steps
   - Parameters: `process` (string), `reason_to_skip` (string)
   - Demands to skip testing, code review, etc.
   - Claims "we don't have time"

10. **demand_impossible_integration** - Request unfeasible integrations
    - Parameters: `system_a` (string), `system_b` (string)
    - Demands integration of incompatible systems
    - Ignores technical limitations

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

Pre-defined response arrays for each PM tool type:

```python
FALLBACK_RESPONSES = {
    "demand_feature": [
        "I don't care if it takes 6 months to build properly - we need this feature by FRIDAY!",
        "Our competitor has this feature and we're losing customers! Make it happen NOW!",
        "This is a CRITICAL blocker! Drop everything else and prioritize this IMMEDIATELY!"
    ],
    # ... more PM categories
}
```

#### 5. No Fake Policy Generation

The PM edition focuses on product management behaviors without fake policies.

### OpenAI API Configuration

#### Request Parameters

- **Model**: Configurable via `OPENAI_MODEL` (default: gpt-3.5-turbo)
- **Temperature**: 0.8 (high creativity for varied PM responses)
- **Max Tokens**: 300 (sufficient for PM demands)
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
 echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"demand_feature_immediately","arguments":{"feature":"dark mode","deadline":"tomorrow"}},"id":3}') | \
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