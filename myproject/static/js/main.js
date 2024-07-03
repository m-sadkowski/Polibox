document.addEventListener("DOMContentLoaded", () => {
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarLinks = document.querySelector('.navbar-links');

    navbarToggle.addEventListener('click', () => {
        navbarLinks.classList.toggle('active');
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const alerts = document.querySelectorAll('.messages .alert');
    alerts.forEach(alert => {
        alert.addEventListener('animationend', () => {
            alert.style.visibility = 'hidden';
        });
    });
});

$(document).ready(function() {
    $('.js-example-basic-single').select2();
});

function generateGreeting() {
    var personId = $('#person-select').val();
    fetch(`/generator/generate/${personId}/`)
        .then(response => response.text())
        .then(data => {
            $('#greeting-text').val(data);
        })
        .catch(error => console.error('Error:', error));
}