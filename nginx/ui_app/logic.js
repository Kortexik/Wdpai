document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('contact-form');
    if (form) {
        form.addEventListener('submit', function (event) {
        });
    } else {
        console.error('Form not found');
    }

    const userListContainer = document.getElementById('user-list');

    fetch('http://localhost:8000')
        .then(response => response.json())
        .then(data => {
            if (data) {
                data.forEach(element => { //bo przy F5 dodawalo do listy tylko jeden element
                    addUserToList(element);
                });
            }
        })
        .catch(error => console.error('Error fetching initial user:', error));

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const firstName = document.getElementById('firstName').value;
        const lastName = document.getElementById('lastName').value;
        const role = document.getElementById('role').value;

        const data = {
            id: null,
            firstName: firstName,
            lastName: lastName,
            role: role
        };

        fetch('http://localhost:8000', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            addUserToList(data.updated_list[data.updated_list.length - 1]);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    function addUserToList(user) {
        const userDiv = document.createElement('div');
        userDiv.classList.add('user');

        const userInfo = document.createElement('p');
        userInfo.innerHTML = `${user.firstName} ${user.lastName}<br><small>${user.role}</small>`;

        const deleteButton = document.createElement('a');
        deleteButton.classList.add('deleteButton');
        deleteButton.href = "#";
        deleteButton.innerHTML = '<i class="fa-solid fa-trash-can"></i>';

        deleteButton.addEventListener('click', function (event) {
            event.preventDefault();
            deleteUser(user, userDiv);
        });

        userDiv.appendChild(userInfo);
        userDiv.appendChild(deleteButton);
        userListContainer.appendChild(userDiv);
    }

    function deleteUser(user, userDiv) {
        fetch(`http://localhost:8000/${user.id}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            console.log('Deleted:', data);
            userListContainer.removeChild(userDiv);
        })
        .catch(error => console.error('Error deleting user:', error));
    }
});
