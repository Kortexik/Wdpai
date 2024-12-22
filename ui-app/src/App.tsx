import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Navigation from './components/Navigation';
import Register from './components/Register';
import Login from './components/Login';
import UserList from './components/UserList';
import './App.css'

function App() {
    return (
        <BrowserRouter>
            <Navigation />
            <Routes>
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login />} />
                <Route path="/users" element={<UserList />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
