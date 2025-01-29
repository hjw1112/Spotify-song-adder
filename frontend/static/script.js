document.getElementById("text_input").onkeydown = function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
    }
};

let selected_type
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
}



// //AJAX

// // function to handle text upload
let response;
document.getElementById('ConfirmButton').addEventListener('click', async () => {
    try {
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
        

        const textResponse = await response.text();
        console.log("Raw Response:", textResponse);

        if (!response.ok) {
            // handle HTTP errors (e.g., 404, 500)
            const errorText = await response.text(); // get the HTML error page as text
            console.error(`Error response: ${errorText}`);
            throw new Error(`Request failed with status ${response.status}`);
        }

        if (!textResponse) {
            throw new Error("Empty response from server");
        }

    //     let result = await response.json();
    //     if (result.error) {
    //         alert(`Error: ${result.error}`);
    //     } else if (result.playlist_id) {
    //         document.getElementById("iframe").src = `https://open.spotify.com/embed/playlist/${result.playlist_id}`;
    //         document.getElementById("iframe").style.display = "block";
    //     }
    // } catch (error) {
    //     console.error("Error:", error);
    //     alert(`An error occurred: ${error.message}`);
    
        let result;
        try {
            result = JSON.parse(textResponse);
        } catch (jsonError) {
            console.error("JSON Parsing Error:", jsonError);
            throw new Error("Invalid JSON response from server");
        }

        if (result.error) {
            alert(`Error: ${result.error}`);
        } else if (result.playlist_id) {
            document.getElementById("iframe").src = `https://open.spotify.com/embed/playlist/${result.playlist_id}`;
            document.getElementById("iframe").style.display = "block";
        }
    } catch (error) {
        console.error("Error:", error);
        alert(`An error occurred: ${error.message}`);
    }
    
});

