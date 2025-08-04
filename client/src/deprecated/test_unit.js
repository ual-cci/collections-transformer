


const TestUnit = () => {
  const handleOpenAITest = async () => {
    try {
      const requestOptions = {
        method: 'GET',
        mode: 'cors',
        headers: {'Content-Type': 'application/json'}
      };

      const response = await fetch((process.env.NEXT_PUBLIC_SERVER_URL || "") + "/backend/test_openai?" + new URLSearchParams({
        question: "What is the capital of the United Kingdom?"
      }), requestOptions);

      const data = await response.json();
      if (data.status === 200) {
        alert(data.data || 'No response received');
      } else {
        alert('Error: ' + (data.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error making request to server');
    }
  };

  const handleAzureTest = async () => {
    try {
      const requestOptions = {
        method: 'GET',
        mode: 'cors',
        headers: {'Content-Type': 'application/json'}
      };

      const response = await fetch((process.env.NEXT_PUBLIC_SERVER_URL || "") + "/backend/test_azure?" + new URLSearchParams({
        question: "What is the capital of the United Kingdom?"
      }), requestOptions);

      const data = await response.json();
      if (data.status === 200) {
        alert(data.data || 'No response received');
      } else {
        alert('Error: ' + (data.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error making request to server');
    }
  };

  const handleOpenRouterTest = async () => {
    try {
      const requestOptions = {
        method: 'GET',
        mode: 'cors',
        headers: {'Content-Type': 'application/json'}
      };
      
      const response = await fetch(
        (process.env.NEXT_PUBLIC_SERVER_URL || "") + "/backend/test_openrouter?" + new URLSearchParams({
        question: "What is the capital of the United Kingdom?"
      }), requestOptions);

      const data = await response.json();
      
      if (response.status === 200) {
        alert(data.data);
      } else {
        alert(data.error || 'An error occurred');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while testing OpenRouter');
    }
  };

  const handleOpenRouterImageTest = async () => {
    try {
      // Using a sample image URL - you can change this to any public image URL
      const imageUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg";
      
      const response = await fetch(
        (process.env.NEXT_PUBLIC_SERVER_URL || "") + "/backend/test_openrouter_image?" + new URLSearchParams({
          image_url: imageUrl
        }),
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      const data = await response.json();
      
      if (response.status === 200) {
        alert(data.data);
      } else {
        alert(data.error || 'An error occurred');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while testing OpenRouter image analysis');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Test Unit</h1>
      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <button
          onClick={handleOpenAITest}
          style={{
            padding: '10px 20px',
            backgroundColor: '#0070f3',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          Test OpenAI
        </button>
        <button
          onClick={handleAzureTest}
          style={{
            padding: '10px 20px',
            backgroundColor: '#0070f3',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          Test Azure
        </button>
        <button
          onClick={handleOpenRouterTest}
          style={{
            padding: '10px 20px',
            backgroundColor: '#10a37f',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          Test OpenRouter
        </button>
        <button
          onClick={handleOpenRouterImageTest}
          style={{
            padding: '10px 20px',
            backgroundColor: '#10a37f',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          Test OpenRouter Image
        </button>
      </div>
    </div>
  );
};

export default TestUnit;

