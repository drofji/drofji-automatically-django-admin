document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("#changelist-form table tbody tr").forEach(function (row) {
        const link = row.querySelector("th > a");

        if (link) {
            row.addEventListener("click", function (e) {
                if (e.target.tagName.toLowerCase() === "input") return;
                window.location = link.getAttribute("href");
            });
        }
    });
});