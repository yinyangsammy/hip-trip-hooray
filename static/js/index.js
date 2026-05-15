document.addEventListener("submit", function () {

    document.querySelectorAll('input[type="text"], textarea')
        .forEach(field => {

            if (field.value) {

                field.value = field.value
                    .toLowerCase()
                    .replace(/\b\w/g, char => char.toUpperCase());

            }

        });

});
