// ---------- LOST FORM ----------
const lostForm = document.getElementById("lostForm");
if (lostForm) {
    lostForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        let formData = new FormData(lostForm);

        let res = await fetch("/api/lost", {
            method: "POST",
            body: formData
        });

        let data = await res.json();
        alert(data.message);
        lostForm.reset();
    });
}

// ---------- FOUND FORM ----------
const foundForm = document.getElementById("foundForm");
if (foundForm) {
    foundForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        let formData = new FormData(foundForm);

        let res = await fetch("/api/found", {
            method: "POST",
            body: formData
        });

        let data = await res.json();
        alert(data.message);
        foundForm.reset();
    });
}
