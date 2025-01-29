function analyzeText() {
    const text = document.getElementById("textInput").value;
    if (!text) {
        alert("Please enter text.");
        return;
    }

    const outputBox = document.getElementById("output");
    const loader = document.getElementById("loader");

    // Show loader and hide output
    outputBox.style.display = "none";
    loader.style.display = "block";

    fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        let output = `<h2>Analysis Results</h2>
                      <p><strong>Language:</strong> ${data.language}</p>
                      <p><strong>Sentiment:</strong> <span class="sentiment">${data.sentiment}</span></p>
                      <p><strong>Key Phrases:</strong> ${data.key_phrases.join(", ")}</p>
                      <p><strong>Entities:</strong> ${data.entities.map(e => `${e.text} (${e.category})`).join(", ")}</p>`;

        if (data.linked_entities.length > 0) {
            output += `<p><strong>Linked Entities:</strong> ${data.linked_entities.map(le => `<a href="${le.url}" target="_blank">${le.name}</a>`).join(", ")}</p>`;
        }

        outputBox.innerHTML = output;
        loader.style.display = "none";
        outputBox.style.display = "block";
        outputBox.classList.add("show");
    })
    .catch(error => {
        console.error("Error:", error);
        loader.style.display = "none";
        outputBox.innerHTML = "<p style='color:red;'>Error analyzing text. Please try again.</p>";
        outputBox.style.display = "block";
    });
}
