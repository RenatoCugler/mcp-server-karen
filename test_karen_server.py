#!/usr/bin/env python3
"""
Simple tests for Karen MCP Server

Run with: python test_karen_server.py

The test will load API keys from .env file if it exists.
This allows you to test with real OpenAI/Imgflip APIs locally.
"""

import asyncio
import sys
import os
from pathlib import Path

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print("📝 Loaded environment variables from .env file")
        if os.getenv("OPENAI_API_KEY"):
            print("✅ OpenAI API key found - tests will use real AI responses")
        else:
            print("⚠️  No OpenAI API key - tests will use fallback responses")
        if os.getenv("IMGFLIP_USERNAME") and os.getenv("IMGFLIP_PASSWORD"):
            print("✅ Imgflip credentials found - meme generation will use real API")
        else:
            print("⚠️  No Imgflip credentials - meme generation will use fallback")
        print()
except ImportError:
    print("⚠️  python-dotenv not installed - skipping .env file")
    print()

from karen_server import (
    demand_feature_immediately,
    override_engineering_estimate,
    change_requirements_post_deployment,
    generate_sarcastic_status_update,
    random_feature_request,
    generate_pm_meme,
)


async def test_demand_feature_immediately():
    """Test the demand_feature_immediately tool"""
    print("Testing demand_feature_immediately...")
    
    result = await demand_feature_immediately(
        feature="real-time collaboration",
        deadline="tomorrow"
    )
    
    assert "PM KAREN DEMANDS" in result
    assert len(result) > 50
    print("✅ demand_feature_immediately works!")
    return True


async def test_override_engineering_estimate():
    """Test the override_engineering_estimate tool"""
    print("Testing override_engineering_estimate...")
    
    result = await override_engineering_estimate(
        task="database migration",
        original_estimate="3 weeks",
        new_deadline="Friday"
    )
    
    assert "ESTIMATE OVERRIDE" in result
    assert len(result) > 50
    print("✅ override_engineering_estimate works!")
    return True


async def test_change_requirements_post_deployment():
    """Test the change_requirements_post_deployment tool"""
    print("Testing change_requirements_post_deployment...")
    
    result = await change_requirements_post_deployment(
        original_feature="simple login",
        new_requirement="OAuth and SSO"
    )
    
    assert "REQUIREMENTS CHANGE" in result
    assert len(result) > 50
    print("✅ change_requirements_post_deployment works!")
    return True


async def test_generate_sarcastic_status_update():
    """Test the generate_sarcastic_status_update tool"""
    print("Testing generate_sarcastic_status_update...")
    
    result = await generate_sarcastic_status_update(
        project="launch project",
        actual_status="complete disaster"
    )
    
    assert "SARCASTIC STATUS UPDATE" in result
    assert len(result) > 50
    print("✅ generate_sarcastic_status_update works!")
    return True


async def test_random_feature_request():
    """Test the random_feature_request tool"""
    print("Testing random_feature_request...")
    
    result = await random_feature_request()
    
    assert "RANDOM FEATURE REQUEST" in result
    assert len(result) > 50
    print("✅ random_feature_request works!")
    return True


async def test_generate_pm_meme():
    """Test the generate_pm_meme tool"""
    print("Testing generate_pm_meme...")
    
    result = await generate_pm_meme(scenario="deadline chaos")
    
    assert "KAREN PM MEME GENERATOR" in result
    assert len(result) > 50
    print("✅ generate_pm_meme works!")
    return True


async def test_with_empty_parameters():
    """Test tools with empty parameters (should use defaults)"""
    print("Testing with empty parameters...")
    
    result = await demand_feature_immediately()
    
    assert "PM KAREN DEMANDS" in result
    assert len(result) > 50
    print("✅ Empty parameters handled correctly!")
    return True


async def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 KAREN MCP SERVER TESTS")
    print("=" * 60)
    print()
    
    tests = [
        test_demand_feature_immediately,
        test_override_engineering_estimate,
        test_change_requirements_post_deployment,
        test_generate_sarcastic_status_update,
        test_random_feature_request,
        test_generate_pm_meme,
        test_with_empty_parameters,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            await test()
            passed += 1
            print()
        except Exception as e:
            failed += 1
            print(f"❌ Test failed: {test.__name__}")
            print(f"   Error: {e}")
            print()
    
    print("=" * 60)
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Tests failed: {failed}/{len(tests)}")
    print("=" * 60)
    
    if failed == 0:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️ Some tests failed!")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
