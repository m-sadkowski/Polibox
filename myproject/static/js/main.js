document.addEventListener("DOMContentLoaded", function() {
    // fade out alert messages
    const alerts = document.querySelectorAll('.messages .alert');
    alerts.forEach(alert => {
        alert.addEventListener('animationend', () => {
            alert.style.visibility = 'hidden';
        });
    });

    // highlight current date
    var today = new Date().toISOString().slice(0, 10);

    var dayCells = document.querySelectorAll('.day-cell');
    dayCells.forEach(function(cell) {
        if (cell.dataset.date === today) {
          cell.classList.add('current-date');
        }
    });

    // responsive navbar
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarLinks = document.querySelector('.navbar-links');

    navbarToggle.addEventListener('click', () => {
        navbarLinks.classList.toggle('active');
    });
});

$(document).ready(function() {
    // Initialize select2
    $('.js-example-basic-single').select2();

    // Existing event dialog functionality
    $('.event').click(function(event) {
        // Prevent the event from bubbling up to the parent elements
        event.stopPropagation();

        var title = $(this).data('title');
        var description = $(this).data('description');
        var eventId = $(this).data('id');
        $('#dialog-title').text(title);
        $('#dialog-description').text(description);

        $('#event-dialog').dialog({
            modal: true,
            width: 400,
            buttons: {
                Ok: function() {
                    $(this).dialog("close");
                }
            }
        });

        // Delete event functionality inside dialog
        $('.delete-event-button').click(function() {
            window.location.href = '/mycalendar/event-delete/' + eventId + '/';
        });

        // Edit event functionality inside dialog
        $('.edit-event-button').click(function(event) {
            window.location.href = '/mycalendar/event-edit/' + eventId + '/';
        });
    });

    // Add event functionality
    $('.day-cell').click(function(event) {
        // Check if the clicked element is not an event (to avoid conflict)
        if (!$(event.target).closest('.event').length) {
            var date = $(this).data('date');
            $('#id_date').val(date); // Ensure the date is set in YYYY-MM-DD format

            $('#add-event-modal').dialog({
                modal: true,
                width: 400,
                buttons: {
                    Ok: function() {
                        $('#add-event-form').submit();
                    },
                    Cancel: function() {
                        $(this).dialog("close");
                    }
                }
            });
        }
    });
});

function generateGreeting() {
    var personId = $('#person-select').val();
    fetch(`/generator/generate/${personId}/`)
        .then(response => response.json())
        .then(data => {
            $('#greeting-text').val(data.greeting_text);
        })
        .catch(error => console.error('Error:', error));
}

function generateMail() {
    var personId = $('#person-select').val();
    fetch(`/generator/generate/${personId}/`)
        .then(response => response.json())
        .then(data => {
            $('#mail-text').val(data.mail_text);
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

    if (searchValue === "") {
        subjects.forEach(subject => {
            subject.style.display = "block";
        });
    }
});