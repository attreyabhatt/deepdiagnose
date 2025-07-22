document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("fileInput");
  const uploadStatus = document.getElementById("upload-status");
  if (!fileInput || !uploadStatus) return;

  fileInput.addEventListener("change", function () {
    const files = this.files;
    const formData = new FormData();

    const csrfTokenInput = document.querySelector("input[name='csrfmiddlewaretoken']");
    if (!csrfTokenInput) {
      alert("CSRF token not found.");
      return;
    }
    const csrfToken = csrfTokenInput.value;

    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp'];

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      if (!allowedTypes.includes(file.type)) {
        alert(`File "${file.name}" is not a supported type. Only PDFs and images are allowed.`);
        return; // stop upload entirely if any file is invalid
      }
      formData.append("files", file);
    }


    // Show spinner
    uploadStatus.style.display = "block";

    fetch("upload-reports/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    })
      .then((response) => {
        if (response.headers.get("content-type")?.includes("application/json")) {
          return response.json();
        }
        throw new Error("Unexpected response format (maybe a login redirect)");
      })
      .then((data) => {
        if (data.success && data.new_reports_html) {
          document
            .getElementById("report-showcase")
            .insertAdjacentHTML("beforeend", data.new_reports_html);
          fileInput.value = ""; // reset input
        } else {
          alert("Upload failed: " + (data.errors?.join(", ") || "Unknown error"));
        }
      })
      .catch((err) => {
        console.error("Upload error:", err);
        alert("Upload request failed.");
      })
      .finally(() => {
        // Hide spinner
        uploadStatus.style.display = "none";
      });
  });
});
