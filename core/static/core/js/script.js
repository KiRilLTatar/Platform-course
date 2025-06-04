document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('registerForm');
    if (!form) return;

    const url = form.dataset.url;

    form.onsubmit = function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const modal = bootstrap.Modal.getInstance(document.getElementById('registerModal'));
                modal.hide();
                form.reset();
                window.location.href = data.redirect_url;
            } else {
                const errors = data.errors || ["Ошибка регистрации"];
                alert(errors.join("\n"));
            }
        })
        .catch(error => console.log('Ошибка:', error));
    };
});

document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.onsubmit = function (e) {
            e.preventDefault(); 

            const url = loginForm.dataset.url; 
            const formData = new FormData(loginForm); 

            fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest", 
                },
            })
            .then((res) => res.json()) 
            .then((data) => {
                if (data.success) {
                    const modal = bootstrap.Modal.getInstance(document.getElementById("signupModal"));
                    modal.hide();

                    loginForm.reset();

                    window.location.reload();  

                } else {
                    
                    document.getElementById("login-error").textContent = data.error;
                }
            })
            .catch((err) => {
                console.error("Ошибка при отправке данных:", err);
            });
        };
    }
});
