/ netlify/functions/anthropic.js
// WORKING VERSION - No dependencies needed

exports.handler = async function(event, context) {
  // Handle CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
      },
      body: ''
    };
  }

  // Only allow POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  let apiKey, messages, max_tokens;

  try {
    // Parse request body
    const body = JSON.parse(event.body);
    apiKey = body.apiKey;
    messages = body.messages;
    max_tokens = body.max_tokens || 4096;

    if (!apiKey || !messages) {
      return {
        statusCode: 400,
        headers: { 'Access-Control-Allow-Origin': '*' },
        body: JSON.stringify({ error: 'Missing apiKey or messages' })
      };
    }

  } catch (parseError) {
    return {
      statusCode: 400,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ error: 'Invalid request body' })
    };
  }

  try {
    // Call Anthropic API
    const anthropicResponse = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: max_tokens,
        messages: messages
      })
    });

    // Get the response as text first
    const responseText = await anthropicResponse.text();
    
    // Parse it
    let responseData;
    try {
      responseData = JSON.parse(responseText);
    } catch (jsonError) {
      return {
        statusCode: 500,
        headers: { 'Access-Control-Allow-Origin': '*' },
        body: JSON.stringify({ 
          error: 'Failed to parse API response',
          details: responseText.substring(0, 100)
        })
      };
    }

    // Return the response
    return {
      statusCode: anthropicResponse.status,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(responseData)
    };

  } catch (error) {
    return {
      statusCode: 500,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ 
        error: 'Server error',
        message: error.message 
      })
    };
  }
};