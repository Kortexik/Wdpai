import { useState } from 'react';
import axios from 'axios';

const Login = () => {
    const [credentials, setCredentials] = useState({ username: '', password: '' });
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            // Make an API POST request to the login endpoint
            const response = await axios.post('http://localhost:8000/api/login/', credentials, {
                headers: {
                    'Content-Type': 'application/json', // Ensures the API expects JSON
                },
            });

            console.log('Login successful:', response.data);
            setError(null)
            sessionStorage.setItem('token', response.data.access);
            alert('Login successful!');
            window.location.reload();
        } catch (err: any) {
            // Handle login error
            console.error('Login failed:', err.response || err.message);
            setError(err.response?.data?.message || 'An error occurred during login.');
        }
    };

    return (
        <div className="contact-page">
            <div className="formheader">Login</div>
            <form className="form" onSubmit={handleSubmit}>
                <label htmlFor="username">Username</label>
                <input
                    type="text"
                    id="username"
                    placeholder="Username"
                    value={credentials.username}
                    onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
                    required
                />

                <label htmlFor="password">Password</label>
                <input
                    type="password"
                    id="password"
                    placeholder="Password"
                    value={credentials.password}
                    onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                    required
                />

                {error && <div className="error-message">{error}</div>}

                <button type="submit" className="submit-btn">Login</button>
            </form>
        </div>
    );
};

export default Login;
