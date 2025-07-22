document.addEventListener("DOMContentLoaded", () => {
  const csrftoken = document.getElementById("csrf_token").value;

  // Use event delegation on the parent container
  document.getElementById("report-showcase").addEventListener("click", (event) => {
    const button = event.target.closest(".delete-report-btn");
    if (!button) return; // Not a delete button

    const reportId = button.dataset.reportId;
    const card = button.closest(".col-xl-2, .col-lg-3, .col-md-4, .col-6");

    fetch("delete-report/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrftoken,
      },
      body: new URLSearchParams({ report_id: reportId }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          card.remove();
        } else {
          alert("Error deleting report: " + (data.error || "Unknown error"));
        }
      })
      .catch((err) => {
        alert("Request failed: " + err);
      });
  });
});
