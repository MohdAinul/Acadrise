// Open the Sign-Up Modal
function openSignUpModal() {
    document.getElementById('signUpModal').style.display = 'flex';
}

// Close the Sign-Up Modal
function closeSignUpModal() {
    document.getElementById('signUpModal').style.display = 'none';
}

// Open the specific form (student or teacher)
function openForm(formId) {
    closeSignUpModal();
    document.getElementById(formId).style.display = 'flex';
}

// Close the specific form
function closeForm(formId) {
    document.getElementById(formId).style.display = 'none';
}

// Toggle mobile menu
function toggleMenu() {
    const mobileNav = document.getElementById('mobileNav');
    mobileNav.classList.toggle('show');
}

// Smooth Scrolling for Navbar Links
document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
        e.preventDefault(); // Prevent default behavior
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
            target.scrollIntoView({
                behavior: "smooth", // Smooth scrolling
                block: "start" // Align the section to the top of the viewport
            });
        }
    });
});
