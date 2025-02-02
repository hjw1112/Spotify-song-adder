document.getElementById("text_input").onkeydown = function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
    }
};

let selected_type
const loader = document.getElementById('loader');
const img_download = document.getElementById('img_download')
//div visiblilty logics
function start() {
    selected_type = document.querySelector('input[name="imgortxt"]:checked').value;
    console.log(selected_type)
    let txt = document.getElementById("txtinput");
    let img = document.getElementById("imginput");
    const radio_button = document.getElementById("imgortxt");
    const startbutton = document.getElementById("initbutton");
    const confirm_button = document.getElementById("ConfirmButton");
    startbutton.style.display = "none";
    radio_button.style.display = "none";
    confirm_button.style.display = "block";
    switch (selected_type) {
        case "txt":
            txt.style.display = "block";
            break;
        case "img":
            img.style.display = "block";
            break;
    }
    loader.style.display = 'none';
}


document.getElementById('text_input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        const confirmButton = document.getElementById('ConfirmButton');
        if (confirmButton) {
            confirmButton.click();
        }
    }
});

// //AJAX

// // function to handle text upload
let response;
document.getElementById('ConfirmButton').addEventListener('click', async () => {
    try {
        loader.style.display = 'block';
        if (selected_type === "txt") {
        const text = document.getElementById('text_input').value;
        response = await fetch('/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
            })
        } else if (selected_type === "img") {
            const fileInput = document.getElementById('image_upload');
            const formData = new FormData();
            formData.append('image', fileInput.files[0]);

            response = await fetch('/process', {
                method: 'POST',
                body: formData
            })
        }
        

        if (!response.ok) {
            // handle HTTP errors (e.g., 404, 500)
            const errorText = await response.text(); // get the HTML error page as text
            console.error(`Error response: ${errorText}`);
            throw new Error(`Request failed with status ${response.status}`);
        }

        const result = await response.json();
        if (result.error) {
            alert(`Error: ${result.error}`);
        } else if (result.playlist_id) {
            loader.style.display = "none"
            console.log(result.playlist_id)
            document.getElementById("iframe").src = `https://open.spotify.com/embed/playlist/${result.playlist_id}`;
            document.getElementById("iframe").style.display = "block";
        }
    } catch (error) {
        console.error("Error:", error);
        alert(`An error occurred: ${error.message}`);
    }
});




