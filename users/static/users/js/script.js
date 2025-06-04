document.addEventListener("DOMContentLoaded", function () {
    const editBtn = document.getElementById("edit-btn");
    const saveBtn = document.getElementById("save-btn");

    const viewMode = document.getElementById("view-mode");
    const editMode = document.getElementById("edit-mode");

    const skillsView = document.getElementById("skills-view");
    const skillsEdit = document.getElementById("skills-edit");
    const skillsTags = document.getElementById("skills-tags");
    const skillsInput = document.getElementById("skills-input");

    const contactsView = document.getElementById("contacts-view");
    const contactsEdit = document.getElementById("contacts-edit");

    const aboutText = document.getElementById("about-text");
    const aboutEdit = document.getElementById("about-edit");

    editBtn.addEventListener("click", () => {
        editBtn.classList.add("d-none");
        saveBtn.classList.remove("d-none");

        viewMode.classList.add("d-none");
        editMode.classList.remove("d-none");

        skillsView.classList.add("d-none");
        skillsEdit.classList.remove("d-none");

        contactsView.classList.add("d-none");
        contactsEdit.classList.remove("d-none");
    });

    saveBtn.addEventListener("click", () => {
        editBtn.classList.remove("d-none");
        saveBtn.classList.add("d-none");

        viewMode.classList.remove("d-none");
        editMode.classList.add("d-none");

        skillsView.classList.remove("d-none");
        skillsEdit.classList.add("d-none");

        contactsView.classList.remove("d-none");
        contactsEdit.classList.add("d-none");


        
        aboutText.textContent = aboutEdit.value;

        const skills = skillsInput.value.split(',').map(s => s.trim()).filter(s => s.length > 0);
        skillsTags.innerHTML = '';
        skills.forEach(skill => {
            const badge = document.createElement("span");
            badge.className = "badge bg-primary";
            badge.textContent = skill;
            skillsTags.appendChild(badge);
        });

        contactsView.innerHTML = `
            <p><i class="bi bi-telephone"></i> ${document.getElementById("phone").value}</p>
            <p><i class="bi bi-envelope"></i> ${document.getElementById("email").value}</p>
            <p><i class="bi bi-globe"></i> ${document.getElementById("portfolio").value}</p>
            <p><i class="bi bi-github"></i> ${document.getElementById("github").value}</p>
        `;
    });



});
