document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.off-screen-menu');
    const navLinks = document.querySelectorAll('.off-screen-menu a');       // Select all menu links

    // Toggle the menu when the hamburger icon is clicked
    hamburger.addEventListener('click', () => {
        console.log('Hamburger clicked');                                   // Debugging line
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Close the menu when a menu link is clicked
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            console.log('Menu link clicked');                               // Debugging line
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
});
