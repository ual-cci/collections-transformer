import { handleAuth, handleCallback } from '@auth0/nextjs-auth0';

export default handleAuth({
  async callback(req, res) {
    try {
      // Handle the Auth0 callback
      const result = await handleCallback(req, res);
      
      // Only record connection if this is a successful login (not logout)
      if (result && result.user && req.url.includes('code=')) {
        // Record the connection in the background
        try {
          const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL || process.env.AUTH0_BASE_URL}/backend/user/record_connection`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: result.user.sub })
          });
          
          if (response.ok) {
            console.log('User connection recorded on login');
          }
        } catch (error) {
          console.error('Failed to record user connection:', error);
          // Don't fail the login if connection recording fails
        }
      }
      
      return result;
    } catch (error) {
      console.error('Auth0 callback error:', error);
      throw error;
    }
  }
});