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

const search = document.querySelector(".search-box input"),
      subjects = document.querySelectorAll(".subject-box");

search.addEventListener("keyup", () => {
    let searchValue = search.value.trim().toLowerCase(); // Trim spaces and convert to lowercase

    subjects.forEach(subject => {
        if (subject.dataset.name.toLowerCase().includes(searchValue)) {
            subject.style.display = "block";
        } else {
            subject.style.display = "none";
        }
    });

    // If the search box is empty, display all subjects
    if (searchValue === "") {
        subjects.forEach(subject => {
            subject.style.display = "block";
        });
    }
});
