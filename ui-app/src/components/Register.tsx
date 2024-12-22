import React, { useState } from 'react';
import axios from 'axios';

const Register = () => {
    const [formData, setFormData] = useState({ username: '', email: '', password: '' });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:8000/api/register/', formData);
            alert('Registration successful!');
            setFormData({ username: '', email: '', password: '' }); // Reset form
        } catch (error) {
            console.error('Registration failed:', error);
            alert(`Registration failed: ${error}`);
        }
    };

    return (
        <div className="contact-page">
            <div className="formheader">Register</div>
            <form onSubmit={handleSubmit} className="form">
                <label htmlFor="username">Username</label>
                <input
                    type="text"
                    id="username"
                    placeholder="Username"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    required
                />

                <label htmlFor="email">Email</label>
                <input
                    type="email"
                    id="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                />

                <label htmlFor="password">Password</label>
                <input
                    type="password"
                    id="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required
                />

                <button type="submit" className="submit-btn">Register</button>
            </form>
        </div>
    );
};

export default Register;
