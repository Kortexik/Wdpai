import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';

const Navigation = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        const token = sessionStorage.getItem('token');
        setIsLoggedIn(!!token);
    }, []);

    return (
        <nav>
            <Link to="/register" className="nav-link">Rejestracja</Link>
            <Link to="/login" className="nav-link">Logowanie</Link> 
            {isLoggedIn ? ( <Link  to="/users" className="nav-link">Lista użytkowników</Link>) : null}
        </nav>
    );
};

export default Navigation;
