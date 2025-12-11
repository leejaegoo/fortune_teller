# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-powered fortune-telling web application that generates personalized daily horoscopes based on user information (name, birthdate, gender). The application currently uses Google Gemini 2.5 Flash as the primary AI backend, with support for Claude and OpenAI clients as alternatives.

## Development Commands

### Running the Application

```bash
# Run the fortune web app (default port 5001)
python3 fortune_app.py

# Run the interactive Claude chat interface
python3 chat.py

# Test Gemini API connection
python3 test_gemini.py
```

### Installation

```bash
# Install dependencies
pip3 install -r requirements.txt --user
```

### API Key Setup

The application requires AI API keys set as environment variables:

```bash
# For Gemini (currently used by fortune_app.py)
export GOOGLE_API_KEY="your-google-api-key"

# For Claude (used by chat.py and claude_client.py)
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# For OpenAI (alternative implementation)
export OPENAI_API_KEY="your-openai-api-key"
```

## Architecture

### AI Client Architecture

The application uses a **swappable AI client pattern** where different AI providers can be used interchangeably:

- **`gemini_client.py`** - Google Gemini 2.5 Flash (currently active in fortune_app.py)
- **`claude_client.py`** - Anthropic Claude 3.5 Sonnet
- **`openai_client.py`** - OpenAI GPT models

All clients follow the same interface with a `chat(message, max_tokens)` method, making it easy to switch providers by changing the import and API key check in `fortune_app.py`.

**To switch AI providers:** Modify the import statement and API key validation in `fortune_app.py:7` and `fortune_app.py:186-191`.

### Fortune Generation Flow

1. **User Input** → `templates/index.html` form collects name, birthdate, gender
2. **Frontend** → `static/js/script.js` sends POST request to `/get_fortune`
3. **Zodiac Calculation** → `fortune_app.py:calculate_zodiac()` determines Chinese zodiac from birth year
4. **AI Generation** → `fortune_app.py:generate_fortune()` creates structured prompt and sends to AI
5. **Response Formatting** → AI returns markdown-formatted fortune with categories
6. **Frontend Display** → JavaScript renders formatted fortune with random quote

### Fortune Categories

The AI generates fortunes across these categories (defined in prompt at `fortune_app.py:87-120`):
- Overall fortune (전체운)
- Love fortune (사랑운)
- Wealth fortune (재물운)
- Health fortune (건강운)
- Work/Study fortune (직장/학업운)
- Lucky color (행운의 색상)
- Lucky number (행운의 숫자)

### Fallback Fortune System

`fortune_generator.py` contains a template-based fortune generator that works without AI APIs. It uses predefined fortune templates and randomization based on user input. This is not currently used but serves as a backup implementation.

## File Structure

```
fortune_app.py          # Main Flask web application (uses Gemini)
gemini_client.py        # Google Gemini API client (active)
claude_client.py        # Claude API client (alternative)
openai_client.py        # OpenAI API client (alternative)
chat.py                 # Interactive CLI chat with Claude
fortune_generator.py    # Template-based fortune generator (unused fallback)
test_gemini.py          # Gemini API connection test
templates/index.html    # Main web UI
static/css/style.css    # Styling
static/js/script.js     # Frontend logic
```

## Important Notes

### Chinese Zodiac Calculation

The zodiac is calculated using modulo 12 on the birth year (`fortune_app.py:48-59`). The zodiac mapping in `ZODIAC_ANIMALS` dictionary starts with index 0 = Monkey (원숭이), following the Chinese zodiac cycle.

### Port Configuration

Default port is 5001. If port conflicts occur, modify the port in `fortune_app.py:199`.

### Conversation History

The `chat.py` interface maintains conversation history via the `ChatInterface` class, allowing multi-turn conversations with Claude. The `claude_client.py` provides a simpler stateless interface for single-turn interactions.

### Quote System

Random inspirational quotes are served from a hardcoded list in `fortune_app.py:29-45` and added to fortune responses independently from AI generation.
