export default async function handler(req, res) {
  try {
    const { question } = req.query;
    
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_SERVER_URL}/backend/test_openrouter?question=${encodeURIComponent(question)}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'An error occurred while testing OpenRouter' });
  }
}
