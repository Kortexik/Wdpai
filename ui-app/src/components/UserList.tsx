import { useState, useEffect } from 'react';
import axios from 'axios';

interface User {
    id: number;
    first_name: string;
    last_name: string;
    role: string;
}

const UserList: React.FC = () => {
    const [users, setUsers] = useState<User[]>([]);
    const [newUser, setNewUser] = useState<Omit<User, 'id'>>({
        first_name: '',
        last_name: '',
        role: '',
    });

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        const token = sessionStorage.getItem('token')
        try {
            const response = await axios.get<User[]>('http://localhost:8000/api/users/', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            console.log(response.data);
            setUsers(response.data);
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    };

    const handleAddUser = async () => {
        try {
            const token = sessionStorage.getItem('token')
            const response = await axios.post<User>('http://localhost:8000/api/users/', newUser, {
                headers: {
                    Authorization: `Bearer ${token}` // Dodanie tokenu do nagłówka
                }
            });
            setUsers((prevUsers) => [...prevUsers, response.data]);
            setNewUser({ first_name: '', last_name: '', role: '' });
        } catch (error) {
            console.error('Error adding user:', error);
        }
    };

    const handleDeleteUser = async (id: number) => {
        try {
            const token = sessionStorage.getItem('token');
            await axios.delete(`http://localhost:8000/api/users/${id}/delete/`, {
                headers: {
                    Authorization: `Bearer ${token}` // Dodanie tokenu do nagłówka
                }
            });
            setUsers(users.filter(user => user.id !== id));
        } catch (error) {
            console.error('Error deleting user:', error);
        }
    };

    return (
        <div className="contact-page">
            <div className="formheader">Add User</div>
            <form onSubmit={handleAddUser} className="form">
                
                <label htmlFor="firstName">First name</label>
                <input
                    type="text"
                    id="firstName"
                    placeholder="First name"
                    value={newUser.first_name}
                    onChange={(e) => setNewUser({ ...newUser, first_name: e.target.value })}
                    required
                />

                <label htmlFor="lastName">Last name</label>
                <input
                    type="text"
                    id="lastName"
                    placeholder="Last name"
                    value={newUser.last_name}
                    onChange={(e) => setNewUser({ ...newUser, last_name: e.target.value })}
                    required
                />

                <label htmlFor="role">Role</label>
                <select
                    id="role"
                    value={newUser.role}
                    onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                    required
                >
                    <option value="" disabled hidden>Select a role</option>
                    <option value="Manager">Manager</option>
                    <option value="Developer">Developer</option>
                    <option value="CEO">CEO</option>
                    <option value="UI/UX">UI/UX</option>
                </select>

                <button type="submit" className="submit-btn">SUBMIT</button>
            </form>

            <div className="user-list">
                {users.map((user) => (
                    <div key={user.id} className="user">
                        <p>{user.first_name} {user.last_name}<br /><small>{user.role}</small></p>
                        <a
                            href="#"
                            className="deleteButton"
                            onClick={(e) => {
                                e.preventDefault();
                                handleDeleteUser(user.id);
                            }}
                        >
                            <i className="fa-solid fa-trash-can"></i>
                        </a>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default UserList;
