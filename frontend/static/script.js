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
    confirm_button.style.display = "flex";
    switch (selected_type) {
        case "txt":
            txt.style.display = "block";
            break;
        case "img":
            img.style.display = "block";
            break;
    }
}



//AJAX

// function to handle text upload

document.getElementById('ConfirmButton').addEventListener('click', async () => {
    if (selected_type == "txt") {
        const text = document.getElementById('text_input').value;
        const response = await fetch('/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        const result = await response.json();
        console.log(result);
    } else {
        const fileInput = document.getElementById('image_upload');
        const formData = new FormData();
        formData.append('image', fileInput.files[0]);

        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        console.log(result);
    }
});

// function to handle image upload

    
        
    