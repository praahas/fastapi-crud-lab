import React from 'react';

function App() {
  // Redirect to backend API docs
  React.useEffect(() => {
    window.location.href = `${process.env.REACT_APP_BACKEND_URL}/api/docs`;
  }, []);

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      backgroundColor: '#1a1a2e',
      color: '#e0e0e0',
      fontFamily: 'system-ui, sans-serif'
    }}>
      <div style={{ textAlign: 'center' }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '1rem' }}>FastAPI CRUD Lab</h1>
        <p>Redirecting to API Documentation...</p>
        <p style={{ marginTop: '1rem', color: '#94a3b8' }}>
          If not redirected automatically, <a 
            href={`${process.env.REACT_APP_BACKEND_URL}/api/docs`}
            style={{ color: '#7c3aed' }}
          >click here</a>
        </p>
      </div>
    </div>
  );
}

export default App;
