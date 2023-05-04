// URL at which the API server is running

// base_url = "http://127.0.0.1:5000";
// Get the input field element
const base_url = document.getElementById('base_url');
chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    // Get the current URL
    let currentUrl = tabs[0].url;
    currentUrl = currentUrl.split("/")[2];
    base_url.value = "http://" + currentUrl;
});

// Load the stored value from local storage
chrome.storage.local.get('inputValue', ({ inputValue }) => {
  if (inputValue) {
    base_url.value = inputValue;
  }
});

// Save the input value to local storage when the input field changes
base_url.addEventListener('input', () => {
  chrome.storage.local.set({ 'inputValue': base_url.value });
});


let toggleNER = 1
let togglePOS = 1
let toggleSimplify = 1
// Inject _getSelectedTextFromTab into current page and 
// populate the textarea for user input in the popup with the selected text
function getSelectedText() {
    extension_id = "mddilokoecbplkgankjpnaigfnpdlmgh"

    // Get information about the currently active tab
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        let tab = tabs[0];

        // Inject JavaScript into the active tab to get the text selected by the user
        chrome.scripting.executeScript(
            {
                target: { tabId: tab.id },              // Specify a target to inject JavaScript
                function: _getSelectedTextFromTab,      // Function to be injected into the target
            },
            ([res]) => {
                // If selection is not empty, populate the input textarea
                if (res["result"] !== "") {
                    document.getElementById("input_text").value = res["result"];
                    getResults()

                }
            }
        );
    });
};

// Get the selected text from the current page
function _getSelectedTextFromTab() {
    var selection = window.getSelection().toString();
    return selection;
}

function getStoryData() {
    var textElements = document.querySelectorAll('div.bookreading_content__textArea__dqYNj');
    var imageElements = document.querySelectorAll('div.bookreading_content__imageArea__2IfX3');

    var resultArray = {};

    for (var i = 0; i < textElements.length; i++) {
        resultArray[i] = { "textArea": '', "imageArea": '' };
        resultArray[i].textArea = textElements[i].textContent;

        var img = imageElements[i].querySelector('img');
        if (img) {
            resultArray[i].imageArea = img.src;
        }
    }

    return resultArray;
}

// Obtain the results from the API server
function getResults() {
    document.getElementById("results").style.display = "none";

    let error_box = document.getElementById("error_box");
    let text = document.getElementById("input_text").value;
    let loading_text = document.getElementById("loading_text");
    let base_url = document.getElementById("base_url");
    console.log(base_url)
    // If there is no input text, throw error 
    if (base_url.value == "") {
        error_box.innerHTML = "API URL is not set!";
        error_box.style.display = "block";
    }
    else if (text == "") {
        error_box.innerHTML = "No text available to help you :( Please enter something!";
        error_box.style.display = "block";
    }
    else {
        error_box.style.display = "none";
        base_url = base_url.value;
        // Start displaying the spinner
        loading_text.innerHTML = "Fetching results...";
        document.getElementById("loading").style.display = "block";

        // Create the JSON request body as specified in the API endpoint
        fetch(base_url + '/api/predict', {
            method: "POST",
            body: JSON.stringify({
                input: text,
                isSimplify: toggleSimplify,
                isNER: toggleNER,
                isPOS: togglePOS,
            }),
            headers: { "Content-type": "application/json; charset=UTF-8" }
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById("loading").style.display = "none";
                if (data.status == 0) {
                    error_box.innerHTML = data.text;
                    error_box.style.display = "block";
                }
                else {
                    // Display the output in the popup
                    render(data)
                    document.getElementById("results").style.display = "block";
                }

            });

    }
}

function render(render_data) {
    // ANIMAL
    // NATURE
    // OBJECT
    // PERSON
    // PLACE
    // VEHICLE
    text = render_data.text;
    spans = render_data.ents;
    render_str = ``
    var offset = 0
    spans.forEach(({ end, entity, pos, start }) => {
        const fragment = text.slice(offset, start)
        const word = text.slice(start, end);
        render_str += fragment
        if (entity != null) {
            render_str += `<mark data-entity="${entity}">${word}</mark>`
        } else {

            if (pos.includes('VB')) {
                render_str += `<mark data-entity="ACTION">${word}</mark>`
            }
            else if (pos.includes('JJ')) {
                render_str += `<mark data-entity="DESCRIPTION">${word}</mark>`
            }
            else {
                render_str += word
            }

            //TODO: Enable turn on and off POS and NER
            // render_str += word

        }

        offset = end
    });
    render_str += text.slice(offset)
    document.getElementById("ner_results").innerHTML = render_str;
}
// end: 3, entity: null, pos: 'VBH', start: 0, word: 'may

// Toggle NER
const buttonToggleNER = document.getElementById("toggleNER");
buttonToggleNER.addEventListener("click", () => {
    if (toggleNER) {
        toggleNER = 0;
    } 
    else if (!toggleNER) {
        toggleNER = 1;
    }
});

// Toggle POS
const buttonTogglePOS = document.getElementById("togglePOS");
buttonTogglePOS.addEventListener("click", () => {
    if (togglePOS) {
        togglePOS = 0;
    } 
    else if (!togglePOS) {
        togglePOS = 1;
    }
});
// Toggle Simplify
const buttonToggleSimplify = document.getElementById("toggleSimplify");
buttonToggleSimplify.addEventListener("click", () => {
    if (toggleSimplify) {
        toggleSimplify = 0;
    } 
    else if (!toggleSimplify) {
        toggleSimplify = 1;
    }
});


document.getElementById("read-mode-button").addEventListener("click", function () {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        // Get the current URL
        const currentUrl = tabs[0].url;
        newUrl = "read://" + currentUrl;

        // Split the URL into an array of segments
        // const urlSegments = currentUrl.split('/');
        // // Get the last segment of the URL
        // const lastSegment = urlSegments[urlSegments.length - 1];
        // var newUrl = '';
        // if (lastSegment != '') {
        //     // Replace the last segment with a new segment
        //     const newSegment = '';
        //     newUrl = currentUrl.replace(lastSegment, newSegment);
        //     newUrl = "read://123" + newUrl;

        // }else{
        //     newUrl = "read://123" + newUrl;
        // }
        // Navigate to the new URL
        chrome.tabs.create({ url: newUrl });
    });
});

document.getElementById("review-mode-button").addEventListener("click", function () {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        // Get the current URL
        const currentUrl = tabs[0].url;

        // Split the URL into an array of segments
        const urlSegments = currentUrl.split('/');
        // Get the last segment of the URL
        const lastSegment = urlSegments[urlSegments.length - 1];
        var newUrl = '';
        if (lastSegment != '') {
            // Replace the last segment with a new segment
            const newSegment = 'review';
            newUrl = currentUrl.replace(lastSegment, newSegment);
        } else {
            newUrl = currentUrl + "review";
        }
        // Navigate to the new URL
        chrome.tabs.create({ url: newUrl });
    });


});

document.getElementById("evaluate-mode-button").addEventListener("click", function () {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        // Get the current URL
        const currentUrl = tabs[0].url;

        // Split the URL into an array of segments
        const urlSegments = currentUrl.split('/');

        // Get the last segment of the URL
        const lastSegment = urlSegments[urlSegments.length - 1];
        var newUrl = '';
        if (lastSegment != '') {
            // Replace the last segment with a new segment
            const newSegment = 'evaluate';
            newUrl = currentUrl.replace(lastSegment, newSegment);
        }
        else {
            newUrl = currentUrl + "evaluate";
        }
        // Navigate to the new URL
        chrome.tabs.create({ url: newUrl });
    });
});

// Trigger the injection of script to get user selected text and 
// populate the input textarea whenever the DOM content is loaded
// (without waiting for images and stylesheets to finish loading)
document.addEventListener("DOMContentLoaded", getSelectedText);

// When the 'Process' button is clicked, send the POST request to the API server to obtain
// the result text and populate the results dynamically
document.getElementById("submit_text").addEventListener("click", getResults);


// // Get all the <mark> elements in the document
// const markElements = document.getElementsByTagName('mark');

// // Initialize an empty array to store the text
// const markText = [];

// // Loop through each <mark> element and add its text content to the array
// for (let i = 0; i < markElements.length; i++) {
//     text = markElements[i].textContent.toLowerCase();
//     if(!markText.includes(text)){
//         markText.push(text);
//     }
// }

// // The markText array now contains all the text content of the <mark> elements
// console.log(markText);
