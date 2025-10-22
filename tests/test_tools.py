import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from tools import web_search_tool, weather_tool

#  Test Web Search Tool
def test_web_search_tool_valid_query():
    """Test that web search returns a non-empty string for a valid query."""
    query = "latest AI technologies"
    result = web_search_tool(query)
    assert isinstance(result, str)
    assert len(result) > 0
    print("\n Web Search Test Passed: Received results.")

def test_web_search_tool_invalid_query():
    """Test web search with gibberish or empty query."""
    query = "asldkfjaslkdfjasd"  # Random gibberish
    result = web_search_tool(query)
    assert isinstance(result, str)
    print("\n Web Search handles invalid query gracefully.")

#  Test Weather Tool
def test_weather_tool_valid_city():
    """Test weather tool for a valid city."""
    city = "Bangalore"
    result = weather_tool(city)
    assert isinstance(result, str)
    assert "Bangalore" in result or "temperature" in result.lower()
    print("\n Weather Tool Test Passed: Valid city handled correctly.")

def test_weather_tool_invalid_city():
    """Test weather tool for an invalid city name."""
    city = "XyzInvalidCity"
    result = weather_tool(city)
    assert isinstance(result, str)
    assert "error" in result.lower() or "⚠️" in result
    print("\n Weather Tool handles invalid city gracefully.")

